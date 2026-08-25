# Response-only reviewer access

## Use when
A reviewer must inspect Google Form submissions but must not alter questions, settings, publication, or collaborators.

## Access model
Google Forms collaboration is for editors. Do not equate a Drive `reader` role on the Form with response-review access. Use two separate permissions:

1. Give the reviewer `reader` on the Form itself, if they need to inspect the form structure.
2. Give the reviewer `reader` on a response-only Google Sheet. Do not grant Form `writer` merely so they can see responses.

## Safe sequence
1. Inventory each Form: title, edit file ID, responder URL, current reviewer role, and `linkedSheetId`.
2. Create or confirm a response destination.
   - Prefer the native linked response Sheet when the supported Form UI/App Script flow is available.
   - If no native destination is present, create a controlled read-only Sheet projection from the Forms Responses API. Include submitted time and one column per question; keep the operational mapping outside the repository if it contains response data or personal addresses.
3. Populate the Sheet before changing Form permissions.
4. Share the Sheet to the reviewer as Drive `reader`, then read back the exact role.
5. Downgrade the reviewer’s Form permission from `writer` to `reader`, then read back that role too.
6. If responses need to remain current, schedule a bounded sync that refreshes the Sheet from the Forms Responses API. Run it once immediately and verify success before reporting that it is live.

## Verification checklist
- Confirm the OAuth owner before any permission mutation.
- Confirm the Form title matches the intended asset, not just an ID.
- Verify Sheet `reader` and Form `reader` separately; permissions do not automatically synchronize.
- Report the response-sheet URL, not only the Form edit/responder URLs.
- Never print response contents, OAuth tokens, or refresh-token files while verifying.

## Pitfalls
- Downgrading an editor before a reviewer can open a response Sheet can lock them out of the information they need.
- A static CSV/export is not an ongoing response view. State its freshness explicitly, or create and verify a scheduled sync.
- Forms with no `linkedSheetId` need a response-destination decision; do not claim native response-sheet linkage exists without checking.
