# Command Recipes

## Auth
- `python3 <skill-root>/scripts/setup.py --check`
- For dependency and OAuth setup decisions, use `references/setup-and-dependencies.md` and `references/auth-and-setup.md`.

## Full reproducible diagram/doc workflow
Use this when you want to recreate the Mermaid/PNG/Google-Docs pipeline in any environment.

Keep the instructions reusable:
- do not name specific project files unless the user asked for them
- do not hardcode machine-specific paths
- use placeholders like `<skill-root>` and `<python-with-google-deps>`

Assume:
- `<skill-root>` is where this skill is installed in the current agent environment
- `<python-with-google-deps>` is a Python interpreter that has the Google Docs dependencies installed

1. Find the source Markdown and identify the canonical diagram blocks.
   - Search the project for Markdown, image assets, and Mermaid fences.
   - Read the actual source files directly.
   - The key idea is to decide which Markdown files are authoritative for each diagram family, then treat those files as the input set for the rest of the pipeline.

2. Extract Mermaid blocks and save their anchors.
   - Strip Mermaid fences from the Markdown buffer before import.
   - Record the nearest heading or paragraph before each diagram so you can re-anchor the image later.
   - Do not assume source line numbers survive the import.

3. Render Mermaid locally with Mermaid CLI.
    - Use Mermaid CLI via `npx`.
    - Example command:
      - `npx --yes @mermaid-js/mermaid-cli@11.4.3 -i input.mmd -o output.png -p /tmp/pp.json -b white -s 4 -w 3200`
   - Create `/tmp/pp.json` with:
     - `{"args": ["--no-sandbox"]}`
   - This matters because Google Docs will not turn Mermaid fences into diagrams for you. Raw Mermaid remains text until you render it.

4. Render Graphviz dot separately when it gives better layout control.
   - For layered block diagrams, use Graphviz dot instead of Mermaid.
   - Example:
     - `dot -Tpng diagram.dot -o diagram.png`
   - Keep the source format and the rendered image as separate artifacts.

5. Import the stripped Markdown into Google Docs.
   - For one file, place it in a temporary directory because the bulk pipeline expects a folder.
   - Example:
     - `mkdir /tmp/gdocs-publish && cp myfile.md /tmp/gdocs-publish/`
     - `python3 <skill-root>/scripts/publish_pipeline.py /tmp/gdocs-publish`
   - If you already have a native Google Doc ID and want to update in place, use:
     - `python3 <skill-root>/scripts/docs_api.py update DOC_ID --md FILE`
   - Use the bulk pipeline for many docs; use the direct update path when the target doc already exists.

6. Insert the rendered images after import.
   - Use:
     - `docs_advanced.insert_image(doc_id, image_path, start_index=..., width_pts=..., height_pts=...)`
   - The first argument must be the native Google Doc ID.
   - The helper uploads the image, makes it readable, and inserts it by URI.
   - Prefer a full-resolution Drive URL when available; thumbnail-only insertion can look soft.

7. Read the live doc structure once, then insert from bottom to top.
   - Inspect the doc with:
     - `python3 <skill-root>/scripts/docs_api.py get DOC_ID --raw`
   - Use `--fields` when you only need a narrow slice of the structure.
   - Insert the later diagram first so earlier anchor indices do not shift.

8. Verify the result, then adjust sizing.
   - Re-export with:
     - `python3 <skill-root>/scripts/docs_api.py get DOC_ID --md`
   - Confirm the document contains inline images, not literal Mermaid fences.
   - In the raw export, look for `inlineObjects` to confirm the images landed.
    - Size diagrams by page space and aspect ratio, not by a fixed width.
    - Tall diagrams usually need a narrower width so they do not consume too much vertical space.

9. Keep layout rules config-driven, not hardcoded into the skill.
   - For recurring doc families, maintain a local wrapper config with per-doc values such as:
     - `landscape` section ranges
     - `page_break_before` headings
   - Keep those heading names in the project-local refresh script, not in the shared skill.
   - This is the cleanest way to preserve user-approved layout intent without making the skill project-specific.

## Fast fallback when `docs_api.py create --md` or `update --md` hits 429 write quota
If direct create+populate or update+populate fails with `WriteRequestsPerMinutePerUser` (429), switch immediately to a Drive import/update path instead of retry-looping Docs `batchUpdate` writes.

Create-new-doc pattern:
1. Put the single markdown file in a temporary folder.
2. Run `publish_pipeline.py <tmpdir>` (the script expects a directory).
3. Read `<tmpdir>/.doc_ids.json` to get the created doc ID.
4. Continue post-processing (rename, image insertion, orientation, validation) on that doc ID.

Existing-doc URL-preserving update pattern:
1. If the edit is non-trivial, copy the live doc first as a preview/simulation.
2. Use Drive `files().update(fileId=<doc_id>, media_body=MediaFileUpload(<file>.md, mimetype='text/markdown', resumable=True), body={'name': <title>})` to replace the doc contents while preserving the native Google Doc ID/URL.
3. Use a longer `httplib2.Http(timeout=240)` plus resumable upload for markdown updates that time out on normal upload.
4. Re-read headings and exported Markdown after the update; verify required sections landed before promoting the same operation to live.

Minimal existing-doc update snippet:
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_httplib2 import AuthorizedHttp
import httplib2, os

creds = Credentials.from_authorized_user_file(
    os.path.expanduser('~/.hermes/google_token.json'),
    ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive'],
)
http = AuthorizedHttp(creds, http=httplib2.Http(timeout=240))
drive = build('drive', 'v3', http=http)
media = MediaFileUpload('/tmp/source.md', mimetype='text/markdown', resumable=True)
req = drive.files().update(
    fileId='<doc_id>',
    media_body=media,
    body={'name': '<Drive title>'},
    fields='id,name,webViewLink,mimeType',
)
res = None
while res is None:
    status, res = req.next_chunk(num_retries=3)
```

Why this works:
- `docs_api.py create --md` / `update --md` can trigger many Docs write operations for style passes and exceed per-minute write quota.
- Drive markdown import/update usually succeeds under the same quota pressure because it avoids that burst pattern and can preserve the existing Google Doc URL when used with `files().update`.

## Single-file markdown with one local PNG
When the source of truth is one Markdown file plus an inline PNG asset, use this pattern:

1. Copy the source Markdown into a temporary directory.
   - `publish_pipeline.py` expects a directory, not a single file.
   - Keep the file name stable so the `.doc_ids.json` mapping is easy to read back.

2. Strip the literal `![](...)` image line before the Markdown import.
   - Import the prose/tables/links first so the doc comes in cleanly.
   - Insert the image afterward with `docs_advanced.insert_image(...)`.

3. Publish the temp directory, then rename the doc.
   - Drive import preserved tables and links more reliably than ad hoc Docs styling.
   - Renaming the Drive file after publish keeps the visible doc title aligned with the source.

4. Keep the first export pass portrait with default styles.
     - Do not pre-emptively switch to landscape during initial import.
     - After content/images are stable, run a second layout pass and apply landscape only to wide sections (or whole doc if truly needed).
     - For each landscape section, include the heading, short explanation, diagram/table, and immediate interpretation block in the same selected-content range when possible.
     - If multiple landscape ranges are needed, apply them from bottom to top so section-break insertion does not corrupt later anchor indices.

5. Find the insertion anchor from the live doc structure, not from source line numbers.
   - Match the imported paragraph text exactly or by normalized text.
   - Insert the image after the paragraph that introduces it.

6. Insert the PNG inline with a page-space-aware width.
     - Use `docs_advanced.insert_image(doc_id, image_path, start_index=..., width_pts=...)`.
     - Wide overview figures often look best around half-page to full-page width depending on surrounding tables.
     - Support diagrams are usually better slightly smaller so the page can keep the title and short explanation together.
     - For square or near-square overview diagrams, reduce portrait width before forcing landscape.

7. Validate both structure and rendering.
   - Check headings and tables in the exported Markdown.
   - Check `inlineObjects` in the raw doc structure.
   - Confirm the image is actually inline, not pasted as literal Markdown text.

9. Do a visual QA pass on the rendered asset, not just the source.
   - Capture the doc or the rendered PNG and inspect it visually.
   - Compare the image against the source Markdown and the nearby prose so you can tell whether the issue is diagram structure, render quality, or Docs insertion.
   - The image can be wrong even when the Mermaid source is valid; layout, aspect ratio, and insertion width still matter.
   - If a diagram is blurry or cramped, adjust the render command and the insert width before changing the content.
    - For wide diagrams, keep the document portrait by default first; then switch only the truly wide sections to landscape after import and image insertion.
    - If a section becomes landscape, include the heading, short intro, diagram, and immediate interpretation in the same range instead of isolating only the raw image.
    - When the Markdown contains placeholder anchors for images, replace them after import using the live doc indices from `docs_api.py --raw`, not the source line numbers.
    - Insert multiple diagrams from bottom to top so earlier anchor indices do not drift.

10. For large preview docs, generate page-audit contact sheets from the exported PDF.
    - A contact-sheet pass is much faster than opening dozens of pages manually one by one.
    - Reusable helper:
      - `python3 <skill-root>/scripts/render_pdf_contact_sheets.py --inputs /path/to/doc.pdf --out-dir /tmp/page_audit_sheets`
    - Use it to classify issues into:
      - blocker: blank pages, unreadable diagrams, broken orientation
      - medium: orphaned headings, split tables/code blocks, sparse carry-over pages
      - cosmetic: mild underfilled pages or awkward but readable breaks
    - Use those findings to decide whether to change source content, page-break rules, or landscape ranges.

11. If the doc is visually corrupted, recreate or clear it.
   - If a Markdown import turns into plain text or heading styles are wrong, it is often faster to clear/recreate the doc than to patch the malformed structure in place.
   - Then republish the stripped Markdown and reinsert the images.

12. If the skill itself changes, sync the repo and PR.
    - Commit and push the skill change in the repository that owns the skill.
    - If the PR body needs updating, patch it with the repository’s normal GitHub workflow.

## Structure-heavy live-tab update after preview approval

Use this when a preview doc has already been approved and you need to mirror a subset of that content into one tab of a shared multi-tab live document.

1. Confirm the preview doc is the approved source of truth.
2. Identify the target live `tab_id` and the exact insertion/replacement anchor inside that tab.
3. Update only the changed tab; do not republish the whole parent doc.
4. Preserve native tables where possible instead of flattening them into plain text.
5. Re-apply tab-local orientation and code-spacing cleanup after the insert.
6. Verify the live tab with a tab-aware read before closing the task.

## Source-first fixes for stubborn layout problems

If a preview remains hard to read after image fitting and landscape placement, fix the source before adding more Docs post-processing:

1. shorten diagram node labels
2. switch tall flowcharts from `TD` to `LR` when that reduces height
3. merge tiny tail notes back into earlier prose instead of letting them create near-empty final pages
4. add short intro sentences under major headings when Docs keeps isolating them as heading-only pages
5. split an over-wide matrix into two smaller tables only when landscape plus shorter labels still does not work


## Publish
- `python3 <skill-root>/scripts/publish_pipeline.py /path/to/markdown/folder`
- `publish_pipeline.py` requires a **directory**, not a single file. For a single file: `mkdir /tmp/gdocs-publish && cp myfile.md /tmp/gdocs-publish/ && python3 ... /tmp/gdocs-publish`
- By default, the pipeline may create a new doc on each publish if it does not find a stored mapping.
- If the user wants to keep the same URL stable, update the existing doc in place instead of republishing a fresh one. Reuse the stored `.doc_ids.json` mapping and `update_doc_content()` / `drive.files().update(...)` against the existing doc ID.
## Rename a doc after publish
The Drive import renders the title as HEADING_1, not a separate doc title field. To fully rename:
1. `drive.files().update(fileId=doc_id, body={'name': 'New Title'})` — updates Drive listing
2. `replaceAllText` on the old HEADING_1 text — updates the visible heading in the doc
Both are needed; one does not cover the other.

## Replace a specific live-doc section in place
Use this when the user wants to edit one section of an existing Google Doc without republishing the whole document.

Preferred workflow:
1. Read the live doc first and confirm the exact anchor text already present in the document.
   - Best case: a unique placeholder such as `(please insert here)` under a known heading.
2. Replace only that exact visible text with `replaceAllText`.
3. Verify that the replacement happened exactly once.
4. Re-read the nearby section to confirm the new content landed under the intended heading.

Example request body:

```json
{
  "requests": [
    {
      "replaceAllText": {
        "containsText": {
          "text": "(please insert here)",
          "matchCase": true
        },
        "replaceText": "1. First item\n2. Second item"
      }
    }
  ]
}
```

Notes:
- This is for visible text replacement only. It does not update links, smart chips, or other structured objects.
- Do not use blind replacement when the marker text appears more than once. Make the anchor unique first or switch to a range-based edit workflow.
- For recurring operational docs, keep a stable placeholder or marker so later section refreshes stay deterministic.

## Deterministic heading-based section editing
Use this when the document already has stable headings and you want to replace one section body without republishing the whole doc.

1. List headings first:
   - `python3 <skill-root>/scripts/docs_api.py headings DOC_ID`
2. Inspect the target section range:
   - `python3 <skill-root>/scripts/docs_api.py section-range DOC_ID --heading "Implementation Read Path"`
3. Replace only that section body from a file or direct text:
   - `python3 <skill-root>/scripts/docs_api.py replace-section DOC_ID --heading "Implementation Read Path" --file /tmp/section.txt`
4. Verify the edit with `docs_api.py get` or a PDF export.

Notes:
- This is best for prose and simple bullet/numbered lists.
- It is not a substitute for full Markdown import when the section contains complex tables or many structural objects.

## Render handcrafted HTML diagrams to tight PNGs
Use this when a hand-authored HTML diagram has too much whitespace or needs reproducible asset rendering.

Example:

```bash
python3 <skill-root>/scripts/render_html_assets.py \
  --pair /abs/path/diagram.html::/abs/path/diagram.png
```

Why this helps:
- headless Chrome renders the HTML consistently
- the script auto-crops white margins
- overview diagrams stay reusable across preview and live workflows

## Native TOC and page numbers
Detect native TOCs from raw Docs structure by looking for `tableOfContents` elements. Do not treat a visible `Table of Contents` heading as proof that a native TOC exists.

Detect page numbers from raw Docs structure by inspecting `headers` / `footers` content for `autoText` entries such as `PAGE_NUMBER` and `PAGE_COUNT`. The Docs API can read these shells; do not rely on PDF text extraction alone.

The Docs API cannot reliably finalize page-number shells or refresh TOC pagination. If headings or pagination changed, inspect/export the doc and report whether the native TOC needs manual refresh in the editor.

For polished docs with an organization publication baseline, do not mark TOC or page-number requirements as passed from API import alone. Verify native TOC and page numbers in the raw structure/PDF. For GDP Labs docs, this maps to `DOC3` and `DOC4`. If required shell elements are missing and cannot be added programmatically, report them as findings and ask for manual insertion or use an existing polished shell as the update target.

Example raw-structure checks:

```bash
python3 <skill-root>/scripts/docs_api.py get <doc_id> --raw --fields 'body/content(startIndex,endIndex,tableOfContents),headers,footers'
```

## Inspect rendered docs
- `python3 <skill-root>/scripts/docs_api.py get <doc_id> --md`
- `python3 <skill-root>/scripts/docs_api.py export <doc_id> --format md` for Markdown export; valid `export` formats are `md`, `html`, and `txt` only.
- For PDF validation, do not call `docs_api.py export --format pdf`; export through Drive API with MIME type `application/pdf`, then render contact sheets.

Minimal PDF export snippet:
```python
import io, sys
sys.path.insert(0, '<skill-root>/scripts')
import docs_api
from googleapiclient.http import MediaIoBaseDownload

drive = docs_api.build_service('drive', 'v3')
req = drive.files().export_media(fileId='<doc_id>', mimeType='application/pdf')
out = io.FileIO('/tmp/doc.pdf', 'wb')
downloader = MediaIoBaseDownload(out, req)
done = False
while not done:
    status, done = downloader.next_chunk()
```

## Inspect raw structure
- `python3 <skill-root>/scripts/docs_api.py get <doc_id> --raw`

## Inspect a narrow structure slice
- `python3 <skill-root>/scripts/docs_api.py get <doc_id> --raw --fields 'title,body/content(startIndex,endIndex,paragraph(elements(textRun(content),inlineObjectElement),paragraphStyle/namedStyleType))'`

## Insert image
- `docs_advanced.insert_image(doc_id, image_path, start_index=..., width_pts=..., height_pts=..., tab_id=...)`
- The first argument should be the native Google Doc ID, not a Drive Markdown file ID.
- Images are center-aligned by default (`updateParagraphStyle.alignment=CENTER` on insert).
- Pass `tab_id` for multi-tab docs to avoid writing into the first tab by mistake.
- The helper now defaults to public Drive access for the uploaded image so Docs can fetch the thumbnail URI.
- `width_pts` / `height_pts` resize the image before upload.
- When inserting multiple diagrams, insert the later one first.
- Verify the final doc with `inlineObjects`, not only with Markdown export.

## Tighten code block spacing
- After markdown import, run `docs_advanced.tighten_code_block_spacing(doc_id, tab_id=...)`.
- This sets paragraph spacing before/after to zero for code-like monospace paragraphs.
- Use it after import/update, not before, because the detection depends on the imported paragraph structure.

## Native Code Block handling
- For new draft/preview docs where native Google Docs Code Blocks are desired, use Drive Markdown import with fenced blocks. Do not insert fenced blocks with Docs API and expect conversion.
- For polished existing docs, prefer pre-created native placeholders such as `CODE_BLOCK_PLACEHOLDER_001`; replace only the placeholder text via Docs API.
- Validate native behavior by checking expected code text plus `\ue907` marker count before/after; marker count should stay unchanged for placeholder fills.
- If no placeholder exists and native blocks are required, use a manual/UI pass or explicitly approved browser automation; otherwise use styled monospace panels and call out the limitation.
- Full policy and probe results: `references/native-code-blocks.md`.

## Bullet/list style presets

Valid `bulletPreset` values for `createParagraphBullets`:

- `BULLET_DISC_CIRCLE_SQUARE` — standard disc bullets
- `BULLET_STAR_CIRCLE_SQUARE` — star bullets
- `BULLET_ARROW_DIAMOND_DISC` — arrow bullets
- `BULLET_CHECKBOX` — checkbox style
- `NUMBERED_DECIMAL_ALPHA_ROMAN` — numbered: 1, 2, 3
- `NUMBERED_UPPERALPHA_ALPHA_ROMAN` — lettered: A, B, C
- `NUMBERED_DECIMAL_NESTED` — nested decimal
- `NUMBERED_ZERODECIMAL_ALPHA_ROMAN` — zero-padded: 01, 02, 03
- `NUMBERED_UPPERROMAN_UPPERALPHA_DECIMAL` — roman/alpha/decimal

To change an existing list's style (must delete first, then recreate):
```python
requests = [
    {'deleteParagraphBullets': {'range': {'startIndex': start, 'endIndex': end}}},
    {'createParagraphBullets': {'range': {'startIndex': start, 'endIndex': end}, 'bulletPreset': preset}},
]
```

Note: The bullet preset is stored on the list object, not the paragraph. Inspect list styles via `doc['lists']` and check `glyphType` on nesting levels (`DECIMAL`, `UPPER_ALPHA`, etc.), not via paragraph-level `bulletPreset`.

## Switch page orientation
- Whole document: `docs_advanced.set_page_orientation(doc_id, landscape=True)`
- Selected range as its own section: `docs_advanced.set_section_orientation(doc_id, start_index, end_index, landscape=True, tab_id=...)`
- Auto-detect per selected range: `docs_advanced.set_section_orientation_auto(doc_id, start_index, end_index, tab_id=...)`
- Preferred default: portrait first, then selected-content landscape only where width is truly needed.
- For wide tables or diagrams, do not target only the raw table/image object; target the full content block that introduces it.
- In practice, the best range usually includes: heading + short explanation + diagram/table + immediate interpretation paragraph(s).
- For multi-tab docs, include `tabId` in `Location`/`Range` for section-break and section-style requests, or the API applies to the first tab by default.
- Docs `get` field masks cannot mix `tabs(...)` with legacy text/body fields in one request; fetch tab metadata and body/style data in separate calls.

## Tab operations (multi-tab docs)
- List tabs: `docs_advanced.list_tabs(doc_id)`
- Add tab: `docs_advanced.add_document_tab(doc_id, "[EXPERIMENTAL] ...")`
- For content writes in tabbed docs, always pass `tab_id` on insert and section-style requests.

## Verify after write/update timeout
If a Docs update command times out after sending content, do not assume it failed and immediately retry. First export/read the target doc and search for the newly expected headings or sentinel text.

Pattern:
1. Run the update with a generous timeout.
2. If the command times out, export the doc as `txt` or `md`.
3. Grep/search for newly inserted section headings or distinctive text.
4. If present, treat the update as likely successful and continue validation.
5. Only retry or switch to Drive import/update if verification shows the content did not land.

Why this matters:
- Google Docs/Drive writes can complete server-side after the local client times out.
- Blind retries can duplicate content, waste quota, or overwrite a successful update.

## Recovery when reads time out
- Do not keep retrying `--raw` on a huge doc.
- Prefer `--fields` to fetch only the paragraphs you need.
- Read the source Markdown first.
- Use one doc-structure read, then insert images in reverse order.
- If the helper script still times out, use a direct Docs client with a longer HTTP timeout and then come back to the skill workflow.

## Fallback when Markdown import is unstable (429/500) but user needs formatted output now
Use this when:
- Docs API `update --md` is blocked by write quota (429)
- Drive `text/markdown` import repeatedly returns 500/timeouts
- User wants native formatting (not raw markdown text)

Recipe:
1. Convert source Markdown to `.docx` with Pandoc.
   - `pandoc <source.md> --resource-path <source_dir> -o <tmp>/doc.docx`
   - `--resource-path` is important so relative images resolve.
2. Import `.docx` to Google Docs via Drive create (`mimeType=application/vnd.google-apps.document`).
3. Post-pass heading mapping if needed (`# -> TITLE`, `## -> HEADING_1`, ...), because DOCX/Drive mapping may differ.
4. Normalize typography to match the target document or organization baseline by targeted `updateTextStyle`/`updateParagraphStyle` ranges:
   - body: target body font and size, with line spacing from the baseline
   - headings/title: target heading font and sizes
   - for GDP Labs docs, the baseline may use Proxima Nova; do not apply that font to non-GDP docs unless requested
   - preserve monospace runs (`Consolas`/`Courier New`/`Roboto Mono`) so code-like text remains readable.
5. Verify with a structure read (`documents.get(includeTabsContent=True)`) and count fonts/sizes before handing off.

Why this works:
- DOCX import often bypasses the flaky Markdown upload path while still producing native headings/tables/links.
- A small style-normalization pass gets the result close to an existing canonical Google Doc look.

## Selective multi-doc creation (not whole directory)
When publishing only some files from a directory, `publish_pipeline.py` doesn't support filtering. Use a standalone script instead:
1. Build an explicit allowlist of existing `.md` paths; do not assume optional docs are present.
2. Strip Mermaid blocks before import, keep the nearest heading as an anchor, and render the diagrams locally to PNG.
3. Keep fenced Markdown blocks when native Google Docs Code Blocks are desired from Drive import; convert only if you intentionally want plain monospace fallback instead of native blocks.
4. Create docs via Drive `MediaIoBaseUpload` with `mimetype="text/markdown"`.
5. Rewrite inter-doc links in a second pass, then `drive.files().update()` each doc in place so URLs stay stable.
6. Insert the rendered PNGs in reverse anchor order so earlier indices do not shift.
7. After images land, switch only the truly wide content blocks to landscape; keep portrait as the default.
8. Run `docs_advanced.tighten_code_block_spacing(...)` after import if the doc contains code blocks.
9. Verify the final doc with `inlineObjects` after insertion, not just a markdown re-export.

## Preview-doc remediation pass (in-place, no full republish)
Use this when preview docs were manually reformatted (orientation/image tweaks) but code blocks or spacing rules regressed.

1. Run code-block spacing normalization across all target preview doc IDs:
   - import `docs_advanced` and call `tighten_code_block_spacing(doc_id)` per doc
   - capture per-doc counts: `detected_code_like_paragraphs`, `updated_paragraphs`
2. Verify a known problematic block by anchor heading (for example `Example: Agent Step Event`):
   - read live doc structure with Docs API
   - find paragraphs after the anchor
   - confirm code-like paragraphs carry paragraph-style spacing overrides (`spaceAbove` / `spaceBelow` set to zero-PT style)
3. If content parity is still required, do this remediation first, then run in-place markdown refresh and re-apply spacing/orientation passes.

Why this helps:
- avoids full republish when only formatting regressed
- gives deterministic proof for user-reported blocks
- keeps preview URLs stable while fixing style compliance

## Validation commands

Validation process lives in `references/validation-workflows.md`. Keep this section to command snippets only.

- Post-refresh audit: `<python-with-google-deps> <skill-root>/scripts/preview_post_refresh_audit.py --docs docA=DOC_ID docB=DOC_ID`
- Post-refresh audit with heading order: `<python-with-google-deps> <skill-root>/scripts/preview_post_refresh_audit.py --docs docA=DOC_ID --heading-order "Section A" "Section B"`
- Contact sheets: `python <skill-root>/scripts/render_pdf_contact_sheets.py --inputs /path/to/doc.pdf --out-dir /tmp/page_audit_sheets`
- Real API smoke test commands: `docs_api.py create`, `docs_api.py update`, `docs_api.py get --md`, then Drive cleanup according to policy
- Skill script compile check: `python -m py_compile <skill-root>/scripts/*.py`

## When to use these
- Use the command recipes when the user needs a direct operational step.
- Keep the main skill short; send detailed mechanics to the reference files.
