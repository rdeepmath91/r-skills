# Drive-file Scope, Mermaid Preview, and Source-Parity Checks

Use this when a Google Docs Markdown preview is needed but the normal helpers fail because OAuth has `documents` plus limited Drive scope such as `drive.file`, or when a Markdown source contains Mermaid that must become an inline image.

## Pattern

1. Load credentials with the scopes already stored in `~/.hermes/google_token.json`.
   - Do not force broad `documents` + `drive` scopes if the token was consented with narrower Drive scope.
   - Docs `documents.get` can still work even when Drive `files.get` returns 404 for files outside the app-created/file-scoped set.
   - Drive create/export can work for new preview docs created by this agent even if existing live docs are not visible via Drive metadata.

2. Create the preview via Drive Markdown import.
   - Use `MediaFileUpload(<source>.md, mimetype='text/markdown')` with body MIME type `application/vnd.google-apps.document`.
   - This preserves native headings, tables, links, lists, and monospace/code-like spans better than manual paragraph insertion.

3. Convert Mermaid before publication.
   - Extract Mermaid fences to `.mmd` files.
   - Replace the source fence with a stable placeholder such as `[ERD diagram placeholder]` in the import buffer.
   - Render to PNG locally, upload the PNG to Drive, make it reader-accessible for Docs, then replace the placeholder with `insertInlineImage`.
   - Do not leave raw Mermaid in the final preview.

4. Size images before insertion.
   - Google Docs API cannot resize existing inline images.
   - Large Mermaid renders can fail with `Invalid requests[].insertInlineImage: The provided image is too large` even if the PNG byte size seems reasonable.
   - Downscale the image dimensions before upload/insertion; for portrait previews, start around 2400px max width for the uploaded asset and insert at <=440pt display width. Recreate/reinsert if size is wrong.

5. Verify source parity after expected transforms.
   - Export the preview back to Markdown.
   - Normalize expected Google export differences: escaped `_` / `+`, generated image references, Docs private glyphs, and Mermaid-to-image replacement.
   - Compare normalized source lines and exported preview lines; report missing/extra lines, table-row parity, heading parity, link count, list count, and inline image count.
   - Treat Markdown export as source-alignment proof only; still run PDF/contact-sheet visual QA for publication readiness.

## Minimal checks that proved the pattern

For a Database Schema preview from Markdown with one Mermaid ERD:
- source headings matched imported heading counts exactly
- 17 source Markdown tables became 17 native Docs tables
- 43 numbered source lines became 43 list paragraphs
- 6 Markdown links became 6 linked text runs
- one Mermaid fence became one inline PNG image
- raw Mermaid and placeholder text were absent after insertion
- normalized source/export text parity was 1.0 with zero missing/extra lines

## Pitfalls

- Do not conclude a doc is inaccessible just because Drive `files.get` returns 404 under `drive.file`; try Docs `documents.get` with the token's stored scopes for read/structure checks.
- Do not use broad helper scope refresh as the only path when the task only needs read/preview creation; it can fail with `invalid_scope` on narrower tokens.
- Do not use `rm -rf` for contact-sheet cleanup in approval-gated environments. Prefer a fresh timestamped output folder so visual QA does not trip destructive-command approval.
- Do not claim visual polish from source parity. Source parity, Docs structure, PDF export, and contact-sheet inspection are separate validation boundaries.
