# Live Doc Promotion And Page Audit

Use this guide when moving approved preview content into an existing live Google Doc or when checking live docs for page-format defects.

Approval boundary: preview creation, preview validation, or a vague phrase like “clone before refreshing” is not live-promotion approval. Do not copy preview content into the live/original doc until the user explicitly approves that promotion.

If the user explicitly says future edits for a named doc should update the live doc as well, treat that as a doc-specific live-promotion preference, not a global default for all Google Docs. Record the preference in memory or local wrapper config, keep using preview validation when layout-sensitive, then update the named live doc and validate it after each write.

For cross-workflow validation boundaries and PR/source-state checks, use `references/validation-workflows.md`.

## Promotion decision rule

Do not whole-doc refresh a polished live doc by default.

Prefer whole-doc refresh only when all are true:

1. the user explicitly accepts replacing the live formatting shell
2. the preview doc is the intended final formatting source
3. live title, TOC, page numbers, section breaks, comments, and manual polish are disposable or already reproducible
4. the doc has been PDF-audited after refresh

Prefer manual owner copy/paste or targeted in-place edits when any are true:

1. the user wants to preserve native Google Docs title, TOC, page numbers, comments, or manual polish
2. only a few sections changed
3. the changed sections contain complex tables, images, code-heavy blocks, or section/orientation rules that the in-place helper cannot safely reproduce
4. live comments are still active and should remain anchored near the reviewed text

If unsure, do not promote automatically. Tell the user that preview content is ready and recommend manual copy/paste or section-by-section live patching.

## Safe live patch scope

Good candidates for direct live patching:

1. one short prose section under a stable heading
2. one requirement paragraph or acceptance criterion
3. small SDK/API wording additions
4. link-only URL fixes
5. page-break/style cleanup with verified ranges
6. narrow missing-section promotion after a dry run, when headings are stable and tables/lists/code can be reconstructed with native Docs API requests

Poor candidates for direct live patching:

1. large cross-document restructures
2. many new sections with tables and code blocks
3. replacing diagram-heavy areas
4. changing generated TOCs or page-number headers/footers
5. any change that would require reconstructing Markdown formatting, links, tables, and images inside an existing section

## Preview-to-live gap check

Before promoting preview/source content into a polished live doc, separate content alignment from visual polish.

Before whole-doc live refresh, list live comments and unresolved comment count. Do not resolve comments as part of promotion unless explicitly asked. In the handoff, report unresolved comments and warn when a whole-doc refresh may have shifted or detached old comment anchors.

For risky live edits, add a simulation gate before live promotion. A preview that looks correct is not proof that the exact programmatic operation will work against the current live doc structure.

Create a fresh copy of the current live doc, run the exact operation there, export/audit it, and only then run the same operation on live when any of these are true:

1. structural table edits or row insertion
2. section orientation or section-break changes
3. header/footer/page-number changes
4. TOC-adjacent changes or heading changes that affect TOC entries
5. image/diagram placement or resizing
6. large style-range updates such as record spacing, list spacing, or bulk bold cleanup
7. same-doc anchor/link regeneration

Trash the simulation copy after successful live validation unless the user asks to retain it for audit history.

For structural table changes specifically, the simulation must prove the right table, row order, links, and headings. Never use first-substring table matching such as "first table containing Time"; match tables by exact header cells.

Use the stable preview for that live doc as the promotion candidate. If multiple preview copies exist, identify the current candidate, trash rejected/superseded experiments, and do not promote from an older copy by accident.

For layout-sensitive docs, preview approval has a required human review gate. Automated structure/PDF/link audits prepare the candidate; the user or document owner must inspect the Google Docs editor view before live promotion unless they explicitly accept skipping that gate.

Compare preview and live by stable structure, not by page count alone:

1. normalized heading tree and order
2. expected changed section ranges
3. content markers for each changed range
4. page count and orientation deltas with explanations
5. sparse-page and large-gap visual checks
6. link hygiene by link class

Link classes must be handled separately:

| Link class | Preview rule | Live-promotion rule |
| --- | --- | --- |
| Same-doc section link | May point to preview heading/bookmark during review | Regenerate or revalidate against live heading/bookmark after promotion |
| Cross-doc canonical link | Should point to the canonical live doc by default | Must point to the canonical live doc |
| External link | Must remain stable unless source changed | Must remain stable unless source changed |
| Preview/experiment link | Allowed only for explicit preview-family review | Must not remain in live docs |

Before final live handoff, audit links and confirm no preview doc IDs, trashed doc IDs, raw Markdown `.md` links, or stale heading anchors remain.

1. list source or preview headings and live headings
2. normalize heading text by removing generated anchors, inline-code backticks, Markdown links, non-breaking spaces, and private glyphs such as `\ue907`
3. ignore intentional live-shell headings such as title pages or generated TOCs when they are not source content
4. identify true missing headings and choose insertion points by stable surrounding headings, not remembered indices
5. dry-run the insertion by printing target heading, start index, end index, and inserted headings
6. after writing, re-list live headings and verify each promoted range contains only the expected inserted headings before the next existing heading

If the source-to-live heading diff is not clean after promotion, do not proceed to comment resolution or final status reporting.

## Required page audit after live edits

After any live edit that touches formatting, page breaks, section breaks, images, large sections, or trailing paragraphs, export the live doc to PDF and inspect every page.

Use two signals together:

1. text density from PDF extraction
2. visual occupancy from rendered PDF pixels

Do not use text extraction alone. Diagram/table/image pages may extract little or no text while still being visually full.

Classify pages this way:

| Signal | Likely meaning | Action |
| --- | --- | --- |
| low text + low visual occupancy | real blank/near-empty page | fix page break, section break, or trailing paragraph |
| low text + high visual occupancy | diagram/table/image page | usually OK; inspect visually before changing |
| cover/title pages sparse | expected | ignore unless the user dislikes cover layout |
| one trailing bullet/sentence before a major heading | optional polish | consider removing forced page break on the next heading |
| heading-only page before code/table | likely keep-with-next/keep-lines artifact | clear excessive keep flags or adjust page break |

## Common live-format failure modes

1. `pageBreakBefore=true` copied onto many inserted paragraphs, causing one-line pages.
2. `keepWithNext` / `keepLinesTogether` on every code-like paragraph, causing a heading or intro sentence to be stranded on the previous page.
3. final `NEXT_PAGE` section break plus required trailing paragraph, causing a blank final page.
4. broad `deleteContentRange` attempts rejected because the range touches a table boundary, section break, or segment-ending newline.
5. markdown-like replacement text showing literal `**bold**`, backticks, or `[text](url)` because heading-based section replacement is plain text unless a separate style/link pass is run.
6. code block text style applied before paragraph cleanup disappears or is visually overridden; apply paragraph block styling first and monospace/color text styling last.
7. live docs and PR branches drift because direct Docs API edits updated the live document but the local Markdown source was not committed and pushed.
8. table edits target the wrong table because the script matched a loose substring like `Time` and selected a metadata table such as `Incident Start Time`; match exact header cells and print the detected table before writing.

## Fix patterns

### Repeated one-line pages after section replacement

Clear `pageBreakBefore` across the inserted section body.

Use the heading range, not remembered indices:

1. find the section range with `docs_api.py section-range DOC_ID --heading "Heading Text"`
2. apply `updateParagraphStyle` over the section body with `pageBreakBefore=false`
3. export PDF and re-check the affected pages

### Heading-only page before a code/table block

Check the heading body for excessive keep flags.

If a whole code block/table-like block has `keepWithNext=true` and `keepLinesTogether=true`, clear those flags over the body range so the block can split naturally.

Do this only when the source content is already valid and the problem is purely pagination.

### Sparse trailing bullet before next section

If a single bullet or sentence is stranded before the next heading, inspect the next heading.

If the next heading has `pageBreakBefore=true`, decide whether that forced break is worth the sparse page. Remove the forced break only when the doc still reads better without it.

### Blank final page

Inspect the final structural elements.

Safe options, in order:

1. delete redundant blank paragraphs before the final required paragraph
2. shrink the required final paragraph to 1pt and zero spacing if it cannot be deleted
3. if a final `NEXT_PAGE` section break creates a blank page, try deleting the adjacent blank paragraph and section break together as one range

Do not assume `updateSectionStyle` can change section type. The Google Docs API rejects `sectionType` updates in some contexts.

### Inserted code blocks look like plain paragraphs

When promoting Markdown code fences into an existing live doc, rebuild them as Docs-native paragraphs instead of leaving literal fences.

Safe order:

1. insert the code text without Markdown fences
2. apply paragraph style for shading, spacing, indentation, and keep behavior
3. apply text style last for monospace font, font size, and foreground color
4. read back a representative paragraph and export the PDF to verify the code panel is visible

If the text style is missing after paragraph cleanup, rerun only the text-style pass over the verified code paragraph ranges.

### Section-break cleanup is rejected

Do not keep retrying guessed deletion ranges around section breaks. If deleting a section break is rejected, prefer a neutralizing style change such as restoring portrait/landscape on the short affected range, then re-export and audit.

`updateSectionStyle` can change orientation, margins, and related style fields, but it cannot reliably change a section break into a different `sectionType`.

## What not to do

1. Do not run a whole-doc markdown refresh on a polished live doc just to fix a small section.
2. Do not repeatedly delete guessed ranges near tables or section breaks.
3. Do not call a page empty just because PDF text extraction sees no text.
4. Do not claim live docs are clean until the exported PDF has been re-audited after the final write.
5. Do not resolve reviewer comments before the live doc, preview doc, or source doc that the reviewer sees actually contains the fix.

## Minimal live audit script shape

The exact implementation can vary, but the audit should:

1. export each live doc with Drive `files().export(..., mimeType="application/pdf")`
2. read text per page with `pypdf`
3. render each page with `fitz` / PyMuPDF, or fall back to `pdftoppm` plus Pillow when `fitz` is unavailable in the active environment
4. compute a non-white pixel ratio with `PIL`
5. print pages with low text, low visual occupancy, or unexpected orientation
6. manually classify flagged pages before applying fixes

Keep this as a verification aid, not an automatic repair tool. Repairs must still be anchored to Docs API structure and stable headings/ranges.
