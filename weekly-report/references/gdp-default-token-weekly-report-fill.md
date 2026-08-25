# GDP Default Token Weekly Report Fill Pattern

Use this when the user asks to use the GDP default Google token to inspect or fill a weekly report.

## Trigger

- User asks for weekly report state/fill and mentions the GDP default token, or the broader writable workspace tokens are expired/unavailable.
- `~/.hermes/google_token.json` belongs to the `gdp-default` OAuth client and has at least Gmail readonly/modify, Calendar, Docs write, and `drive.file`.

## Key lesson

`drive.file` may not discover weekly reports owned/created by the report agent through Drive search. Do not conclude the report is missing just because Drive search returns no files. Use Gmail report reminder links to discover the Google Doc ID, then use Docs API directly.

## Discovery workflow

1. Refresh `~/.hermes/google_token.json` with its refresh token before live reads/writes.
2. Search Gmail for exact report-reminder phrases, for example:
   - `"Fill Weekly Report: <REPORT_SUBJECT>" newer_than:14d`
   - `"Open Weekly Report" "<REPORT_SUBJECT>" newer_than:14d`
   - exact date-range subject when known, e.g. `"[Fill Weekly Report: <REPORT_SUBJECT>] 07 June 2026 - 13 June 2026"`
3. Parse `https://docs.google.com/document/d/<DOC_ID>/...` links from the message body.
4. Fetch the document via `https://docs.googleapis.com/v1/documents/<DOC_ID>` and classify state:
   - blank template: `(please insert here)` appears under each section
   - filled: placeholder count is zero and each expected section has content
5. If filling, fetch the immediately previous report from Gmail/known link and compare structure before editing.

## Safe fill pattern

- Replace only the `(please insert here)` paragraph under each stable heading.
- Preserve the existing title and heading paragraphs.
- Remove the trailing template guide note only after all sections are filled.
- Use Docs API section replacements rather than Drive import so the live doc ID stays stable.
- After inserting links/bullets, run a text-style repair pass on inserted body paragraphs because Google Docs may leave unstyled text runs around linked PR markers.

## Formatting repair checklist

After edits, re-read the Docs API structure and verify:

- Title is `HEADING_1`; top-level report sections are `HEADING_2`.
- `Pull Requests` is treated the same way as the current/reference report; recent reports use it as `HEADING_2`.
- No blank/body paragraphs accidentally have `HEADING_2`.
- Body/list text uses Proxima Nova 11 pt and `NORMAL_TEXT`.
- PR URLs are attached only to the trailing `#N` marker; raw URLs are not visible in text export.
- Placeholder count is zero unless a section was intentionally left for the report subject.
- PDF export succeeds and a contact-sheet visual check has no blank pages, huge spacing gaps, or heading leaks.

## State-only report check

When the report subject only asks for the state and URL, do not refill. Discover the doc via Gmail, fetch it via Docs API, and report:

- title
- URL
- placeholder count
- missing sections
- raw URL count
- PR link count if applicable
- concise filled/blank status
