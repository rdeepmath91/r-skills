# Markdown Pipeline

## Core decision
- Use Drive import with `text/markdown` when you want a clean native Google Doc from Markdown.
- Use Drive `files.update(..., media_body=MediaIoBaseUpload(..., mimetype='text/markdown'))` when you want to replace an existing doc in place.
- Drive in-place Markdown update preserves the Google Doc file ID/URL, but it replaces the document body. Treat it as whole-doc replacement, not a targeted edit.

## What this handles well
- headings
- tables
- lists
- inline formatting
- simple code blocks

## Code blocks
- If native Google Docs Code Blocks are desired in a new draft/preview, keep fenced Markdown blocks and use Drive Markdown import; Google's import pipeline can create native Code Blocks.
- If preserving a polished live doc, do not use whole-doc Markdown update just to create native Code Blocks unless the user explicitly accepts polish reset risk.
- For existing polished docs, prefer pre-created native Code Block placeholders and fill them with Docs API, or use styled code panels/manual/UI conversion. See `native-code-blocks.md`.
- Do not try to transfer imported Code Blocks into another doc by reading the source structure and reinserting it with Docs API; Private Use Area markers are stripped and the target becomes a styled panel.
- After import or update, run a code-block spacing pass where needed so monospace paragraphs use compact spacing.
- Use `docs_advanced.tighten_code_block_spacing(doc_id, tab_id=...)` after the markdown import is stable.

## Mermaid stripping rule
- If you extract Mermaid blocks, make sure the Drive import uses the stripped Markdown buffer, not the original source string.
- A common mistake is writing `content_no_mermaid` and then importing `content` by accident.

## Tables and headings
- If a publish path needs element-level control, re-read the doc after import and then style against real indices.
- Do not assume Markdown positions survive the import unchanged.

## Heading mapping policy
- In the `docs_api.py` markdown population path, heading mapping is:
  - `#` -> `TITLE`
  - `##` -> `HEADING_1`
  - `###` -> `HEADING_2`
  - and so on.
- If you use raw Drive `text/markdown` import instead, Google defaults to `#` -> `HEADING_1`. Run a post-pass if you need `#` to be title semantics.

## Polished Google Docs from Markdown
- For boss-facing or user-reviewed docs, do not rely on plain body insertion that looks like copied Markdown. Use Drive Markdown import/update to get native headings, tables, lists, links, and code blocks, then polish with Docs API helpers.
- For email-style memos or plain business notes, prefer plain prose with selective bold labels and real hyperlinks over visible markdown tables or markdown-looking headings. If the rendered result is meant to read like an email, the live doc should not expose `**`, `|`, or markdown header markers.
- Render Mermaid/Graphviz/HTML diagrams to image assets and insert them with `docs_advanced.insert_image`; do not leave raw Mermaid in the doc unless explicitly requested.
- After import, replace/remove any placeholder anchors, tighten code block spacing, export to PDF, and inspect contact sheets. See `polished-markdown-doc-publication.md`.
- Google Docs API may not accept an `insertTableOfContents` batchUpdate request; use a clean manual TOC plus the Google Docs outline unless a native TOC is required and can be inserted through the UI or another proven path.

## Verify after import
- Re-export with `docs_api.py get <doc_id> --md`.
- Check that headings, tables, code blocks, and links still look right.
- If the source Markdown contains diagram/image refs, confirm the published doc points at the current exported asset names and not a superseded filename.
- For code blocks, verify both monospace formatting and paragraph spacing; Google Docs often preserves the font but keeps too much paragraph space unless you tighten it explicitly.
