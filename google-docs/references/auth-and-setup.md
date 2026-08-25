# Auth and Setup

## Overview

The google-docs skill uses OAuth2 to access your Google account.
You need two things:

1. **A Google Cloud project** with Docs API and Drive API enabled, plus an OAuth client ID.
2. **A token** obtained by running the auth flow on your machine.

Minimum access for the current scripts is a Google account that can access the target docs plus OAuth consent for both `documents` and `drive`. The skill intentionally asks for full Drive scope because it publishes Markdown through Drive import, exports PDFs, uploads images, renames/updates files, and works with existing shared docs. `drive.file` is a narrower Google scope, but it is not sufficient for the current general-purpose scripts unless the workflow is redesigned around app-created files only.

For Python packages, external CLIs, and workflow-specific minimum setup, start with `references/setup-and-dependencies.md`. This file covers OAuth only.

If you are working inside a repo that already carries Google OAuth tokens in its environment
(e.g. `GOOGLE_OAUTH_TOKEN_DOCS`, `GOOGLE_OAUTH_TOKEN_DRIVE`, or `GMAIL_OAUTH_TOKEN`),
check those before starting a new browser-based auth flow. In some workspaces the live
Docs token is already exported in `backend/.env`, which is enough to read or update docs via
the API directly.

## Quick check

```
python3 <skill-root>/scripts/setup.py --check
```

Use the workspace's configured Python environment when one exists. If system `python3` is externally managed or missing Google client libraries, do not install packages into the system interpreter just for a docs task; switch to the repo/skill virtualenv or create one for Google Workspace tooling.

- `AUTHENTICATED` or `AUTHENTICATED (refreshed)` → you are done, stop here
- `NOT_AUTHENTICATED` → no token yet, follow the full setup below
- `REFRESH_FAILED` → token expired and renewal failed, see Troubleshooting
- `TOKEN_CORRUPT` → token file is broken, run `--revoke` then re-auth

If you get `NOT_AUTHENTICATED` and have never set this up before, you need
to create OAuth credentials first. See Step 1 below.

---

## Step 0 — Do you already have a Google Cloud project?

Before creating anything, check what you already have.

**Personal Gmail account:**
You do not have an enterprise project. Create your own — skip to Step 1.

**Workspace (company) account:**

| Option | Pros | Cons |
|--------|------|------|
| Use your company's existing GCP project | Already exists, IT manages it | IT controls OAuth clients and scopes; you may need approval to create credentials; they can revoke your access anytime |
| Create your own personal GCP project | Full control, no approval bottleneck | Your org may block project creation by non-admins |

**Recommendation:** Create your own project even in an enterprise.
It isolates your credentials from the shared project and avoids approval gates.

**How to check if you can create projects:**
Go to https://console.cloud.google.com → look at the project dropdown (top bar).
If you see a **New Project** button, you can create one.
If it's greyed out or missing, your org restricts it — ask IT to either:
- Give you the `resourcemanager.projects.create` permission, or
- Create a project for you with Docs API + Drive API enabled and let you create an OAuth client ID in it

---

## Step 1 — Create a Google Cloud project (one-time)

Skip this if you already have a project with Docs and Drive APIs enabled.

1. Go to **https://console.cloud.google.com**
2. Click the project dropdown (top bar) → **New Project**
3. Name it anything (e.g. `hermes-gdocs`) → **Create**
4. Make sure the new project is selected in the dropdown

## Step 2 — Enable the APIs

1. In Cloud Console, go to **APIs & Services → Library**
2. Search **Google Docs API** → click it → **Enable**
3. Search **Google Drive API** → click it → **Enable**

## Step 3 — Configure the OAuth consent screen

1. Go to **APIs & Services → OAuth consent screen**
2. Choose **External** (unless you are in a Workspace org, then Internal is fine) → **Create**
3. Fill in:
   - App name: anything (e.g. `Hermes Docs`)
   - User support email: your email
   - Developer contact: your email
4. Click **Save and Continue**
5. On the **Scopes** step, click **Add or Remove Scopes** and add:
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/drive`
6. **Save and Continue** through the rest (skip test users for now)
7. On the summary page, note the warning about verification — for personal use you can ignore it

## Step 4 — Create OAuth client credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Application type: **Desktop app**
4. Name: anything (e.g. `hermes-desktop`)
5. Click **Create**
6. A dialog shows the client ID and secret. Click **Download JSON**
7. Save the file somewhere safe (e.g. `~/Downloads/client_secret_....json`)

The downloaded file looks like this:

```json
{
  "installed": {
    "client_id": "123456789-xxxxx.apps.googleusercontent.com",
    "client_secret": "GOCSPX-xxxxx",
    "redirect_uris": ["http://localhost"]
  }
}
```

## Step 5 — Store the client secret

```
python3 <skill-root>/scripts/setup.py --client-secret ~/Downloads/client_secret_XXXXX.json
```

This copies the file to `<hermes-home>/google_client_secret.json`.

## Step 6 — Run the auth flow

**6a. Get the auth URL:**

```
python3 <skill-root>/scripts/setup.py --auth-url
```

It prints a long URL. Copy it.

**6b. Visit the URL in your browser:**

- Sign in with the Google account you want to use for docs
- Grant the permissions (Docs + Drive access)
- After approving, the browser redirects to `http://localhost/?code=4/0AX4Xf...`

**6c. Copy the full redirect URL and exchange it for a token:**

```
python3 <skill-root>/scripts/setup.py --auth-code "http://localhost/?code=4/0AX4XfWhATEVER"
```

Or just paste the bare code:

```
python3 <skill-root>/scripts/setup.py --auth-code "4/0AX4XfWhATEVER"
```

It saves the token to `<hermes-home>/google_token.json`.

## Step 7 — Verify

```
python3 <skill-root>/scripts/setup.py --check
```

Should print `AUTHENTICATED`.

---

## Files involved

| File | What | Created by |
|------|------|-----------|
| `<hermes-home>/google_client_secret.json` | OAuth client ID + secret | You (step 4) then `setup.py --client-secret` (step 5) |
| `<hermes-home>/google_oauth_pending.json` | Temporary state for auth flow | `setup.py --auth-url` (step 6a) |
| `<hermes-home>/google_token.json` | Access + refresh token | `setup.py --auth-code` (step 6c) |

`google_oauth_pending.json` is deleted after a successful auth.
`google_token.json` auto-refreshes when the access token expires.

## Scopes

| Scope | What it grants |
|-------|---------------|
| `https://www.googleapis.com/auth/documents` | Read/write all Google Docs |
| `https://www.googleapis.com/auth/drive` | Read/write all Drive files (needed for import, search, image upload) |

If an organization will not approve the full Drive scope, the practical fallback is to ask an admin for an approved OAuth client or a service account/domain-delegated flow that grants the same effective capabilities for the target docs. Do not switch only the consent screen to `drive.file` and expect the existing scripts to keep working against arbitrary live docs.

## Troubleshooting

**`setup.py --check` says `NOT_AUTHENTICATED`**
You have not run the auth flow yet. Go to step 6.

**`setup.py --check` says `REFRESH_FAILED`**
Your token expired and can't refresh. Two recovery paths:

*Option A — Direct refresh (faster, preserves existing refresh token):*
If you already ran `--client-secret` previously, the client secret is in
`<hermes-home>/google_client_secret.json`. Refresh the token directly:
```python
import json, urllib.request, urllib.parse
from pathlib import Path

token = json.loads(Path.home().joinpath('.hermes/google_token.json').read_text())
secret = json.loads(Path.home().joinpath('.hermes/google_client_secret.json').read_text())

data = urllib.parse.urlencode({
    'client_id': secret['installed']['client_id'],
    'client_secret': secret['installed']['client_secret'],
    'refresh_token': token['refresh_token'],
    'grant_type': 'refresh_token',
}).encode()

resp = urllib.request.urlopen(
    urllib.request.Request('https://oauth2.googleapis.com/token', data=data),
    timeout=10
)
result = json.loads(resp.read().decode('utf-8'))
token['token'] = result['access_token']
import datetime
token['expiry'] = (datetime.datetime.utcnow() + datetime.timedelta(seconds=result['expires_in'])).isoformat() + 'Z'
Path.home().joinpath('.hermes/google_token.json').write_text(json.dumps(token, indent=2))
```

*Option B — Full revoke and re-auth:*
```
python3 setup.py --revoke
```
Then repeat steps 6-7.

**`setup.py --check` times out**
This can happen when the token is very stale. Run `--client-secret` first if
not already stored, then use the direct refresh script from Option A above.

**Browser says "This app isn't verified"**
For personal use, click **Advanced → Go to Hermes Docs (unsafe)** to bypass.
This only matters for apps published to the public — personal use is fine.

**Browser redirects to localhost but nothing happens**
The redirect goes to `http://localhost:1` which doesn't serve a page.
That's expected. Copy the full URL from the address bar and use it with `--auth-code`.

**`client_secret` format error**
Make sure you downloaded the JSON as **Desktop app** type, not Web application.
The file must have an `"installed"` key at the top level.

## Revoking access

```
python3 <skill-root>/scripts/setup.py --revoke
```

This deletes local files. To fully revoke from Google's side, go to
**https://myaccount.google.com/permissions** and remove the app.

## When to mention this to the user

- Only when auth is the blocker (setup.py --check fails).
- Otherwise, keep it implicit and continue with the doc task.
