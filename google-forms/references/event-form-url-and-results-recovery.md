# Event form URL recovery and response-access triage

Use this when asked to recall an event feedback e-form URL and check whether results are accessible.

## Recovery order

1. Search local generated artifacts first when the form was created through the helper:
   - `~/gform_automation/generated/*summary.json`
   - `*_created.json`
   - `*_readback.json`
   - QR/deck QA folders that may include a `responder_url` or slide readback.
2. Treat the newest `*_summary.json` with `status: created_and_verified`, matching event title/date, public `responderStatus: 200`, and matching QR/deck responder URL as the best final-form evidence.
3. Confirm with live `gform.py get FORM_ID` when the Apps Script account can open the form. Compare `responderUri` to the URL in the summary/QR artifact.
4. If multiple duplicate drafts exist with the same title, prefer the one that was inserted into the user-facing QR/deck or the one whose summary says it was verified. Do not hand off earlier draft responder URLs just because they share the same title.

## Response-access triage

When `gform.py responses FORM_ID` fails or times out, distinguish access paths instead of saying results are unavailable generically:

- Public responder page HTTP 200 only proves respondents can open the form.
- Browser edit URL redirecting to `viewform?edit_requested=true` with `Minta akses pengeditan` means the current browser account lacks edit access.
- Forms API 403 means the current OAuth/token path lacks permission or scopes for that form.
- Public `/viewanalytics` 403 means public analytics are not enabled.
- Apps Script `responses` timeout can happen on forms with responses or Apps Script slowness; retry once with a longer timeout, then fall back.

## Fallbacks for results

1. Search Drive for a linked spreadsheet named like `<form title> (Responses)` and export it as CSV if present.
2. If no linked sheet is visible, ask for either edit access to the form under the configured account or a linked response spreadsheet.
3. If only public responder access is available, report that the URL is verified but results are not accessible through the current auth path.

## Report shape

Keep the answer compact:

- final responder URL
- edit URL / form file ID if known
- evidence used to identify the final form
- whether form structure is accessible
- whether responses/results are accessible
- exact blocker and next access step
