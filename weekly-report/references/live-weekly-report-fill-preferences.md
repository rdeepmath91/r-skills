# Weekly report live-fill corrections

Use this reference when filling the report subject's recurring weekly report Google Doc.

## User workflow preferences captured

- Preserve the live template structure and typography; avoid making sections feel like a generated report.
- For `Key Metrics / OMTM`, use the past week's performance/metrics baseline when available instead of leaving the placeholder or inventing metrics.
- For `Technology, Business, Communication, Leadership, Management & Marketing`, prioritize new agent-space items and major model releases. Avoid multiple articles about the same release; one canonical intro/release article is enough.
- For `Next Actions`, keep wording simple and direct. Avoid long compound status sentences.
- Verify edits against the live Google Doc ID, not an exported preview or duplicate.

## Concrete patterns

### Formatting fingerprint from accepted weekly reports

For Raymond's accepted weekly report format, top-level sections (`Issues`, `Accomplishments`, `Meetings/Events/Training/Conferences`, `Key Metrics / OMTM`, `Next Actions`, `Technology, Business, Communication, Leadership, Management & Marketing`, `Out of Office`) use `HEADING_1`; `Pull Requests` under `Accomplishments` uses `HEADING_2` and bold text. Body text is `NORMAL_TEXT`, Proxima Nova, compact `lineSpacing: 100`, and Proxima Nova should be verified against the previous accepted report before changing typography.

Use style spacing, not manual blank paragraphs, for major-section breathing room. Keep `Issues` tight under the title (`spaceAbove: 0pt`), set later top-level `HEADING_1` sections to about `spaceAbove: 12pt`, and set `Pull Requests` to about `spaceAbove: 6pt`. Do not add spacer paragraphs for this; they destabilize page breaks and can produce trailing blank pages.

Issues should come from the latest matching `AIP Current Issues` child tab for the report week, not merely the latest tab observed by an earlier cron log. Re-fetch the source doc directly before editing because a new child tab may have appeared after the cron ran. Preserve native numbering from the source where possible, and add/link GitHub tags embedded in the source text just like PR achievements: link PR markers to PR URLs and issue markers to issue URLs. Disambiguate bare references across GDP-ADMIN before linking; for example `#1022` may refer to `GDP-ADMIN/glaip-sdk#1022`, not `GDP-ADMIN/ai-agent-platform#1022`.

When Raymond asks to copy an updated AIP issue into "this week's" weekly report, target the current weekly report first even if an older weekly report already contains the same issue. If the current report's `Issues` section is still `(please insert here)`, replace only that placeholder/section with the updated issue item; do not backfill or rewrite other sections. If an older weekly report has stale status, treat it as secondary unless Raymond explicitly asks to update that historical report. After editing, read back the `Issues` section and confirm that non-Issues placeholders remain untouched so the handoff proves the scope stayed narrow.

`Out of Office` is plain body text, not a numbered list, unless the reference report for that week says otherwise.

After any visual-format repair, export both target and reference PDFs and compare contact sheets, not just Docs API paragraph styles. If `Key Metrics / OMTM` starts at the bottom of a page and splits immediately, add a clean page split in the preceding long numbered section (for example before meeting item 17 when it mirrors the reference) so Key Metrics appears as a coherent block. Remove trailing blank paragraphs afterward and re-export; fail validation on a trailing blank page.

### Metrics section

Keep the section's existing template headings. Populate from the previous/current performance sources using the existing GLChat / bug-report / AIP report structure where possible. Do not add explanatory meta-lines like `Using past week performance baseline:` or `Latest available source:` unless the live template already uses that style. Prefer `📊 GLChat Weekly Report`, a blank line, `Month-to-Date (...)`, a blank line, `🐛 Daily Bug Report`, a blank line, `Bugs from Internal Report`, a blank line, the metric rows, a blank line before `Datasaur Environment GLChat Bugs Report`, and a blank line before Datasaur metric rows.

### Tech section

Good item mix:

1. one canonical major model-release source, e.g. `Introducing Claude Opus 4.8 — Anthropic`
2. coding-agent / enterprise-agent adoption item, e.g. OpenAI Codex enterprise engineering
3. browser/security/admin agent item
4. enterprise workflow-agent item
5. agent governance/infrastructure item

Do not add several duplicate items about the same model release just because they are from different vendors. Research current official sources first and present 3-5 candidates for approval before writing. After Raymond chooses items, insert only those selected items as short numbered announcements with a linked `[Source]` marker; do not expose raw URLs in visible text.

### Next Actions

Prefer short items like:

```text
1. Finalize GLChat agent management policy and dashboard alignment.
2. Follow up token streaming and file-link fixes.
3. Continue A2UI, GL Runner, and GitHub agent action reviews.
4. Finish /goal orchestration follow-ups and defaults cleanup.
5. Continue Agent Skills sharing and adoption follow-ups.
```

### Live-doc verification

After editing, verify:

- exact live doc title and document ID
- newest matching weekly report in Drive
- no same-week duplicate exact title except the intended live doc
- placeholders count is zero, unless the user explicitly asked to leave a section blank
- raw visible URLs count is zero
- heading/body styles preserved, especially Proxima Nova body styling when the template uses it
- PR/article links remain hyperlink metadata, not raw text

If the user asks whether the update landed in the live report, answer with the live Google Docs URL, doc ID, modified time, and readback of the edited section.
