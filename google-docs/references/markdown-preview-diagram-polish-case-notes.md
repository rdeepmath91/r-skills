# Markdown Preview Diagram Polish Case Notes

Use this reference when refreshing Markdown-backed Google Docs previews where live docs have polished GDP-style formatting but Drive cannot copy the live file, or where dense Mermaid diagrams become unreadable after import.

## Dense ERD pattern: split exact Mermaid, not custom summary first

When a source Markdown doc has a dense `erDiagram` that becomes unreadable at portrait width:

1. Preserve the source Mermaid semantics.
2. Split the one dense ERD into multiple smaller Mermaid `erDiagram` panels by concern.
3. Render each panel to PNG and insert all panels under the original ERD section.
4. Add a short bridge paragraph explaining that the ERD is split for readability and that the panels collectively cover the original relationship set.
5. Use custom HTML/SVG summaries only if the user explicitly wants a conceptual overview rather than ERD fidelity.

Good split dimensions for schema docs:

- Identity / Auth / Backend Scope
- Runnable Registry / Versioning
- Scheduling
- Run Execution / Events

If the split needs to remain self-contained, add FK-derived scope edges that are implied by table fields but omitted from the original single diagram. State this in the bridge text so readers understand why the panels may contain more edges than the original source rendering.

Example bridge text:

```text
To keep the full relationship view readable, the ERD is split into four Mermaid-rendered panels. Together they cover the original Mermaid relationship set, with FK-derived tenant/account scope edges called out in the panel divisions.
```

## Preview refresh pattern when live copy is unavailable

If Docs API can read live docs but Drive API cannot copy/export live docs because of `drive.file` visibility:

1. Regenerate the preview from clean local Markdown, not from truncated tool output.
2. Replace Mermaid blocks with unique placeholders before DOCX/Drive import.
3. Render Mermaid locally to PNG.
4. Insert rendered images by replacing placeholders in reverse order.
5. Read live named styles and representative code-span text styles via Docs API.
6. Before polishing, compare heading hierarchy from the intended copy boundary (`Executive Summary` through bottom) against the live doc. If every preview heading is shifted down one level after import, promote headings in place with `updateParagraphStyle.namedStyleType` and re-read until common-heading mismatches are zero.
7. Apply range-level overlays to the regenerated preview:
   - body/heading font, size, color, line spacing, paragraph spacing from live named styles
   - Roboto Mono / green code-like text style restored after body overlay
   - image paragraphs centered
8. Export PDF and render contact sheets.
9. Report explicitly that this is a preview/style assimilation, not a live-derived copy and not live promotion.

This is safer than promoting a fresh DOCX/Markdown import directly to live, but it is still not identical to cloning the live shell. Keep final promotion behind a human review gate.

## Validation checklist for this pattern

For each regenerated preview, capture:

- preview doc URL
- source Markdown path
- expected Mermaid image count vs actual inline object count
- raw marker counts: no ` ```mermaid`, no `@@MERMAID_`, no `OUTPUT TRUNCATED`
- table count and heading count
- live-vs-preview common heading `namedStyleType` mismatches from the intended copy boundary; require zero before saying the preview can be copied seamlessly into live
- exported PDF path and page count
- contact sheet directory
- visual QA notes for early pages, image-heavy pages, and final pages

Treat low-text pages that contain full-page diagrams differently from true blank pages. Use both text extraction and rendered contact sheets; PDF text extraction often reports image-only pages as empty even when the rendered page is valid.

## Common pitfalls

- Do not replace a dense ERD with a simplified custom summary while the section is still titled `Minimal ERD`; users may read that as broken or incomplete.
- Do not assume one Mermaid image is better than multiple. Exactness plus readability often requires splitting the diagram.
- Do not rely on Docs API structure alone for layout quality. Export PDF and inspect contact sheets.
- Do not call regenerated previews “live docs.” The live document remains untouched until explicitly promoted.
- When a user says there is one blank page but otherwise approves, distinguish whether it is a real rendered blank page or an accepted visual tradeoff before spending more time optimizing pagination.