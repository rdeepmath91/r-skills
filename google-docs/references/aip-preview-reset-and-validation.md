# AIP Preview Reset and Validation

Use this when a monthly AIP/DX preview copy has the right content but broken Google Docs formatting, or when you need to restart from a clean template without touching the live doc.

## What usually broke

Symptoms from the May 2026 AIP fill incident:

- Preview exported PDF expanded from the template's 4 pages to 7 pages.
- `Executive Summary` child headings such as `Issues` and `Monthly Achievements` became plain `NORMAL_TEXT`, disappeared from the document outline, or lost blue heading styling.
- Native nested lists became normal paragraphs with literal prefixes like `1.`, `2.`, `3.` and repeated list numbering.
- Many inserted paragraphs had large inherited spacing such as `spaceAbove: 10pt` or heading-like `spaceAbove: 26pt`, causing sparse pages.
- Links that should be styled text appeared as raw URLs.

Root cause: large section replacement inserted Markdown/plain text paragraphs and inferred lists, instead of preserving the template's Google Docs paragraph/list objects and spacing.

## Safe reset workflow

1. Do not edit the live/original doc.
2. Preserve the broken preview before overwriting it:
   - Drive API `files.copy(fileId=PREVIEW_ID, body={"name": "... broken preview backup before reset"})`.
   - Keep the backup link in the handoff in case filled text needs to be salvaged.
3. Export the restored/current live doc as DOCX:
   - Drive API `files.export(fileId=LIVE_ID, mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document")`.
4. Import that DOCX over the reusable preview doc ID:
   - Drive API `files.update(fileId=PREVIEW_ID, media_body=<docx upload>, body={"name": "... preview reset from live", "mimeType": "application/vnd.google-apps.document"})`.
   - This preserves the preview URL while making its content/format match the live template.
5. Re-fill from the clean preview using style-preserving edits, not whole-section paste.

## Validation checklist

After reset, compare live and preview before editing again:

- Export both docs to Markdown and verify equality if the preview should be an exact clone.
- Export both to PDF and compare page counts.
- Query Docs API paragraph structure and compare:
  - non-empty paragraph count;
  - `namedStyleType` counts;
  - heading texts/order;
  - bullet/list paragraph count;
  - paragraph signature including text, style, bullet presence, nesting level, `spaceAbove`, and `spaceBelow`.
- For layout-sensitive reports, generate PDF contact sheets and visually scan density/spacing before handoff.

## Handoff language

State plainly:

- live doc was not touched;
- preview was reset from live/template;
- broken preview was backed up with a link;
- validation metrics passed;
- any previously filled content is now only in the backup/local draft and must be re-applied carefully.
