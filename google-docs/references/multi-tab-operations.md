---
name: google-docs-multi-tab
description: Operations for multi-tab Google Docs — reading tab structure, listing comments via Drive API, and deleting ghost/experimental tabs.
---

# Multi-Tab Google Doc Operations

## Tab structure

The Docs API returns tabs with this structure:

```python
doc = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
for tab in doc.get("tabs", []):
    tab_id = tab["tabProperties"]["tabId"]       # e.g. "t.j21e5f2qnwz5"
    title  = tab["tabProperties"]["title"]        # e.g. "Architecture"
    index  = tab["tabProperties"]["index"]        # 0-based position
    content = tab["documentTab"]["body"]["content"]
    children = tab.get("childTabs", [])           # nested sub-tabs
```

Each tab's content uses the same element structure as a single-tab doc (`paragraph`, `textRun`, `paragraphStyle.namedStyleType`, etc.).

## Tab IDs in URLs

Tab-specific URLs use the tab ID as a query param:
```
https://docs.google.com/document/d/<DOC_ID>/edit?tab=<TAB_ID>
```

## Listing comments (Drive API)

Comments live on the Drive side, not the Docs side. Use `drive.comments().list()`:

Note: Drive comments are attached at file level. There is no native tab field in comment creation. Tab targeting must be inferred from quoted text and verified against target-tab content.

```python
from googleapiclient.discovery import build
drive = build("drive", "v3", credentials=creds)

results = drive.comments().list(
    fileId=DOC_ID,
    fields="comments(id,author,content,createdTime,modifiedTime,resolved,"
           "quotedFileContent,replies(id,author,content,createdTime))",
    pageSize=100
).execute()

for c in results.get("comments", []):
    resolved = c.get("resolved", False)
    author = c["author"]["displayName"]
    text = c["content"]
    replies = c.get("replies", [])
```

Fields to request:
- `resolved` — boolean, True if thread was resolved
- `quotedFileContent.value` — the text the commenter highlighted
- `replies[]` — all replies in the thread

## Renaming or moving a tab

Use `documents.batchUpdate` with `updateDocumentTabProperties`, not `updateDocumentTab`. The update request can rename a tab with `fields: "title"` and can reparent/reorder a tab with `fields: "parentTabId,index"`.

Some installed `google-api-python-client` discovery caches may not yet expose the newest tab request schemas. If the generated client rejects `updateDocumentTabProperties` even though live discovery includes it, call the REST endpoint directly with an authorized session:

```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

creds = Credentials.from_authorized_user_file(
    os.path.expanduser("~/.hermes/google_token.json"),
    ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"],
)
sess = AuthorizedSession(creds)
sess.post(
    f"https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate",
    json={"requests": [{
        "updateDocumentTabProperties": {
            "tabProperties": {"tabId": TAB_ID, "title": "Version 2.0"},
            "fields": "title",
        }
    }]},
).raise_for_status()
```

To move an older version under a `Legacy` parent tab:

```json
{
  "updateDocumentTabProperties": {
    "tabProperties": {"tabId": "<old_tab_id>", "parentTabId": "<legacy_tab_id>", "index": 0},
    "fields": "parentTabId,index"
  }
}
```

## Creating a new tab

Use `documents.batchUpdate` with the `addDocumentTab` request. Some installed `google-api-python-client` discovery caches may not expose the newest tab request schemas, so the REST endpoint via `AuthorizedSession` is the most reliable path:

```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

creds = Credentials.from_authorized_user_file(
    os.path.expanduser("~/.hermes/google_token.json"),
    ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"],
)
sess = AuthorizedSession(creds)
resp = sess.post(
    f"https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate",
    json={"requests": [{
        "addDocumentTab": {"tabProperties": {"title": "Suggestions - Option 2"}}
    }]},
)
resp.raise_for_status()
```

After creating the tab, re-read the document with `includeTabsContent=True` and find the new tab by title to get its `tabId`. Insert content into that tab with `insertText.endOfSegmentLocation.tabId`, then apply paragraph styles with ranges containing `tabId`.

Permission pitfall: comment-only access is not enough to add tabs or write tab content. The API returns `403 Forbidden ... Write access is required, comment-only access is not sufficient.` If edit access cannot be granted immediately, create a separate suggestion/preview Google Doc from Markdown and hand off its URL plus a local Markdown backup; do not imply the original doc was updated.

## Deleting a tab

Use `documents.batchUpdate` with the `deleteTab` request:

```python
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": [{"deleteTab": {"tabId": GHOST_TAB_ID}}]}
).execute()
```

This is useful for removing experimental or accidental tabs created during API testing.

## Comparing tab content against local markdown

1. Extract headings from each tab's `paragraphStyle.namedStyleType`
2. Extract headings from local `.md` files (lines starting with `#`)
3. Compare the heading sets to find structural drift

Style mapping (Docs → Markdown):
- `TITLE` → `# `
- `HEADING_1` → `## `
- `HEADING_2` → `### `
- `HEADING_3` → `#### `

## Preferred live-tab update pattern

Use this for shared multi-tab docs that already have stable reviewer URLs.

1. Refresh and approve the corresponding preview doc first.
2. Update only the changed live tab, not the whole parent document.
3. Preserve stable tab IDs / URLs for sibling tabs.
4. Re-run tab-local orientation and spacing post-passes after the content lands.
5. Verify the changed tab again with a tab-aware structure read.

This pattern is safer than republishing the entire parent document when only one tab changed.

## Field-mask caution

- `includeTabsContent=True` is required for tab-aware reads.
- Field masks for tab reads are brittle. If a narrow `fields=` selector errors on nested tab content, fall back to a broader tab-content read and filter locally.
- Do not mix `tabs(...)` selectors with legacy top-level `body/...` fields in one request.

## Orientation and section-break safety in tabs

- Apply multiple orientation ranges from bottom to top so earlier section breaks do not shift later indices.
- After tab-local orientation changes, scan the tab for empty heading paragraphs introduced at break boundaries and normalize them back to `NORMAL_TEXT`.
- If you see split words or headings after an orientation pass, treat that as a deterministic bug in the tab update process, not a cosmetic wrap issue.

## Auth

Token file: `<hermes-home>/google_token.json` (NOT at `~/.hermes/tokens/`).

The `google-workspace` venv has the required deps (`google-api-python-client`, `google-auth-httplib2`, etc.). Activate it before running:
```bash
source ~/.hermes/venvs/google-workspace/bin/activate
```
