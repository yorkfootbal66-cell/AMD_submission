# Using the organiser-provided AMD Token Factory endpoint

The event's FAQ names `notebooks.amd.com/tokenfactory` as the access route and says only its API is needed: no billing, no credit card, no GPU instance of our own. (The own-vLLM-endpoint requirement belongs to the optional Evolus track, which this entry does not use.)

## Steps (for whoever holds the Token Factory login)

1. Sign in at `notebooks.amd.com/tokenfactory` with the AMD AI Developer Program account.
2. From the provider's own page, copy: the API base URL (OpenAI-compatible, ending in `/v1`), the model identifier, and the API key.
3. Put them in the environment (host secret settings or the shell), never in a file:
   `ORDERDESK_MODEL_BASE_URL`, `ORDERDESK_MODEL_NAME`, `ORDERDESK_MODEL_API_KEY`
4. `python scripts/check_amd_endpoint.py` reads all ten sample emails and writes `AMD_ENDPOINT_CHECK.json`.
5. `python -m orderdesk.server`, then work through `docs/DEMO_SCRIPT.md`.

## Evidence to keep, and exactly what each establishes

| Evidence | Establishes |
|---|---|
| Screenshot or saved text of the provider's page naming the service, base URL and model (key hidden) | That the organiser-provided AMD Token Factory service is the endpoint used, as that page describes it |
| `AMD_ENDPOINT_CHECK.json` | That this endpoint host answered these ten requests, with this model name, these readings and these latencies |
| `data/ledger.jsonl` from the demo session | That the application sent real requests there: per case, the model, endpoint host and time |
| The demo video | The above, shown running |

## What none of this establishes

An HTTP answer does not show the GPU model or the software stack behind it. No `rocm-smi` output exists for this entry, because the service is managed and the machine is not ours. The submission says "served by AMD's Token Factory", as the provider describes itself, and makes no claim about specific hardware beyond what the provider's page states.

## What was actually used (2026-10-17/18)

Base URL `https://developer.amd.com.cn/radeon/api/v1`, model `DeepSeek-V4-Flash`. The key was supplied by the build session's proxy and never appeared in any file or command. Provider usage check: 20 requests, no errors, cost 0.0007 USD against a 1 USD daily limit, 20 requests per minute allowed (`docs/evidence/USAGE_CHECK.json`; organisation ids omitted). The model list reports non-zero per-token prices; the actual charge seen is the figure above.
