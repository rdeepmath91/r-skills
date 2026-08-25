# Boss-facing reply/doc formatting with diagrams

Use this pattern when the user wants a polished Google Doc or reply draft that should feel clean, readable, and closer to a reference document than a raw technical note.

## When to use

- Reply drafts for leadership or cross-team stakeholders
- Short Google Docs that need to explain skills/layering/architecture clearly
- Edits where the user explicitly asks to simplify bullets, keep a code snippet, and replace a dense comparison block with a diagram

## Pattern

1. Simplify the bullets first.
   - Keep each bullet short.
   - Prefer direct, non-repetitive wording.
   - Remove nested explanation unless it adds real clarity.

2. Keep the code snippet if it proves the workflow.
   - Preserve the smallest useful example.
   - Avoid bloating the snippet with extra context.

3. Replace horizontal layering tables with a visual diagram when the reference doc uses diagrams.
   - If the reference doc is diagram-led, mirror that framing instead of forcing a table.
   - Insert the diagram as an actual image in the doc, not as a raw Markdown image path.
   - Size the image for a wide, readable layout before insertion.

4. Keep the local Markdown draft in sync with the live doc.
   - Treat the Markdown file as the source of truth during iteration.
   - Verify exports after promotion so the live doc and source still match.

5. Validate the final doc visually.
   - Export Markdown/HTML to confirm structure.
   - Check that the diagram is centered and that the closing text still reads naturally after the figure.

## Common pitfalls

- Leaving the old "horizontal layering view" text in place after switching to a diagram.
- Keeping overly long bullets that make the doc look heavier than the reference.
- Using a raw image reference instead of inserting the image into the Google Doc.
- Forgetting to verify the export after the live doc update.

## Good handoff shape

- One short intro paragraph
- 3–5 simple bullets
- One compact code block
- One diagram image
- One closing sentence
