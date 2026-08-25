# Operating Rules

Use this reference for cross-cutting defaults that apply across Google Docs publish, refresh, edit, and promotion workflows.

## State Boundaries

- Treat local Markdown, generated preview docs, polished live docs, Drive comments, and GitHub PR branches as separate states.
- A live Docs API edit proves the live doc changed; it does not prove the source Markdown or PR changed.
- Before saying a reviewer comment is fixed, verify the exact surface the reviewer sees: source, preview, live doc, or tab.
- Preserve stable live doc IDs, tab IDs, comments, native title/TOC/page numbers, section breaks, and manual polish unless the user explicitly accepts replacing them.
- Keep preview state bounded: one stable reusable preview per live doc by default, plus temporary experiment copies only when needed for side-by-side comparison.
- Trash rejected or superseded preview copies after the current preview is chosen, unless the user asks to preserve them.

## Standard Phase Order

Run document work in this order unless the user asks for a narrow direct edit:

1. setup and auth readiness
2. source scope and link plan
3. text import or in-place content edit
4. diagram/image rendering and insertion
5. fit and orientation
6. spacing and style cleanup
7. validation
8. comment replies or handoff

Do not resolve comments or report final status before the validation phase completes.

## Publishing Scope

- Create all target docs first, collect URLs, then rewrite cross-doc links in a second pass so `.md` links do not leak into published docs.
- Publish only the requested Markdown subtree or explicit allowlist.
- For repeated doc families, keep doc IDs, tab IDs, landscape ranges, and page-break headings in a local wrapper config.
- Keep project-specific heading names and layout preferences out of the shared skill.

## Markdown And Code Blocks

- Use Drive `text/markdown` import when native headings, lists, tables, links, and native Code Blocks matter in a draft/preview.
- Keep fenced Markdown blocks when native Code Blocks are desired from Drive import; do not convert them to indented code in that path.
- Whole-doc Drive Markdown update can create native Code Blocks while preserving file ID/URL, but it replaces the body and can break live polish.
- After import, run code-block spacing cleanup once content and orientation are stable.
- For inserted code in existing live docs, use native placeholders when available; otherwise use styled panels or a manual/UI conversion pass. See `native-code-blocks.md`.

## Diagrams And Images

- Do not rely on Google Docs to render Mermaid fences.
- Import stripped Markdown first, then insert rendered diagrams/images by real heading or placeholder anchors.
- Insert images from bottom to top so earlier indices do not drift.
- Center-align the paragraph containing each standalone diagram, figure, or rendered asset by default.
- Treat left-aligned standalone diagrams/figures as defects unless a specific document style or readability reason is documented.
- Keep diagram source assets only when useful for future maintenance; publish readable rendered or native content.
- Verify exports contain no raw Mermaid, HTML source, image placeholder text, or unexpected private glyph artifacts. Native Code Block markers such as `\ue907` are expected only in native-code-block validation and should not appear as stray visible prose.

## Tables

- Center standalone tables where the import/API supports table-block positioning.
- If true table-block centering is unavailable, prefer a readable full-width table and apply intentional cell alignment rather than leaving accidental narrow left-aligned tables.
- Wide tables may justify landscape, but landscape is not a substitute for table readability, centering, or source-side simplification.
- Normalize table-cell text after heading-adjacent imports. Body tables should not inherit heading-blue color, oversized heading fonts, or accidental heading emphasis.
- Preserve the document default body font when normalizing table text. Avoid introducing explicit fallback fonts such as Arial in a doc whose default body font is different; clear the explicit font or set the project-approved body font deliberately.

## Code Blocks

- Prefer preserving native Google Docs Code Blocks already present in the live shell.
- Docs API can fill/edit existing native Code Blocks, including multiline placeholder replacement, after Google's import/UI has created the native block context.
- Do not rely on private glyphs or raw text insertion to create native Code Blocks. Existing native blocks may expose `\ue907` private marker characters in the API; API insertion strips those markers and does not recreate the native editor widget.
- For arbitrary new native Code Blocks in polished docs, use pre-created placeholders, manual/UI conversion, or an explicitly approved browser-automation experiment. If native conversion cannot be proven safe, use styled panels and call out the limitation.
- See `references/native-code-blocks.md` for the detailed decision table and probe results.

## Orientation And Layout

- Keep portrait as the default.
- Use landscape for genuinely width-heavy tables or figures; do not accept unreadable diagrams just because they fit on a portrait page.
- Treat wide version-control/front-matter tables as width-heavy tables when portrait clips columns or causes unreadable wrapping.
- Apply landscape to the smallest useful content block, usually heading + short explanation + table/figure + immediate interpretation.
- Apply multiple section-orientation ranges from bottom to top.
- After section-break insertion, normalize accidental empty headings back to `NORMAL_TEXT` with zero spacing.
- Do not let landscape leak into prose-heavy appendix/reference sections. Appendix prose and record blocks should return to portrait unless a wide table/figure requires a bounded exception.
- If bounded `updateSectionStyle` changes leak landscape into later prose sections or diverge from the editor view, prefer an all-portrait safe preview and reintroduce landscape only after manual/editor validation of exact section boundaries.
- If a page still looks bad after fit/orientation, prefer source-side simplification before adding more Docs-side layout hacks.

## Text Emphasis

- Avoid accidental full-paragraph bold in normal body content.
- For record-style appendices, bold the record title/key label and field labels only; leave explanatory body text regular weight unless it is a deliberate warning/callout.
- Treat full-bold prose records as a formatting defect during preview review.

## Header, Footer, And TOC

- Detect headers and footers from the raw Docs structure before editing polished docs; page-number shells often live in footer segments with `autoText` values such as `PAGE_NUMBER` and `PAGE_COUNT`.
- Use the target organization's publication baseline for footer format. For GDP Labs docs, see `references/gdp-labs-publication-baseline.md`.
- Detect native TOCs from `tableOfContents` structural elements; do not treat a visible `Table of Contents` heading alone as proof that a native TOC exists.
- Preserve native TOC/header/footer/page-number shells in polished live docs unless the user explicitly approves replacing them.
- TOC refresh is not a reliable API-controlled finalization step; after heading or pagination changes, inspect/export the doc and report if a manual TOC refresh is needed.
- Do not claim page numbers or TOC passed from text extraction alone; verify raw structure and PDF/editor rendering.

## Organization-Specific Publication Baselines

- Keep this shared skill generic: org-level shell rules belong in a baseline reference, and project-specific doc IDs, heading names, and layout ranges belong in local wrapper configs.
- For polished GDP Labs docs, apply `references/gdp-labs-publication-baseline.md` before handoff.
- For non-GDP docs, do not apply GDP-specific footer, title-shell, or `DOC1-DOC8` reporting rules unless the user explicitly requests that standard.

## Live-Doc Safety

- Do not whole-doc refresh a polished live doc unless the user explicitly accepts replacing the live formatting shell.
- Prefer heading-scoped in-place edits for small live changes.
- Prefer preview approval before live updates when structure, diagrams, tables, or many sections changed; reuse the stable preview instead of creating another copy when possible.
- For risky live edits, patch a fresh copy of the current live doc first. Promote only after the simulation passes PDF/page, raw-structure, and link hygiene checks. Risky edits include orientation, headers/footers/page numbers, TOC-adjacent changes, image placement, large style ranges, structural tables, and same-doc anchor regeneration.
- Avoid delete-heavy cleanup around tables, section breaks, and trailing newlines unless the exact range behavior has been proven.
- If section-break deletion is rejected, prefer a neutralizing style change and re-audit rather than guessing more delete ranges.

## Validation Boundary

- Structural validation proves headings, links, images, orientation, and styles landed.
- Artifact validation proves the exported PDF/pages are readable and not blank or broken.
- Semantic validation proves the content is correct and consistent.
- PR validation proves the Git branch contains the intended source changes.
- Link validation proves URLs and anchors resolve to the intended surfaces; it must distinguish same-doc, cross-doc, external, and preview/experiment links.

Do not claim one boundary from another. For example, a clean live PDF audit does not prove PR 33 was pushed.

## Link Defaults

- Cross-doc links in previews should point to canonical live docs unless the user explicitly requests an unpublished preview-family review.
- Same-doc section references should be linked to headings/bookmarks where practical.
- Do not promote preview same-doc anchors blindly to live; regenerate or revalidate live anchors after promotion.
- Final live docs must not contain preview doc IDs, trashed doc IDs, raw Markdown `.md` links, or stale heading anchors.
