# Weekly report PR pruning pattern

Use this when a live weekly report Google Doc needs stale test PR entries removed from a list section.

## What worked in the June 2026 session

- The report was already live as a Google Doc.
- The unwanted entries were in a single list section: `Accomplishments → Pull Requests`.
- The report needed the closed/merged test PRs removed, not annotated.
- The live doc was updated in place through the Docs API.

## Workflow

1. Read the live doc first.
2. Search for the unwanted PR numbers or titles.
3. Collect each matching paragraph's `startIndex` / `endIndex`.
4. Delete those ranges from **bottom to top** with `deleteContentRange`.
5. Re-read the doc and confirm the PR numbers no longer appear.

## Why bottom-to-top matters

Docs indices shift after each deletion. Removing the highest ranges first keeps earlier ranges stable and avoids accidental off-by-one deletions.

## Good fit

- removing closed test PRs from a weekly report
- deleting obsolete list items from a live doc
- pruning a section without reformatting the rest of the page

## Bad fit

- restructuring the whole report
- changing section headings
- bulk reflowing a template

## Verification

After deletion, do a second read/search for the removed identifiers. Do not trust the edit until the live doc no longer contains them.
