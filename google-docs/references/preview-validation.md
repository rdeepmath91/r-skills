# Preview Validation Rules

## Purpose
- Use these rules when validating a Google Docs preview rebuilt from Markdown.
- The goal is deterministic review: the preview should be source-faithful, readable, and free of layout accidents before it replaces a live shared doc.
- For validation boundaries and minimum checks across setup, source alignment, live docs, comments, PR state, and skill integrity, use `references/validation-workflows.md`.

## Rules

### R0: Preview lifecycle

- Keep one stable reusable preview per live doc by default.
- Reuse that preview for successive validation passes instead of creating a new timestamped copy each time.
- Create a separate experiment preview only when side-by-side comparison or rollback isolation is genuinely needed.
- Rename the surviving preview to a durable name such as `<Doc Name> Preview` after it becomes the current candidate.
- Trash rejected or superseded preview experiments once the current candidate is clear, unless the user asks to keep archival copies.

### R1: Source-driven preview
- Rebuild the preview from the current local Markdown source.
- Do not patch the preview manually in ways that diverge from source unless the change is a documented Docs-only formatting fix.

### R2: Heading mapping
- Do not blindly omit the top-level Markdown `#` title. For polished/boss-facing docs, keep a visible native title in the body or preserve the existing title shell unless the user explicitly wants the body title removed.
- If a preview workflow intentionally treats the top-level `#` as Drive title only, document that choice and verify the first page still reads like a finished Google Doc.
- Map headings deterministically:
  - `##` -> `Heading 1`
  - `###` -> `Heading 2`
  - `####` -> `Heading 3`
  - continue similarly for deeper headings

### R3: Mermaid and asset transform
- Do not leave raw Mermaid fences in the Google Doc.
- Render Mermaid locally to PNG.
- Upload and insert diagrams and local assets as inline images.
- When Markdown uses diagram anchors/placeholders, replace each anchor with its rendered inline image in the relevant section; do not leave an image-only appendix/gallery unless the source intentionally calls for one.
- After rebuild, verify that no Mermaid fences, placeholder tokens, or diagram anchors remain. Also count inline image objects and compare against the expected diagram count before claiming the preview is refreshed.

### R4: Ordered lists only
- Preserve ordered lists from source as ordered lists in the preview.
- Do not introduce generic unordered bullets where the source expresses sequence, procedure, or numbered obligations.
- For slide outlines, presenter notes, and form-question recommendations, avoid relying on one long auto-numbered list across many headings. Prefer explicit labels such as `Slide 3 — Demo` or `Question 4 — Platform` when the numbering itself will be reviewed.

### R5: Block placement and fit
- Center diagrams, figures, and standalone visual assets by default.
- Center table blocks where the import/API supports it; if table block centering is not available, use a readable full-width table and center/align table contents deliberately.
- Left-aligned diagrams, figures, or standalone tables are layout defects unless a specific doc style or readability reason is documented.
- Do not let a figure or table create an avoidable blank page or a visibly broken text/figure split.
- Treat orphaned headings, heading-only pages, and continuation-only pages as layout defects, not as acceptable defaults.
- Treat visually large vertical gaps before headings, after headings, or between list/index entries as layout defects even when the page is not sparse by automated text-density rules.
- Normalize paragraph spacing before approval: headings should not inherit excessive `spaceAbove` / `spaceBelow`, lists should not have report-style block gaps unless the spacing is deliberate, and record/index entries should remain compact enough for human scanning.
- Body records should not be full-paragraph bold by accident. Bold only the record title/key label or field labels unless the whole line is intentionally a heading or callout.

#### R5a: Diagram fit rule
- Oversized diagrams must be corrected before review is considered complete.
- Do not use one fixed insertion width for every diagram.
- Size each inserted diagram from its aspect ratio.
- Portrait defaults for inline diagrams:
  - max width: `440pt`
  - target max height: about `360pt`
- Landscape defaults for inline diagrams when landscape is already justified:
  - max width: `620pt`
  - target max height: about `420pt`
- If a diagram is too tall at portrait size, fix it in this order:
  1. change the source layout so the diagram is shorter, for example `flowchart LR` instead of `flowchart TD`
  2. reduce insertion width using aspect-ratio-aware sizing
  3. split the diagram into two diagrams if the logic is still readable that way
  4. use landscape only when width, not height, is the true readability constraint
- If one-page portrait readability is explicitly required, run a strict fit gate (not a visual estimate):
  - compute `height_at_440pt = image_height_px * (440 / image_width_px)`
  - if `height_at_440pt` is far above ~`360pt`, fail one-page portrait readability and redesign (layout change or split)

### R6: Orientation must be justified
- Portrait is the default.
- Landscape is allowed only when portrait-first fitting still leaves a table or figure unreadable.
- Apply landscape to a dedicated section only.
- Restore portrait immediately after the justified landscape section.
- Wide front-matter tables, especially version-control/reviewer tables, are valid landscape candidates when portrait clips columns or forces unreadable wrapping.
- For square or near-square overview diagrams, prefer portrait with a reduced width before forcing landscape.
- Landscape is a width remedy, not a generic "large figure" remedy.
- Text-heavy appendices should remain portrait by default. A landscape appendix range is acceptable only for genuinely wide diagrams/tables, and must return to portrait before prose-heavy reference records.
- After any appendix orientation change, audit from the first appendix heading through the end of the document to ensure no landscape section leaks into prose-only appendix pages.
- If exact landscape section boundaries cannot be made stable in both editor and PDF export, prefer an all-portrait preview over leaking landscape into prose-heavy appendices.

### R7: No fully blank pages
- The exported PDF must not contain real blank pages.
- A trailing text-extraction artifact does not count as a real page.
- A final page that is visually blank in the PDF is a real issue even when the raw Docs structure still contains a trailing empty paragraph.

### R8: Sparse pages require justification
- Sparse pages are acceptable only when they are a deliberate section-boundary tradeoff that preserves readability.
- If a sparse page exists, verify that removing it would require a worse failure such as unreadable landscape content, broken figure placement, or a merged section orientation.
- If a page contains only a carry-over bullet, one validation sentence, or one lonely code brace, treat it as a pagination defect unless there is a very strong reason to keep it.

### R8b: Large-gap pages require inspection

- A page can fail visual review without meeting the sparse-page threshold.
- Flag pages where large blank bands appear between normal paragraphs, before a heading, or between short list entries.
- Fix large-gap pages by adjusting paragraph spacing, keep flags, page breaks, or section boundaries before considering content cuts.

### R8c: Link hygiene

- Preview docs must not introduce accidental links to obsolete previews or trashed documents.
- Cross-doc links in previews should point to canonical live docs unless the user explicitly requested an unpublished preview-family review.
- Same-doc section references should link to headings/bookmarks where practical.
- Same-doc preview links must be regenerated or revalidated after live promotion because preview anchors are not final live anchors.
- Final live validation must prove there are no preview doc IDs, trashed doc IDs, raw `.md` links, or unresolved same-doc references that should be links.

### R8a: No section-break artifacts
- Orientation changes must not split visible words, headings, or list items.
- After any section-orientation pass, check for accidental text fragmentation such as `its` / `elf` or `App` / `endices`.
- The exported Markdown should not contain stray empty headings such as bare `#` or `##` lines created by section-break insertion.

### R9: Code blocks
- Code blocks should remain monospace.
- Normalize spacing so code does not look like broken prose paragraphs.
- Avoid page breaks that leave only a closing brace, one package name, or one trailing code line on a page by itself.
- In presentation outlines and workshop plans, keep snippets intentionally small. If syntax is not essential, replace the code fence with a prose marker list so PDF pagination cannot create orphan fences or lone carryover lines.

### R10: Default Google Docs style
- Use default Google Docs document styling unless a deliberate override is needed.
- Any override should serve readability or source fidelity, not decoration.

## Decision Matrix

### Orientation matrix

| Content type | Portrait-first action | When landscape is justified | Required follow-up |
| --- | --- | --- | --- |
| Normal prose section | Keep portrait | Never, unless the section contains a genuinely wide figure or table | None |
| Small or medium inline diagram | Fit within portrait sizing caps | Not justified if portrait remains readable | Keep centered |
| Tall flowchart | Shorten source layout first, then resize | Usually not justified; landscape does not solve height-driven overflow well | Prefer `LR` layout or split diagram |
| Wide matrix or cross-check table | Try portrait only if still readable | Justified when labels or columns become cramped or unreadable in portrait | Use dedicated landscape section and restore portrait after |
| Mixed section with one wide artifact | Keep surrounding prose portrait | Justified only for the artifact subsection | Surround with section breaks |

### Table readability matrix

| Symptom | Decision |
| --- | --- |
| one or more columns wrap into one-word or tiny-fragment vertical ladders | shorten labels/cell text or split the table before accepting the layout |
| a header wraps awkwardly, for example `Recommendation` split into multiple fragments | rename the column or widen/split the table |
| long evidence/reference cells dominate row height | abbreviate references, move detail to prose, or use footnotes/appendix references |
| landscape fixes width but leaves very tall rows from verbose cells | treat as a source/table-design issue, not an orientation issue |
| most substantive pages are wide tables | whole-document landscape can be acceptable for a report, but still audit every page and report the tradeoff |

### Diagram sizing matrix

| Condition | Decision |
| --- | --- |
| Diagram fits portrait at `<= 440pt` wide and `<= 360pt` tall | Keep portrait and center it |
| Diagram is too tall but conceptually simple | Change source layout first, for example `TD` -> `LR` |
| Diagram is still tall after layout improvement | Reduce width using aspect-ratio-aware sizing |
| Diagram becomes too small to read after width reduction | Split the diagram or simplify labels |
| Diagram is wide rather than tall and remains unreadable in portrait | Put only that section in landscape |

### Sparse-page matrix

| Situation | Decision |
| --- | --- |
| Full blank page appears | Must fix |
| Sparse page caused by an oversized diagram | Fix the diagram sizing or source layout |
| Sparse page caused by justified section orientation change | Accept only if the next section genuinely needs that orientation |
| Sparse page caused by accidental page break or bad block placement | Must fix |

## Review checklist
- Source and preview match in structure and order.
- Heading promotion is correct.
- No raw Mermaid or placeholder tokens remain.
- Inline diagrams are centered and fit the page.
- Standalone tables are centered or full-width/readable with intentional cell alignment.
- Table cell text must not inherit heading styling by accident. Flag oversized or colored body-table text, especially if cells show heading-blue text or heading-sized font.
- Landscape appears only where justified and returns to portrait afterward.
- Text-heavy appendices are portrait unless a documented table/figure exception applies.
- No real blank pages remain in the PDF export.
- Any sparse pages are explicitly justified.
- Obvious large vertical gaps are fixed or explicitly accepted.
- Full-paragraph bold in body records is absent unless explicitly intended.
- Cross-doc links point to live docs by default.
- Same-doc section references are linked where practical and are marked for live-anchor regeneration after promotion.

## Code Block Gate

- Prefer native Google Docs Code Blocks when they already exist in the polished live shell.
- Do not assume the Docs API can create native Code Blocks reliably. The API may expose existing native code blocks as normal paragraphs with private marker characters, but inserting those markers through the API is not a reliable conversion path.
- If native Code Block conversion is required, simulate first and require human editor inspection before live promotion.
- If API conversion fails or cannot be proven safe, preserve readable manual code formatting and report that manual editor conversion is needed for true native Code Block rendering.

## Human Review Gate

Automated validation is necessary but not sufficient for publication-ready Google Docs.

After the preview passes API/PDF/link/layout checks, pause and ask the user or document owner to inspect the Google Docs editor view before live promotion when any of these changed:

1. page orientation or section breaks
2. headers, footers, TOC, or page numbers
3. diagrams, images, tables, or wide content
4. appendix/reference formatting
5. large spacing/style cleanup
6. links that affect reviewer navigation

The handoff must clearly separate:

| Validation type | Who/what validates | What it proves |
| --- | --- | --- |
| API/raw structure audit | Agent/tooling | headings, links, images, TOC/footer structures exist |
| PDF/page audit | Agent/tooling | exported pages are not blank/sparse and orientation is mechanically visible |
| Google Docs editor inspection | Human owner/reviewer | the actual editing surface looks acceptable and pagination/spacing match expectations |

Do not promote a layout-sensitive preview to live until the human review gate is explicitly passed or the user explicitly accepts skipping it.

## Evaluation model

Use this split so review claims stay precise.

### Deterministic checks

These should be verified from exported artifacts or raw Docs structure, not by opinion.

- heading order and heading presence
- whether raw Mermaid fences/placeholders remain
- inline image count
- image width/height ranges
- one-page portrait fit math when requested (`height_at_440pt` gate)
- connector geometry gate when required by style policy (rendered SVG connector segments are orthogonal-only)
- section orientation counts and target ranges
- presence of empty heading paragraphs after section-break insertion
- code-block spacing markers / paragraph-style fields
- whether published links still point at `.md` paths

### Artifact-based visual checks

These rely on preview PDF / preview doc screenshots or rendered page inspection.

- whether a figure is obviously oversized on the page
- whether a sparse page is acceptable or distracting
- whether a square-ish figure reads better in portrait than landscape
- whether the immediate heading + intro + figure + interpretation stay together readably
- whether a heading is stranded alone or with only one short follow-up line
- whether tables split in a way that loses row/header context across pages

## Large-doc audit workflow

For long docs, do not rely only on spot checks.

1. export the preview to PDF
2. render contact sheets for all pages
   - Reusable helper: `python3 <skill-root>/scripts/render_pdf_contact_sheets.py --inputs /path/to/doc.pdf --out-dir /tmp/page_audit_sheets`
3. classify issues by severity:
   - blocker: blank page, unreadable diagram/table, obviously wrong orientation
   - medium: orphaned headings, split tables/code blocks, highly underfilled continuation pages
   - cosmetic: mild sparse pages that remain readable
4. fix blockers first, then medium issues, then cosmetics only if they materially affect review confidence

### LLM / reviewer judgment checks

These are content-quality judgments and should be stated as such.

- whether a section is too verbose or repetitive
- whether a comparison section should be merged/trimmed
- whether the architecture packaging feels complete for external reviewers
- whether the chosen doc order improves readability enough to justify churn
