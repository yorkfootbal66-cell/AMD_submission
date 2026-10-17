"""What the agent may do alone, and when a person takes the case.  Plain rules, no model: every decision here can be read and tested.

The model reads the email; these rules decide.  A rule never trusts the model's reading where the firm's own records say something else: the order, its amount, its status and
its dates come from the order book.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

ISSUES = ("late_delivery", "damaged_item", "wrong_item", "cancel_order", "refund_request", "other")
REFUND_LIMIT = 50.00          # the agent refunds or replaces up to this amount without a person
RETURN_WINDOW_DAYS = 30
LATE_DAYS_AGENT_MAY_ANSWER = 7
MIN_CONFIDENCE = 0.70
#: words that send a case to a person whatever else is true (matched on the customer's own text, not on the model's reading)
ESCALATE_WORDS = ("lawyer", "legal action", "chargeback", "injured", "injury", "allergic", "fraud", "police", "press", "sue ")


@dataclass(frozen=True)
class Decision:
    action: str                 # REFUND, REPLACE, CANCEL, SEND_TRACKING or HAND_TO_A_PERSON
    reasons: tuple = field(default_factory=tuple)

    @property
    def by_the_agent(self) -> bool:
        return self.action != "HAND_TO_A_PERSON"


def hand_over(*reasons: str) -> Decision:
    return Decision("HAND_TO_A_PERSON", tuple(reasons))


def decide(case: dict, order: dict | None, email_text: str, today: date) -> Decision:
    """``case``: what the model read from the email (issue, order_id, confidence).  ``order``: the order book's record, or None."""
    lowered = email_text.lower()
    flagged = [word.strip() for word in ESCALATE_WORDS if word in lowered]
    if flagged:
        return hand_over("the customer's message mentions: " + ", ".join(flagged))
    if case["issue"] not in ISSUES or case["issue"] == "other":
        return hand_over("the request is not one of the kinds the agent handles")
    if case["confidence"] < MIN_CONFIDENCE:
        return hand_over(f"the model was not sure of its reading (confidence {case['confidence']:.2f}, needed {MIN_CONFIDENCE:.2f})")
    if order is None:
        return hand_over("no order with that number is in the order book")
    age = (today - date.fromisoformat(order["ordered_on"])).days
    if case["issue"] == "cancel_order":
        if order["status"] == "processing":
            return Decision("CANCEL", ("the order has not shipped",))
        return hand_over(f"the order is already {order['status']}: a cancellation is no longer a simple step")
    if case["issue"] == "late_delivery":
        if order["status"] != "shipped":
            return hand_over(f"the order is {order['status']}, not on its way")
        late = (today - date.fromisoformat(order["promised_by"])).days
        if late <= LATE_DAYS_AGENT_MAY_ANSWER:
            return Decision("SEND_TRACKING", (f"shipped, {max(late, 0)} day(s) past the promised date",))
        return hand_over(f"{late} days past the promised date: more than the {LATE_DAYS_AGENT_MAY_ANSWER} the agent may answer alone")
    # damaged_item, wrong_item, refund_request
    if order["status"] != "delivered":
        return hand_over(f"the order is {order['status']}; a refund or replacement is for a delivered order")
    if age > RETURN_WINDOW_DAYS:
        return hand_over(f"ordered {age} days ago: outside the {RETURN_WINDOW_DAYS}-day window")
    if order["amount"] > REFUND_LIMIT:
        return hand_over(f"the order is {order['amount']:.2f}: above the {REFUND_LIMIT:.2f} the agent may settle alone")
    if case["issue"] == "refund_request":
        return Decision("REFUND", (f"delivered {age} day(s) ago, {order['amount']:.2f} is within the limit",))
    return Decision("REPLACE", (f"{case['issue'].replace('_', ' ')}, delivered {age} day(s) ago, {order['amount']:.2f} is within the limit",))
