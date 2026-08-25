# Polished Markdown-to-Google-Doc Publication

Use this when a user asks for a proper Google Doc from Markdown, especially when the doc includes tables, code snippets, diagrams, or architecture/SOP content. Do not merely paste raw Markdown into the document body.

## Preferred workflow

1. Prepare a clean Markdown source
    - Keep headings, tables, lists, links, and fenced code blocks in normal Markdown.
    - For polished/boss-facing docs, create a Docs-specific import buffer instead of uploading the raw source verbatim when the source front matter or inline-code markers would look pasted. Convert title/front matter into a visible title plus native metadata table when appropriate, and preserve fenced code only where code is actually useful.
    - Replace diagram placeholders with an explicit marker if the diagram will be inserted as an image later.
    - Before touching any Google Doc, verify the Markdown image count matches the refresh wrapper's image list. Fail in local preflight if the counts differ.
    - Do not leave raw Mermaid in the live Google Doc unless the user explicitly wants source text.

2. Use Drive Markdown import/update for native formatting
   - For creating/replacing a doc body while preserving the doc ID, use Drive `files.update(..., media_body=MediaFileUpload(..., mimetype='text/markdown'))`.
   - This converts headings, tables, lists, links, and many code blocks into Google Docs-native structures better than `docs_api.py update` plain population.
   - Treat this as whole-document replacement. Do not use it on a polished live doc unless the user accepts that body polish may reset, or the doc is intentionally being regenerated.

3. Render diagrams as images before insertion
   - Render Mermaid/Graphviz/HTML diagrams locally to PNG/SVG.
   - Visually inspect the rendered image for cropping, readability, and balance before insertion.
   - For multiple diagrams, replace each Markdown image in the import source with a unique plain-text anchor such as `DIAGRAM_ANCHOR_RUNTIME_CONTEXT_LOOP`. After Drive import, loop through anchors: find the current text index, insert the image with `docs_advanced.insert_image(...)`, then `replaceAllText` the anchor to empty. Re-fetch the doc before each anchor lookup because insertions shift indexes.
   - Keep captions such as `Figure 1. ...` in the Markdown/doc immediately after each anchor. Google Docs Markdown export may escape punctuation in bold captions (`Figure 2\.`), so validation should search tolerant patterns or use plain text extraction when exact Markdown matching fails.

4. Apply post-import polish
     - Set readable margins if needed.
     - For table-heavy comparison docs, use landscape orientation before shrinking text aggressively.
     - Style table header rows and tighten table cell padding; reduce table font only enough to prevent wrapping/clipping.
     - Do not leave metadata as a plain multi-line paragraph when a title block or small metadata table would read better in Google Docs.
     - Avoid excessive inline monospace/green styling from Markdown backticks in executive prose. If it makes the doc look raw-pasted, strip inline backticks in the import buffer and reserve code styling for actual snippets, paths, or compact examples.
     - Split wide comparisons into summary/decision/detail tables rather than one over-wide table when the user needs quick decisions.
     - Use page breaks only to prevent orphan headings or awkward table starts; re-export after each page-break change because fixing one section can push links/notes onto a sparse final page.
     - Tighten imported code block spacing with `docs_advanced.tighten_code_block_spacing(doc_id)`.
    - For Google Docs API limitations, use pragmatic fallbacks: the API may not support inserting a native dynamic TOC via `batchUpdate`; a clean manual TOC plus the Docs outline is acceptable unless the user specifically requires a native TOC.

5. Prefer compact executive-doc polish for architecture/SOP notes
   - Keep front matter short when present: creator and last-updated metadata are enough unless the user asks for a fuller cover page.
   - Use selective italics to frame key context or recommendations, not entire paragraphs.
   - Bold only the core takeaway phrase or capability statement that a reader should remember.
   - Keep setup snippets illustrative and compact. Use a fenced native-code-block-friendly language tag such as `py`, omit nonessential configuration with `...`, and include only the surfaces needed by the examples.
   - Add one plain transition sentence after a fenced code block before the next heading so Markdown import does not visually or structurally attach the code block to the heading.

6. Validate in the live document
    - If the user names multiple doc IDs as live/current targets, refresh and validate each named doc explicitly. Do not rely on stale preview/live labels.
    - Re-export plain text with `docs_api.py export <doc_id> --format txt > /tmp/live-export.txt` and confirm visible text has no raw placeholders or Markdown artifacts such as `DIAGRAM_ANCHOR`, `TOC_ANCHOR`, `assets/*.png`, `![]`, `|---|`, raw Mermaid fences, or accidental duplicate front matter.
    - Use Markdown export only as a secondary source-alignment check. Google Docs Markdown export serializes native headings, images, tables, and code blocks back into Markdown syntax, so `#`, `![][image1]`, table pipes, and fenced code in that export are not by themselves raw-paste evidence.
    - Run `docs_api.py headings <doc_id>` to verify expected sections landed as native headings.
    - Check the raw Docs structure for expected native tables, heading styles, and inline image object count when diagrams should be present.
    - Confirm no visible raw Markdown fences or raw Mermaid remain in the Google Doc body unless intended. Markdown export may show fenced code for a correctly imported native code block; that is not a failure by itself.
   - For fenced-code imports, verify native code markers exist when native code blocks are expected, no marker is attached to headings, and code-block spacing cleanup ran after import.
   - Export to PDF and render contact sheets using `scripts/render_pdf_contact_sheets.py` for visual review.
   - Inspect contact sheets for huge gaps, blank pages, broken tables, oversized/tiny diagrams, raw Markdown artifacts, and code block readability.

## Minimal Python pattern

```python
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_httplib2 import AuthorizedHttp
import httplib2, os

DOC_ID = "..."
md_path = Path("/tmp/source.md")
image_path = Path("/tmp/diagram.png")
creds = Credentials.from_authorized_user_file(
    os.path.expanduser("~/.hermes/google_token.json"),
    ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"],
)
http = AuthorizedHttp(creds, http=httplib2.Http(timeout=240))
drive = build("drive", "v3", http=http)
docs = build("docs", "v1", http=http)

media = MediaFileUpload(str(md_path), mimetype="text/markdown", resumable=True)
req = drive.files().update(fileId=DOC_ID, media_body=media, body={"name": "Doc title"})
while req.next_chunk(num_retries=5)[1] is None:
    pass

# Then find marker index, insert rendered image with docs_advanced.insert_image,
# remove marker, tighten code spacing, export PDF, and inspect contact sheets.
```

## Pitfalls

- `docs_api.py update --md` may populate content but can look like copied Markdown rather than a polished Google Doc, depending on source and converter path. For boss-facing docs, prefer Drive Markdown import plus post-polish.
- A structure-only pass can miss the exact defect the user notices: tables that are still raw Markdown text, duplicated front matter, over-styled inline code, or visually pushed content. For table-heavy docs, explicitly verify both the plain-text export (`|---|` absent) and a PDF contact sheet.
- Do not treat Markdown export syntax as the visual truth. Native Google Docs structures are intentionally converted back to Markdown in `--format md`; use raw structure, plain text, PDF, and contact sheets for final publication QA.
- Whole-doc Drive import usually creates native tables, but it does not guarantee good fit. Expect a second pass for landscape, margins, header styling, row padding, font size, and page-break placement.
- Raw Mermaid source in Google Docs is usually not acceptable for polished docs. Render and insert an image.
- Automated structure checks are necessary but not sufficient. Always export and visually inspect contact sheets for layout-sensitive docs.
- Whole-doc Drive import preserves the file ID but replaces body content. Use preview-first if the existing live doc contains manual polish, comments, special tabs, or carefully curated structure.
