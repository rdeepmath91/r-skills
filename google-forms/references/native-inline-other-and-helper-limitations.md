# Native inline Other and Google Forms helper limitations

Session lesson: when preserving an existing Google Form URL and the user asks for `Other` respondents to specify details, native inline `Other: ____` is preferable to appending a separate paragraph question.

## What happened
- The helper could add an optional final paragraph question, but that was only a fallback.
- The user manually fixed the form using Google Forms' native inline `Other` option.
- `gform.py get` still showed only item index/type/title and could not reveal native `Other` metadata, choice labels, required flags, or option-level state.
- The fallback paragraph question became redundant and needed removal.

## Correct decision rule
1. Prefer native inline `Other: ____` for multiple-choice/checkbox questions when possible.
2. Use a separate optional paragraph question only as a clearly labeled fallback when native inline Other cannot be enabled through available tooling.
3. Do not claim helper output confirms native inline Other unless choice-level metadata is available.
4. If the fallback was added and the user later enables native inline Other, remove the fallback question if the tooling can delete items; otherwise tell the user exactly which question to delete manually.

## Tooling constraints observed
- `gform.py get` via the current Apps Script endpoint returns only:
  - `index`
  - `type`
  - `title`
- It does not expose:
  - choice labels
  - `isOther` / native Other state
  - required flags
  - section/page metadata
- Current helper supports add-only form mutation (`addQuestions`) and cannot delete the redundant fallback question unless the deployed Apps Script is enhanced.
- Be precise: Google Forms and Apps Script can delete questions; the limitation is the current helper/deployment, not the platform itself. See `helper-enhancement-delete-and-detailed-get.md` for a minimal `deleteQuestion` action.
- Direct Forms API access can fail when Forms API is disabled on the OAuth project (`SERVICE_DISABLED`) or when auth lacks Forms scopes.
- Enabling Forms API via `gcloud services enable forms.googleapis.com --project=<project>` may fail with `PERMISSION_DENIED`; do not assume it is available.

## Better future fix
Enhance the Apps Script web app and helper with:
- detailed `get` output for choice options and native Other state (`Choice.isOther` where available)
- item deletion by index/title with response-count guardrails
- item update paths for enabling native Other where Apps Script supports it

Until that exists, use the Forms UI for native Other and item deletion when preserving an existing URL matters.