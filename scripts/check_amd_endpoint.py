"""Check the model endpoint the app is configured for, and write down what it answered.  Run it yourself once the endpoint exists.

    python scripts/check_amd_endpoint.py [--out AMD_ENDPOINT_CHECK.json]

It reads ORDERDESK_MODEL_BASE_URL, ORDERDESK_MODEL_NAME and ORDERDESK_MODEL_API_KEY from the environment, asks the endpoint which models it serves, and has it read every
sample email.  It records the endpoint's host, the model names, each reading, whether it matches what the sample expects, and the timings.

WHAT THIS DOES NOT PROVE.  An HTTP answer does not say what hardware produced it.  The hardware behind a managed endpoint is stated by its provider (the Token Factory manual), not shown by this script. See docs/TOKEN_FACTORY.md. Keep those next to this script's output.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from orderdesk import stub_model  # noqa: E402
from orderdesk.model import ChatModel, ModelUnusable  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("AMD_ENDPOINT_CHECK.json"))
    args = ap.parse_args(argv)
    try:
        model = ChatModel()
    except ModelUnusable as problem:
        print(f"NOT CHECKED: {problem}")
        return 2
    record = {"checked_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "endpoint_host": model.endpoint_host, "model_asked_for": model.name,
              "is_the_local_stand_in": model.name == stub_model.NAME, "models_served": None, "readings": [],
              "what_this_proves": "that an OpenAI-compatible endpoint at this host answered as recorded; NOT what hardware it runs on"}
    try:
        request = urllib.request.Request(model.base_url + "/models", headers={"Authorization": f"Bearer {model._key}"} if model._key else {})
        with urllib.request.urlopen(request, timeout=30) as response:
            record["models_served"] = [entry.get("id") for entry in json.loads(response.read()).get("data", [])]
    except Exception as problem:  # noqa: BLE001
        record["models_served_error"] = f"{type(problem).__name__}: {problem}"
    right = 0
    for sample in json.loads((ROOT / "samples" / "emails.json").read_text(encoding="utf-8")):
        try:
            reading = model.read_email(sample["email"])
            row = {"sample": sample["name"], "reading": reading.case, "latency_ms": reading.latency_ms, "attempts": reading.attempts, "model_answering": reading.model, "usage": reading.usage}
        except ModelUnusable as problem:
            row = {"sample": sample["name"], "unusable": str(problem)}
        record["readings"].append(row)
        right += "reading" in row
    record["samples_read"] = f"{right} of {len(record['readings'])}"
    args.out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: record[k] for k in ("endpoint_host", "model_asked_for", "is_the_local_stand_in", "models_served", "samples_read")}, indent=1))
    print("wrote", args.out)
    return 0 if right == len(record["readings"]) else 1


if __name__ == "__main__":
    sys.exit(main())
