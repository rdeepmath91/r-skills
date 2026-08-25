# Google Doc access-denial triage for read-only review

Use this when a user asks to read/review a Google Doc link and export/API access fails. The goal is to distinguish a private/unshared document from a local OAuth/setup problem without escalating scopes or asking for credentials unnecessarily.

## Minimal evidence sequence

1. Extract the document ID from the URL.
2. Try the normal helper export first:
   - `python <skill-root>/scripts/docs_api.py export DOC_ID --format md > /tmp/doc.md`
3. If helper export fails with `invalid_scope`, use `references/read-only-token-doc-export.md`: load the token with its stored scopes and call Drive export directly.
4. If Drive `files().get(fileId=DOC_ID, ...)` returns HTTP 404, treat it as `not found or no permission` for the authenticated Google account, not proof the document does not exist.
5. Probe public-link access separately without auth:
   - `https://docs.google.com/document/d/DOC_ID/export?format=txt`
   - `401 Unauthorized` or redirect to Google sign-in means the doc is not publicly readable.
6. Optional browser probe: navigating to the edit URL redirecting to Google sign-in is useful corroboration, but browser auth state is separate from API token auth.

## How to report

Report the probes as evidence, not speculation:

- Browser access redirects to Google sign-in.
- Public export returns `401 Unauthorized`.
- Drive API with the available token returns `404 File not found / permission`.
- Other stored tokens, if checked, are expired/revoked/invalid only as local auth context — do not over-focus on them if the read-only token already proves lack of document access.

Then give clear next actions:

1. Share the doc with the Google account Hermes is authenticated as.
2. Change sharing to "Anyone with the link can view" if appropriate.
3. Export/paste the content into the chat.

## Pitfalls

- Do not broaden scopes or switch to write-capable tokens just to read a document.
- Do not say the document is deleted based on a Drive 404; Google returns 404 for missing permission too.
- Do not frame expired secondary tokens as the primary blocker when the direct evidence is that the target doc is private/unshared.
- Keep exported content in `/tmp` and avoid pasting sensitive content unless the user explicitly asks and it is safe.