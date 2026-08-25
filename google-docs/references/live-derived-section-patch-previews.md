# Live-derived section patch previews

Use this when a polished live Google Doc must receive updated preview/source content while preserving the live document's shell, page setup, orientation, TOC, version table, margins, page numbering, heading styles, list styling, diagram behavior, and manual polish.

## Lesson

A live-derived preview is safer than importing a fresh preview and trying to overlay styles. But the safe unit is a bounded section patch, not a whole-document structural clone.

The successful pattern from the GL Runner doc package was:

1. Copy the live doc into an isolated test/preview doc.
2. Choose a small section boundary, such as `Executive Summary` through before `Quick Read`.
3. In the live-derived copy, preserve the existing paragraph/list/heading containers.
4. Replace only the text inside matching paragraph ranges from the updated preview/source.
5. Export PDF and contact-sheet QA before scaling.

This preserved:
- title/version shell
- TOC shell
- page numbering
- margins and section/page setup
- heading/list styling
- live typography

## Anti-patterns found

### Do not broad style-overlay imported previews

Applying live text-run styles onto a freshly imported preview can over-apply special formatting:
- body paragraphs may become green monospace if the sampled live run is code-like
- numbered list items may inherit hyperlink blue/underline
- visible styling may look live-ish while underlying structure remains import-derived

If a doc has manual polish, prefer live-derived copies and content patching.

### Do not wholesale-clone the body via Docs API unless you can preserve structure exactly

A full body reconstruction from `Executive Summary` downward caused hard-to-debug layout defects:
- list numbering continued across the whole document (`1`, `5`, `600+`) instead of resetting naturally
- tables became compressed or overlapped with headings
- diagrams sometimes became thin/empty-looking boxes after copied image insertion
- TOC page numbers became stale or nonsensical until manually refreshed
- database schema appendix tables overlapped later sections

This is not a durable promotion path without a much richer structural copier.

## Recommended scaling approach

1. Start with a small section patch in a live-derived copy.
2. Validate visually.
3. Patch section-by-section, using real live paragraph containers where possible.
4. For sections with tables or images, use a stricter path:
   - table sections: rebuild or patch one table at a time and visually inspect that page
   - image/diagram sections: insert images at final size and validate the rendered page
   - list-heavy sections: verify numbering resets and no global continuous numbering appears
5. Refresh/check TOC manually in the editor before treating the preview as final.
6. Only promote to live after PDF/contact-sheet QA passes.

## Validation checklist

- No raw Markdown, Mermaid fences, placeholders, or truncation sentinels.
- No body-wide continuous numbering.
- No table-heading overlap.
- No compressed or unreadable tables.
- Diagrams render as real diagrams, not thin empty boxes.
- TOC page numbers look plausible after refresh.
- No visually blank pages except intentional live title/shell pages.
- Contact sheets inspected at front, diagram-heavy pages, table-heavy pages, and tail.
