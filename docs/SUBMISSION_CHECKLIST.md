# Submission checklist: state as of 2026-10-18 (04:57 UTC)

Official cutoff: 18 October 2026, 6:00 AM EDT (owner's participant-page screenshot).

| Item | State |
|---|---|
| Model read on AMD infrastructure | **Done, with attribution.** `DeepSeek-V4-Flash` on AMD's managed Token Factory endpoint, 10 of 10 sample emails (check) and 10 of 10 (application run), 2026-10-17. Hardware is stated by the provider's manual; not independently measured. Evidence: `docs/evidence/`. |
| Usage / cost | Provider usage endpoint, 2026-10-18: 20 requests, 0 errors, cost 0.0007 USD of a 1 USD daily limit (`docs/evidence/USAGE_CHECK.json`). Shared key limit: 20 requests per minute. |
| Working prototype | Done (32 tests; real run recorded). |
| Public repository | https://github.com/yorkfootbal66-cell/AMD_submission (MIT, copyright Johnathon Slaughter) |
| Cover image | `docs/cover.svg` (PNG export needed if the form wants a raster) |
| Slides | `docs/slides.html` (print to PDF if needed) |
| Demo video | **NOT DONE.** Local app calling the remote endpoint; see `docs/DEMO_SCRIPT.md`, `docs/NARRATION.md`. |
| Application URL | **NOT DONE.** Render Free, `render.yaml`; needs the owner's Render login and a revocable API key (`docs/DEPLOY_RENDER.md`). |
| Submission on lablab | **NOT DONE.** Owner signs in and submits; fields in `docs/SUBMISSION_TEXT.md`. |
| Container build | Not verified (no Docker daemon in the build session); the Render deployment is native Python. |
| Authorship | Written by an AI model (Claude, Anthropic) for the owner; synthetic data only. |
