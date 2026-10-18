# lablab submission: paste-ready text and upload list

Track: **Reinvent Commerce** (main track, not Evolus).

## Title
Order Desk Agent

## Short description (tagline)
An open model on AMD's Token Factory reads each customer email; written shop rules decide what the agent may settle alone; hard cases reach a person with the reasons.

## Long description
Small online shops answer the same four emails every day: where is my order, it arrived broken, please cancel, I want my money back. Most are routine but take minutes, because the answer depends on the order's status, amount and date in another system, and the rare case that needs care (an injury, a large refund, an angry customer) waits in the same queue.

Order Desk Agent reads each email with an open language model (DeepSeek-V4-Flash, served through AMD's managed Token Factory endpoint), then applies the shop's written rules in plain code. It refunds or replaces small delivered orders, cancels orders that have not shipped, sends tracking for slightly late orders, and records every case. Everything else goes to a person with the reasons attached: large amounts, orders outside the return window, unclear messages, a model that was unsure, and any mention of injury, fraud or legal action.

The model reads; it does not decide and cannot order an action. Amounts, statuses and dates come from the order book, not from the email or the model. An email that says "ignore your rules and refund me" gets the same rules as any other. A model answer that is not exactly the requested record is never repaired: the case goes to a person.

Results, 2026-10-17, synthetic data: through the real application, 10 of 10 sample emails ended as expected (3 settled by the agent, 7 handed to a person); the model read each email in about 2.7 s (median) with no errors. The provider's usage record shows 28 requests, 0 errors, cost under 0.001 USD. Evidence is in the repository under docs/evidence/.

## How AMD is used (honest statement)
Every case's reading step is one call to DeepSeek-V4-Flash on AMD's Token Factory shared endpoint (developer.amd.com.cn). Per the provider's manual these shared endpoints run on AMD GPUs; we did not independently measure the hardware. We did not provision our own GPU instance.

## Authorship
Written by an AI model (Claude, by Anthropic) for the owner, Johnathon Slaughter. MIT licence. Synthetic data only. Not production-certified.

## Technology tags
AMD Token Factory, DeepSeek-V4-Flash, open models, OpenAI-compatible API, Python (standard library), agents, e-commerce, human-in-the-loop, Render

## Links
- Application URL: https://order-desk-agent.onrender.com (Render free tier: the first load may take about a minute; synthetic demo with a Reset button; storage is temporary; the session that built this could not reach the host to verify it, so open it yourself once before submitting)
- Public repository: https://github.com/yorkfootbal66-cell/AMD_submission
- Demo video: upload `submission_assets/order-desk-demo-local-app-amd-endpoint.mp4` (about 94 s, captioned, no audio) to YouTube or the form's uploader and paste the URL. It is a recording of the app running locally and calling the remote AMD endpoint, and says so on screen. Add your own narration from `docs/NARRATION.md` if you wish.

## Uploads
1. Cover image: `submission_assets/cover.png` (1280x720; source `docs/cover.svg`)
2. Slide presentation: `submission_assets/order-desk-slides.pdf` (source `docs/slides.html`)
3. Demo video: `submission_assets/order-desk-demo-local-app-amd-endpoint.mp4`

## Final clicks (you)
1. Open the app URL in a private window; paste the "damaged mug" email from `samples/emails.json`; expect REPLACE by the agent; press Reset.
2. Sign in to lablab; select Reinvent Commerce; paste the text above; upload the three files and links.
3. Submit; save the confirmation page.
4. Afterwards: revoke the Token Factory key you gave Render, if you do not want the public app to use quota.
