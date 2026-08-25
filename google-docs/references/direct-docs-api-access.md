# Direct Google Docs API access when Drive metadata is unavailable

Use this path for read-only review when a configured Google token has Docs access, but Drive metadata or export returns `404` for the same document.

## Read the document

Set `HERMES_HOME` to the directory that contains the working `google_token.json`, then call the Docs API helper directly:

```bash
DOC_ID="..."
GOOGLE_DOCS_HOME="/path/to/hermes-home-with-working-token"
HERMES_HOME="$GOOGLE_DOCS_HOME" \
  python /home/raymond-christopher/.hermes/skills/productivity/google-docs/scripts/docs_api.py \
  get "$DOC_ID" --md > /tmp/google-doc.md
```

Use the output file for local, targeted inspection. `headings` and `section-range` work through the same direct Docs API path:

```bash
HERMES_HOME="$GOOGLE_DOCS_HOME" python /home/raymond-christopher/.hermes/skills/productivity/google-docs/scripts/docs_api.py headings "$DOC_ID"
HERMES_HOME="$GOOGLE_DOCS_HOME" python /home/raymond-christopher/.hermes/skills/productivity/google-docs/scripts/docs_api.py section-range "$DOC_ID" --heading "Executive Summary"
```

## Interpretation and safety

- A Drive `files.get` `404` means “not found or inaccessible through that Drive request.” It does not prove that `documents.get` will fail for the same token.
- Prefer `get DOC_ID --md` for this case; do not use a failed Drive lookup as the access verdict.
- Keep token files out of terminal output, repositories, commits, and chat. Allow the helper to refresh credentials in place when required.
- This procedure proves read access only. Use the normal preview and approval workflow before any document edit.
