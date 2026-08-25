# Reliability and Timeout Guidance

## The support path
When a docs workflow fails, follow this order:
1. Check auth.
2. Check the Drive file MIME type.
3. If the file is not `application/vnd.google-apps.document`, stop and fix the import step.
4. Keep the write path in one foreground script or notebook cell.
5. If you need a retry, rerun the same foreground script after a short backoff.
6. Only use a direct Google API client with a longer HTTP timeout for verification.

## Preferred execution pattern
- One script creates/imports the doc.
- The same script checks MIME type.
- The same script renders Mermaid.
- The same script inserts images.
- The same script prints the doc ID and the exact next verification step.
- Before editing an existing doc, verify the live title/content matches the intended target; do not rely on a remembered doc ID if the document may have been repurposed.
- If any step fails, stop and fix that step before starting another background job.

## What usually breaks
- Hiding writes behind `nohup` or a background shell process.
- Calling Docs API edits on a Drive Markdown file instead of a native Google Doc.
- Using a fake anchor like `start_index=1` instead of a real heading end index.
- Using whole-doc markdown refreshes for small wording fixes when a heading-scoped in-place edit would preserve the document shell and avoid expensive writes.
- Re-reading the full raw document repeatedly on a large doc.
- Running `docs_api.py update` on a large doc when you only need a content refresh; the clear-and-repopulate path can trigger Docs write quotas because it deletes paragraphs one by one. If you see 429s, stop and verify the document before retrying because the doc may already be partially rewritten. Prefer a single Drive `files.update(..., mimetype='text/markdown')` import, a targeted section update, or a single-batch `deleteContentRange` + `insertText` recovery if plain text is acceptable. For live docs, use whole-document replacement only after explicit live-promotion approval; otherwise apply it to the preview clone only. If non-resumable Drive upload times out, retry with `MediaFileUpload(..., resumable=True)` and a longer `httplib2.Http(timeout=240)` client.
- Treating Docs-side cleanup as free. Repeated per-paragraph delete/update passes can easily become the slowest part of the pipeline.
- Promoting preview docs into polished live docs with a whole-doc refresh when the user expected the live formatting shell, comments, TOC, and page numbers to survive.
- Calling a PDF page blank based only on extracted text; diagram/table pages often have low text and high visual occupancy.

## What is usually slow

In practice, the biggest time sinks are usually:

1. Drive markdown import/update
2. waiting for placeholder tokens to become visible in the imported doc structure
3. per-image Drive upload + permission change + Docs insert cycles
4. heavy post-passes that touch hundreds of paragraphs

Mermaid rendering is often *not* the bottleneck once the render command is stable.

## Speed guidance

- Prefer one Drive markdown import plus targeted post-passes over many small structural edits.
- For small live-doc edits, prefer heading-based section replacement over `docs_api.py update`, which clears and repopulates the whole document.
- Keep post-passes narrow:
  - headings
  - code-like paragraphs
  - doc-specific page-break headings
  - selected landscape ranges
- Avoid repeated full-doc `documents.get(... --raw)` loops when one targeted read will do.
- Use `docs_api.py headings` and `section-range` to anchor edits deterministically instead of relying on remembered indices.
- Insert images only once per refresh cycle; if image fit is wrong, fix source labels/layout before re-uploading many near-identical images.
- For high-image docs, expect the image upload/permission/insert loop to dominate runtime.
- If a cleanup step relies on `deleteContentRange`, prove it works on the exact kind of paragraph/range first; Docs commonly rejects ranges that include the segment-ending newline.

## Minimum checks before image insertion
- The imported file is a native Google Doc.
- The diagram PNG is public.
- The page is landscape if the diagram is wide.
- The insert runs in the same foreground process that created the anchor data.
- If there are multiple diagrams, insert the later one first.
- Match plain text headings in the doc structure; Markdown heading markers disappear during import.
- Verify success by reading `inlineObjects` from the Docs API, not by relying only on markdown export.

## Batch multi-doc creation
When creating several docs from a folder of Markdown files:
- Use `publish_pipeline.py /path/to/folder` for the initial import. It handles large files and retries better than ad-hoc Drive API calls.
- The pipeline generates titles from filenames: `"architecture.md"` becomes `"Architecture"` (filename.title() with hyphens/underscores replaced by spaces).
- If you want a different naming convention (e.g. "Product - Architecture"), search for existing docs first to avoid duplicates, or rename after creation with `drive.files().update(fileId=..., body={"name": new_title})`.
- Import the docs first, then insert Mermaid images in a second pass. Mixing import and image insertion in one script is fine but keep them as separate steps.
- If direct `MediaIoBaseUpload` times out on a large Markdown file (84KB+), the pipeline script typically succeeds where the one-off call fails.
- Check for existing docs by name before creating to avoid duplicates: `drive.files().list(q="name='TITLE' and mimeType='application/vnd.google-apps.document' and trashed=false")`.
- After pipeline import, insert Mermaid images as a separate step — the pipeline does not handle image insertion.

### Multi-doc preview creation under write quota pressure

When creating several preview docs with `docs_api.py create --md`, the helper may create the Google Doc and insert most content before failing during heading/list cleanup with a Docs API 429 write quota error. Do not assume the doc was lost.

Recovery pattern:
1. Read the traceback URL/error for the `documentId` that failed during `batchUpdate`.
2. Wait at least 60-70 seconds for the per-user write quota window to reset.
3. Verify the partially created doc with `docs_api.py headings DOC_ID`; if content exists, repair only the broken styling (for example remove a raw `# ` left in the title with `docs_advanced.replace_text`) instead of recreating the doc and producing duplicates.
4. Continue with the remaining docs after the backoff.
5. Insert diagrams/images in a separate second pass after all docs exist; verify with the Docs API `inlineObjectElement`/`inlineObjects` count.

This is especially useful for preview-first multi-doc refreshes where preserving the created preview links matters more than perfect atomic creation.

### Whole-doc update 429 / partial-rewrite recovery

If `docs_api.py update DOC_ID --md FILE` fails with a Docs API 429 during heading/list cleanup, the document may already contain the new body text but with raw or escaped Markdown artifacts. Avoid blindly rerunning the same update: it can compound formatting damage and hit quota again.

Recovery pattern:
1. Wait 60-70 seconds for the per-user write quota window to reset.
2. Export the doc as `txt` or `md` and inspect the first sections plus the rows/terms the user cares about.
3. If content is correct and only styling is degraded, either hand off with an explicit formatting caveat for low-polish internal docs, or do a single-batch cleanup.
4. For a reliable low-polish cleanup, convert Markdown to readable plain text locally, then run one Docs `batchUpdate` with:
   - `deleteContentRange` from index `1` to current body end minus one
   - `insertText` at index `1` with the cleaned plain text
5. Verify by exporting `txt` and grepping/checking title, key options, table headers, and any newly requested fields.

This loses native tables/headings but is useful when the user mainly needs searchable content/links quickly and the formatted import path is quota-bound.

## Verification fallback
If `docs_api.py get <doc_id> --md` times out:
- use a direct `docs.googleapis.com` client
- set `httplib2.Http(timeout=120)`
- fetch the smallest useful payload
- do not switch back to `--raw` loops

## Auth check expectation

`setup.py --check` should be treated as a write-readiness check, not only a token-presence check.

If it reports a scope mismatch, fix auth before starting a write workflow.

## Safer alternatives to expensive Docs-side cleanup

Prefer these, in order:

1. source-content simplification (shorter labels, less dense tables, tighter intro text)
2. config-driven `page_break_before` heading rules in the local refresh wrapper
3. bottom-up landscape range application
4. code-spacing normalization

Prefer **not** to rely on:

1. broad delete/reinsert paragraph cleanup
2. aggressive range deletion around blank lines or trailing paragraphs
3. repeated whole-doc repaints when a source or config tweak would solve the same issue more cheaply

## Live-doc pagination cleanup

When live pages look wrong, diagnose before editing:

1. Export the live doc to PDF.
2. Inspect both extracted text density and rendered-page visual occupancy.
3. Ignore expected sparse cover/title pages and visually full diagram/table pages.
4. For true blank/near-empty pages, inspect the Docs structure around the page boundary.

Common safe fixes:

1. clear accidental `pageBreakBefore=true` on inserted section paragraphs
2. clear excessive `keepWithNext` / `keepLinesTogether` on code-like blocks that strand a heading or intro line
3. remove an unnecessary forced page break before the next heading when it strands a single bullet/sentence
4. shrink the final required paragraph to 1pt / zero spacing if Docs refuses to delete it
5. delete adjacent blank paragraph + final section break together only after inspecting exact structural ranges

Common unsafe fixes:

1. deleting guessed ranges around tables, section breaks, or final newlines
2. trying to change `sectionType` with `updateSectionStyle`; the API can reject this field
3. running a whole-doc refresh only to fix pagination

## Drive markdown import timeout (408 / 500)

Some Markdown files fail to import via Drive `text/markdown` — the API returns 408 (Request Timeout) or 500 (Internal Error) even with long timeouts and resumable uploads. This is a Google Drive API issue with certain Markdown content structures.

## DOCX fallback when markdown import is flaky but formatting matters

If `text/markdown` import keeps returning 500 or timing out, and Docs API style-rebuild is rate-limited (429 write quota), use a DOCX conversion fallback:

1. Convert Markdown to DOCX with Pandoc and set the resource root so relative images resolve:
   - `pandoc /path/to/doc.md --resource-path /path/to/doc/folder -o /tmp/doc.docx`
2. Import the DOCX as a native Google Doc (`application/vnd.google-apps.document`).
3. Run a light post-pass for heading mapping if needed:
   - promote first heading to `TITLE`
   - shift `HEADING_2 -> HEADING_1`, `HEADING_3 -> HEADING_2`, etc. to match `# -> TITLE`, `## -> HEADING_1`.

Why this works:
- DOCX import usually preserves tables, links, and emphasis without many Docs write requests.
- It bypasses flaky markdown upload behavior and avoids heavy `docs_api.py update` clear/repopulate loops during quota pressure.

Caveat:
- If `--resource-path` is omitted, local images may be dropped during conversion/import.

**Symptoms:**
- `drive.files().update()` or `drive.files().create()` with `mimetype='text/markdown'` hangs indefinitely or returns 408/500
- Non-resumable upload returns 500 Internal Error
- Other Markdown files in the same session import fine
- The file size is reasonable (under 20KB)

**Workaround:**
Upload as `text/plain` instead of `text/markdown`. The content will be imported without Markdown formatting (no heading styles, no table rendering), but the text will be there.

```python
# Instead of:
media = MediaIoBaseUpload(io.BytesIO(content.encode("utf-8")), mimetype="text/markdown")
# Use:
media = MediaIoBaseUpload(io.BytesIO(content.encode("utf-8")), mimetype="text/plain")
```

**Trade-off:** You lose heading styles, table formatting, and code block styling. For docs that need proper formatting, consider using the Docs API `insertText` + manual styling as a fallback, or retry the markdown import later when the API is less flaky.

**When to suspect this:** If a Drive markdown import hangs for more than 60 seconds on a file under 50KB, switch to text/plain.

**Restoring formatting after plain text import:**

If you had to upload as `text/plain`, the doc will have raw markdown syntax (headings with `#`, bullets with `-`, bold with `**`, links with `[text](url)`). Apply formatting manually using the Docs API:

```python
import sys, re, time
sys.path.insert(0, "<skill-root>/scripts")
from docs_api import build_service, _apply_heading_styles, _apply_bullets

docs = build_service("docs", "v1")
DOC_ID = "..."

# 1. Apply heading styles (# -> HEADING_1, ## -> HEADING_2, etc.)
_apply_heading_styles(DOC_ID)

# 2. Apply bullet formatting (- -> bullets)
_apply_bullets(DOC_ID)

# 3. Apply bold for **text**
doc = docs.documents().get(documentId=DOC_ID).execute(num_retries=5)
for el in doc.get("body", {}).get("content", []):
    if "paragraph" not in el:
        continue
    for pe in el["paragraph"].get("elements", []):
        tr = pe.get("textRun", {})
        text = tr.get("content", "")
        start = pe.get("startIndex", 0)
        for m in re.finditer(r"\*\*(.+?)\*\*", text):
            bs = start + m.start()
            be = start + m.end()
            docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [{
                "updateTextStyle": {
                    "range": {"startIndex": bs, "endIndex": be},
                    "textStyle": {"bold": True}, "fields": "bold"
                }
            }]}).execute(num_retries=3)

# 4. Apply links for [text](url)
for el in doc.get("body", {}).get("content", []):
    if "paragraph" not in el:
        continue
    for pe in el["paragraph"].get("elements", []):
        tr = pe.get("textRun", {})
        text = tr.get("content", "")
        start = pe.get("startIndex", 0)
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
            url = m.group(2)
            if url.startswith("http"):
                ls = start + m.start(1) - 1
                le = start + m.end(1) + 1
                docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [{
                    "updateTextStyle": {
                        "range": {"startIndex": ls, "endIndex": le},
                        "textStyle": {"link": {"url": url}}, "fields": "link"
                    }
                }]}).execute(num_retries=3)
```

Note: this approach applies styles one at a time per paragraph element, which can be slow for large docs. For faster processing, batch all requests into a single `batchUpdate` call. Also, the link regex matching against individual textRun elements can fail if a link spans multiple textRun boundaries — in that case, match against the full paragraph text instead.

## Applying a target font to all text runs

`updateNamedStyle` (to change the document's default heading/paragraph font) does NOT work with the current Google Docs API — it returns 400 "Unknown name" errors. Instead, apply the target font directly to every text run.

Choose `FONT_FAMILY` from the target document or organization baseline. Do not hardcode GDP Labs typography such as Proxima Nova for non-GDP documents unless the user requests it.

```python
FONT_FAMILY = "Proxima Nova"  # Example only; choose from the target baseline.

doc = docs.documents().get(documentId=DOC_ID).execute(num_retries=3)
requests = []
for el in doc.get("body", {}).get("content", []):
    if "paragraph" not in el:
        continue
    for pe in el["paragraph"].get("elements", []):
        tr = pe.get("textRun", {})
        if not tr:
            continue
        start = pe.get("startIndex", 0)
        end = pe.get("endIndex", 0)
        if end > start:
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": {"weightedFontFamily": {"fontFamily": FONT_FAMILY}},
                    "fields": "weightedFontFamily"
                }
            })

# Apply in batches of 400 (API limit ~500 per batch)
for i in range(0, len(requests), 400):
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests[i:i+400]}).execute(num_retries=3)
```

## Rewriting cross-links to Google Docs URLs

When publishing Markdown to Google Docs, relative links like `[Architecture](architecture.md)` must be rewritten to live Google Docs URLs. `replaceAllText` does NOT work for links — it only replaces visible text, not the `link.url` field.

Instead, iterate text runs and update the link URL per element:

```python
LINK_MAP = {
    "architecture.md": "https://docs.google.com/document/d/ARCH_ID/edit",
    "design.md": "https://docs.google.com/document/d/DESIGN_ID/edit",
    # ...
}

doc = docs.documents().get(documentId=DOC_ID).execute(num_retries=3)
for el in doc.get("body", {}).get("content", []):
    if "paragraph" not in el:
        continue
    for pe in el["paragraph"].get("elements", []):
        tr = pe.get("textRun", {})
        ts = tr.get("textStyle", {})
        link = ts.get("link", {}).get("url", "")
        if not link:
            continue
        for md_file, gdoc_url in LINK_MAP.items():
            if md_file in link and "docs.google.com" not in link:
                anchor = ""
                if "#" in link:
                    anchor = "#" + link.split("#", 1)[1]
                new_url = gdoc_url + anchor
                docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [{
                    "updateTextStyle": {
                        "range": {"startIndex": pe["startIndex"], "endIndex": pe["endIndex"]},
                        "textStyle": {"link": {"url": new_url}},
                        "fields": "link"
                    }
                }]}).execute(num_retries=3)
```
