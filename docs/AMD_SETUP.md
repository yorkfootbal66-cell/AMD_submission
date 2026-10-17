# Serving the model on AMD Developer Cloud

**Not carried out yet.** These are the steps to take and the evidence to keep. Exact instance names, images and commands on AMD Developer Cloud were not available when this was written; follow AMD's current instructions where they differ, and note what you used.

## What is needed

- An AMD AI Developer Program account with AMD Developer Cloud access (the event page mentions free credits for new members).
- One GPU instance with the ROCm software stack.
- An open model that fits the instance. The app needs a model that follows an instruction to answer with a small JSON object; an instruction-tuned model of a few billion parameters is enough for this task.

## Steps

1. Create the GPU instance. Write down its type, its region and its hourly price, and set a spending cap.
2. On the instance, start a vLLM server with the chosen model, listening on port 8000, with an API key of your choosing. Use the vLLM build or container AMD documents for ROCm.
3. Open port 8000 to the address the app runs from, and to nothing else.
4. On the machine that runs the app, set `ORDERDESK_MODEL_BASE_URL`, `ORDERDESK_MODEL_NAME` and `ORDERDESK_MODEL_API_KEY`, then run `python scripts/check_amd_endpoint.py`.
5. Start the app and work through `docs/DEMO_SCRIPT.md`.
6. Stop the instance when you are done, and confirm on the provider's page that it is stopped.

## Evidence to keep (an HTTP answer does not show what hardware produced it)

| Evidence | Where it comes from |
|---|---|
| The instance page of AMD Developer Cloud showing the GPU type, while the instance runs | Screenshot |
| `rocm-smi` on the instance while `check_amd_endpoint.py` runs, showing the GPU in use by the vLLM process | Terminal capture on the instance |
| The vLLM start log, showing the model and the device it loaded on | The server's own log |
| `AMD_ENDPOINT_CHECK.json` | `scripts/check_amd_endpoint.py` |
| The app's ledger for the demo session, with the endpoint host and model of every case | `data/ledger.jsonl` |

In the demo video, show the instance page and `rocm-smi` next to the app handling an email.
