"""The app: a small web page and a JSON API over the order desk.  Standard library only.

    python -m orderdesk.server            (reads ORDERDESK_* from the environment; listens on ORDERDESK_PORT, default 8080)

  GET  /            a page: paste an email, see what the agent did and why, and which model on which endpoint read it
  POST /api/cases   {"email": "..."} -> the handled case
  GET  /api/cases   the last cases from the ledger
  GET  /api/model   which endpoint and model the agent uses, and whether that endpoint is the local stand-in
  GET  /healthz     "ok"
"""
from __future__ import annotations

import html
import json
import os
import shutil
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import stub_model
from .agent import OrderDesk
from .model import ChatModel

ROOT = Path(__file__).resolve().parents[1]
PAGE = """<!doctype html><meta charset="utf-8"><title>Order desk agent</title>
<style>body{{font:16px/1.45 system-ui,sans-serif;max-width:860px;margin:24px auto;padding:0 16px}}textarea{{width:100%;height:140px}}
.case{{border:1px solid #bbb;border-radius:6px;padding:10px 14px;margin:12px 0}}.person{{border-color:#b45309}}small{{color:#555}}.warn{{background:#fef3c7;padding:8px 12px;border-radius:6px}}</style>
<h1>Order desk agent</h1>
<p>Model: <b>{model}</b> at <b>{host}</b></p>{warning}
<form method="post" action="/"><textarea name="email" placeholder="Paste a customer email here"></textarea><p><button>Handle this email</button></p></form>
<h2>Cases</h2>{cases}"""


def model_facts(model: ChatModel) -> dict:
    stand_in = model.name == stub_model.NAME
    return {"endpoint_host": model.endpoint_host, "model": model.name, "is_the_local_stand_in": stand_in,
            "runs_on_amd": "NOT SHOWN: this is the local stand-in" if stand_in else "CLAIMED BY CONFIGURATION ONLY: the endpoint is whatever the owner configured (intended: AMD Token Factory); see docs/TOKEN_FACTORY.md for what the evidence shows"}


def make_handler(desk: OrderDesk, model: ChatModel):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, body, status=200, kind="application/json"):
            data = body.encode("utf-8") if isinstance(body, str) else json.dumps(body, indent=1).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _page(self):
            facts = model_facts(model)
            warning = '<p class="warn">This is the local stand-in, not a language model and not AMD. Nothing on this page shows the product running on AMD hardware.</p>' if facts["is_the_local_stand_in"] else ""
            rows = []
            for case in reversed(desk.cases(20)):
                reading = case.get("reading") or {}
                rows.append(f'<div class="case {html.escape(case["by"])}"><b>{html.escape(case["action"])}</b> by the {html.escape(case["by"])} '
                            f'<small>{html.escape(case["case_id"])} · order {html.escape(str(reading.get("order_id")))} · {html.escape(str(reading.get("issue")))} · '
                            f'{(case.get("model") or {}).get("latency_ms", "-")} ms</small><br>{html.escape("; ".join(case["reasons"]))}<br><i>{html.escape(case["reply"])}</i></div>')
            self._send(PAGE.format(model=html.escape(facts["model"]), host=html.escape(facts["endpoint_host"]), warning=warning, cases="".join(rows) or "<p>None yet.</p>"), kind="text/html")

        def do_GET(self):  # noqa: N802
            if self.path == "/healthz":
                self._send("ok", kind="text/plain")
            elif self.path == "/api/model":
                self._send(model_facts(model))
            elif self.path == "/api/cases":
                self._send(desk.cases())
            elif self.path == "/":
                self._page()
            else:
                self._send({"error": "not found"}, 404)

        def do_POST(self):  # noqa: N802
            raw = self.rfile.read(min(int(self.headers.get("Content-Length", "0")), 200_000))
            if self.path == "/api/cases":
                try:
                    email = json.loads(raw)["email"]
                    assert isinstance(email, str) and email.strip()
                except (ValueError, KeyError, AssertionError, TypeError):
                    return self._send({"error": 'send {"email": "<the customer\'s message>"}'}, 400)
                self._send(desk.handle(email))
            elif self.path == "/":
                from urllib.parse import parse_qs
                email = (parse_qs(raw.decode("utf-8")).get("email") or [""])[0]
                if email.strip():
                    desk.handle(email)
                self._page()
            else:
                self._send({"error": "not found"}, 404)

        def log_message(self, *args):
            return
    return Handler


def build(data_dir: Path | None = None, model: ChatModel | None = None) -> tuple:
    data = Path(data_dir or os.environ.get("ORDERDESK_DATA_DIR") or ROOT / "data")
    data.mkdir(parents=True, exist_ok=True)
    if not (data / "orders.json").is_file():
        shutil.copyfile(ROOT / "samples" / "orders.json", data / "orders.json")
    model = model or ChatModel()
    return OrderDesk(model, data / "orders.json", data / "ledger.jsonl"), model


def main() -> int:
    desk, model = build()
    port = int(os.environ.get("ORDERDESK_PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), make_handler(desk, model))
    print(f"order desk on port {port}; model {model.name} at {model.endpoint_host}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
