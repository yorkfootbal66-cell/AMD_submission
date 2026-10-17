"""One customer email in, one handled case out: read (model), decide (rules), act (order book and ledger), or hand to a person with the reasons.

Every case is written to the ledger whatever happened to it, with which model on which endpoint read it and how long that took.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import threading
import time
from datetime import date, datetime, timezone
from pathlib import Path

from . import policy
from .model import ModelUnusable

REPLIES = {
    "REFUND": "We have refunded {amount:.2f} for order {order_id}. It reaches your account in 3 to 5 working days.",
    "REPLACE": "We are sorry about order {order_id}. A replacement is on its way; you do not need to send anything back.",
    "CANCEL": "Order {order_id} is cancelled and you will not be charged.",
    "SEND_TRACKING": "Order {order_id} is on its way. You can follow it here: {tracking_url}",
    "HAND_TO_A_PERSON": "Thank you for your message. A member of our team will reply to you personally within one working day.",
}
STATUS_AFTER = {"REFUND": "refunded", "REPLACE": "replacement_sent", "CANCEL": "cancelled"}


class OrderDesk:
    def __init__(self, model, orders_file: Path, ledger_file: Path, today=None):
        self.model, self.orders_file, self.ledger_file = model, Path(orders_file), Path(ledger_file)
        self.today = today or date.today
        self._lock = threading.Lock()

    def _orders(self) -> dict:
        return {order["order_id"]: order for order in json.loads(self.orders_file.read_text(encoding="utf-8"))}

    def handle(self, email_text: str) -> dict:
        received = datetime.now(timezone.utc).isoformat(timespec="seconds")
        case_id = "C-" + secrets.token_hex(5)                                    # of its own: the same email sent twice is two cases
        record = {"case_id": case_id, "received_utc": received, "email_sha256": hashlib.sha256(email_text.encode("utf-8")).hexdigest()}
        try:
            reading = self.model.read_email(email_text)
        except ModelUnusable as unusable:
            decision = policy.hand_over(f"the model could not be used: {unusable}")
            record.update(reading=None, model={"usable": False})
            order = None
        else:
            record.update(reading=reading.case, model={"usable": True, "name": reading.model, "endpoint_host": reading.endpoint_host, "latency_ms": reading.latency_ms,
                                                       "attempts": reading.attempts, "usage": reading.usage})
            with self._lock:
                order = self._orders().get(reading.case["order_id"]) if reading.case["order_id"] else None
            decision = policy.decide(reading.case, order, email_text, self.today())
        record.update(action=decision.action, by="agent" if decision.by_the_agent else "person", reasons=list(decision.reasons))
        with self._lock:
            if decision.by_the_agent and decision.action in STATUS_AFTER:        # the "other system": the order book is updated, once, under the lock
                orders = self._orders()
                current = orders[order["order_id"]]
                if current["status"] != order["status"]:                         # somebody else changed the order since it was read: do not act on a stale record
                    decision = policy.hand_over(f"the order changed to {current['status']} while the case was being handled")
                    record.update(action=decision.action, by="person", reasons=list(decision.reasons))
                else:
                    current["status"] = STATUS_AFTER[decision.action]
                    temporary = self.orders_file.with_suffix(".tmp")
                    temporary.write_text(json.dumps(list(orders.values()), indent=1), encoding="utf-8")
                    temporary.replace(self.orders_file)
            record["reply"] = REPLIES[record["action"]].format(order_id=(order or {}).get("order_id", ""), amount=(order or {}).get("amount", 0.0),
                                                               tracking_url=(order or {}).get("tracking_url", ""))
            record["handled_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            record["seconds"] = round(time.time() - datetime.fromisoformat(received).timestamp(), 3)
            with open(self.ledger_file, "a", encoding="utf-8", newline="\n") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        return record

    def reset(self, pristine_orders: Path) -> None:
        """Back to the synthetic starting state: the sample order book, an empty ledger."""
        with self._lock:
            self.orders_file.write_text(Path(pristine_orders).read_text(encoding="utf-8"), encoding="utf-8")
            self.ledger_file.write_text("", encoding="utf-8")

    def cases(self, last: int = 50) -> list:
        if not self.ledger_file.is_file():
            return []
        return [json.loads(line) for line in self.ledger_file.read_text(encoding="utf-8").splitlines()[-last:] if line.strip()]
