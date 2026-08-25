# One-time event feedback forms from participant sheets

Use this when building a lightweight Google Form for a single gathering/event from a participant roster spreadsheet.

## Participant identity pattern

For one-time public responder forms, prefer a simple identity block over complex routing:

1. `Role` — dropdown (`DF`, `DL`, `DM`, `CT`, `Other`, or the event's actual roles).
2. `Group / Date` — dropdown from the roster's group/date column.
3. `Name` — dropdown of confirmed participant names sorted A–Z, plus `Other / Nama belum ada di list`.
4. `Kalau pilih Other, tulis nama kamu` — optional short answer.

Why: Google Forms cannot do true live dependent dropdown filtering (`role + group -> filtered names`) in a standard form. It can approximate this with section routing, but for one-time events that creates many sections and is usually overkill. Use section routing only when wrong-name prevention matters more than form simplicity.

## Access pattern

- Responder link can be public: anyone with the link can respond.
- Edit access stays private via explicit collaborator sharing.
- Results stay private unless the form setting `View summary charts and text responses` is enabled for respondents.
- For selected people to view results, share the Form or linked response Sheet with viewer/editor access; do not expose the public respondent link as a results link.
- Public responder access, Apps Script/FormApp structure access, browser edit permission, Forms API scopes, public analytics, and response export are separate gates. Report them separately instead of collapsing everything into “can/cannot access the form.”
- If `gform.py responses FORM_ID` times out or Forms API returns 403, say that the form URL/structure is accessible but results export needs owner/edit access, a working Apps Script response export, or a linked response Sheet fallback.

## Duplicate-draft and QR recovery

One-time event forms often leave same-title drafts from rating/scale/helper redeploy attempts. To identify the production form later:

1. Prefer the local creation summary/readback pair that says `created_and_verified`, with final `formId`, `editUri`, `responderUri`, question count, and public responder HTTP status.
2. Cross-check downstream deck/QR readback artifacts. If the QR slide used a responder URL, treat that as the participant-facing production URL unless the user says it was replaced later.
3. Use `gform.py get FORM_ID` to confirm title, description, `responderUri`, and question count. Current helper readback may not expose all option labels/settings.
4. Do not pick the newest similarly titled form from `gform.py list` by modification time alone; Apps Script listing may show duplicate drafts and may not match the URL actually distributed to participants.

## Feedback question shape

Prefer mostly quantitative questions in the event language, with only a few free-text prompts.

Indonesian default scale:

`1 = Sangat kurang`, `2 = Kurang`, `3 = Cukup`, `4 = Baik`, `5 = Sangat baik`

Typical sections:

- Overall satisfaction and relevance.
- Per-program-segment ratings, based on the slide/deck agenda (e.g. Games, Praise & Worship, testimony/story, Q&A, small group).
- Flow/duration question.
- 1–3 free-text questions: most meaningful part, improvement suggestion, one intended follow-up action.
- Add prayer/follow-up request only when the team is ready to handle it privately.

## Roster filtering

When reading a participant spreadsheet, filter the dropdown name list to confirmed/active participants. Exclude cancelled rows and blank rows. Preserve `Other / Nama belum ada di list` in case the roster misses someone or a guest attends.
