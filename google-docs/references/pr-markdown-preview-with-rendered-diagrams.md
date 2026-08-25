# PR Markdown Preview With Rendered Diagrams

Use this when a PR updates Markdown docs and the user wants to test a simple Google Docs refresh path before touching live docs.

## Pattern

1. Pull the PR Markdown source by branch/ref into `/tmp` or a project scratch directory.
2. Create a preview Google Doc first; do not update the live doc ID unless the user explicitly approves promotion.
3. If the Markdown contains Mermaid blocks:
   - extract the Mermaid block to a `.mmd` file,
   - replace the fenced block in the import buffer with a unique placeholder,
   - render the Mermaid locally to PNG,
   - import the stripped Markdown as a Google Doc,
   - find the placeholder in the live Docs structure and replace it with `insertInlineImage`.
4. Validate the preview via the Docs API, not by trusting the create call:
   - expected title/headings are present,
   - native table count roughly matches source Markdown table count,
   - expected terms/sentinels appear or are absent,
   - raw Mermaid text and placeholder are absent,
   - inline object count is non-zero when a diagram was expected.
5. Clean up failed scratch docs/images so the user only sees the final preview artifact.

## Limited-scope token workaround

If the standard helper fails with `invalid_scope: Bad Request`, do not conclude the document is inaccessible. Load credentials with the scopes already stored in `~/.hermes/google_token.json` and call Docs/Drive APIs directly. This is especially useful when the token has `documents` plus limited Drive scopes such as `drive.file`.

Drive `files.get` may still 404 for docs not created/opened by the app under `drive.file`; Docs `documents.get` can still succeed. For write/import/create flows, verify the exact operation rather than relying on Drive metadata access as a proxy.

## Mermaid image-size pitfall

Docs `insertInlineImage` can reject very large rendered PNGs even when the file size is not huge:

```text
Invalid requests[...].insertInlineImage: The provided image is too large.
```

Fix by resizing the rendered image before upload/insertion. A safe first pass is max width around `2400px`, then insert around `440pt` wide for portrait pages. Preserve the original full-size PNG only as a local artifact; upload the resized PNG for Docs insertion.

## Minimal validation payload to report

Report concise evidence:

- preview URL
- source file path/ref and line/byte count
- native table count vs Markdown table count
- first headings
- inline object count
- sentinel term checks
- whether live docs were untouched

Avoid overclaiming visual polish unless you also export PDF/contact-sheet QA.