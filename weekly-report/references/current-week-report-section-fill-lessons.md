# Current-week weekly report section-fill lessons

Use this when updating Raymond's current weekly report after the initial report shell already exists, especially when copying `AIP Current Issues`, filling Calendar sections, or pasting metrics.

## AIP Issues copying

When Raymond asks to copy the updated issue into this week's report and the source is `AIP Current Issues`, do **not** copy only the one issue discussed in chat unless he explicitly asks for only that single item.

Default workflow:

1. Re-fetch the latest matching `AIP Current Issues` child tab for the report week with `includeTabsContent=true`.
2. Copy **all top-level issues** from that tab into the weekly report's `Issues` section.
3. Preserve nested issue details (`1 / a / b / c` or native list equivalent), bold top-level issue titles, and normal body text for details.
4. Link issue/PR refs inside the Issues section only.
5. Re-read the weekly report and verify the number of top-level issues matches the source tab.

Pitfall: replacing only the placeholder paragraph under `Issues` can leave the following `Accomplishments` heading styled as body text if the inserted list/paragraph operations bleed formatting into the next paragraph. After any Issues replacement, explicitly repair and verify:

- `Issues` = `HEADING_1`
- `Accomplishments` = `HEADING_1`, parallel to `Issues`
- `Pull Requests` = `HEADING_2`

Export/render at least the affected first page when the user reported mobile visual breakage.

## Calendar reauth and section fill

If Calendar read fails because the token is expired/invalid, generate a separate read-only Calendar OAuth flow and save it to `~/.hermes/google_calendar_token.json`. Do not overwrite the Docs/Drive token used for document edits.

For a pasted redirect URL:

1. Validate `state` against `~/.hermes/calendar_oauth_pending.json`.
2. Exchange the code with the stored PKCE `code_verifier`.
3. Save an authorized-user token with scope `https://www.googleapis.com/auth/calendar.readonly`.
4. Verify by reading `calendarList` before fetching events.

For Meetings/Events/Training/Conferences:

- Query the report week in `Asia/Jakarta`, inclusive start and exclusive next-week start.
- Exclude `workingLocation`, `outOfOffice`, and routine prep blocks such as `Daily Prep`.
- Deduplicate by event summary.
- Keep scheduled calendar meetings/events even if the invite response is declined when matching Raymond's prior weekly-report style; the report is a calendar-events summary, not attendance proof.
- Add labels from recurrence metadata: `[Weekly]`, `[Biweekly]`, `[Monthly]`.
- Use the same numbered-list style as previous reports.

For Out of Office:

- Fill from `eventType=outOfOffice` events.
- Preserve hourly leave and multi-day leave in readable prose, e.g. `Monday June 29th, 18:30–19:30 WIB — hourly leave`.
- If there is no guide paragraph after Out of Office, replace only the placeholder paragraph after the heading; do not require a trailing sentinel heading.

## Key Metrics / OMTM paste-in

When Raymond provides the metrics block, fill `Key Metrics / OMTM`, not `Accomplishments`, even if his wording says "following for the accomplishments". Accomplishments remains the PR section.

Formatting pattern:

- Use plain paragraphs, Proxima Nova 11 pt, line spacing 100.
- Bold only metric headers/subheaders: main report heading, date range, bug-report headings, model/concurrency lines, and performance/AIP report headings.
- Preserve the user's numbers exactly.
- Keep indentation for metric rows (`Total Opened`, `P0/P1/P2`, scenario rows).
- After Drive text export, decode bytes as UTF-8 to verify emoji correctly; terminal display mojibake alone is not a document failure.

## Final validation

After section fills:

- Export Drive text and confirm only intentionally unfilled placeholders remain.
- Export PDF and render/check the pages covering changed sections.
- Specifically inspect: heading hierarchy, numbered list alignment, Key Metrics indentation, Out of Office readability, and trailing blank pages.
