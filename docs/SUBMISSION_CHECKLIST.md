# Submission checklist: what is done, what is missing

Checked against the event page and its live page as fetched on 2026-10-13 (09:30 UTC). This file is the honest state of the entry; update it as items close.

## Deadline

- The event page says "Online Build: 12-18 October 2026". The organiser's live page says "Online Build: 12-17 October 2026" and "Live · Submissions open".
- Neither page gives a submission time or a time zone.
- **Plan to submit by the end of 16 October 2026**, until the organisers confirm in writing.

## Required of every project

| Requirement (page wording) | State | What is missing |
|---|---|---|
| "Every project must run a meaningful part of its workload on AMD infrastructure or AMD hardware." | **NOT MET** | An AMD Developer Cloud instance serving the model. The app is ready to use one. |
| "The AMD component must be part of the working product shown to the judges." | **NOT MET** | The same. The page and the ledger already show which endpoint and model read each case. |
| "Working prototype" | Done with the stand-in; not yet with a real model | A run against the AMD endpoint (`scripts/check_amd_endpoint.py`) |
| "Selected challenge" | Proposed: Track 3, "Reinvent Commerce" | The owner's choice of entry |
| "Project title", "Short and long descriptions", "Technology tags" | Drafted in `docs/PITCH.md` | The owner's wording |
| "Cover image" | **MISSING** | An image |
| "Demo video" / "Video presentation" | **MISSING** | A recording; the script is `docs/DEMO_SCRIPT.md` |
| "Pitch presentation" / "Slide presentation" | Outline in `docs/PITCH.md`; **slides MISSING** | Slides |
| "Clear explanation of the problem and intended user" | Drafted in `docs/PITCH.md` | |
| "Public GitHub repository" | **MISSING**: this is a local repository | The owner's GitHub account and the decision to publish |
| "Demo application platform", "Application URL" | **MISSING** | A host for the container and its address |
| "Submissions must be original and MIT-compliant." | MIT licence file present; code written for this entry | The copyright holder's name in `LICENSE`; the organisers' answer on what "MIT-compliant" requires |

## If the entry goes to the Evolus partner track instead

Not built. That track also requires an Evolus event workspace (event code from kickoff), at least two Evolus building blocks, the app driving Evolus through its APIs, and the model on "your own vLLM endpoint on AMD Developer Cloud". None of those accounts or keys exist on the machine this was written on.

## Inputs only the owner can supply

1. Which entry: this prototype, the September market-research slice, or the October opportunity-screening build.
2. AMD AI Developer Program membership and AMD Developer Cloud access; one GPU instance, the model to serve, and a spending cap.
3. For the Evolus track: the event code, the workspace, its application id and API key (as environment variables only).
4. Enrolment on lablab, the team, and the submission deadline with its time zone as given to participants.
5. The text of the hackathon rules and participation terms (the pages returned no text to a fetch), or the organisers' written answers on prior code, AI-written code and "MIT-compliant".
6. The public GitHub repository and the copyright holder's name.
7. A host for the demo application.
8. How the entry's authorship is to be stated: this code was written by an AI model (Claude) for the owner.

## What was verified, and how

| Claim | Evidence |
|---|---|
| The app's 30 tests pass | `python -m pytest -q` on Python 3.13, 2026-10-13 |
| The ten sample emails end as `samples/emails.json` says, with the stand-in (3 settled by the agent, 7 handed to a person) | The same tests, and `docs/LOCAL_DEMO_RUN.json` |
| The container builds and runs | **NOT VERIFIED**: the Docker daemon was not running on the machine |
| The model runs on AMD hardware | **NOT VERIFIED**: no AMD instance |
