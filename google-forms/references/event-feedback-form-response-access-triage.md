# Event feedback form response-access triage

Use this when a user asks to recall a one-time event feedback Google Form and check whether responses are accessible.

## Identify the final form when duplicates exist

One-time event forms often have several duplicate drafts with the same title. Do not trust title alone.

Prefer this evidence order:
1. The responder URL actually embedded in the event deck/QR slide.
2. A generated `*_summary.json` or `*_created.json` artifact that records `status`, `formId`, `editUri`, and `responderUri`.
3. `gform.py get FORM_ID` readback matching the exact responder URL.
4. Drive modified time/title only as a weaker tie-breaker.

For deck-linked feedback forms, check any QR/update readback artifact first: the public responder URL used in the QR slide is usually the authoritative final URL, not earlier duplicate form drafts.

## Access layers are separate

Report these separately instead of collapsing them into “can/cannot access the form”:

| Layer | What it proves | Typical result |
|---|---|---|
| Public responder URL | Attendees can open/submit the form | HTTP 200 / live form HTML |
| Apps Script `get` | Script owner can inspect title/questions/responder URL | Form structure available even if browser edit access is missing |
| Browser edit URL | Current browser Google account has edit access | May redirect to responder form with “Minta akses pengeditan” |
| Forms API | Current OAuth token has Forms API access and file permission | 403 if token lacks Forms scopes or permission |
| Public `/viewanalytics` | Public summary charts enabled | Often 403 even when responder URL is public |
| Apps Script `responses` | Script can export raw responses | May timeout before redirect/body for forms with many/slow responses |

## Response export fallback order

1. Try `python3 scripts/gform.py responses FORM_ID` once.
2. If it times out, retry once with a longer timeout or a direct POST/redirect probe to distinguish POST timeout from redirected GET timeout.
3. Search Drive for a linked responses spreadsheet, but do not assume one exists; many Forms have no linked Sheet.
4. If Forms API returns 403 and token scopes are only Drive/Docs, say that the current OAuth path cannot read responses; ask for Forms scopes/share access or use the Apps Script-owner path.
5. If browser edit access shows “Minta akses pengeditan”, say the current browser account lacks edit access even if Apps Script can still read structure.

## User-facing summary pattern

Keep the answer crisp:

- Final e-form URL
- Edit URL / form ID if known
- What was verified live
- Whether responses are accessible
- Exact blocker and next viable path

Avoid dumping full attendee names or free-text responses unless the user explicitly asks for response details.