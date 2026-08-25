# Weekly report deterministic contract vs heuristic boundaries

Use this whenever the user asks why a weekly report drifted, asks what can be made deterministic, or after a formatting/content repair exposes a repeatable failure mode.

## Test modes

Every preview/test run must declare which mode it performed:

1. `generate-from-sources` — create a fresh preview/template copy, gather current sources, fill, validate, repair the preview only, and revalidate. This is the only mode that tests report generation.
2. `copy-and-repair` — restore or repair already-filled content from another doc. Useful for recovery, but it does not prove the skill can generate the report.
3. `validate-only` — inspect an existing doc and report pass/fail without edits.

Do not claim generation was tested if the agent copied the already-filled live report into a preview.

## Validation verdicts

Use separate verdicts instead of one vague PASS:

- `CONTENT_PASS` — sections/content/link hygiene are complete enough: section order, placeholders, raw URLs, PR count, PR duplicate refs, PR link ranges.
- `FORMAT_PASS` — title, heading styles, body styles, list type, list nesting, and spacing match the reference/fingerprint.
- `DATA_GENERATION_PASS` — content was gathered from the intended data sources for this week, not copied from an already-filled live doc.
- `FINAL_PASS` — all applicable verdicts pass for the declared mode.

A helper script pass, including `repair_weekly_report_format.py`, is never by itself a `FINAL_PASS`. If content passes but reference formatting fails, report `CONTENT_PASS / FORMAT_FAIL`. If the preview was copied from live, report `DATA_GENERATION_NOT_TESTED`.

## Deterministic contract

A weekly report run should produce a machine-checkable artifact, not a best-effort visual approximation.

1. Target identity
   - Compute the week range in `Asia/Jakarta`.
   - Match the title exactly: `[Weekly Report: <REPORT_SUBJECT>] <DD Month YYYY> - <DD Month YYYY>`.
   - Resolve the target doc by known doc ID or exact-title Drive/Gmail discovery.
   - If multiple same-title docs exist, stop and report candidates instead of guessing.

2. Reference/style fingerprint
   - Always read the immediately previous accepted report, or the specific sample the report subject provided.
   - Extract a style fingerprint before writing:
     - title `namedStyleType`
     - main section heading `namedStyleType`
     - `Pull Requests` heading/body style
     - body font family/size
     - list metadata by section: native list vs manual text, list preset, nesting levels, and section restart behavior
     - paragraph spacing and indents
     - PR/article hyperlink ranges
   - Apply the fingerprint; do not infer list/heading style from memory.

3. Section schema
   - Maintain a canonical ordered section schema:
     - Issues
     - Accomplishments
     - Pull Requests
     - Meetings/Events/Training/Conferences
     - Key Metrics / OMTM
     - Next Actions
     - Technology, Business, Communication, Leadership, Management & Marketing
     - Out of Office
   - For each section, store expected content type: numbered list, nested numbered list, plain metrics block, manual numbered text, or article-link list.
   - Validate that every body/list/blank paragraph is `NORMAL_TEXT`; only the title and expected section headings may use heading styles.

4. Numbered list rendering
   - If the sample shows `1. / a. / i.`, use native Docs numbering with `NUMBERED_DECIMAL_ALPHA_ROMAN` unless the sample is visibly manual text.
   - Create each section's list range separately so numbering restarts at `1.`.
   - End list ranges before the following blank/heading paragraph; Docs API can absorb adjacent paragraphs into the list.
   - After list creation, delete bullets/numbering from headings and blank spacers, then re-apply heading/body styles.
   - Export PDF or text and verify visible markers: Issues starts `1.`, nested rows use `a.` and `i.`, PRs restart at `1.`.

5. PR row normalization
   - Treat PR entries as structured data: `{role, title, pr_number, url, status, activity_timestamp, inclusion_reason}`.
   - Render exactly once as `Role: title #N`.
   - The final trailing `#N` is the only hyperlink range.
   - Remove duplicate or unlinked issue/PR references before the final marker:
     - `(#1555) #1556` -> `#1556`
     - `fix #1365 — ... #1449` -> `#1449`
     - `for #1386 #1508` -> `#1508`
     - raw URL plus `#N` -> linked `#N` only
   - Postflight must fail if any PR row contains more than one visible `#\d+` reference or if any PR link text is not exactly `#\d+`.

6. PR inclusion audit
   - Use strict `pr_summary`/GraphQL evidence, not loose GitHub search.
   - Include authored PRs created in the week.
   - Include reviewed/commented PRs only when the report subject had a review/comment event in the week.
   - Exclude close-only, merge-only, bot-only, or stale `updatedAt` activity.
   - Sort by the report subject's actual activity timestamp, not PR `updatedAt`.
   - Keep an audit table/log locally with inclusion reason and timestamp for every row.

7. Link hygiene
   - PR links: only final trailing `#N` markers.
   - Technology/article links: article titles, not raw URLs.
   - No visible raw URLs unless the reference report explicitly uses raw URLs.

8. Preflight checks
   - Confirm OAuth scopes/access for Docs write and Drive/Docs export.
   - Confirm target doc ID and reference doc ID.
   - Backup or copy the live doc before structural rewrites.
   - Export target/reference text and Docs API JSON before writing.

9. Postflight checks
   - Export text/PDF and read Docs API structure.
   - Check placeholder count.
   - Check section order and heading styles.
   - Check no blank heading leaks.
   - Check list metadata and visible numbering per section.
   - Check PR duplicate refs and hyperlink ranges.
   - Check raw URL count.
   - Check Proxima Nova/body font where detectable.
   - Check page count/contact sheet when layout changed.

## Heuristic or user-confirmed areas

These can be assisted by evidence but should not be silently finalized as if deterministic:

1. Technology/Business article selection
   - Candidate sourcing can be automated.
   - Final item choice is editorial; present candidates when the user wants filtering.

2. Next Actions wording
   - Start from prior report baseline and current issues/PR themes.
   - Final phrasing is editorial; keep concise and report assumptions.

3. Meetings fallback
   - Calendar-derived events are deterministic if Calendar access works.
   - Reusing prior-week meetings without Calendar access requires explicit approval.

4. Key Metrics / OMTM
   - Exact metrics are deterministic only from Pamela/GLChat/pasted metrics.
   - If source access is missing, leave a note or ask for input; do not invent.

5. Issue status language
   - Tracker/doc status is deterministic when current issue tracker is accessible.
   - Summarizing status labels into polished wording is editorial; preserve source meaning.

## Failure behavior

If a deterministic input is missing, stop or mark the section incomplete. Do not fill by vibes.

Examples:
- Reference report unavailable -> do not guess list style; ask for sample or use last verified fingerprint.
- Calendar scope missing -> do not fabricate meetings.
- PR audit unavailable -> do not use `updatedAt` as a substitute.
- Style validation fails -> repair and rerun validation before handoff.
