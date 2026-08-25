# Editing In Place

Use this workflow when you need to edit an existing Google Doc without republishing the entire document.

## Live-doc safety rule

When the target is an existing live doc, do not edit it first by default.

1. Reuse the stable preview doc for this live doc when one exists.
2. If no stable preview exists, copy the current live doc to create one and give it a durable name such as `<Doc Name> Preview`, not a timestamped experiment name.
3. Apply the intended section/link/image/style patch to the preview.
4. Export or inspect the preview until content, pagination, and formatting are acceptable.
5. Promote the same targeted patch back to the original live doc.
6. Re-export or inspect the live doc and report any manual TOC/page-number refresh needed.
7. Trash obsolete preview experiments after a newer preview replaces them, keeping only the stable preview plus the live doc unless the user asks for archival copies.

Skip the preview-copy loop only when the user explicitly asks to skip it or when the edit is a trivial, low-risk text/link correction with no layout impact.

## Structural table edit safety rule

When promoting edits that add, remove, or reorder rows in an existing Google Docs table, do not combine untested table mutations with prose section replacements in the same first live run.

1. Create a fresh simulation copy from the current live doc, not from an older preview.
2. Identify the target table by exact header cells, for example `Time (UTC+7)` + `Event`; do not select by loose substring because metadata tables often contain similar words such as `Incident Start Time`.
3. Run the table mutation on the simulation copy only.
4. Export the simulation and verify row order, links, code styling, and heading tree.
5. Only then apply the same operation to live.
6. If the live operation fails, revert only the operations that already succeeded and stop for user review.

## When this is the right tool

Prefer in-place editing when all or most of these are true:

1. the user wants to preserve native Google Docs shell formatting such as title, TOC, page numbers, or manual polish
2. only one section, one link family, or one image needs changing
3. the doc already exists and is structurally healthy
4. the edit is smaller than a full Markdown refresh

Do **not** default to a full markdown refresh when the real task is a small targeted edit.

## Best candidates for in-place editing

- wording fixes in one section
- replacing the body under one stable heading
- link URL rewrites
- swapping one image/diagram under a known heading
- adding one short paragraph or note

## Poor candidates for in-place editing

- full document rewrites
- docs with malformed import structure that should be recreated cleanly
- heavy table surgery across many sections
- large cross-doc restructuring where headings, images, and orientation all shift at once
- promoting many preview-only sections into a polished live doc when the live doc's native formatting shell must be preserved

## Deterministic section workflow

1. If editing a live doc, reuse its stable preview or create one if none exists, then perform the workflow below against that preview first.
2. Check auth first:
   - `python3 <skill-root>/scripts/setup.py --check`
3. List headings to confirm the live or preview structure:
   - `python3 <skill-root>/scripts/docs_api.py headings DOC_ID`
4. Read the target section range:
   - `python3 <skill-root>/scripts/docs_api.py section-range DOC_ID --heading "Heading Text"`
5. Replace only that section body:
   - `python3 <skill-root>/scripts/docs_api.py replace-section DOC_ID --heading "Heading Text" --file /path/to/section.txt`
6. Re-read the doc or export a narrow verification view.
7. If preview validation passes, repeat the same targeted operation on the original live doc and validate live output.

The section replace path is deterministic because it:

- anchors on real Google Docs headings, not remembered indices
- replaces only the body under the heading until the next same-or-higher heading
- can preserve simple numbered/bulleted lists from plain text markers

## What the section edit path currently supports well

- paragraphs
- blank-line-separated paragraphs
- simple numbered lists like `1. foo`
- simple bullet lists like `- foo`

## Current limitations

- not a full Markdown renderer for one section
- Markdown emphasis markers such as `**Label:**` may be inserted as literal text during targeted section replacement; use plain `Label:` text unless you plan a separate text-style pass
- for email-style memos, do not feed markdown table syntax or visible `**` markers into `replace-section`; use plain prose with selective emphasis instead
- does not preserve complex tables/chips/embedded objects inside a replaced section
- links in replacement text are plain text unless you run a separate link-style pass
- replacing a parent heading section will also replace its nested subsections
- inserted plain text can inherit unexpected paragraph styling from nearby content; re-read the section structure and clear unwanted styles such as `pageBreakBefore` before calling the edit done
- paragraph style passes can disturb code-like text appearance; for inserted code blocks, apply block paragraph styling first and monospace/color text styling last
- structural table mutations are brittle when table selection is ambiguous; use `scripts/docs_table_tools.py inspect` to print table headers and row anchors before writing
- when a heading is immediately followed by a table, `insertText` at `heading.endIndex` can fail because that index is outside an existing paragraph; insert `"\n<new paragraph text>"` at `heading.endIndex - 1`, then re-fetch and style the new paragraph before validating the table

## Link-only edits

If only links changed, do **not** republish the doc.

Instead:

1. read the doc structure
2. update `textStyle.link.url` for matching spans
3. verify the new URLs in a narrow read/export

## Version-control and first-page metadata edits

When a polished live doc has a front-page subtitle plus a `Version Control` table, treat updates as targeted live-shell edits, not Markdown source edits.

1. Read the first structural elements and identify the subtitle paragraph and version-control table by exact header cells such as `Version`, `Date`, `Author(s)`, `Reviewer(s)`, `Notes`.
2. Update the subtitle with the new version/date, preserving the paragraph style.
3. Add the new version row into an existing empty row when available; do not recreate the whole table unless explicitly necessary.
4. Keep notes technical and stakeholder-relevant. Do not mention routine Google Docs layout/polish work in the version note unless that is the actual deliverable.
5. Re-read the first page after the patch and verify typo cleanup in existing rows, for example misspelled `Address` or stray reviewer initials.
6. Report these as live-doc metadata changes separately from source/PR changes.

## Image-only edits

If only one diagram changed:

1. render the asset locally
2. find the heading or anchor where that image belongs
3. replace or reinsert only that image
4. re-check fit/orientation locally in preview docs before touching live docs

## Diagram-heavy Google Docs edits

When improving a Google Doc section that contains an executive comparison diagram, keep the diagram visually different from a table. Prefer a few large boxes with short role labels and small tag chips; move the actual explanation into the prose above the diagram. Put the most important comparison sentences before the image and apply emphasis with targeted bold/highlight spans, then verify by PDF export that the explanation and diagram do not split awkwardly across pages.

### Google Docs diagram formatting pass

When asked to improve a Google Doc section "as per our Google Docs diagram" or similar, treat the task as both a document-formatting pass and a diagram-asset pass:

1. Use the GDP Labs diagram workflow for the image source: white background, title-only header unless a subtitle is essential, compact two-box/side-by-side layouts for comparisons, no decorative flows/arrows when the user asked for boxes and differences.
2. Render an editable HTML/SVG source to PNG, then run the Google Docs fit check before insertion. Prefer a diagram size that stays readable at Docs width; fix effective text-size, overflow, margin, and clipping warnings before upload.
3. Insert the diagram as an inline image at the real heading/placeholder anchor, centered, with a Docs-friendly width around 500 pt for portrait pages unless the section is landscape.
4. Apply the surrounding Docs formatting in the same pass: clear placeholder text, use heading hierarchy, readable paragraph spacing, and bold only the core answer sentence when useful.
5. Export the full doc to PDF after insertion, render the affected pages, and visually verify no clipping, awkward split, or unreadable scaling before reporting success.

## Text-only professionalization without layout changes

For broad wording cleanup in a formatted live Doc, simulate the exact patch on a live-derived preview and use text-only operations. Preserve paragraph newlines, table cells, heading objects, list IDs, links, and inline objects.

Two API behaviors require explicit checks:

- `replaceAllText` preserves paragraph/list structure but can flatten mixed inline styling inside a matched paragraph, including monospace spans. Avoid whole-paragraph `replaceAllText` when the paragraph contains mixed styles or links unless those spans are reapplied and verified.
- Deleting and reinserting all text before a paragraph newline preserves its paragraph style and list ID, but Google may normalize the output-only `bullet.textStyle` metadata. Treat this as acceptable only when paragraph styles/list IDs are unchanged and the preview/live PDF confirms the bullet rendering is visually unchanged.

For style-preserving rewrites, reapply surviving linked/code/emphasized tokens after insertion, compare table shapes and link URL inventories, and visually inspect the affected pages before live promotion.

## Decision rule

Use refresh mode for preview docs and large structural changes.

Use edit mode when preserving live formatting matters more than keeping the live doc mechanically regenerated from Markdown on every pass.

## Style-preserving draft tabs and appendix inserts

When creating or revising a draft tab inside an existing polished Google Doc, match the original document's native typography unless the user explicitly asks for a new visual style. Avoid turning a focused appendix draft into a title-page-like layout.

- Inspect nearby original sections for named style levels before styling the new tab. If the original appendix heading is `HEADING_2`, use `HEADING_2` for the draft heading rather than `TITLE`.
- Prefer original-doc-like black/default text color for body copy. Do not impose branded blue body text or highlight backgrounds unless the source doc already uses them for the same semantic purpose.
- Keep paragraph spacing compact for appendix-style explanatory prose: line spacing near 100%, small `spaceBelow` values, and no blank-line-only paragraph padding unless needed for readability.
- Use bold for emphasis in the few core comparison sentences; avoid large colored callouts that consume vertical space.
- After changing spacing/style, export to PDF and visually check that the section no longer has excessive whitespace and that the content fits naturally with the surrounding document.

For preview-to-live promotion, do not automatically replace a polished live doc from Markdown. If the change set is large, ask the user to approve full refresh risk or recommend manual copy/paste from preview; use in-place edits only for small, stable sections. Prefer promoting the same targeted patch operation over copying the whole preview document back onto live.

Reuse the same stable preview across successive iterations for the same live doc. Create a separate experiment copy only for risky alternatives that must be compared side by side, and trash that experiment when it is rejected or superseded.

After direct live edits, report live-doc state and source/PR state separately. Do not imply GitHub or an open PR was updated unless the local source changes were committed and pushed.
