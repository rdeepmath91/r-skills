# GDP Labs Publication Baseline

Use this reference when creating, refreshing, or validating polished GDP Labs Google Docs. This is an organization-level publication baseline, not a project-specific doc-family configuration.

## Applicability

Apply this baseline to polished, live, reviewable, or executive-facing GDP Labs documents unless the user explicitly asks for a lightweight draft.

Do not hardcode project-specific doc IDs, heading names, tab IDs, page-break locations, landscape ranges, or reviewer-specific links here. Keep those in local wrapper configs or repository docs.

This file is intentionally GDP Labs-specific. General Google Docs API behavior, Markdown import behavior, native Code Block limitations, and generic live-edit safety rules belong in the other references.

## DOC Rules

Use `DOC1-DOC8` when reporting findings so Google Docs publication issues do not get mixed with diagram-source/style issues.

| Rule | Name | Requirement |
| --- | --- | --- |
| `DOC1` | Document identity | Use meaningful document title and tab names. Avoid generic tab names like `Tab 1` in polished docs. |
| `DOC2` | Title shell | Include a title/front-matter block with document name, status, owner, version or date when available. |
| `DOC3` | Native TOC | Include a native Google Docs table of contents for non-trivial docs, especially docs with many headings or more than roughly 5 pages. |
| `DOC4` | Page numbers | Include page numbers in the header or footer for paged documents. Default GDP Labs footer format is `PAGE_NUMBER of PAGE_COUNT` without a document-name prefix unless the user asks otherwise. |
| `DOC5` | Live-shell preservation | Preserve stable live doc IDs, tab IDs, comments, TOC, page numbers, section breaks, and manual polish during in-place updates. |
| `DOC6` | Figure placement | Insert figures as normal body content under the intended heading, not inside heading paragraphs. Keep headings text-only so TOC and anchors stay clean. |
| `DOC7` | Figure orientation and sizing | Choose portrait vs landscape from inserted-view readability. Use the smallest useful chunk: heading, short explanation, figure/table, and immediate interpretation. Split the figure or ask for a new asset if sizing/orientation cannot make it readable. |
| `DOC8` | PDF/page validation | Validate exported PDF/contact-sheet pages for readability, blank pages, severe orphaning, and figure/table breakage before handoff. |

## Figure Fit Notes

Portrait is the default, but fitting on a portrait page is not sufficient for figures.

Use landscape for genuinely width-heavy tables or figures when the smallest text is not readable at normal Docs/PDF fit view. If landscape still leaves text too small, split the figure by question rather than shrinking it further.

Assume the diagram asset already follows the approved diagram source/style standard before it reaches the Google Docs publishing step. This baseline only evaluates Google Docs placement, orientation, sizing, and page/export readability.

## Validation Checklist

Before handoff, report these boundaries separately:

1. Docs structure: `DOC1-DOC6` pass or findings are listed
2. Figure placement validation: `DOC6-DOC7` pass or findings are listed
3. PDF/visual artifact: `DOC8` passes or findings are listed
4. Semantic/content review: terminology and content are correct for the target product
5. Source/PR validation: source files are committed and pushed when the task includes GitHub/source updates

Markdown import alone is not enough for a polished GDP Labs document. After Drive or Docs import, explicitly validate the shell and say whether the doc is a lightweight draft or publication-ready. A document is not publication-ready when it only has imported headings/tables but lacks required native TOC, page numbers, title/front-matter shell, or page-layout review.

For table-heavy reports, exported PDF/contact sheets are required before calling layout done. If many tables remain cramped in portrait, either apply justified landscape sections, simplify/split the tables at source, or report a `DOC7` finding. A clean heading check does not prove table readability.

For table readability, inspect column behavior, not just page orientation. A table still fails `DOC7` when any column becomes a vertical ladder of one-word or tiny-fragment wraps, when a header such as "Recommendation" splits awkwardly across lines, or when long references force every row to become overly tall. Fix in this order: shorten column labels and cell references, move verbose evidence into prose or footnotes, split the table into narrower thematic tables, merge low-value columns, then use landscape only when the simplified table still needs width. Landscape is a remedy, not a substitute for table design.

Useful commands:

```bash
python <skill-root>/scripts/docs_api.py headings <doc_id>
python <skill-root>/scripts/docs_api.py get <doc_id> --md
python <skill-root>/scripts/render_pdf_contact_sheets.py --inputs /path/to/doc.pdf --out-dir /tmp/page_audit_sheets
```

Do not add private doc links, project-specific IDs, or cross-skill dependencies to this baseline.
