# Morning guide: remaining steps, in order (official cutoff: 18 Oct 2026, 6:00 AM EDT)

State when written (23:00 UTC, 17 Oct): repo public, real Token Factory run recorded in `docs/evidence/` (10 of 10 samples as expected, DeepSeek-V4-Flash, median 2.7 s). Not done: usage check, video, hosted URL, submission, copyright name.

## 0. Copyright name
Edit line 3 of `LICENSE` on GitHub (currently a bracketed placeholder).

## 1. Usage check (before any further model calls)
Open the Token Factory page / manual and look at the usage view for free-quota status. Shared usage is described as free; the model list shows non-zero per-token prices, so confirm nothing is being charged. The earlier run used about 30 short requests.

## 2. Hosted app (Render, Free)
1. render.com, sign in (a card may be requested; if so, stop and use another free host).
2. New, Blueprint, connect GitHub repo `yorkfootbal66-cell/AMD_submission`, branch `main`; it reads `render.yaml`.
3. When asked for secrets enter: `ORDERDESK_MODEL_BASE_URL` = `https://developer.amd.com.cn/radeon/api/v1`, `ORDERDESK_MODEL_NAME` = `DeepSeek-V4-Flash`, `ORDERDESK_MODEL_API_KEY` = a key you can revoke after judging.
4. Wait for the health check; open the URL; the page must show model DeepSeek-V4-Flash at developer.amd.com.cn with no stand-in warning. Paste the "damaged mug" email: expect REPLACE by the agent. Press Reset afterwards.
5. Without Render's key route, a local run works the same way (below).

## 3. Video (about 3 minutes) -- local app using the remote AMD endpoint
Label it that way in the video and in the submission if the app is not hosted.
```
export ORDERDESK_MODEL_BASE_URL=https://developer.amd.com.cn/radeon/api/v1
export ORDERDESK_MODEL_NAME=DeepSeek-V4-Flash
export ORDERDESK_TODAY=2026-10-13
export ORDERDESK_MODEL_API_KEY=<your key>     # needed on your own machine; never show it on screen
python -m orderdesk.server                     # then open http://127.0.0.1:8080
```
Follow `docs/NARRATION.md`. Paste, in this order (from `samples/emails.json`): damaged mug, expensive refund, legal threat, "ignore your rules". Show `/api/cases` and `docs/evidence/`. Say: AMD hardware is stated by the provider's manual; we did not measure it. Say the code was written by Claude. Do not show the key or terminal environment.
Note: model readings vary a little between calls; the rules decide, so outcomes should match, and any difference should be shown honestly.

## 4. lablab submission (you sign in)
Paste fields from `docs/SUBMISSION_TEXT.md`. Uploads/links: cover (`docs/cover.svg`, PNG if required: export from the SVG), slides (`docs/slides.html`; export to PDF with the browser's Print), video URL, app URL, repo URL https://github.com/yorkfootbal66-cell/AMD_submission. Select track Reinvent Commerce. Check every link opens in a private window, then submit and save the confirmation page.

## Honest-claims list (keep in the submission)
- Ran against DeepSeek-V4-Flash on the AMD Token Factory shared endpoint on 2026-10-17; per the provider's manual these run on AMD GPUs; not independently measured.
- Synthetic data only. Code written by Claude (Anthropic) for the owner. MIT.
- Not claimed: production certification, HUNT involvement, GPU model, deployment (until the URL works), any result not in `docs/evidence/`.
