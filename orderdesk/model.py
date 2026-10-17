"""The one place the agent talks to a language model: an OpenAI-compatible chat endpoint (vLLM serves one).  Standard library only.

Configuration, from the environment and from nowhere else (no key is ever written to a file):
  ORDERDESK_MODEL_BASE_URL   for example http://<your AMD Developer Cloud instance>:8000/v1
  ORDERDESK_MODEL_NAME       the open model that endpoint serves
  ORDERDESK_MODEL_API_KEY    optional bearer key of that endpoint

The model READS an email into a small JSON record.  It decides nothing: orderdesk/policy.py does.  An answer that is not that record, after one more try, is not repaired or
guessed at: the case goes to a person.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urlparse

from .policy import ISSUES

SYSTEM = ("You read one customer email for an online shop's order desk. Reply with ONE JSON object and nothing else, with exactly these keys: "
          '"order_id" (the order number in the email as a string, or null), "issue" (one of: ' + ", ".join(ISSUES) + "), "
          '"summary" (one sentence, your own words), "confidence" (a number from 0 to 1: how sure you are of order_id and issue). '
          "If the email is about several things or is unclear, use issue \"other\" and a low confidence. Do not invent an order number.")


class ModelUnusable(Exception):
    """The endpoint could not be reached, or what it answered is not the record asked for."""


@dataclass(frozen=True)
class Reading:
    case: dict
    model: str
    endpoint_host: str
    latency_ms: int
    attempts: int
    usage: dict


def parse(content: str) -> dict:
    """The record in a model's answer, or ModelUnusable.  Strict: the four keys, an issue the desk knows, a confidence between 0 and 1."""
    start, end = content.find("{"), content.rfind("}")
    if start < 0 or end <= start:
        raise ModelUnusable("no JSON object in the answer")
    try:
        record = json.loads(content[start:end + 1])
    except ValueError as problem:
        raise ModelUnusable(f"not JSON: {problem}") from None
    if not isinstance(record, dict) or set(record) != {"order_id", "issue", "summary", "confidence"}:
        raise ModelUnusable("not exactly the four keys asked for")
    if record["issue"] not in ISSUES or not isinstance(record["summary"], str):
        raise ModelUnusable("an issue the desk does not know, or no summary")
    if record["order_id"] is not None and not isinstance(record["order_id"], str):
        raise ModelUnusable("order_id is neither a string nor null")
    confidence = record["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ModelUnusable("confidence is not a number from 0 to 1")
    return {"order_id": record["order_id"].strip().upper() if record["order_id"] else None, "issue": record["issue"], "summary": record["summary"].strip()[:300], "confidence": float(confidence)}


class ChatModel:
    def __init__(self, base_url: str | None = None, name: str | None = None, api_key: str | None = None, timeout: float = 60.0):
        self.base_url = (base_url or os.environ.get("ORDERDESK_MODEL_BASE_URL") or "").rstrip("/")
        self.name = name or os.environ.get("ORDERDESK_MODEL_NAME") or ""
        self._key = api_key if api_key is not None else os.environ.get("ORDERDESK_MODEL_API_KEY", "")
        self.timeout = timeout
        if not self.base_url or not self.name:
            raise ModelUnusable("ORDERDESK_MODEL_BASE_URL and ORDERDESK_MODEL_NAME are not set")

    @property
    def endpoint_host(self) -> str:
        return urlparse(self.base_url).netloc

    def _post(self, path: str, payload: dict) -> dict:
        request = urllib.request.Request(self.base_url + path, data=json.dumps(payload).encode("utf-8"), method="POST",
                                         headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {self._key}"} if self._key else {})})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as problem:
            raise ModelUnusable(f"the model endpoint did not answer usably: {type(problem).__name__}: {problem}") from None

    def read_email(self, email_text: str) -> Reading:
        started, problem, usage = time.monotonic(), None, {}
        for attempt in (1, 2):
            messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": email_text[:6000]}]
            if problem:
                messages.append({"role": "user", "content": f"Your last answer could not be used ({problem}). Reply with the JSON object only."})
            answer = self._post("/chat/completions", {"model": self.name, "messages": messages, "temperature": 0, "max_tokens": 300})
            try:
                content = answer["choices"][0]["message"]["content"]
                usage = answer.get("usage") or {}
                return Reading(parse(content), str(answer.get("model") or self.name), self.endpoint_host, int((time.monotonic() - started) * 1000), attempt, dict(usage))
            except (KeyError, IndexError, TypeError):
                problem = "the reply was not a chat completion"
            except ModelUnusable as unusable:
                problem = str(unusable)
        raise ModelUnusable(f"two answers could not be used; the last problem: {problem}")
