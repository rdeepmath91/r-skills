# Multi-Doc PR Preview To Live Sync

Use this when a PR finalizes a Markdown-backed Google Docs package and the user asks whether to sync directly to live docs.

## Decision rule

Do not live-sync blindly when the PR changes multiple structure-heavy docs. First compare PR/source Markdown to the current live docs, then create or refresh previews for changed docs, validate, and only promote after explicit approval.

Good candidates for preview-first:
- architecture/design/implementation packages
- docs with rendered diagrams or Mermaid
- docs with many tables or appendices
- any live doc with manual polish, version-control shells, TOCs, or comments

## Workflow

1. Identify changed docs from the PR file list and map each source Markdown file to its live Google Doc ID from `docs/SUMMARY.md` or the user's provided links.
2. Read live docs with the Docs API and compare against source:
   - heading counts and missing/extra headings
   - marker terms that indicate stale live content
   - table counts and image counts
   - raw Markdown links or stale local `.md` references
3. Create previews for only the changed live-doc targets.
4. Validate each preview separately:
   - source/export normalized parity
   - headings imported in order
   - native table count matches source table count when possible
   - no raw Mermaid fences or placeholder tokens remain
   - expected inline image count landed
   - PDF export and contact-sheet visual QA for layout-sensitive docs
5. Recommend live promotion only for previews that have passed structure + visual checks. Keep other previews as review candidates.
6. On live promotion, update the existing live doc IDs in place; do not replace links with fresh doc IDs unless the user explicitly accepts that.

## Large-doc import fallback

For large Markdown docs, fetch source files directly to disk instead of routing file contents through capped tool stdout. For GitHub files, use `gh api ... --jq .content | base64 -d > /tmp/source.md` or `gh api ... --output /tmp/raw.json` plus local decode; then scan for sentinel strings such as `OUTPUT TRUNCATED` before creating previews. Do not write `execute_code`/terminal captured output into the source file for large Markdown because the tool output cap can insert truncation markers into the document body.

Drive Markdown import/update may time out or return transient 500s. Treat that as a pipeline issue, not as a reason to skip previews.

Fallback:
1. Fetch local image assets referenced by Markdown (`![](assets/...)`) into the correct relative `assets/` path.
2. Convert Markdown to DOCX with Pandoc using a resource path:
   ```bash
   pandoc --resource-path=<source-root>:<source-root>/docs <source.md> -o <tmp>/<doc>.docx
   ```
3. Import the DOCX to Google Docs via Drive create/update with MIME type `application/vnd.openxmlformats-officedocument.wordprocessingml.document` and target Google Docs MIME type `application/vnd.google-apps.document`.
4. Verify that headings, native tables, and inline images landed.
5. If the source contains Mermaid, strip Mermaid blocks before DOCX conversion, leave unique placeholders, render each block to PNG, upload PNGs, and replace placeholders with inline images in reverse document order.

## Mermaid/image sizing

- Render Mermaid to PNG; do not leave raw Mermaid in the preview.
- For wide Mermaid diagrams, cap uploaded PNG dimensions/file size before insertion so Docs does not reject the image as too large.
- Insert images with aspect-aware widths:
  - portrait max width: 440pt
  - target max height: about 360pt
  - reduce width for tall diagrams instead of forcing landscape
- Insert later placeholders first so earlier indices do not shift.

## Orientation lessons

Orientation can be set per selected section, not only for the whole document. Whole-document landscape is only a diagnostic stress test, not a final default.

Before applying selective landscape:
- prove the artifact is width-constrained, not height-constrained
- include the heading + intro + artifact + immediate explanation in the landscape range
- restore portrait immediately after
- re-export and inspect for section-break artifacts, split words, leaked landscape, blank pages, and sparse pages

Do not landscape square/tall ERDs just because they are large; landscape does not solve height-driven overflow.

## Preserving live formatting shells

When current live docs have a polished title/version/TOC shell or manual typography, do not treat a regenerated preview as promotion-ready just because source parity passes. Use `references/live-style-shell-pr-sync.md` before final sync. In particular, compare content validity separately from style validity; if Drive API cannot copy the live doc because the token only has `drive.file`, ask for a live-derived copy or patch only a carefully bounded range after explicit approval.

## Validation and handoff language

Separate these states clearly:
- live doc compared, no mutation
- preview created
- preview structurally validated
- preview visually polished
- human editor review pending/passed
- live promotion approved/done

Never describe a preview as live-synced. Never claim PR/source updates imply live Google Docs updates.