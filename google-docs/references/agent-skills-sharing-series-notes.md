# Agent Skills Sharing Series Doc Notes

Use this as an example of applying the presentation-outline refresh workflow to an Agent Skills brownbag/workshop planning doc.

## Stable doc/form context

- Live doc: `Agent Skills Sharing Series`.
- Current session titles:
  - `Agent Skills for Daily Work`
  - `Skill Engineering Workshop`
- Current form title: `Agent Skills quick check (5 minutes)`.
- When the user explicitly asks to update live, keep the reusable preview and live doc in sync; otherwise follow the normal preview-first gate.

## Content structure that worked

1. Keep the document title short: `Agent Skills Sharing Series`.
2. Use two sessions:
   - Session 1: cross-functional, practical, role-agnostic.
   - Session 2: technical workshop for builders, AIP/GLConnector/GDP Labs stack oriented.
3. Separate reviewer scan flow from dense notes:
   - `Top-Level Slide Outline — Session 1`
   - `Detailed Presenter Notes — Session 1`
   - `Top-Level Slide Outline — Session 2`
   - `Detailed Presenter Notes — Session 2`
4. Put `Form / Survey Recommendation` on its own page and include the send-ready default email draft there.
5. Use `Question N — ...` labels for form questions; never let form questions become `Slide N — ...` labels.

## Presentation readability patterns

- Add per-slide `Visual / illustration direction`, `Suggested visual copy`, and `Alternative speaker line`.
- Use numbered lists for key links, session package details, success criteria, post-session questions, and references.
- Keep nested form answer options as bullets to avoid confusing survey metadata with ordered recommendations.
- Add `Highlight:` callouts for executive direction, session snapshots, and form/survey purpose.
- Convert dense comparison tables into bullet cards when PDF output wraps too much.
- Keep code snippets minimal; turn non-essential code blocks into prose markers.

## Pagination lessons

- Good parent-section page breaks: major sessions, top-level slide outlines, detailed presenter notes, form/survey recommendation, success criteria, references.
- Risky child-item page breaks: individual survey questions, single slide notes, and isolated snippets. These often create near-blank orphan pages.
- Contact-sheet audits can over-flag normal presenter-note continuation. Treat as blocker only when the page is blank/near-blank, a heading has no body, a code block/fence is split, numbering breaks, or a single detached bullet is isolated without enough surrounding content.
- If a manual page break creates a fully blank page after a short section, inspect the raw Docs structure around the preceding heading and delete the page-break element directly rather than adding more breaks elsewhere.
- When a page-break fix strands a later slide heading at the bottom of a page, insert the break before the stranded heading and rerender all contact sheets. Do not assume an early-page fix leaves later pages unchanged.

## Survey appendix and formatting recovery pattern

When survey results materially support this Agent Skills session split:

1. Keep the main `Survey Signal and Content Implications` section short and scannable near the top.
2. Put detailed numerical counts and free-text themes in `Appendix A — Survey Results Supporting Evidence`.
3. Link Appendix A from the start of the doc using a same-doc heading link; regenerate or revalidate the anchor if promoting preview changes to live.
4. If `replace-section` inserts escaped Markdown such as `\*\*Label:\*\*`, replace with plain label text (`Label:`) and apply Docs text/paragraph styles separately.
5. For this outline, use literal `•` bullets plus `--no-simple-lists` for compact survey summary blocks when Google Docs auto-list conversion creates repeated `1.` numbering.
6. If an appended appendix leaves duplicate/raw-markdown content behind, replace the appendix body programmatically from the Appendix A heading to the document end, keeping the heading itself and avoiding delete ranges that include the final segment newline.
7. Re-export Markdown after cleanup and check: no escaped raw star artifacts (`\\*`), no repeated broken numbering, exactly one Markdown Appendix A heading, and exactly one A1 heading. Do not treat normal exported Markdown bold markers (`**Label:**`) or repeated linked mentions of Appendix A as defects unless they are visible as raw Markdown in the PDF/editor.
8. Export PDF and render contact sheets for all pages before handoff. Audit specifically for blank pages, broken numbering, raw Markdown, duplicate appendix, orphan headings, and severe awkward page breaks.
9. If a user flags a specific Google Docs editor screenshot as “weird,” do not rely on prior PDF/contact-sheet pass alone. Inspect the actual paragraphs in that section via Docs API, looking for blank paragraphs, heading styles accidentally applied to labels, and normalized paragraph spacing.
10. `docs_api.py replace-section` can normalize inserted section-body paragraphs to generous spacing (for example 10pt above / 4pt below / 115% line spacing). For compact evidence blocks, follow replacement with direct Docs API paragraph updates: body spacing around 0pt above / 2pt below / 105% line spacing; literal `•` paragraphs get hanging indents (`indentStart` about 18pt, `indentFirstLine` about -18pt); inline labels such as `At-a-glance signals:` should be normal text with modest space above and `keepWithNext`, not `HEADING_3`.
11. If compaction shifts pagination and creates sparse later pages, inspect page-break-only paragraphs and delete just the page-break element range, not the trailing segment newline. Re-export PDF and rerender all sheets because early spacing fixes can change late-page layout.
