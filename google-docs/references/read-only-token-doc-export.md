# Read-only token Google Doc export workaround

Use this when `scripts/docs_api.py export DOC_ID --format md|txt` fails during credential refresh with an error like:

```text
google.auth.exceptions.RefreshError: ('invalid_scope: Bad Request', ...)
```

## Why it happens

`docs_api.py` currently constructs credentials with the helper's default full write scopes:

- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/drive`

Some Hermes Google tokens are intentionally read-only and already sufficient for reading docs:

- `https://www.googleapis.com/auth/documents.readonly`
- `https://www.googleapis.com/auth/drive.readonly`

Other tokens may have a mixed, narrower grant such as `documents` plus `drive.file`. Preserve and use the stored scope list for the refresh probe rather than forcing the helper's broader `documents` + `drive` scopes.

`drive.file` has an important boundary: it can access files created by the app or explicitly opened with it, not every document shared with the same Google account. A `404 File not found` after a successful refresh commonly means the credential is valid but cannot see that particular Doc; it is not evidence that refresh failed. Try a separate token with `drive` or `drive.readonly` access before asking the user to share the Doc or provide an export.

Forcing broader scopes during refresh can make Google reject the refresh even though the token can read/export the requested document.

## Safe workaround for read-only review

For read-only document access, build credentials using the token's stored `scopes` value instead of overriding with write scopes, then use Drive export directly.

Minimal probe pattern:

```python
import io, json, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

DOC_ID = "..."
TOKEN = pathlib.Path.home() / ".hermes/google_token.json"
info = json.loads(TOKEN.read_text())
scopes = info.get("scopes") or [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]
creds = Credentials.from_authorized_user_info(info, scopes=scopes)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

drive = build("drive", "v3", credentials=creds, cache_discovery=False)
meta = drive.files().get(
    fileId=DOC_ID,
    fields="id,name,mimeType,modifiedTime,webViewLink",
).execute()

req = drive.files().export_media(fileId=DOC_ID, mimeType="text/plain")
buf = io.BytesIO()
dl = MediaIoBaseDownload(buf, req)
done = False
while not done:
    _, done = dl.next_chunk()
text = buf.getvalue().decode("utf-8", errors="replace")
print(meta)
print(text[:4000])
```

## Reporting guidance

- Report the document title, modified time, and export size as proof of access.
- Save the export to `/tmp` or another scratch path for local inspection.
- If the document contains exploit code, credentials, API keys, or vulnerability reproduction detail, summarize at a high level and avoid pasting weaponized content or secrets back into chat unless the user explicitly asks and it is safe to share.

## When not to use this

Do not use this workaround for edits or publication. Editing still requires an appropriately scoped write token and the normal preview/live-doc guardrails in the main Google Docs skill.
