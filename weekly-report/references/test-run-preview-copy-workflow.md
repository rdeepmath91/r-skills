# Test Run Preview Copy Workflow

Use this when the user asks for a "generate-from-sources" test run on a TEST copy, not the live doc.

## Steps

1. **Identify the template/master doc** — The `Master Data` doc (not the already-filled live weekly report) is the clean template.
2. **Create fresh TEST copy** — Use `google_workspace_full_token.json` (full `drive` scope required) to copy the master doc:
   ```
   POST https://www.googleapis.com/drive/v3/files/{MASTER_ID}/copy
   { "name": "[TEST Weekly Report: <SUBJECT>] <START> - <END>" }
   ```
3. **Fill from SOURCES, not the live doc** — Use:
   - GitHub GraphQL PRs for the exact week (Asia/Jakarta timezone: Saturday 00:00 to Saturday 23:59)
   - Calendar events (if Calendar scope available)
   - Key Metrics from GLChat/Bugle/Pamela (if Gmail/Chat scope available)
   - Previous week's report as formatting baseline only
4. **Validate against deterministic contract** — Run `scripts/repair_weekly_report_format.py` but do NOT treat its PASS as final. Compare against reference/fingerprint for:
   - Title style (HEADING_1 vs TITLE)
   - Section headings (HEADING_2, bold, Proxima Nova 16pt)
   - "Pull Requests" sub-heading must be HEADING_2
   - Native list types per section (Issues/PRs/Meetings/NextActions = NUMBERED_DECIMAL_ALPHA_ROMAN with section restart; Technology = BULLET_DISC_CIRCLE_SQUARE)
   - Issues nesting (3 levels: 1./a./i.)
   - PR links only on final `#N` markers
   - Proxima Nova 11pt body, 16pt headings
   - 0 placeholders, 0 raw URLs
5. **Repair preview only** — If validation finds safe mechanical issues (bad list style, missing links, wrong heading style), fix in the TEST copy and revalidate.
6. **Report** — Preview URL, doc ID, what was filled, what needs input, validation result, safe-to-apply recommendation.

## Common Pitfalls

- **Token scope**: `drive.file` cannot copy to different owner. Use `google_workspace_full_token.json` with full `drive` scope.
- **PR GraphQL query**: Must filter by Raymond-authored timeline events WITHIN the target week (Asia/Jakarta UTC+7), not by `updatedAt`.
- **Week boundaries**: Saturday 00:00 to Saturday 23:59 Asia/Jakarta = Friday 17:00 to Friday 17:00 UTC.
- **Repair script limitation**: Converts native→manual numbering. Do not use as final oracle.
- **Pull Requests heading**: Must be HEADING_2 (repair script demotes it to NORMAL_TEXT).
- **Issues nesting**: Previous reports use 3 levels (1. / a. / i.). Current fill often produces flat lists.