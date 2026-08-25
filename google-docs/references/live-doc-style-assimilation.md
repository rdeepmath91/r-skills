# Live Doc Style Assimilation

Use this when source/PR Markdown must update an existing polished Google Doc whose formatting shell matters.

## Core rule

Prefer live-derived copies over fresh imports when the live doc has manual polish, native title/version/TOC shell, comments, or established typography.

Best workflow:
1. Read the live doc with Docs API and compare style/content against the preview/source.
2. If possible, copy the live doc first and patch the copy in place.
3. Preserve the live shell: title page, subtitle/version, version-control table, TOC, margins, named styles, comments, and page setup.
4. Replace only the stale body ranges, usually from the first source heading such as `Executive Summary` through the end or through a stable next shell boundary.
5. Render Mermaid/diagrams as images before insertion; do not leave raw fences.
6. Validate heading tree, marker terms, tables/images, links, PDF layout, and contact sheets before live promotion.

## Drive vs Docs API permission nuance

Docs API `documents.get` can succeed while Drive API `files.get`, `files.copy`, or export fails for the same doc.

Common cause: the token has `https://www.googleapis.com/auth/documents` plus `https://www.googleapis.com/auth/drive.file`. The app can read document structure through Docs API, but Drive API only sees files created/opened/shared with the app. For original live docs outside that app-visible set, Drive returns `404 File not found` for get/copy/export.

Do not report this as a general auth failure. State it precisely:
- Docs API read: available
- Drive copy/export: unavailable because the file is not visible to the app under Drive scope/file authorization

Options:
- user manually makes live-derived copies and shares the URLs
- re-auth with broader Drive scope such as full Drive access when policy allows
- explicitly approve direct live patching after a preview/simulation gate

## Style comparison and assimilation

Even without Drive copy access, Docs API can compare formatting:
- named styles: `NORMAL_TEXT`, `TITLE`, `SUBTITLE`, `HEADING_1..4`
- font family and size
- line spacing and paragraph spacing
- heading colors
- explicit text runs such as `Roboto Mono` code/identifier spans
- paragraph style distribution
- table/image counts and link URLs

Fresh DOCX imports often drift to Cambria/Calibri/Consolas. Live GDP-style docs may use Proxima Nova body, GDP cyan headings, Trebuchet MS H4, and Roboto Mono green identifiers. If a preview was created through DOCX fallback, run a style audit before promotion.

The Google Docs API supports range-level `updateTextStyle`, `updateParagraphStyle`, `updateDocumentStyle`, `updateTableCellStyle`, and `updateSectionStyle`, but it does not support rewriting named style definitions directly. A style overlay can make visible text match the live doc, but the doc's underlying named style defaults may still be from import.

### Prefer live-derived copies over preview style overlays

When the user wants preview content to be copy-compatible with a polished live doc, do not start by force-applying live text styles onto an imported preview. Style overlays can overfit a source text run and accidentally turn whole body paragraphs into monospace/green identifier text or convert numbered list entries into blue link-styled text. This is especially likely when copying first-run styles from paragraphs that contain inline code or links.

Safer default:
1. Create an isolated copy of the live doc.
2. Patch only the target body text/ranges from the preview/source into the live-derived copy, preserving existing live paragraph structures, named styles, lists, TOC shell, page numbering, version table, margins, and diagram/layout behavior.
3. Start with one small section, such as `Executive Summary` through the next heading, not the full doc family.
4. Export to PDF and render a contact sheet before scaling the method to the full preview or live promotion.

Use style overlays only for narrow repairs after a live-derived patch is impossible or after confirming that code/link/list ranges will be restored explicitly.

## Incremental format reset gate

When the user asks to reset or mimic live-doc formatting, do not immediately apply a whole-document style pass. First run a partial, reversible assimilation test:

1. Create an isolated test copy of the preview doc, or if Drive copy is unavailable, stop and ask for a re-auth/manual copy rather than patching the working preview directly.
2. Pick one small representative range, usually `Executive Summary` through before `Quick Read`.
3. Read the matching range from the live doc and apply only that live range's paragraph/text styles to the test copy, preserving preview text content.
4. Export the test copy to PDF, render a contact sheet, and compare visually against the live doc before expanding the method.
5. Only after the partial test is accepted should the same live-style approach be applied to larger sections or full preview docs.

This avoids large irreversible style churn and catches copied-format incompatibilities early. It is especially important when a preview has already been regenerated from Markdown and may contain newer content than the live doc.

## Large Markdown source safety

For large Markdown docs, fetch source directly to disk. Do not write capped terminal/tool stdout into source files, because truncation sentinels such as `[OUTPUT TRUNCATED ...]` can become document content.

Good pattern for GitHub files:

```bash
gh api repos/OWNER/REPO/contents/path/to/file.md?ref=BRANCH --jq .content | base64 -d > /tmp/source.md
```

Then scan for sentinel text before preview generation.

## Database Schema manual-promotion pattern

When the preview already matches live named styles and only the body content changed, manual promotion can be acceptable:
- keep the live title/version/TOC shell
- copy from `Executive Summary` through the bottom from the preview into the live doc
- update the version-control table separately
- manually refresh the TOC after headings change
- re-export/PDF audit after the copy

For the GL Runner Database Schema case, the preview matched live named styles while the body content changed materially; this was a good candidate for copying from `Executive Summary` downward rather than whole-doc replacement.

## ERD and diagram sizing

A Mermaid ERD inserted at about 440 pt width is already near the safe portrait content width. If it still looks too small, the issue is diagram density, not insertion width.

Options, from least to most invasive:
1. Make only the ERD section landscape via selected-content page setup, then widen the image manually.
2. Split a dense ERD into 2-3 smaller diagrams by concern, such as core identity, execution/history, and supporting registries.
3. Redraw as custom HTML/SVG when Mermaid ERD routing/table sizing makes labels unreadable.

Do not assume dragging wider in portrait will fix a dense ERD; use selective landscape or split diagrams.