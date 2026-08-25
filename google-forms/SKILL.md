---
name: google-forms
description: Create and manage Google Forms via Google Apps Script Web App.
tags: ["Google", "Forms", "Automation"]
version: 3.1.0
---

# Google Forms Skill

Create and manage Google Forms through a Google Apps Script Web App.

## What this skill uses
- Web-app flow only, no OAuth
- One env var: `GFORMS` (the deployed Web App URL)
- Python helper: `scripts/gform.py` (handles redirects, no shell pipes)

## Pre-flight check
Before using any command, run this:

```bash
python3 scripts/gform.py list
```

- If it returns JSON with forms → proceed with the user's request
- If it returns `GFORMS not set` → run the **From scratch setup** below
- If it returns an HTTP error or timeout → the web app URL may be wrong or not deployed as Anyone access
- If `scripts/gform.py` is missing in an older local checkout, use a tiny Python/urllib POST helper against `GFORMS` from `~/gform_automation/.env` instead of stopping. Do not print the `GFORMS` URL; load it from `.env`, POST JSON like `{"action":"get","formId":"..."}` or `{"action":"responses","formId":"..."}`, and summarize the returned JSON.

## From scratch setup
1. Open [script.new](https://script.new)
2. Paste the full contents of `~/gform_automation/scripts/appscript_code.gs`
3. Save the script
4. Deploy → New deployment → Web app
5. Set Execute as: Me
6. Set Who has access: Anyone
7. Copy the deployed Web App URL into `~/gform_automation/.env`

## Local config
Create `~/gform_automation/.env`:
```bash
cat > ~/gform_automation/.env <<'EOF'
GFORMS=https://script.google.com/macros/s/YOUR_WEBAPP_ID/exec
EOF
```

## Core workflow — Python helper (primary)

Use `scripts/gform.py` for all actions. It handles the redirect automatically and works in sandboxed environments where `curl | sed` piping is blocked.

### List forms
```bash
python3 scripts/gform.py list
```

### Get form
```bash
python3 scripts/gform.py get FORM_ID
```

### Create a form
```bash
python3 scripts/gform.py create --title "My Form" --description "Optional desc"
```

For forms with questions, use a JSON file:
```bash
cat > /tmp/questions.json <<'JSON'
[
  {"type": "text", "title": "Your name", "required": true},
  {"type": "paragraph", "title": "Your feedback", "required": true}
]
JSON
python3 scripts/gform.py create --title "Feedback Form" --questions /tmp/questions.json
```

### Add questions to existing form
```bash
python3 scripts/gform.py add-questions FORM_ID /tmp/questions.json
```

### Get responses
```bash
python3 scripts/gform.py responses FORM_ID
```

If response export times out, retry once with a longer timeout before giving up; Apps Script redirect/export can be slow even for modest response counts. If it still times out or returns an Apps Script HTML error page, fall back to the linked Google Sheets response export via Drive API. For summarizing survey results, aggregate single-select answers directly, flatten checkbox lists, and keep free-text answers separate. See `references/response-results-analysis.md` and `references/response-sheet-export-fallback.md`.

For one-time event feedback where the user asks for a full PDF, charts, executive summary, scores, and qualitative inputs, use `references/event-feedback-visual-reporting.md`: produce a visual HTML/SVG report, convert to PDF, and QA with a contact sheet before delivery.

### Raw JSON mode
```bash
python3 scripts/gform.py '{"action":"list"}'
```

## Core workflow — bash helper (fallback)

If Python is unavailable, define this bash function first:

```bash
gform() {
  resp=$(curl -s -i -X POST "$GFORMS" -H 'Content-Type: application/json' --data-binary "$1")
  loc=$(printf '%s' "$resp" | sed -n 's/^location: //Ip' | tr -d '\r')
  if [ -z "$loc" ]; then printf '%s' "$resp" | tail -c 500; else curl -s "$loc"; fi
}
```

Then: `gform '{"action":"list"}'`

**Warning:** Some sandbox environments block `curl ... | sed ...` piping. Use the Python helper instead when this happens.

## Markdown template
For a copy-paste starting point with every question type, see `references/form-markdown-template.md`. Write the form structure in markdown first, then convert to JSON for the payload.

## Session references
- Account binding + heading formatting pitfalls: `references/account-binding-and-formatting.md`
- Restricted responder links, `1FAIpQL...` vs edit file IDs, and Forms OAuth scope upgrade pitfalls: `references/restricted-responder-links-and-forms-oauth.md`
- Agent Skills survey wording + platform naming notes: `references/agent-skills-survey-platform-wording-notes.md`
- Agent Skills survey revision patterns: `references/agent-skills-survey-revision-patterns.md`
- Native inline Other vs fallback paragraph question + helper limitations: `references/native-inline-other-and-helper-limitations.md`
- Helper enhancement snippets for `deleteQuestion` and detailed option inspection: `references/helper-enhancement-delete-and-detailed-get.md`
- Response result aggregation and summary pattern: `references/response-results-analysis.md`
- Event feedback visual PDF reporting pattern: `references/event-feedback-visual-reporting.md`
- Response export fallback via linked Google Sheet: `references/response-sheet-export-fallback.md`
- Least-privilege reviewer access: response-only Sheets, permission downgrade order, and sync verification: `references/response-only-reviewer-access.md`
- One-time event feedback forms from participant rosters, including public-response/private-results access, `Other / Nama belum ada di list` identity handling, duplicate-draft recovery, and QR-slide responder-link verification: `references/one-time-event-feedback-forms.md`
- Agent Skills quick-check form recap context: `references/agent-skills-quick-check-recap-notes.md`
- Agents vs Pipelines survey review pattern: `references/agents-vs-pipelines-survey-review.md`
- One-time event feedback forms: participant dropdowns with Other fallback, public responder/private editor access, rating-mode pitfalls, and endpoint redeploy verification: `references/one-time-event-feedback-form-pattern.md`
- One-time gathering feedback form pattern: `references/one-time-gathering-feedback-forms.md`
- Final event form URL recovery and response-access triage: `references/event-form-url-and-results-recovery.md`

## Question patterns
Use generic, reusable patterns when building forms:

### Decision-mechanism surveys with multiple projects
When the goal is to understand how teams decide between architectures (for example agents vs deterministic pipelines), frame the form as `one response = one project/feature/decision`, not `one response = one person`. Tell respondents to submit multiple responses if they have multiple projects with different choices. Capture the project list with structured fields first (project, team, stage, architecture choice), then capture the decision mechanism with analyzable fields: conditions, factors that mattered, the single deciding factor, outcome rating, and whether they would choose the same architecture again. Use free text only after structured questions to preserve nuance without making analysis manual. See `references/agents-vs-pipelines-survey-review.md`.


### Fast diagnostic surveys (<=5 minutes)
When the user asks for a quick team diagnostic survey, default to:
- 5-7 questions total
- mostly single-select multiple choice
- one multi-select use-case question
- avoid long free-text unless explicitly requested
- explicit question type labeling in drafts (`single-select`, `multi-select`, `rating 1-5`, `free text`) so reviewers can quickly validate structure

Recommended flow for skill/adoption diagnostics:
1) role
2) familiarity/adoption stage statement (behavior-based, not abstract "do you understand?")
3) usage frequency window (prefer past month for near-term enablement planning; use longer windows only when trend/history matters)
4) platform/context where skills were used (multi-select)
5) use cases (multi-select)
6) for diagnostic surveys: benefits observed (multi-select with a non-user option)
7) for diagnostic surveys: blockers (multi-select; blockers often stack, so avoid forcing a single "biggest blocker" unless the user explicitly needs prioritization)

For <=5 minute brownbag/intake forms, simplify further: keep 5-7 questions total, avoid separate benefit + blocker questions, and use one plain understanding/usage probe instead of generic topic preference wording. Prefer a softer prompt like "What do you want to understand better about Agent Skills? (select all that apply)" over "Which part is least clear..." when the user wants less negative wording. Options should reveal whether the audience understands what skills are, where to use them, how to find existing skills, when repeated work should become a skill, how to make/request a skill, and how teams share/maintain skills. See `references/agent-skills-survey-revision-patterns.md`.

Wording guardrails for "skills" surveys:
- Use the phrase "intentionally used Agent Skills" only when users may confuse built-in assistant behavior with deliberate skill selection/installation. If the user asks for simple/non-difficult terms, use "used Agent Skills".
- For usage frequency in a near-term session intake, prefer count-based options over fuzzy cadence labels: `Not yet`, `1 time`, `2-3 times`, `4-10 times`, `More than 10 times`. This is easier to interpret than `a few times`, `weekly`, or `almost daily`.
- For platform/context questions, group by interface rather than vendor/brand: web chat/browser app (e.g. Claude web), IDE/editor agent, CLI/terminal agent (Claude Code/Codex CLI/OpenCode/Hermes CLI), AIP/GLChat, Other, Not yet. Avoid org-container labels like "GDP Labs app" when the actual interface is AIP/GLChat.
- Include PM/non-engineer surfaces when relevant; do not make the form feel CLI-only.
- For role questions in Agent Skills brownbag/intake forms, keep UI/UX Design and Data Developer (DD) as separate options when both audiences are relevant; avoid combined labels like `Design / DD`.
- Do not add generic catch-all org roles such as `Business / Operations` unless the user confirms that audience exists. Prefer the user's actual audience taxonomy plus `Other`. For Raymond's Agent Skills brownbag audience, do not include `Business / Operations` unless he explicitly asks for it.
- Include one explicit non-user option in platform/benefit/use-case questions, such as "Not yet" for simple intake forms or "I have not intentionally used Agent Skills yet" for diagnostic forms.
- If the goal is to learn actual historical usage, avoid future-looking prompts like "What repeated work should we turn into a skill?" Prefer "If you have created or edited a custom Agent Skill, what recurring work was it for?"
- For single-select adoption-stage questions, ensure options are mutually exclusive. Avoid overlapping choices like "I have used an existing Agent Skill" and "I have created or edited an Agent Skill"; use a ladder that separates heard-only, used-but-not-created, created/edited, and unsure.
- The current helper exposes form structure but not all Google Forms Settings. Do not claim a form collects or does not collect respondent identity unless verified in the Forms UI/settings. Tell the user to check Settings -> Responses for Collect email addresses, Limit to 1 response, and org restriction/sign-in settings.

- `text`: short free-text answer
- `paragraph`: longer free-text answer
- `multiple_choice`: one answer from a list
- `checkbox`: many answers from a list
- `dropdown`: one answer from a compact list
- `rating`: numeric rating from 1 to N
- `date`: date picker
- `time`: time picker
- `grid`: matrix-style question with rows and columns
- `email`: email field with validation

### Generic examples
```json
{"type":"text","title":"Your name","required":true}
```

```json
{"type":"multiple_choice","title":"Which option best fits?","required":true,"options":["Option A","Option B","Option C"]}
```

```json
{"type":"checkbox","title":"Select all that apply","required":false,"options":["Option A","Option B","Option C"]}
```

```json
{"type":"rating","title":"Rate this item","required":true,"scaleMax":10}
```

## Supported question types
| Type | Fields | Notes |
|------|--------|-------|
| `text` | `title`, `required` | Short answer |
| `paragraph` | `title`, `required` | Long answer |
| `multiple_choice` | `title`, `required`, `options[]` | Radio buttons |
| `checkbox` | `title`, `required`, `options[]` | Multi-select |
| `dropdown` | `title`, `required`, `options[]` | Dropdown list |
| `rating` | `title`, `required`, `scaleMax` | 1-N stars/hearts/thumbs |
| `date` | `title`, `required` | Date picker |
| `time` | `title`, `required` | Time picker |
| `grid` | `title`, `required`, `rows[]`, `cols[]` | Grid table |
| `email` | `title`, `required` | Email validation |

## Rating questions
Google Forms rating questions use `addRatingItem()`. They support 1-10 levels and three icon styles: STAR, HEART, THUMB_UP.

```json
{
  "type": "rating",
  "title": "Rate this section",
  "required": true,
  "scaleMax": 10,
  "ratingIcon": "STAR"
}
```

## Deploy checklist
After editing `scripts/appscript_code.gs`:
1. Save in Apps Script
2. Deploy → Manage deployments → Edit → New version → Deploy
3. Copy the new Web App URL into `~/gform_automation/.env` if it changed
4. If `Page Not Found` appears, verify access is still set to Anyone

## Ownership and account verification
- Forms created through this skill belong to the Google account behind the deployed Apps Script Web App (`GFORMS`), not necessarily the currently active browser profile.
- This web-app flow is account-bound by deployment and is not switched by local OAuth tokens used by other tools.
- To verify you are using the intended account before creating/editing:
  1) run `python3 scripts/gform.py list` and confirm you can see known forms from that account;
  2) open one returned `edit` URL and check the avatar/account in the top-right of Google Forms UI.
- If you need forms under a different account, redeploy Apps Script while logged into that account (`Execute as: Me`), then update `GFORMS` to the new `/exec` URL.
- If the form appears in `gform.py list` but cannot be read by separate Drive tokens, treat the web-app account as source of truth for ownership and verify in UI.
- Before handing off a public responder link, test the responder URL unauthenticated. A 401/sign-in page means the form is not public-ready even if creation succeeded.
- If a newly-created form returns a blank title in `get`/create response, treat it as a stale or mismatched Apps Script deployment. Redeploy the known-good script from the intended account before creating the final form; do not hand off the malformed form.

## Known pitfalls
1. Saving code does not update the web app; you must deploy a new version.
2. **All actions redirect** (302 + Location). In some environments `curl -L` will return JSON correctly, but `urllib`-based helpers can hang on POST→redirect→GET. If `gform.py` times out, run a direct `curl -sS -L -H 'Content-Type: application/json' -d '{"action":"list"}' "$GFORMS"` probe first to isolate endpoint health vs client behavior.
3. Use `addRatingItem()` for numbered 1-10 rating questions instead of `addScaleItem()`.
4. If a command times out, retry once after a short pause; avoid backgrounding the write path.
9. If create fails silently, check the raw response for errors. Do not blindly retry create or you will produce duplicate forms.
10. Multiline descriptions must contain real newline characters; avoid literal `\\n` text in payload strings or Forms will render backslash-n visibly.
11. `gform.py` uses custom command parsing; `--help` is not guaranteed to work like argparse defaults.
12. If forms are created with blank titles, treat it as a deployment-code mismatch (or payload contract drift) in the Apps Script endpoint. Run a title probe create (`{"action":"create","title":"Title probe"}`) and verify title via `get`. If blank persists, redeploy from known-good `appscript_code.gs` and retest before bulk form creation.
12a. If `{"type":"rating"}` returns `Unknown question type: rating`, or `{"type":"scale"}` creates/readbacks as `MULTIPLE_CHOICE`, the deployed Web App is stale even if the local `appscript_code.gs` supports rating/scale. Do not keep creating replacement forms through that endpoint. Redeploy the current Apps Script code, then rerun a one-question probe for `rating` and/or `scale` before creating the production form.
13. `add-questions` is add-only in the current helper. It does not replace stale versions of questions. After revising an existing form, run `get`, inspect all titles/types, and explicitly tell the user whether old single-select or old time-window questions still remain. If the existing form is malformed and has zero responses, prefer creating a clean replacement form rather than appending corrected questions to the broken one; otherwise duplicates will remain and the user must manually delete stale items. Do not say Google Forms questions cannot be deleted; say the current deployed helper lacks a delete action unless `deleteQuestion` has been added. See `references/helper-enhancement-delete-and-detailed-get.md`.
14. When the user asks whether a responder link is correct, verify against the live form's `responderUri` from `python3 scripts/gform.py get FORM_ID`; do not rely on unauthenticated public scraping, which may return 401 for private/org-restricted Google Forms even when the link is correct. If the user only provides a respondent URL (`forms.gle/...` or `/forms/d/e/1FAIpQL.../viewform`), remember that `1FAIpQL...` is a published responder ID, not the editable Form file ID. `gform.py get` requires the edit-file ID from `/forms/d/FORM_FILE_ID/edit`. If the responder page is restricted and Drive search cannot find the backing file, ask for the edit URL or for the form to be shared with the OAuth/Apps Script account. See `references/restricted-responder-links-and-forms-oauth.md`.
15. Current `gform.py get` / Apps Script `getForm` output only exposes item index, type, and title.
    - First run `python3 scripts/gform.py list` to confirm the configured Apps Script/OAuth account is working. Then try to match by comparing known forms' `responderUri` values, or by searching Drive/OAuth for the published ID/title if Drive credentials are available. If no match is visible, ask for the edit URL `/forms/d/FORM_FILE_ID/edit` or for the form to be shared with the configured account.
    - Do not conclude “Google Forms access is unavailable” just because browser access redirects to Google sign-in; distinguish public browser access, Apps Script account access, and Drive/OAuth file visibility.
15. Current `gform.py get` / Apps Script `getForm` output only exposes item index, type, and title. It does not expose choice labels, `isOther`, required flags, section metadata, or native inline Google Forms `Other: ____` state. If native Other matters, say this limitation explicitly and verify via the Forms UI or a Forms API/App Script enhancement that returns `Choice.isOther` / option metadata.
16. If the user asks for “Other” respondents to specify details while preserving the same form URL, prefer native inline `Other: ____` on the relevant multiple-choice/checkbox items. Use an appended optional paragraph question only as a clearly labeled fallback, such as `If you selected Other in any question above, please specify here.` Then re-run `get` and `responses` to confirm the same `responderUri`, new question count, and response count. Do not claim this is the native inline Google Forms `Other: ____` choice unless Forms API/App Script support for that setting has been verified. If the user manually adds native inline Other, check whether the fallback paragraph question is now redundant and should be removed manually or with a proper item-delete/update path.
17. Apps Script project source can be exported through Drive as `application/vnd.google-apps.script+json`, but updating Apps Script source through Drive requires the `drive.scripts` OAuth scope. A Docs/Drive token without `drive.scripts` can inspect/export but cannot patch/deploy the web app; do not promise helper-code changes unless that scope/deployment path is available.
18. Direct Forms API calls require Forms OAuth scopes and the Forms API enabled on the OAuth project. gcloud's default Cloud SDK token can return `ACCESS_TOKEN_SCOPE_INSUFFICIENT`; a Docs/Drive OAuth token can also fail with `SERVICE_DISABLED` if Forms API is not enabled. Do not claim you can rename/delete/update form items through Forms API until scoped auth and API enablement are verified.
19. When a responder link is restricted and redirects to Google sign-in, do not conclude the Forms skill is unusable. Try the configured OAuth token and distinguish three separate blockers: (a) browser login/cookie access to the public form, (b) Drive/FormApp access to the underlying editable form file ID, and (c) Google Forms API enablement/scopes. A `/forms/d/e/1FAIpQL.../viewform` ID is a published responder ID and may not work with `FormApp.openById` or Forms API calls that expect the editable file/form ID from `/forms/d/FORM_FILE_ID/edit`. If the user asks to add Google Forms scopes, re-consent with `forms.body` or `forms.body.readonly` plus `forms.responses.readonly`, preserve existing Drive/Docs scopes, then verify with a cheap Forms API call. If the result is `SERVICE_DISABLED`, ask the user to enable `forms.googleapis.com` for the OAuth client project before retrying; do not treat that as a missing scope.
20. When `gform.py responses FORM_ID` repeatedly times out or the Apps Script endpoint returns an HTML error such as `Fungsi skrip tidak ditemukan: doGet`, do not stop if the form has a linked response spreadsheet. Search Drive for a spreadsheet named like `<form title> (Responses)` and export it as CSV through Drive API. This can succeed even when Apps Script response export is unhealthy. See `references/response-sheet-export-fallback.md`.
