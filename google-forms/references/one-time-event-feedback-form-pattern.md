# One-time event feedback form pattern

Use this when building a public-response Google Form for a one-time gathering/event with a known participant list.

## Participant fields

Prefer a simple, non-routing structure unless the user explicitly needs dependent dropdowns:

1. `DATA PESERTA — Role` — dropdown/ListItem
2. `DATA PESERTA — Group / Date` — dropdown/ListItem
3. `DATA PESERTA — Nama` — dropdown/ListItem with all confirmed names sorted A-Z plus `Other / Nama belum ada di list`
4. `DATA PESERTA — Kalau nama kamu belum ada di list, tulis di sini` — optional short text

Google Forms does not support live dependent dropdowns (Role + Group filters Name) in a normal form. If filtering is required, approximate it with section routing, but this creates many sections and is usually too bulky for one-time feedback.

## Rating questions

If the user asks for 1-5 ratings with words/phrases for each rating:

- Do not put the scale block only in the form description.
- Prefer actual `rating` items when the deployed Apps Script supports them.
- Use consistent labels across similar questions:
  - lower label: `Sangat kurang`
  - upper label: `Sangat baik`
  - optional help text if the helper supports it: `1 = Sangat kurang · 2 = Kurang · 3 = Cukup · 4 = Baik · 5 = Sangat baik`

For event feedback, split ratings into individual rating questions rather than one grid if the user specifically wants Google Forms rating mode.

## Suggested sections/question groups

Keep the form short but grouped:

- Data peserta
- Overall feedback
- Feedback per section acara
- Kesan & saran

Typical rating questions:

- `OVERALL — Secara keseluruhan, seberapa puas kamu dengan [event]?`
- `OVERALL — Seberapa relevan tema [theme] dengan kebutuhan kamu saat ini?`
- `OVERALL — Seberapa nyaman suasana gathering untuk berinteraksi dan sharing?`
- `OVERALL — Seberapa baik alur acara dari awal sampai akhir?`
- `OVERALL — Seberapa pas durasi acara hari ini?`
- `SECTION — [Session]: ...`

Free-text questions:

- `KESAN & SARAN — Bagian mana yang paling berkesan buat kamu? Kenapa?`
- `KESAN & SARAN — Apa yang bisa diperbaiki untuk gathering berikutnya?`
- `KESAN & SARAN — Kalau ada satu hal yang kamu mau mulai lakukan setelah gathering ini, apa itu?`
- `OPSIONAL — Ada prayer request atau hal yang ingin kami doakan?`

Only include prayer request if the organizer is prepared to handle follow-up privately.

## Access model

For public event feedback:

- Public responder link: anyone with link can respond.
- Edit/results access: share the edit form or linked response Sheet only with selected people.
- Do not assume responder access is public. Verify the responder URL with an unauthenticated HTTP/browser probe when possible.

## Deployment/account pitfalls

Forms created by this helper belong to the Apps Script deployment account (`Execute as: Me`). OAuth tokens for Drive/Docs do not switch ownership.

Before production creation:

1. Confirm `GFORMS` points to the intended `/exec` endpoint.
2. Run a cheap endpoint probe (`GET` should return the Apps Script API message/actions).
3. Run a small create/get probe if question-type behavior is uncertain.
4. If title readback is blank or `rating` returns `Unknown question type: rating`, redeploy the current Apps Script code as a new Web App version before creating the production form.

After updating `.env`, run an ad-hoc verification script under `/tmp/hermes-verify-*.py` that checks:

- `.env` exists
- `GFORMS` matches the intended endpoint
- endpoint returns HTTP 200
- endpoint reports expected Apps Script API status/actions

Label this as ad-hoc verification, not full suite green.
