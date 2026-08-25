# Agent Skills Survey Revision Patterns

Use this when revising an existing Agent Skills / internal enablement survey, especially for a brownbag or multi-session skills-sharing program.

## Recommended question-shape changes

- Usage-frequency windows should be short enough to guide immediate enablement planning. Prefer "past month" over "past 3 months" when the survey is feeding a near-term session or workshop.
- For quick intake, prefer count-based usage options over vague cadence labels. Use stems like "How many times have you used Agent Skills in the past month?" with options such as "Not yet", "1 time", "2-3 times", "4-10 times", and "More than 10 times". This is easier to interpret than "a few times / weekly / almost daily".
- For a <=5 minute brownbag intake form, avoid separate benefit and blocker questions unless the user explicitly asks for a diagnostic survey. They are often redundant with usage/use-case questions and make the form feel long.
- Do not use generic "What should we cover in the session?" wording when the goal is to adjust materials to the audience's current level. Use a probing understanding question instead. If the user wants softer wording, prefer "What do you want to understand better about Agent Skills? (select all that apply)" over negative/deficit phrasing like "Which part is least clear...". Options should cover what skills are, where skills can be used, finding existing skills, when repeated work should become a skill, making/requesting a simple skill, sharing/maintaining skills, and "I am not sure yet".
- Use plain wording for broad/internal audiences. Prefer "use Agent Skills" over "intentionally use Agent Skills" when the user says the form must be simple; reserve "intentionally" for diagnostic surveys where confusion with generic assistant behavior is a known risk.
- For single-select adoption-stage questions, make options mutually exclusive. Avoid overlapping choices like "I have used an existing Agent Skill" and "I have created or edited an Agent Skill" unless the question is multi-select. Prefer a ladder such as: "I have not heard of Agent Skills before", "I have heard of Agent Skills, but have not used them yet", "I have used Agent Skills, but have not created or edited one", "I have created or edited an Agent Skill", "I am not sure".
- For usage frequency, prefer count-based answer choices for intake interpretation: "Not yet", "1 time", "2-3 times", "4-10 times", "More than 10 times".
- For platform/context questions, group by interface rather than brand/vendor: web chat/browser app (e.g. Claude web), IDE/editor agent, CLI/terminal agent, AIP/GLChat, Other, Not yet. Put Claude Code, Codex CLI, OpenCode, Hermes CLI under one CLI/terminal bucket. Avoid vague org-container labels like "GDP Labs app" when the relevant interface is AIP/GLChat.
- Keep explicit non-user options in multi-select questions, such as "Not yet" or "I am not sure yet". Avoid longer phrases like "Not applicable" when the user asks for simple wording.
- If the survey is meant to learn how people have used skills so far, replace future-looking free text like "What repeated work should we turn into a skill?" with a historical custom-skill prompt such as "If you have created or edited a custom Agent Skill, what recurring work was it for?"
- The helper cannot verify all respondent identity settings. Before saying a form is anonymous/no-credential collection, check the Google Forms Settings UI for Collect email addresses, Limit to 1 response, and organization restriction/sign-in requirements.
- For role segmentation in Agent Skills brownbag/intake forms, do not collapse UI/UX Design and Data Developers into one option. Use separate single-select options such as `Engineering`, `Data Developer (DD)`, `Product / PM`, `UI/UX Design`, `Business / Operations`, and `Other`. If the audience includes both design and data roles, the combined `Design / DD` label is ambiguous and should be removed.

## Existing-form edit caveat

The current `gform.py add-questions` path is add-only. It does not rename, replace, reorder, or delete old questions. After adding revised versions to an existing form:

1. Run `python3 scripts/gform.py get FORM_ID` and inspect titles/types.
2. Check for stale originals such as older time-window questions or single-select benefit/blocker questions.
3. Tell the user plainly whether duplicates remain.
4. Do not claim a question was replaced unless the automation actually updated or deleted the original item.
5. If the form has zero responses and the old item structure is malformed or over-edited, create a clean replacement form and tell the user to use/share that URL. If replacing, verify the new form with `get`, hand off both edit and responder URLs, then trash or clearly label the superseded form so users do not keep sharing it. If they must preserve the old URL, call out that manual deletion/reordering in the Google Forms editor is required.
6. Do not claim browser/responder-page visual verification unless it actually succeeded. In restricted org forms, unauthenticated responder fetches can return 401, and containerized browser checks can fail on Chrome sandbox issues; API metadata verification is still useful but should be described as metadata/API verification only.

## Verification snippet

```bash
python3 scripts/gform.py get FORM_ID > /tmp/form_after.json
python3 - <<'PY'
import json
from pathlib import Path
f=json.loads(Path('/tmp/form_after.json').read_text())
for i,q in enumerate(f.get('questions', []), 1):
    print(i, q.get('type'), q.get('title'))
PY
```

Expected for the revised Agent Skills brownbag/intake pattern:
- usage frequency: `MULTIPLE_CHOICE`, stem says `past month`, and uses count-based options such as `Not yet`, `1 time`, `2-3 times`, `4-10 times`, `More than 10 times`
- platform/context: `CHECKBOX`, stem says `select all that apply`, and groups surfaces by interface rather than brand: web chat/browser app, IDE/editor agent, CLI/terminal agent, AIP/GLChat, Other, Not yet
- use cases: `CHECKBOX`, stem says `select all that apply`
- understanding probe: `CHECKBOX`, stem asks what the respondent wants to understand better, not generic "what should we cover"
