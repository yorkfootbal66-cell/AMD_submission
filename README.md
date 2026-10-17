# Order desk agent

A small agent for an online shop's order desk. It reads a customer email with an open language model, decides by written rules what may be done without a person, does it in the order book, and hands every other case to a person with the reasons.

Built for the AMD Developer Hackathon ACT III (track "Reinvent Commerce": help a business serve and retain customers). The model is meant to run on AMD hardware: an open model served by AMD's Token Factory, reached through its OpenAI-compatible API.

**Status, stated plainly.** On 2026-10-17 the application ran against `DeepSeek-V4-Flash` on AMD's Token Factory shared endpoint (`developer.amd.com.cn/radeon/api/v1`): all 10 synthetic sample emails ended as expected (3 settled by the agent, 7 handed to a person), median model read 2.7 s. Raw results are in [docs/evidence/](docs/evidence/). Per the provider's manual these shared endpoints run on AMD GPUs; we did not observe the hardware ourselves. The container build and a deployed public URL are not verified here.

## What it does

1. **Reads.** The email goes to the model, which answers with a small record: the order number, the kind of request, a one-sentence summary, and how sure it is.
2. **Decides.** Plain rules in [`orderdesk/policy.py`](orderdesk/policy.py) decide. The amount, the status and the dates come from the order book, never from the email or the model.
3. **Acts or hands over.** The agent refunds or replaces small delivered orders, cancels orders that have not shipped, and sends tracking for orders a few days late. Everything else goes to a person: large amounts, old orders, unclear messages, a model that was unsure, and any message that mentions injury, fraud or legal action.
4. **Keeps a record.** Every case is written to a ledger with the action, the reasons, the model and endpoint that read it, and the time it took.

The model cannot order an action. A model answer that is not exactly the record asked for is not repaired: the case goes to a person.

## Run it in two minutes (stand-in model, no GPU)

Needs Python 3.11 or newer. No packages to install for the app.

```
python -m orderdesk.stub_model 8001
```

In a second terminal:

```
set ORDERDESK_MODEL_BASE_URL=http://127.0.0.1:8001/v1
set ORDERDESK_MODEL_NAME=local-stand-in-not-a-model
python -m orderdesk.server
```

Open http://127.0.0.1:8080 and paste an email from [`samples/emails.json`](samples/emails.json). (On Linux or macOS use `export` in place of `set`.)

The stand-in is a few regular expressions behind the same HTTP interface. It is not a language model and not AMD, and the page says so while it is in use.

## Run it against the model on AMD (Token Factory)

The model is read through AMD's Token Factory (`notebooks.amd.com/tokenfactory`), the organiser-provided OpenAI-compatible service. Steps and what the evidence does and does not show: [docs/TOKEN_FACTORY.md](docs/TOKEN_FACTORY.md). Keys go in the environment, never in a file:

```
export ORDERDESK_MODEL_BASE_URL=<base URL from Token Factory, ending in /v1>
export ORDERDESK_MODEL_NAME=<model id from Token Factory>
export ORDERDESK_MODEL_API_KEY=<your key>
python scripts/check_amd_endpoint.py
python -m orderdesk.server
```

`check_amd_endpoint.py` has the endpoint read all ten sample emails and writes what it answered.

## Authorship

This code was written by an AI model (Claude, by Anthropic) for the repository owner. Licence: MIT.

## Container

```
docker build -t order-desk-agent .
docker run --rm -p 8080:8080 -e ORDERDESK_MODEL_BASE_URL=... -e ORDERDESK_MODEL_NAME=... -e ORDERDESK_MODEL_API_KEY=... order-desk-agent
```

The container holds the app only. It needs no GPU; the model runs behind the endpoint.

## Tests

```
pip install pytest
python -m pytest -q
```

30 tests: the rules (limits, windows, hand-over words), what a model answer must look like, the ten sample emails end to end, that an action changes the order book once, that an unusable model changes nothing, and the client and the app over HTTP against the stand-in. No test shows anything about AMD hardware.

## Configuration

| Variable | Meaning |
|---|---|
| `ORDERDESK_MODEL_BASE_URL` | The OpenAI-compatible endpoint, ending in `/v1` |
| `ORDERDESK_MODEL_NAME` | The model that endpoint serves |
| `ORDERDESK_MODEL_API_KEY` | Bearer key of the endpoint, if it has one |
| `ORDERDESK_PORT` | Port of the app (default 8080) |
| `ORDERDESK_DATA_DIR` | Where the order book and the ledger live (default `data/`) |

## Who wrote this

Written by Claude (Anthropic's AI model) working for the repository owner, in October 2026. No code from another project is included. See [LICENSE](LICENSE).
