"""A STAND-IN for the model endpoint, for tests and for trying the app without a GPU.  It is NOT a language model and NOT AMD: a few regular expressions behind the same
HTTP interface (/v1/models, /v1/chat/completions).  Nothing shown with this stand-in is evidence of the product running on AMD hardware; the app says so on its page.

    python -m orderdesk.stub_model [port]
"""
from __future__ import annotations

import json
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

NAME = "local-stand-in-not-a-model"
_ORDER = re.compile(r"\b(?:order|#)\s*(?:number|no\.?|id)?\s*[:#]?\s*([A-Z]{2}-?\d{4,})", re.I)
_RULES = (("cancel_order", r"\bcancel"), ("damaged_item", r"\b(broken|damaged|cracked|smashed)"), ("wrong_item", r"\b(wrong (item|product|one)|sent (me )?the wrong|not what i ordered|different (item|colour|color|size))"),
          ("late_delivery", r"\b(late|still (hasn't|has not|not) arrived|where is my|not arrived|delayed)"), ("refund_request", r"\b(refund|money back)"))


def read(email: str) -> dict:
    found = _ORDER.search(email)
    issues = [issue for issue, pattern in _RULES if re.search(pattern, email, re.I)]
    issue = issues[0] if len(issues) == 1 else "other"
    return {"order_id": found.group(1).upper() if found else None, "issue": issue, "summary": email.strip().splitlines()[0][:120] if email.strip() else "",
            "confidence": 0.9 if (found and len(issues) == 1) else 0.4}


class _Handler(BaseHTTPRequestHandler):
    def _send(self, body: dict, status: int = 200) -> None:
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        self._send({"object": "list", "data": [{"id": NAME, "object": "model"}]} if self.path.rstrip("/").endswith("/models") else {"error": "not found"}, 200 if self.path.rstrip("/").endswith("/models") else 404)

    def do_POST(self):  # noqa: N802
        payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))) or b"{}")
        email = next((m["content"] for m in payload.get("messages", []) if m.get("role") == "user"), "")
        self._send({"id": "stand-in", "object": "chat.completion", "model": NAME, "choices": [{"index": 0, "message": {"role": "assistant", "content": json.dumps(read(email))}, "finish_reason": "stop"}],
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}})

    def log_message(self, *args):  # quiet
        return


def serve(port: int = 0) -> tuple:
    """Start the stand-in on 127.0.0.1; returns (server, base_url).  ``server.shutdown()`` stops it."""
    server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/v1"


if __name__ == "__main__":
    running, url = serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8001)
    print(f"STAND-IN model endpoint (not a model, not AMD) at {url}  model name: {NAME}")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        running.shutdown()
