# Live Style-Shell PR Sync

Use this when a Markdown-backed PR updates a polished Google Docs package and the live docs have a manually polished shell: title page, version-control table, TOC, page numbers, comments, custom heading styles, or manually placed diagrams.

## Core lesson

Do not promote a regenerated preview over the live document just because the content is newer. Start from the live document's style shell when the user cares about formatting.

Preferred flow:

1. Compare live vs PR/source with Docs API first.
2. Identify whether the preview is content-valid and style-valid separately.
3. If the live doc has a polished shell, preserve it:
   - copy from the live doc when Drive permissions allow, or
   - ask the user to make a live-derived copy, or
   - use targeted body-section patching only after explicit approval.
4. Replace from the first body heading such as `Executive Summary` through the bottom, leaving the live title/version/TOC shell intact.
5. After promotion, manually refresh the Google Docs TOC in the editor.
6. Export PDF/contact sheets after the final write.

## Drive `drive.file` trap

A token with `documents` + `drive.file` can read document structure through Docs API but still fail Drive API `files.get`, `files.copy`, or `files.export` on live docs that the app did not create or open.

Typical evidence:

- `docs.documents.get(documentId=...)` succeeds.
- `drive.files.get(fileId=...)` returns `404 File not found`.
- `drive.files.copy(fileId=...)` returns `404 File not found`.
- Owned preview docs created by the app are copyable/exportable.

Interpretation: this is app/file authorization scope, not proof that the doc ID is wrong or that Google auth is globally broken.

Fix options:

- Re-auth with full Drive scope (`https://www.googleapis.com/auth/drive`) when policy allows.
- Have the user manually make a live-derived copy and share/send that copy URL.
- Ask the user to explicitly open/share the specific live file with the app/account if their Workspace setup supports that.
- If only style/content comparison is needed, continue with Docs API; Drive copy/export is not required for style diffing.

## Style comparison checklist

Docs API is enough to compare live vs preview formatting:

- named styles: `NORMAL_TEXT`, `TITLE`, `SUBTITLE`, `HEADING_1..4`
- font family, size, foreground color
- line spacing, spacing above/below
- paragraph-style distribution
- explicit text-run fonts such as `Roboto Mono`, `Consolas`, `Cambria`, `Calibri`
- table count, row/cell count
- inline image/object count
- raw Mermaid or placeholder tokens

Watch for DOCX fallback drift:

- live GDP docs often use Proxima Nova body, GDP cyan headings, Roboto Mono code.
- Pandoc DOCX import may create Cambria body, Calibri headings, Consolas code.
- Google Docs API does not support `updateNamedStyle`; you can overlay visible `updateTextStyle`/`updateParagraphStyle`, but the underlying named style definitions remain from the import.

## Source-fetch safety

For large GitHub Markdown files, do not persist captured tool stdout into source files. Fetch directly to disk:

```bash
gh api repos/OWNER/REPO/contents/docs/file.md?ref=BRANCH --jq .content | base64 -d > /tmp/file.md
```

Then scan for sentinel text before preview creation:

```bash
grep -n "OUTPUT TRUNCATED\|chars omitted" /tmp/file.md || true
```

If a preview already contains truncation markers, treat it as invalid even if the formatting looks acceptable.

## Diagram strategy for schema docs

Mermaid ERD is good for exact machine-ish schema coverage, but can become unreadable when squeezed into portrait Google Docs.

Options:

1. Least disruptive: keep Mermaid ERD, make only the `Minimal ERD` section landscape, and resize the image wider.
2. Best exact-readable review artifact: split the dense Mermaid ERD into multiple Mermaid-rendered panels by concern, preserving the original relationship set and adding only clearly FK-derived scope edges needed to make each panel self-contained. For schema docs, a useful four-way split is identity/auth/backend scope, runnable registry/versioning, scheduling, and run execution/events.
3. Better executive overview: replace the dense Mermaid ERD with a custom readable HTML/SVG/PNG summary that groups entities by ownership seam and shows key fields only.

When the section is titled `Minimal ERD`, prefer option 2 before option 3. A custom summary can look “broken” or incomplete if the user expects an ERD with actual relationships. When replacing an ERD with a readable summary, state clearly that it is a readable ERD summary rather than a complete literal Mermaid dump.

For the concrete split-ERD + live-style preview pattern, see `references/markdown-preview-diagram-polish-case-notes.md`.

## Preview-to-live copy compatibility gate

When the user says the preview must be copied seamlessly into the live doc later, validate copy compatibility separately from content correctness and visual polish.

Minimum gate before handoff:

1. Read live and preview through Docs API from the intended copy boundary, usually `Executive Summary` through the bottom.
2. Compare common heading texts and their `namedStyleType` values. A common import failure is every preview heading being one level too low (`HEADING_1` in live becomes `HEADING_2` in preview, `HEADING_2` becomes `HEADING_3`, etc.). This breaks the live outline/TOC after manual copy even when visual thumbnails look acceptable.
3. If headings are shifted, update the preview headings in place with `updateParagraphStyle.namedStyleType` before styling or handoff. Promote each heading by the detected offset, then re-read and require zero common-heading level mismatches.
4. Compare paragraph-style distribution, explicit fonts, table count/shape, inline image count, and raw marker counts. Treat these as compatibility evidence, not as proof the content is identical.
5. Export the preview PDF and render contact sheets. Blank-page detectors can miss large vertical gaps, so still inspect representative sheets visually.
6. Separate remaining gaps into:
   - copy-compatibility blockers: heading-level mismatch, raw Markdown/Mermaid/placeholders, blank pages, broken images, unreadable diagrams, table corruption;
   - content/version drift: renamed headings, missing/extra sections, intentional split diagrams, changed table counts.

Handoff should explicitly say whether the preview is safe to copy from `Executive Summary` downward into the live doc without breaking heading hierarchy, and list content/version drift separately.

## Handoff language

Separate these states in the final note:

- live doc compared, no mutation
- preview content-valid
- preview style-valid or style-drifted
- preview-to-live copy compatible, including common-heading `namedStyleType` match from the copy boundary
- preview invalid due to truncation or import artifact
- live-derived copy needed
- manual copy range recommended, e.g. `Executive Summary` through bottom
- live promotion approved/done
