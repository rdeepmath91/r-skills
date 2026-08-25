# Restricted responder links and Forms OAuth

Session lesson: a Google Forms respondent URL (`/forms/d/e/1FAIpQL.../viewform` or `forms.gle/...`) is not the same identifier as the editable Form file ID used by `FormApp.openById()` or most Drive operations.

## Diagnostic pattern

When asked to inspect a respondent link:

1. Try the browser/public fetch first.
2. If it redirects to Google sign-in or returns HTTP 401, treat it as a restricted responder form, not as a public form.
3. Do not call `gform.py get` with the `1FAIpQL...` published ID and expect it to work. `gform.py get` needs the edit file ID from `https://docs.google.com/forms/d/FORM_FILE_ID/edit`.
4. Use Drive OAuth search to see whether the configured account can see a matching form, but do not assume a responder ID is searchable in Drive metadata/fullText.
5. If the user says “use our OAuth,” test explicitly:
   - direct HTTP fetch of the responder URL with `Authorization: Bearer TOKEN`
   - Forms API `forms.get` if the API and scopes are available

## Important distinction

Drive/Docs OAuth bearer tokens are API credentials. They do not make an unauthenticated browser session signed in to Google Forms, and Google’s web responder page may still return 401 or a sign-in page.

## Scope upgrade path

For Google Forms API read access, re-authorize with:

- `https://www.googleapis.com/auth/forms.body.readonly`
- `https://www.googleapis.com/auth/forms.responses.readonly` if responses are needed

Preserve existing scopes when generating the consent URL. Use `include_granted_scopes=true` and `prompt=consent`.

Even after re-auth, the OAuth project may need Forms API enabled. If `forms.googleapis.com` returns `403 SERVICE_DISABLED`, enable Google Forms API in the same Google Cloud project as the OAuth client.

## What still may be required

Forms API access generally still requires the configured account to have access to the form. If the only thing available is a restricted respondent link and Drive cannot find the backing file, ask for one of:

- the edit URL (`https://docs.google.com/forms/d/FORM_FILE_ID/edit`)
- sharing the form with the OAuth account
- pasted/exported question text

## Reporting language

Be precise: “OAuth is working, but this responder link is not accessible to the configured account / browser session” is better than “we don’t have Google Forms access.”
