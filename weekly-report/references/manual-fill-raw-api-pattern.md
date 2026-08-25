# Manual weekly-report fill via raw Docs/Drive APIs

Use this when the higher-level Google Docs scripts are insufficient for a live weekly report fill, especially when formatting must be preserved while only some sections can be grounded.

## When to use

- the user asks to start filling an existing report now.
- The report template already exists and must keep prior font/heading/list style.
- Docs/Drive OAuth works but Gmail/Chat metrics are unavailable.
- You need to link only PR markers and verify native Google Docs structure.

## Pattern proven on 24 May 2026 - 30 May 2026 report

1. Ground the week first in `Asia/Jakarta`, then Drive-search the exact title and export the target plus immediately previous filled report.
2. Refresh expired OAuth tokens before raw calls:
   - Docs/Drive token: `~/.hermes/google_token.json`
   - Calendar token: `~/.hermes/google_calendar_token.json`
3. Fill only grounded sections:
   - Issues: fetch `AIP Current Issues` with `includeTabsContent=true`; inspect child tabs under the month because parent tabs may be empty.
   - Accomplishments: run strict PR audit from `pr_summary`; do not trust `updatedAt` alone.
   - Meetings/OOO: query Calendar for `[week_start, next_week_start)` in `Asia/Jakarta`, dedupe by summary, exclude Out of office from meetings, and keep OOO separately.
   - Next Actions: adapt previous-report themes to current issues/PR themes.
   - Key Metrics and Technology/Business: leave placeholders unless metrics are available or the user selected candidate articles.
4. For section replacement, use raw `documents.batchUpdate` if needed:
   - delete only the body range under the stable heading, not the heading itself;
   - insert the new section text at `body_start`;
   - apply `NORMAL_TEXT`, Proxima Nova 11 pt, line spacing 100 to inserted body ranges;
   - apply native numbering/bullets only where the reference/current report expects it;
   - style `Pull Requests` as `HEADING_2` when the current/reference report does so;
   - link only the final trailing `#N` marker for each PR paragraph.
5. Verify by Drive text export and Docs API readback:
   - placeholder count and which placeholders remain;
   - no raw URLs visible;
   - PR link count equals PR row count;
   - body/list text is Proxima Nova 11 pt and `NORMAL_TEXT`;
   - headings are native `HEADING_1`/`HEADING_2`;
   - no accidental `HEADING_2` body/blank paragraphs.

## Small cleanup pitfall

Issue-source tabs may contain a copied line with a trailing stray backslash. If the exported target report shows `tenant\` or similar obvious copy artifact from the issue source, perform a narrow replace on that exact line only after insertion and re-export to verify. Do not broadly normalize issue wording.

## Handoff wording

Report exactly what was filled and why placeholders remain. Example:

```markdown
Filled:
- Issues from AIP Current Issues -> May 2026 -> Week N
- Accomplishments/Pull Requests from strict GitHub audit since YYYY-MM-DD
- Meetings and Out of Office from Calendar
- Next Actions from current issues + PR themes

Needs input:
- Key Metrics / OMTM: metrics block unavailable in current scope
- Technology/Business: choose candidate articles before insertion

Validation:
- placeholders: 2
- raw URLs visible: 0
- PR links: N/N
- body font/readback: Proxima Nova 11 pt, headings preserved
```
