# Google Forms response export fallback via linked Google Sheet

Use this when `gform.py responses FORM_ID` times out repeatedly, the Apps Script web app returns an HTML error such as `Fungsi skrip tidak ditemukan: doGet`, or the response count is large enough that Apps Script export is unreliable.

## Trigger symptoms

- `python3 scripts/gform.py responses FORM_ID` fails with `Error: The read operation timed out`, even with a long timeout.
- `python3 scripts/gform.py list` or raw POST returns an HTML Apps Script error page instead of JSON.
- Direct POST redirect handling reaches an HTML `doGet` / script-function-not-found error.

## Fallback workflow

1. Use Drive search to find the response spreadsheet linked to the form. Search by form title and prefer a spreadsheet named like `<form title> (Responses)`.
2. Export the spreadsheet as CSV through Drive API, not the Forms helper.
3. Aggregate the CSV exactly like normal response data:
   - first row is question headers;
   - single-select answers count once;
   - checkbox answers may be comma-joined in one cell;
   - native inline `Other` values appear as free/custom labels in the same cell;
   - keep free-text response IDs/names/emails out of the final recap unless the user explicitly asks and privacy permits.

## Known-good Python pattern

```python
import pathlib, requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

sheet_id = "RESPONSE_SHEET_ID"
creds = Credentials.from_authorized_user_file(str(pathlib.Path.home() / ".hermes/google_token.json"))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
headers = {}
creds.before_request(Request(), "GET", "https://www.googleapis.com/drive/v3/files/x/export", headers)
url = f"https://www.googleapis.com/drive/v3/files/{sheet_id}/export?mimeType=text/csv"
r = requests.get(url, headers=headers, timeout=180)
r.raise_for_status()
open("/tmp/form_responses.csv", "wb").write(r.content)
```

Prefer `requests.get(..., timeout=180)` for the export path if `googleapiclient.files().export_media(...).execute()` times out through `httplib2`.

## Agent Skills quick-check example

For the Agent Skills quick-check form, the linked response sheet discovered through Drive was named `Agent Skills quick check (5 minutes) (Responses)`. Exporting it to CSV succeeded when the Apps Script helper timed out and returned Apps Script HTML. The CSV export produced the current large-N recap directly.
