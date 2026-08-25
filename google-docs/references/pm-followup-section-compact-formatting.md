# PM follow-up section: compact formatting, numbered structure, and compatibility wording

Use this when adding or revising a PM-facing follow-up section in an existing Google Doc, especially after a technical audit.

## Reader-facing narrative

1. Avoid naming the work `skill migration` when the customer already has working skills in another agent/runtime.
2. Prefer:
   - `existing skill compatibility validation`
   - `existing skill reuse in AIP`
   - `OpenCode-to-AIP skill compatibility`
   - `AIP readiness for Datasaur's existing skills`
3. Narrative shape:
   - Customer already has working skills in OpenCode.
   - The open question is whether AIP can reuse those skills with equivalent behavior, reliability, and safety.
   - Adaptation or rebuild is a possible outcome only after compatibility gaps are proven.
4. Avoid implying GDP Labs is committing to a broad migration/rebuild unless the user explicitly wants that scope language.

## Structure preference

Use summary first, then details. Do not use generic bullet glyphs for PM-facing scanability when Raymond asks for numbered/lettered structure.

Recommended section order:

1. Summary
2. Details
3. What this means for the project/customer
4. What is not fully solved yet
5. Suggested follow-up plan
6. PM-facing summary

For details, use explicit numeric labels such as:

```text
1. Existing skill compatibility: ...
2. More reliable Skill usage: ...
```

For follow-up plans, use a native Google Docs table with a numbered `#` column rather than a bullet list or Markdown-looking pipe table in the rendered doc.

## Google Docs spacing pitfall

When inserting a section with the Docs API, paragraphs may inherit large `spaceAbove` values, often `24pt`, from nearby heading/body styles. This can create huge visual gaps in the editor even if the Markdown export looks acceptable.

Do not fix this by flattening all spacing to zero. That produces a cramped section and breaks the document rhythm. First inspect nearby approved content in the same doc, then match its paragraph style cadence.

Recommended correction workflow:

1. Inspect raw paragraph styles inside the target section and in the immediately previous approved section.
2. Remove only genuinely empty paragraphs or accidental blank headings. Do not delete intentional section breathing room.
3. Match nearby approved spacing unless the user asked for a compact one-page fit. A common rhythm is:
   - body/list paragraphs: `lineSpacing: 100`, `spaceAbove: 12pt`, `spaceBelow: 12pt`
   - subsection headings: `spaceBelow: 4pt`, with moderate `spaceAbove`
   - main section heading: regular `HEADING_1` scale and spacing, not a full-page hero gap
4. If a new section starts awkwardly midway down the previous page, use `pageBreakBefore: true` on the section heading rather than collapsing paragraph spacing.
5. Restore selective bold labels after broad style passes, because range-wide text style updates can clear bold emphasis.
6. Export to PDF and render contact sheets. Validate visually in the rendered pages and, when available, compare against the Google Docs editor screenshot.

## Common QA checks

1. No blank `HEADING_1` / `HEADING_2` paragraphs before the inserted section.
2. No generic `*` / `-` bullets inside the PM-facing inserted section when numeric/lettered lists were requested.
3. No table header orphaned alone at the bottom of a page.
4. No giant gaps between heading, summary, details, and table.
5. No Markdown leakage such as visible `|`, `---`, or literal `**` in the Google Docs editor.
6. Wording uses `compatibility`, `reuse`, or `validation` when the work is proving whether existing skills run in AIP, not `migration` by default.
