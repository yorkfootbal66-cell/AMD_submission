# Deploy on Render (Free web service, native Python, no Docker)

Settings (also in `render.yaml`, verified against the source: the server binds 0.0.0.0, reads `ORDERDESK_PORT`, serves `/healthz`, creates `ORDERDESK_DATA_DIR` itself):

| Setting | Value |
|---|---|
| Runtime / plan | Python / Free |
| Build command | `python -m compileall -q orderdesk` |
| Start command | `ORDERDESK_PORT=$PORT python -m orderdesk.server` |
| Health check path | `/healthz` |
| `ORDERDESK_DATA_DIR` | `/tmp/orderdesk` (temporary: lost on restart; disclosed on the page) |
| `ORDERDESK_TODAY` | `2026-10-13` (the sample orders have fixed dates; this keeps the rules' answers as recorded) |
| `ORDERDESK_MODEL_BASE_URL`, `ORDERDESK_MODEL_NAME`, `ORDERDESK_MODEL_API_KEY` | Secret values typed into Render's Environment page (not in the repo, not copied from the Claude session) |

Free services sleep when idle (first request after a pause is slow) and may be limited in hours; open the URL once shortly before judging. Anyone with the URL can submit text and use the shared Token Factory key's quota: use a key you can revoke after judging.
