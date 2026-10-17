"""Handle every sample email with the LOCAL STAND-IN and write what happened to docs/LOCAL_DEMO_RUN.json.

    python scripts/local_demo.py

This shows the app's path from an email to a handled case on this machine.  The "model" is the stand-in (regular expressions): the record says so in its first field, and it is
no evidence of anything running on AMD hardware.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from orderdesk import stub_model  # noqa: E402
from orderdesk.agent import OrderDesk  # noqa: E402
from orderdesk.model import ChatModel  # noqa: E402

FIXED_DAY = date(2026, 10, 13)          # the sample order book's dates are written for this day


def main() -> int:
    server, url = stub_model.serve()
    samples = json.loads((ROOT / "samples" / "emails.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as folder:
        shutil.copyfile(ROOT / "samples" / "orders.json", Path(folder) / "orders.json")
        desk = OrderDesk(ChatModel(url, stub_model.NAME), Path(folder) / "orders.json", Path(folder) / "ledger.jsonl", today=lambda: FIXED_DAY)
        rows = []
        for sample in samples:
            handled = desk.handle(sample["email"])
            rows.append({"sample": sample["name"], "expected": sample["expect"], "action": handled["action"], "by": handled["by"], "as_expected": handled["action"] == sample["expect"],
                         "reasons": handled["reasons"], "reply": handled["reply"], "model": handled["model"]})
    server.shutdown()
    record = {"MODEL_USED": "THE LOCAL STAND-IN (regular expressions). NOT a language model, NOT AMD hardware.", "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "order_book_day": FIXED_DAY.isoformat(), "cases": len(rows), "as_expected": sum(row["as_expected"] for row in rows),
              "settled_by_the_agent": sum(row["by"] == "agent" for row in rows), "handed_to_a_person": sum(row["by"] == "person" for row in rows), "rows": rows}
    (ROOT / "docs" / "LOCAL_DEMO_RUN.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k != "rows"}, indent=1))
    return 0 if record["as_expected"] == record["cases"] else 1


if __name__ == "__main__":
    sys.exit(main())
