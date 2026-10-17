# Evidence (2026-10-17, synthetic data only)

- `models_response.json`: raw `GET /models` from the Token Factory endpoint.
- `AMD_ENDPOINT_CHECK.json`: `scripts/check_amd_endpoint.py`, 10 of 10 read; median 2.7 s.
- `APP_RUN_RESULTS.json`, `ledger.jsonl`, `orders_after_run.json`: the real application handling the ten samples; 10 of 10 matched expectations.
- Note: the two runs are separate model calls. The email "told to ignore the rules" was read with confidence 0.9 in the check and 0.2 in the app run; both ended with a person (by the rules in one, by low confidence in the other). Model output varies between calls.
- What this shows: the app sent real requests to this endpoint and got these answers. Hardware is attributed to the provider's manual (shared endpoints run on AMD GPUs); no independent measurement exists. The provider's price list shows non-zero per-token prices for the model; usage here was ~30 short requests.
