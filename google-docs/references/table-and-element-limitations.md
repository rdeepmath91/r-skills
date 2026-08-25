# Table and Element Limitations

## Tables — limitations and safe operations

- **Cannot delete a table** — `deleteContentRange` on the table's start/end indices returns "Invalid deletion range."
- **Can insert rows, but only with exact table/cell targeting** — `insertTableRow` works when the table is identified by stable structure and the row index is recomputed after each write.
- **Do not assume loose table matching is safe** — a table whose first cell contains `Incident Start Time` is not the same as a timeline table with header `Time (UTC+7)`. Match exact header cells.
- **Row/column deletion remains high risk** — deletion and complex restructuring can fail or target the wrong range when indices shift around table boundaries. Simulate on a fresh copy first.
- **Cannot delete content inside table cells** — `deleteContentRange` with cell-relative indices often fails with "Invalid deletion range." The API's cell index tracking is unreliable for in-cell mutations.
- **Cannot insert page numbers** — no API request for dynamic page number fields. Must be done via UI: Insert > Page numbers.
- **Cannot insert smart chips** — Person chips, Date chips, and other `@`-triggered smart chips are UI-only. The API has no equivalent request type.

## Practical workarounds

### If you need to change table structure (add/remove columns)
- Delete the entire table content by clearing every cell, then re-insert. This is fragile.
- **Preferred**: recreate the doc from source Markdown with the correct table structure. Faster and more reliable than fighting the API.

### If you need TOC or page numbers
- Detect native TOCs through `tableOfContents` structural elements in the raw Docs response.
- Detect page-number shells through header/footer segments that contain `autoText` values such as `PAGE_NUMBER` and `PAGE_COUNT`.
- Prefer preserving an existing polished shell with native TOC and page numbers instead of recreating it.
- If creating or deleting a TOC through the API, test the exact request in preview first and validate the raw structure afterward; TOC refresh/page-number recalculation is not a reliable API-controlled finalization step.
- If page numbers are missing, report a manual editor action or use an existing polished shell as the live target.

### If you need smart chips
- Insert plain text placeholders (e.g. "Author: [Name]", "Last updated: [Date]") via API.
- Tell the user to replace the text with `@` smart chips manually. Takes 15 seconds.

## What the API CAN do with tables
- `insertTable(rows, cols)` — create new tables with optional cell data
- `insertTableRow` — add rows to an existing table when using strict table header matching and recomputed row indexes
- `replaceAllText` — works for text replacement within cells (exact match only)
- `updateParagraphStyle` / `updateTextStyle` — works on cell content for formatting
- `insertText` — works to append text to cells

## Safe row insertion workflow

Use `scripts/docs_table_tools.py` for inspection and simple append-after-anchor row insertion instead of hand-rolled one-off scripts.

1. Inspect all tables and confirm the exact target header:
   - `python <skill-root>/scripts/docs_table_tools.py inspect DOC_ID --max-rows 5`
2. Create a fresh simulation copy of the live doc.
3. Insert rows into the simulation with an exact header and anchor row.
4. Export the simulation and verify row order and formatting.
5. Apply to live only after the simulation succeeds.

Never select a table with vague logic like "first table containing Time". Prefer exact header arrays such as `["Time (UTC+7)", "Event"]`.

## What the API CAN detect in document shells

- Native TOC elements as `tableOfContents` structural elements in body content.
- Headers and footers as `headers` / `footers` maps, with segment IDs for their content.
- Dynamic page-number fields as `autoText` entries such as `PAGE_NUMBER` and `PAGE_COUNT` inside header/footer content.
- Section orientation through `sectionBreak.sectionStyle.flipPageOrientation` and PDF page-size audits.

## Alignment rules

- Center standalone tables where the import path or editor supports table-block positioning.
- The Docs API is better at formatting content inside table cells than positioning the table block itself; do not assume table-block centering can be repaired reliably after import.
- If table-block centering is not available through the API, use a readable full-width table and intentionally align cell content.
- Avoid accidental narrow, left-aligned tables. Treat them as layout defects and fix by source/table design, import settings, or manual editor adjustment if API support is insufficient.
- Diagrams and figures are not subject to this table limitation: center-align the containing paragraph for standalone inline images by default.

## Decision heuristic

When the user asks for table structure changes:
1. If it is row insertion into a known table → simulate using exact header matching, then promote.
2. If the doc has been through multiple edits already and needs broad table restructuring → recreate from source Markdown.
3. If it is a fresh doc → get the table right before publishing.
4. If it is a minor text-only change inside cells → use `replaceAllText`.
