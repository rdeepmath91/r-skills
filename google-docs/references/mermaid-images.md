# Mermaid and Inline Images

## Rule
- Render Mermaid locally first.
- Do not rely on the Docs API to render Mermaid fences.

## Recommended sequence
1. Read the source Markdown and extract every ```mermaid block.
2. Record the paragraph or heading immediately before each block as the anchor.
3. Strip the Mermaid fences from the Markdown before Drive import.
4. Import the stripped Markdown into Google Docs.
5. Render each Mermaid block locally to PNG.
6. Read the doc structure once, locate the anchor paragraphs, and insert the images after those anchors.
7. Re-export the doc and confirm the images sit in the right place.
8. Do the import and insert steps in one foreground script or notebook cell so you can see success/failure immediately.

## Common mistakes
- Importing the original Markdown after already producing `content_no_mermaid`.
- Using `start_index=1` as a generic anchor instead of the end index of the real heading paragraph.
- Hiding the doc write behind `nohup` or a background shell process, which makes API failures invisible.
- Using a short search fragment (e.g. "Context") that matches multiple paragraphs. Use a longer unique substring from the heading, or read the doc structure first and pick the exact `endIndex`.

## Recommended command
- `npx --yes @mermaid-js/mermaid-cli@11.4.3 -i input.mmd -o output.png -p /tmp/pp.json`
- Use a `pp.json` containing `{"args": ["--no-sandbox"]}`.

## Insert the image
- Use `scripts/docs_advanced.py insert_image(doc_id, image_path, start_index=..., width_pts=..., height_pts=..., tab_id=...)`.
- Images/diagrams are center-aligned by default on insert.
- Insert after the paragraph or heading that introduces the diagram.
- Do not insert at the raw fence location.
- Prefer one structure read, then insert all images in reverse order so indices stay stable.
- If there are multiple Mermaid blocks, insert the last one first so earlier indices do not shift.
- Make the uploaded image public before inserting it; the Docs API is much more reliable when the thumbnail URI is readable.
- `width_pts` and `height_pts` are resize hints before upload, not a Docs API object-size flag.
- When the heading text is imported from Markdown, the `###` markers disappear. Match the plain text heading text in the doc structure instead.
- If the imported doc has no blank paragraph where the diagram should live, emit a unique placeholder paragraph during Markdown preprocessing, insert the image at the placeholder paragraph's `endIndex - 1`, then delete the placeholder text so the image remains in its own paragraph.
- Inserting at a heading end index directly often fails with `The insertion index must be inside the bounds of an existing paragraph`; always anchor to a real paragraph.
- After insertion, verify `inlineObjects` in the live Docs API response so you know the image really landed.
- If the doc is republished from Markdown and the Mermaid fences are still visible as text, that is expected until you explicitly render each block locally and insert the PNGs; the Docs API will not convert Mermaid fences into images for you.
- The reliable pattern is: import the stripped Markdown, render Mermaid blocks locally, insert the rendered PNGs after the matching heading/anchor paragraphs (or placeholder paragraphs), then re-read the live doc and confirm the inline image count matches the number of Mermaid blocks.

## Sizing
- Keep the image conservative so it fits within the page.
- Size diagrams based on both the remaining space in the current page and the diagram aspect ratio.
- Default to **500-560 pt** for the first wide overview diagram if it is sharing space with nearby text.
- Default to **440-500 pt** for the second runtime/boundary diagram so it does not push the surrounding prose down too hard.
- Use **600 pt only when the diagram is still readable and the page is landscape with enough surrounding whitespace**.
- For landscape docs with wide diagrams, use **650-700 pt** width.
- For tall diagrams, cap the width and let the aspect ratio reduce the height.
- If the next diagram would clearly spill into the next page, decide deliberately whether to shrink it, split it, or let it start on the next page with a short explanatory lead-in.
- If the diagram still feels huge, shrink it again instead of letting it float awkwardly through the text.
- Do not use one fixed width for every diagram; use per-diagram sizing based on aspect ratio.
- For the full fit/orientation decision rules, see `references/preview-validation.md`.

## Landscape orientation
Use portrait by default, then switch only the genuinely wide sections to landscape after the content and images are already in the document:
1. Import the doc in portrait first.
2. Insert images while the doc is still in portrait so you can inspect real anchor positions.
3. If a diagram or table is genuinely width-heavy, wrap the surrounding content in its own section and flip only that section to landscape.
4. Include the heading, the short lead-in explanation, the diagram or table, and the immediate interpretation text in the same landscape section when possible.
5. Use `docs_advanced.set_section_orientation(doc_id, start_index, end_index, landscape=True, tab_id=...)` or `set_section_orientation_auto(...)` for that selected range.
6. Keep medium-width diagrams in portrait and shrink them before reaching for another landscape section.
7. Use whole-document landscape only when the majority of the document is genuinely wide.
8. Render at higher scale: `-s 3` or `-s 4` in `mmdc` for crisp output.
9. Optionally pass `-w 2400` to `mmdc` to set a minimum output width.

## Higher resolution rendering
- Default mmdc scale is 1x. For Google Docs, use at least `-s 2`.
- For landscape or detailed diagrams, use `-s 3` with `-w 2400`.
- For sequence diagrams or diagrams with many labels, use `-s 4` and keep the inserted width modest rather than stretching a low-resolution render.
- Example: `npx --yes @mermaid-js/mermaid-cli@11.4.3 -i input.mmd -o output.png -p /tmp/pp.json -b white -s 3 -w 2400`
- Important: `docs_advanced.insert_image(..., width_pts=...)` currently resizes the image before upload to roughly `width_pts * 96 / 72` pixels. That can make diagrams look blurry in Google Docs. For high-detail figures, upload a full-resolution PNG and set the Docs `insertInlineImage.objectSize` display width/height instead of using `width_pts` as a resize hint. Keep the PNG below Google Docs image-size limits; 3000-4000 px wide is usually a good balance.

## Section sizing rule of thumb
- Prefer making a diagram smaller before creating another landscape section.
- For section-landscape pages, wide overview diagrams often work best around **540-600 pt** rather than maximum width.
- Smaller support diagrams often look better around **460-520 pt**, which leaves room for the heading and short explanation on the same page.
- If the landscape section still creates blank or orphan pages, shrink the image further or return that section to portrait.

## Dense ERD handling
- Do not replace a dense source ERD with a simplified "summary" diagram under a heading such as `Minimal ERD` unless the user explicitly wants a conceptual summary. A readable-looking summary can silently drop relationships and become misleading.
- First preserve exactness: extract the Mermaid `erDiagram` relationships and table definitions, then split the source into multiple thematic ERD panels such as identity/auth, runnable registry/versioning, scheduling, and execution/events.
- Before proposing a split ERD, compare each panel against the original relationship list. Note any FK-derived edges added for self-contained readability separately from source Mermaid edges.
- Generate a contact sheet of alternatives and let the user choose before replacing an existing Google Doc image. Do not mutate the live/preview doc just because one generated option looks better locally.
- If a panel remains too tall or dense after splitting, split again rather than shrinking it until unreadable. Execution/run-history panels often need their own figure separate from scheduling.
- Label the final doc honestly: use `Minimal ERD` for field-level relationship diagrams; use `Schema Summary` or `Relationship Map` for conceptual cards that omit detailed relationships.

## Mermaid source retention
- If a doc is still under active iteration, keep the Mermaid source in an appendix section as a fenced code block.
- Add a short line near the rendered diagram such as `Mermaid source: Appendix X` so future edits can find the source quickly.
- Do not rely on the rendered image as the only long-term editable source.

## Python environment
- `docs_advanced.insert_image` requires `Pillow` (`pip install Pillow`).
- Use a Python interpreter that has Pillow and the Google API dependencies installed.
- If those packages are missing, you will see `ModuleNotFoundError: No module named 'google.oauth2'` or `No module named 'PIL'`.
- For the full dependency matrix, use `references/setup-and-dependencies.md`.

## Verify
- Re-export the doc.
- Confirm the image is present and the surrounding paragraph flow still makes sense.
- If a full doc read times out, switch to the reliability notes and avoid repeated full export calls.

## Connector geometry QA (when orthogonal style is required)
- Validate connector geometry from rendered SVG, not from visual guesswork.
- Render the Mermaid source with Playwright and inspect `svg path.flowchart-link` segments.
- Fail the geometry check if any connector segment has both non-zero `dx` and non-zero `dy` (diagonal segment).
- Treat this as a `DOC7` readability/figure-quality gate when publishing to Google Docs.
- Arrowhead triangles can look tilted due to marker orientation; treat this as a style/polish concern unless the connector path itself is diagonal.
- If one-page portrait readability is requested, run fit math before insertion: `height_at_440pt = image_height_px * (440 / image_width_px)`.
- If `height_at_440pt` is far above `360pt`, fail `DOC7` for one-page portrait readability and redesign (`TD` -> `LR`) or split the diagram.

## Graphviz dot/PNG images

Some docs use `.dot` (Graphviz) files for presentation-grade block diagrams instead of Mermaid. The workflow is:

1. `dot -Tpng diagram.dot -o diagram.png` to render
2. Import the markdown (which references `assets/diagram.png`)
3. The PNG is referenced via `![...](assets/diagram.png)` in the markdown

For publishing to Google Docs, the PNG images in `assets/` need to be inserted as inline images after the image reference heading, similar to Mermaid.

### Graphviz text centering bug

Graphviz's HTML `ALIGN="CENTER"` on TD elements does NOT render correctly in SVG — all text gets `text-anchor="start"` regardless. To fix:

```python
import re, cairosvg
# Generate SVG from dot
subprocess.run(["dot", "-Tsvg", "diagram.dot", "-o", "diagram.svg"])
svg = Path("diagram.svg").read_text()

# Fix text centering: for each <text> with text-anchor="start",
# find nearest preceding <polygon> and center within it
lines = svg.split('\n')
last_poly_bounds = None
for i, line in enumerate(lines):
    poly_m = re.search(r'<polygon[^>]*points="([^"]*)"', line)
    if poly_m:
        pts = poly_m.group(1).strip().split()
        xs = [float(p.split(',')[0]) for p in pts]
        last_poly_bounds = (min(xs), max(xs))
    if 'text-anchor="start"' in line and '<text' in line and last_poly_bounds:
        mid_x = (last_poly_bounds[0] + last_poly_bounds[1]) / 2
        old_x = re.search(r'x="([^"]*)"', line)
        if old_x:
            lines[i] = line.replace(f'x="{old_x.group(1)}"', f'x="{mid_x:.2f}"')
            lines[i] = lines[i].replace('text-anchor="start"', 'text-anchor="middle"')

svg = '\n'.join(lines)
Path("diagram_centered.svg").write_text(svg)
cairosvg.svg2png(url="diagram_centered.svg", write_to="diagram.png", dpi=150)
```

Requires `cairosvg` (`pip install cairosvg`).
