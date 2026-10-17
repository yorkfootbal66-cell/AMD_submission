# Decisions and open inputs after the owner's hand-over of 2026-10-13

Written by Claude. This prototype is Claude-authored. Its 30 tests run against a stand-in model. It is not HUNT-native work and it has not run on AMD hardware.

## Decided in the hand-over

| Matter | Decision |
|---|---|
| Entry | Order desk agent, main Track 3 "Reinvent Commerce" (the recommended minimum entry) |
| AMD spending cap | 0 USD |
| Internal completion target | 16 October 2026, 5:00 PM America/New_York. This is not an official deadline. |
| Publication | Not authorized. No repository is created or pushed. |
| Repository name | `lilDavid-HUNT-ACTIII` is a proposal only, until the owner gives the GitHub owner and name |
| Licence notice | The copyright holder in `LICENSE` stays a placeholder until the owner gives the exact legal name |

## What the public pages say (read 2026-10-13, without signing in)

- **Event page** (`lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii`): online build 12 to 18 October 2026. No date is labelled as the submission cutoff, and no time zone is given. The live dashboard read 12 to 17 October earlier the same day. The official deadline is unverified.
- **Access, from the event's FAQ:** the event is hosted at `notebooks.amd.com/tokenfactory`. No billing or card is needed. A participant needs only the API from Token Factory, not the 100 USD credit for new members.
- **Token Factory page** (`notebooks.amd.com/tokenfactory`): a sign-in wall. The only content is "Sign in with AMD AI Developer Program". No API address, model list, quota or terms can be read without an account. I did not sign in.
- **Requirements that bind this entry:** a meaningful part of the workload runs on AMD infrastructure, and that part is in the product shown to judges. A submission holds a working application URL, a public repository, a cover image, a demo video and slides.

## What this means for the prototype

- The model client is already a setting, not code: `ORDERDESK_MODEL_BASE_URL`, `ORDERDESK_MODEL_NAME`, `ORDERDESK_MODEL_API_KEY`. It speaks the OpenAI-compatible chat interface.
- Whether Token Factory's API has that shape is unknown until someone with access reads its page. If it differs, `orderdesk/model.py` is the one file to change.
- `scripts/check_amd_endpoint.py` is the first thing to run once an endpoint exists. It sends one request and reports what answered.

## Inputs only the owner can supply

1. Token Factory access: sign in with the AMD AI Developer Program account, then give the endpoint address, the model name and the key as the three environment variables above. The key never goes into the repository.
2. The enrolled-participant submission cutoff with its time zone, from the organiser.
3. The GitHub owner and repository name, and the word to publish.
4. The exact copyright holder for `LICENSE`.
5. The cover image, the demo video and the slides, or the word to prepare drafts.

## Not done, and not authorized by the hand-over

No sign-in, no paid data, no cloud node, no GPU or model launch, no Docker provisioning, no publication, no production activation.
