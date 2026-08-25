# Live Google Doc accidental edit recovery

Use this when a live/shared Google Doc was edited when the safer workflow should have been a copy or preview.

## Immediate priorities

1. Stop making additional live edits.
2. Preserve evidence of the current state if needed by copying the damaged live doc to a clearly named backup.
3. Find the last clean Drive revision from before the accidental edit.
4. Restore the live doc from that clean revision while preserving the original document ID.
5. Create a separate working copy from the restored live doc and continue all draft/fill work there.
6. Trash accidental intermediate copies once the live doc and draft copy are verified.

## Revision inspection pattern

Use Drive revisions, not memory or assumptions. Export candidate revisions as Markdown/text and check for the accidental sentinel text and the expected original sentinel text.

Durable checks:
- Accidental sentinel: a distinctive phrase inserted by the bad edit.
- Clean sentinel: distinctive content known to exist before the bad edit.
- Original-placeholder sentinel: a placeholder that should still exist if the live template was restored.

Do not assume the immediately previous revision is clean. Google Docs may create multiple revisions after API edits, and the last pre-recovery-looking revision can still contain the accidental content.

## Restore pattern

1. Download the clean revision as DOCX using the revision `exportLinks` entry for `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
2. Replace the live doc content via Drive `files().update(fileId=<live_doc_id>, media_body=<clean_docx>, body={'name': <original_name>})`.
3. Export/read the live doc and verify:
   - accidental sentinel is absent
   - clean sentinel is present
   - expected placeholders/formatting survived
4. Only after that, copy the restored live doc to create the draft working copy.

## Pitfalls

- Do not restore from a revision just because it was modified by someone else or appears before the current timestamp; verify by exporting content.
- Do not create the draft copy from a still-damaged live doc.
- Do not report recovery complete until both live restoration and draft-copy fill are verified.
- If the user complained about live formatting damage, treat recovery as higher priority than continuing content work.
