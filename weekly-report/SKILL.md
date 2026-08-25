---
name: weekly-report
description: Auto-fill the report subject's weekly report from GitHub PRs, Google Chat bug metrics, and calendar. Creates Google Doc with proper formatting matching existing reports.
version: 1.1.2
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [weekly-report, github, google-docs, productivity, automation]
    related_skills: [google-docs, pr_summary]
---

# Weekly Report Generator

Generates <REPORT_SUBJECT>'s weekly report by pulling data from multiple sources and formatting it as a Google Doc matching existing reports.

Reference: `references/google-doc-weekly-report-fill-lessons-2026-05.md` captures recent lessons for preserving template structure, using prior-week performance baselines, simplifying Next Actions, and selecting agent-space technology items. For GL Sandbox daily updates sourced from `ai-agent-platform` and `glaip-sdk`, use `references/sandbox-daily-tracking-from-cross-repo-prs.md`: enforce a sandbox-only scope gate, inspect recent merged PR file paths in addition to keyword searches, use provider + owning-surface labels, and distinguish AWS infrastructure deployment from AIP Helm configuration that merely connects to it. Use `references/current-week-report-section-fill-lessons.md` when updating the current report after the shell already exists, especially for copying all AIP Current Issues from the latest tab, repairing heading bleed after Issues edits, Calendar reauth/fill, Out of Office, and pasted Key Metrics blocks. Use `references/deterministic-weekly-report-contract.md` whenever a run needs to distinguish deterministic rules from heuristic/editorial choices: style fingerprinting, numbered-list contracts, PR row normalization, inclusion audits, and postflight validation. Use `references/test-run-preview-copy-workflow.md` when the user wants a fresh TEST preview copy filled from sources with validation feedback loop; use `references/preview-generation-test-loop.md` for a generic other-agent test prompt. Use `references/pr-graphql-weekly-report.md` for the exact GraphQL query and filtering logic for PRs touched in the target week. Also see `references/live-weekly-report-fill-preferences.md` for live-doc validation expectations: prove edits landed in the live report, avoid duplicate model-release articles, keep metrics template-like, and keep Next Actions concise. Use `references/gdp-default-token-weekly-report-fill.md` when the user asks to use the GDP default token: if Drive search fails under `drive.file`, discover the current report from Gmail links, write directly through Docs API, replace only placeholders, repair Proxima Nova/body styling after links/bullets, and validate with export + PDF contact sheet. Use `references/live-weekly-report-restore-from-copy-format-repair.md` when the live report was restored to a blank/template state but filled content exists in a copy: transfer content back into the stable live doc while matching a previous report's heading/list convention, then validate bullets/headings/links. Use `references/weekly-report-cron-log-troubleshooting.md` when a scheduled weekly report run fails and you need to distinguish the report cron from the Gmail digest cron or investigate OAuth/token scope errors from the cron output. For finished GitHub task cleanup/tagging, use `references/github-project-weekly-task-tagging.md`: ProjectV2 `Sprint Name`/`Story Point` are often the source of truth, every finished task must carry the report subject/`raychrisgdp`, a specific sprint tag, and story points, and the final handoff must distinguish items that merely needed the report subject added as assignee.

## Data Sources

1. **Report discovery** — Gmail reminder if Gmail scope/tooling is available; otherwise Drive search for `[Weekly Report: <REPORT_SUBJECT>]` docs is usually enough to locate the current blank report and recent AI-filled references.
2. **Issues** — current issue tracker Google Doc/tab when the user provides one; for tabbed Docs, fetch with `includeTabsContent=true` and inspect `childTabs` because the top-level month tab may be empty.
3. **Accomplishments** — GitHub PRs via `gh api graphql` (authored + reviewed + commented, exclude Close-only entries).
4. **Finished GitHub tasks** — closed issues/tasks from the report window. For each finished task, verify the report subject's name/account is attached and capture the specific sprint tag plus story-point/review-effort value from labels or ProjectV2 fields. Surface missing sprint/point metadata as an audit gap.
5. **Meetings** — Google Calendar API (recurring meetings) or reuse from previous week only when the user explicitly approves fallback reuse.
5. **Key Metrics** — GLChat bug report from Google Chat, Pamela email, or a pasted block from the report subject.
6. **Readings / Technology-business section** — user input, recent session topics, or current-week GenAI/AI-agent news candidates. If the user says they will filter items, present candidates first; do not insert them until selected. Use `references/technology-section-candidate-sourcing.md` for the angle-rotation rule and official-source shortlist pattern.
   - A reply such as `choose all 4` to the scheduled handoff is an explicit selection when the target report and four candidates are unambiguous. Apply all listed candidates to that report immediately; do not ask the user to repeat the titles or reconfirm the target.
   - Before writing, re-read the Technology section. Replace only the exact placeholder or the exact previously presented candidate set; if unrelated content appeared since the handoff, stop rather than overwrite it. Insert one linked article title per native top-level numbered-list item, preserve the report's body style, and make the operation idempotent.
   - Read back the live Doc after insertion and verify: selected title order, one full-title link per item, a single native list group, `NORMAL_TEXT` body paragraphs, no visible raw URLs, no heading-style leaks, and the expected reduction in placeholder count.
7. **Previous report formatting baseline** — immediately previous report for the subject, used for native list styles, spacing, Proxima Nova styling, and section-specific conventions.

See `references/fill-existing-weekly-report-doc.md` for the tested workflow for filling an existing report doc from issue tabs, PR summary, Calendar, Out of Office edits, Technology/Business candidate sourcing, and previous-report formatting validation. If higher-level Docs scripts are too coarse for a live fill, use `references/manual-fill-raw-api-pattern.md` for the raw Docs/Drive API section-replacement pattern that preserves Proxima Nova styling, native headings/lists, PR-marker links, and partial-fill handoffs. For monthly Developer Experience / AIP reports, use `references/monthly-dx-aip-report.md`: work in a preview copy, preserve native Google Docs list formatting, summarize org/repo-level AIP outcomes instead of PR numbers, keep Achievements to implemented items, and use executive-readable team/product grouping. For recurring Saturday cron jobs, also use `references/scheduled-weekly-report-handoff.md` so the final Telegram update includes filled sections, validation results, and the report subject's confirmation/decision list. For test-run preview copies (fresh TEST copy/doc, fill, validate, repair preview only, revalidate), use `references/test-run-preview-copy-workflow.md` and `references/preview-generation-test-loop.md`. If a filled report's visual formatting is wrong, use `scripts/repair_weekly_report_format.py DOC_ID [TAB_ID]` only as a legacy/manual-numbering repair helper; its output is not a final reference-format PASS. **CRITICAL**: The repair script converts native Docs numbering to visible manual numbering (1., 2., 3...), but the deterministic contract and reference formatting prefer native `NUMBERED_DECIMAL_ALPHA_ROMAN` with proper section restarts and nesting. Do not report repair script PASS as final validation — always compare against reference/fingerprint for title, headings, list style, nesting, and PR/link conventions.

## Saturday Automation Workflow

Use this skill for the report subject's recurring Saturday weekly report run. The scheduled run should be autonomous but conservative: fill what can be grounded, preserve placeholders or explicit note lines for missing/ambiguous data, and report decisions needed from the report subject.

1. Compute the target week in `Asia/Jakarta`: Saturday 00:00 through Saturday 23:59, with report title `[Weekly Report: <REPORT_SUBJECT>] <start> - <end>`.
2. Locate the target report in Drive by exact title first, then by recent `[Weekly Report: <REPORT_SUBJECT>]` docs. If multiple candidates or same-title copies exist, choose the most recent owner/agent template only after exporting and checking content; include all candidate links in the handoff if ambiguous.
3. Locate the immediately previous filled report for the subject and export it before writing anything.
4. Fill sections in confidence order: Issues, Accomplishments/Pull Requests, finished GitHub tasks, Meetings, Key Metrics, Next Actions, Technology/Business, Out of Office.
5. For each section, record whether it was filled from observed data, left for the report subject, or needs confirmation.
6. For finished GitHub tasks, enforce the report subject's tagging audit before handoff: every completed/closed task should explicitly carry the report subject's name/account, a specific sprint tag, and a story-point or review-effort value. Check both issue labels and GitHub ProjectV2 fields when accessible; for GDP-ADMIN AI Agents use ProjectV2 `Sprint Name` and `Story Point` as the source of truth. If the user asks to "tag it properly," mutate the board fields, add `raychrisgdp` as assignee where needed, then verify by reading the item back before reporting.
7. In the finished-task handoff, list repo/issue, title, sprint tag, story point, status, and assignment note. Explicitly distinguish items that only needed the report subject added as assignee from items that still lack sprint/story/status metadata. Never imply assignment-only work if sprint/status/date/story were also set.
8. After writing, run the full previous-report validation checklist below and send the user a concise status with doc link, filled sections, remaining placeholders, and confirmation/decision items.

## Report Discovery Workflow

When the user asks to find this week's report and compare past AI-filled reports:

1. Check today's date/time first so the target weekly range is grounded.
2. Check Google auth scopes before attempting Gmail. If `~/.hermes/google_token.json` only has Docs/Drive scopes, do not claim Gmail was searched; say Gmail is unavailable and use Drive as fallback.
3. Search Drive for `name contains '<REPORT_SUBJECT>' and trashed=false` and `name contains 'Weekly Report' and trashed=false`. The current report is typically the latest `[Weekly Report: <REPORT_SUBJECT>] <Saturday> - <Saturday>` doc owned by `agent@gdplabs.id`.
4. Export candidate Google Docs as `text/plain` via Drive API to classify blank vs filled. Blank templates contain `(please insert here)` under each section and are safe to identify as not yet filled.
5. Also export the immediately previous filled report and build a section-by-section comparison: placeholder count, which sections are blank/filled, and a short preview per section. This is the quickest way to answer the user's "do you know how to fill based on what I told you and compared to previous report?" without editing anything.
6. Return the current report link plus 3-5 recent reference report links with a short fill-status summary. Do not create/edit the doc until the user explicitly asks to start filling.

When the user asks whether you know how to fill it, answer with a concise mapping rather than a plan: Issues → latest AIP Current Issues child tab for the report week; Accomplishments → Pull Requests from strict `pr_summary`; Meetings and Out of Office → Calendar; Key Metrics → pasted/available GLChat metrics; Next Actions → previous report baseline adapted to current issues/PR themes; Technology/Business → candidate URLs for approval before writing.

For Raymond-specific visual spacing, source issue tag/link updates, and security-issue grouping, use `references/weekly-report-visual-spacing-and-issue-tags.md`. For safe live weekly-report section replacement, especially copying all AIP Current Issues from the latest tab into `Issues` while preserving `Accomplishments` / `Pull Requests` heading styles, use `references/weekly-report-section-replacement-guardrails.md`. When Raymond asks whether AIP issues were already created for a previous weekly-report period, use `references/aip-weekly-issues-creation-audit.md`: export the prior report's Issues section, search both open/closed GitHub issues for the exact date window, verify referenced numbers because `#N` may resolve to a PR rather than an issue, and check native sub-issues for roadmap items. When Raymond asks to add/update AIP issue status in the tabbed `AIP Current Issues` Google Doc, use `references/aip-current-issues-tab-update.md`, `references/aip-current-issues-tab-update-pattern.md`, and `references/aip-weekly-status-reconciliation-and-native-lists.md`.

**Weekly AIP rollover and reconciliation:** before copying a prior-week tab, inspect its Docs API paragraph structure as well as its text. Resolve every carried tracker and every existing link target against live GitHub in the correct repository; do not guess a repo from a bare `#N`. Remove truly completed prior-week work instead of carrying a `[SOLVED]` history item. If a parent/roadmap tracker is still open after child PRs merge, retain it as `[WIP]` and state exactly what remains open. When an external operational tracker shows that core implementation is finished but its newest entry still has latency, verification, rollout, or monitoring work, use a scoped status such as `[OPERATIONAL — UNDER MONITORING]` and state both the completed core and remaining evidence. Every visible `OWNER/REPO#N` must link to that exact issue or PR URL.

**Raymond-specific AIP capacity wording:** frame the capacity issue as a fact about AIP ownership expanding because critical workloads now depend on it, including GLChat projects, Developer Experience, internal automations, and other production use cases. Do not add headcount targets, ownership-plan language, hiring/internal-transfer workflows, or onboarding plans unless Raymond explicitly requests them. It is acceptable to prioritize adding a senior engineer and explain the need through architecture, technical review, mentoring, incident response, release support, and long-term reliability. If Raymond asks to “mirror this” immediately after correcting one issue, update only that corrected issue in the weekly report by default; do not silently resync the entire source tab.

**List fidelity:** if the source tab uses native `NUMBERED_DECIMAL_ALPHA_ROMAN` lists, recreate the native list with matching top-level/child indents. Never type visible `1.` / `a.` prefixes into an otherwise native list, because it invalidates the mobile layout. Re-read the target child tab and assert: top-level titles are bold, child lines are normal, the title/child nesting matches the source, no manual number/letter prefixes remain, and all visible repository references have links.

Then read the tabbed document with `includeTabsContent=true`, target the exact child week by `tabId`, insert with `endOfSegmentLocation.tabId`, and read back the same tab after writing. If the report period is absent from the tab tree, use `references/aip-current-issues-month-rollover-tab-bootstrap.md` to create and verify the missing month parent and weekly child before populating it. If the Doc cannot be read/written because OAuth is revoked or browser access requires sign-in, do not stop at the auth blocker: use `references/gl-aip-weekly-update-from-github-when-doc-inaccessible.md` to produce a copy-paste-ready GL AIP update list from `ai-agent-platform` and `glaip-sdk` GitHub PR evidence, with grouped status themes, PR links, and a separately labeled weekend carry-in when the report window may start Saturday.

## Monthly Developer Experience / AIP Report Workflow

Use this when the user asks to fill a monthly Developer Experience (DX) report for AIP/GLAIR.

1. Never edit the live Google Doc first. Restore/verify the live template if needed, create or use a preview copy, and only edit the copy unless the user explicitly approves live edits.
2. Check prior monthly DX reports before drafting. Match their level of abstraction: Executive Summary should be top-level team/product outcomes, not a detailed PR dump.
3. Gather repo activity across the relevant repos, not only the report subject's contributions. Use GitHub data for grounding, but do not include PR numbers or long repo-specific implementation lists unless the user asks.
4. For AIP-focused reports, frame content as Developer Experience outcomes:
   - orchestration/workflow clarity (`/goal`, defaults, resume-state) only when clearly implemented/merged
   - long-running sessions/context compaction
   - observability/model usage/debugging only when clearly completed; roadmap telemetry/reporting belongs in Next Steps, not Achievements
   - streaming/final-response reliability
   - multimodal artifacts and structured UI/A2UI only when clearly implemented end-to-end; otherwise omit or soften
   - tools/MCP/filesystem/runtime contracts
   - CLI/TUI reliability
   - GL Runner / GL SDK foundations that improve AIP development
   - live/published documentation and onboarding updates; verify GitBook live pages from `gl-sdk:docs/gitbook-sync` and HTTP 200 browser-style curl before claiming them; do not count preview docs, source-only docs, or GitBook sync mechanics as executive achievements unless the user asks for doc-pipeline work
5. Keep copy-paste markdown concise. Prefer 1 Executive Summary bullet for GLAIR/AIP and 4-5 grouped achievements under the team section. Avoid deep nesting, PR references, and implementation detail.
6. When formatting a Google Doc, preserve the template's native headings/lists/spacing. Do not replace large sections with markdown/plain text if it will break list objects or paragraph spacing. If a preview gets corrupted, reset it from the live template and re-fill from there.
7. For existing weekly report Docs, prefer section-level replacements under stable headings. Keep headings intact, use native Docs bullets/numbering, preserve/restore Proxima Nova 11 pt body text, link PR/article titles instead of showing raw URLs, and validate via Docs API/export readback. See `references/weekly-report-fill-existing-doc-2026-05.md`.
8. Validate after changes by comparing live vs preview exports and Docs API structure: page count, heading list, paragraph styles, bullet counts, and excessive `spaceAbove/spaceBelow`.
9. For the Technology/Business section, rotate the angle week to week and keep **one item per angle**. Preferred buckets include model releases, coding agents, agent infrastructure/security, and enterprise agent deployments. Avoid multiple duplicate articles from the same angle; use official sources and present alternatives first when the user asks to choose.

Drive fallback commands using the cached OAuth token:

```bash
TOKEN=$(python3 -c "import json, pathlib; print(json.load(open(pathlib.Path.home()/'.hermes/google_token.json'))['token'])")
python3 - <<'PY'
import json, urllib.parse, urllib.request
from pathlib import Path
TOKEN=json.loads((Path.home()/'.hermes/google_token.json').read_text())['token']
q="name contains '<REPORT_SUBJECT>' and trashed=false"
params=urllib.parse.urlencode({'q':q,'pageSize':'20','fields':'files(id,name,mimeType,modifiedTime,createdTime,webViewLink,owners(displayName,emailAddress))','supportsAllDrives':'true','includeItemsFromAllDrives':'true'})
req=urllib.request.Request('https://www.googleapis.com/drive/v3/files?'+params, headers={'Authorization':'Bearer '+TOKEN})
print(urllib.request.urlopen(req, timeout=30).read().decode())
PY
```

## Calendar Section Workflow

When the user asks to draft the Meetings/Events/Training/Conferences section from their calendar and gives a reference weekly report doc:

1. Read both Google Docs first: target report for the week/date range and reference report for exact formatting.
2. Extract the target section range and the reference Meetings/Events/Training/Conferences section. The established format is a simple numbered list with prefixes like `[Weekly]` and `[Monthly]`; do not include date/time/duration unless the reference doc does.
3. Check Calendar auth before reading events. A Docs/Drive token is not enough; Calendar reads require Calendar scope and will otherwise return `Request had insufficient authentication scopes`.
4. If Calendar scope is missing or the separate Calendar token fails refresh, generate an OAuth URL for Calendar read access and pause for the user to paste the redirect URL. Save the result to `~/.hermes/google_calendar_token.json`, not the Docs/Drive token. Validate the OAuth `state`, exchange using the stored PKCE verifier, and verify `calendarList` before fetching events.
5. Do not fabricate events from memory or reuse stale prior-week meetings unless the user explicitly approves fallback reuse.
6. After fetching events, deduplicate by summary, exclude working-location / out-of-office / routine prep blocks from Meetings, label recurring items (`[Weekly]`, `[Biweekly]`, `[Monthly]`) from recurrence metadata, and write the numbered list in the same style as the previous report. Keep declined-but-scheduled events if matching Raymond's prior calendar-summary style.
7. Fill Out of Office separately from Calendar `eventType=outOfOffice`; if no sentinel paragraph follows that section, replace only the placeholder after the heading.

## Google Doc Format

- Title: match the reference report's title `namedStyleType` exactly. Recent accepted reports may use `TITLE`, while older notes mention `HEADING_1`; do not hard-code this from memory.
- Section headers: match the reference report's heading `namedStyleType` and bold/font treatment exactly. The stable top-level headings are Issues, Accomplishments, Meetings/Events/Training/Conferences, Key Metrics / OMTM, Next Actions, Technology/Business/Communication/Leadership, Management & Marketing, and Out of Office. Recent docs may also require `Pull Requests` as its own `HEADING_2` under Accomplishments; verify against the current/reference report instead of assuming it is body text.
- Body/list content must remain `NORMAL_TEXT`. After any section replacement, explicitly reset every inserted issue, PR, meeting, next-action, technology, OOO, and blank spacer paragraph to `NORMAL_TEXT`; do not let it inherit the preceding `HEADING_2` section style. Then read back the target and assert that the only `HEADING_2` paragraphs are the known section headings plus `Pull Requests`; a heading-count-only check misses inherited body-heading leaks. Blank paragraphs accidentally styled as `HEADING_2` are a common hidden formatting bug and must be demoted before handoff.
- GDP weekly reports use Proxima Nova in the live docs. When writing directly through the Docs API, explicitly apply Proxima Nova 11 pt to filled body/list text and Proxima Nova 16 pt to headings/subheadings; do not rely only on named styles, which may default to Arial.
- Numbered/list content must mirror the reference section-by-section. Do not default to bullet dots. If the sample shows native `1. / a. / i.` numbering, use Docs API `createParagraphBullets` with `bulletPreset: NUMBERED_DECIMAL_ALPHA_ROMAN`, create each section's list group separately so it restarts at `1.`, and export text/PDF to verify visible numbering. Use visible/manual numbering only when the reference itself uses manual text numbering.
- `Accomplishments` should include `Pull Requests` before the numbered PR entries. Match the reference/current doc: some reports use `Pull Requests` as a plain body line, while newer/current reports may expect it as an actual `HEADING_2`.
- Issue titles: `NORMAL_TEXT`, bold (e.g., `[WIP] Agent Skills adoption`)
- Issue body: `NORMAL_TEXT`, not bold
- PR entries: `NORMAL_TEXT`, not bold, format: `Role: title [#number](url)` or `Role: title #number` with only the final trailing `#number` text run linked to the PR URL. Normalize before inserting so no row contains duplicate visible PR/issue refs (`(#1555) #1556`, `fix #1365 ... #1449`, raw URL plus marker, etc.). Before inserting, run the strict `pr_summary` timestamp audit: each included PR must have a report-subject-authored event at/after the report cutoff; GitHub `updatedAt` alone is not enough.
- Meetings/Events/Training/Conferences: use the same numbered-list style as the reference report. If the immediately previous report uses native numbered lists, use raw Docs API `createParagraphBullets` with `bulletPreset: NUMBERED_DECIMAL_ALPHA_ROMAN` after inserting unnumbered lines; `NUMBERED_DECIMAL` is not a valid Docs API preset. Create each section's list group separately, then export text to confirm each section restarts at `1.` and no blank/caveat paragraphs were absorbed into numbering. When using `google-docs/scripts/docs_api.py replace-section`, pass `--no-simple-lists` only when the reference/current doc uses visible manual numbering; otherwise it can preserve text but drift from native prior-week formatting.
- Metrics headers (GLChat Weekly Report, Month-to-Date): `NORMAL_TEXT`, bold
- Metrics data: `NORMAL_TEXT`, not bold
- Next Actions: when the user asks what to follow up, inspect the immediately previous report's `Next Actions` first, then adapt only after checking current-week issues/PR themes. Do not invent a fresh plan without showing the previous baseline.

## PR Summary Format

```
Implement: title [#N](url)
Implement (WIP): title [#N](url)
Review & Implement: title [#N](url)
Review: title [#N](url)
```

Use `gh api graphql` (not `gh search prs`) for full data. See `pr_summary` skill for query details. If a user questions whether the PRs were actually touched this week, rerun the strict audit immediately and replace the doc section with the confirmed set rather than defending the initial count.

## Final Verification Before Handoff

After filling or changing the report:

1. Export the Doc as `text/plain` through Drive and count `(please insert here)` placeholders; expected final count is `0` only when every section has grounded content or an explicit "no entries found" line.
2. Spot-check changed sections in the export: issue nesting, PR count, meetings list, metrics block, Next Actions wording, Technology bullets/links, Out of Office, and tip removal.
3. Compare against the immediately previous report for the subject, not a generic template:
   - Export both docs as `text/plain`.
   - Read back Docs API structure for the target and previous sections.
   - Confirm title and section heading `namedStyleType`, bold, font family, and font size match the reference/fingerprint. Expected heading texts may include `Pull Requests` as a subheading; validate exact texts and styles, not just the count.
   - Confirm no body/list/blank paragraphs accidentally use a heading style; demote spacer/body paragraphs to `NORMAL_TEXT` before handoff.
   - Confirm body/list text uses Proxima Nova, 11 pt, line spacing 100.
   - Raymond's Technology/Business section uses native decimal numbering (`1.`, `2.`, ...), not bullet dots. Out of Office and Meetings also use native numbering; create each section's list group separately so numbering restarts at `1.`.
   - Confirm Key Metrics follows the previous report's blank-line rhythm and does not add indentation that the previous report did not use.
4. Verify links are attached to the intended text runs only:
   - PR links only on final trailing `#N` markers inside Accomplishments.
   - Technology article links on article-title text, with no raw URLs visible unless the previous report style explicitly requires raw URLs and the report subject did not ask for direct title links.
5. If Google Docs mobile/phone view appears blank while exports are filled, do not argue from export alone. Search Drive for same-title copies, compare doc IDs/owners/modified times, and ask the user to copy the link from the phone before editing another copy.
6. If Google Docs API text deletion fails with `range cannot include the newline character`, retry ending the delete range one index before the paragraph newline.
7. If the user reports that font formatting was ruined after a fill, first inspect Docs API paragraph `namedStyleType` values. Common failure modes are: inserted body paragraphs inheriting a heading style; blank spacer paragraphs inheriting a heading style; a section heading such as `Issues` being fake-styled as `NORMAL_TEXT` 16pt bold instead of the reference heading style; native/manual list conversion causing spacing/indent drift compared with the reference; and missing or mis-styling the `Pull Requests` line under `Accomplishments`. Repair by applying `NORMAL_TEXT` to all non-heading body/list/blank ranges, preserving title and heading styles from the reference/fingerprint, converting native lists to visible manual numbering only when the reference report uses that style, resetting body indents as needed, and revalidating against the reference/fingerprint. The packaged repair script `scripts/repair_weekly_report_format.py` is only a legacy/manual-numbering repair helper, not the final reference-format validator.
8. When comparing formatting, do not rely only on Drive text export. Read Docs API structure for paragraph styles, line spacing, spaceAbove/spaceBelow, bullets, indents, textStyle font family, font size, bold, and link runs; if the user provides a screenshot, use it to confirm visual spacing and heading placement before final handoff.
   - If the user asks for a formatting comparison against a specific reference weekly report, treat it as a read-only comparison unless he explicitly asks for edits. Compare target vs reference section-by-section: heading namedStyleType (`HEADING_1` vs `HEADING_2`/`TITLE`), body/list `spaceAbove` drift, native bullet/list counts, Proxima Nova/line-spacing/bold on Key Metrics, PR link count, Technology article link count, placeholder count, raw URL count, blank heading leaks, and unexpected headings. Report concrete mismatches and what is still missing before modifying the live doc.
   - Common post-fill drift: the live report may be fully filled but visually too spread out because inserted body/list paragraphs have `spaceAbove: 20` while the reference has no `spaceAbove`; Key Metrics may be compressed into combined lines and lose explicit Proxima Nova/bold/line-spacing; Technology/Business may be content-filled with internal topics but still missing the reference-style 5 linked external article bullets; Out of Office may need manual numbering (`1. None`) if the reference uses numbered text.
9. Prefer `curl --max-time` with the cached refreshed OAuth token for flaky Docs batchUpdate calls; Python Google clients/urllib may time out or the remote may close the connection on large batches. Retry in smaller chunks around 20 requests.
10. Final handoff must include:
   - target doc link and title
   - filled sections
   - sections intentionally left blank or filled with "no entries found"
   - exact confirmation/decision list for the report subject
   - validation summary: placeholder count, raw URL count, previous-report style comparison result

## Creating / Editing the Google Doc

Token pitfall from Jun 2026 recovery: `~/.hermes/google_token.json` may only have `documents.readonly` / `drive.readonly`, which is enough for discovery/export but not `replace-section`. Before live writes with `google-docs/scripts/docs_api.py`, verify scopes or copy a writable token into the helper location:

```bash
mkdir -p ~/.google-docs-skill
cp ~/.hermes/google_forms_token.json ~/.google-docs-skill/google_token.json
python3 ./hermes-skills/google-docs/scripts/docs_api.py headings DOC_ID
```

If `google_workspace_full_token.json` refreshes with `invalid_grant`, use `google_forms_token.json` when it has `https://www.googleapis.com/auth/documents` and `https://www.googleapis.com/auth/drive`.

Use `gmail_auth_v3.py` (or latest auth script) to get OAuth token with all scopes:
```bash
~/.hermes/venvs/google-workspace/bin/python3 ~/.hermes/scripts/gmail_auth_v3.py url
# User authorizes, then:
~/.hermes/venvs/google-workspace/bin/python3 ~/.hermes/scripts/gmail_auth_v3.py exchange <code>
```

Token at `~/.hermes/google_token.json`. Refresh with:
```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
creds = Credentials.from_authorized_user_info(data, data['scopes'])
creds.refresh(Request())
```

## Doc Creation (batch update approach)

1. Create doc: `POST https://docs.googleapis.com/v1/documents` with title
2. Insert full text as single block at index 1
3. Apply styles in batches of 30:
   - `updateParagraphStyle` with `namedStyleType` for HEADING_1/HEADING_2
   - `updateTextStyle` with `bold: true` for issue titles and metrics headers

**IMPORTANT**: Do NOT use individual delete+insert per section — this corrupts indices. Insert all at once, then style.

## Gmail Labels

- `[P0] GitHub Assigned` (Label_7) — applied to Pamela bug reminders and escalation emails
- Filter: `pamela-glair@gdplabs.id` + `[Reminder] Bug Issue` → Label_7
- Filter: `subject:[Escalation]` → Label_7

## Bug Metrics Source

GLChat bug report comes from:
- Google Chat: Bugle app in GLAIR General Space (private)
- Email: pamela-glair@gdplabs.id weekly summary
- Format: Internal/External bugs by P0/P1/P2, opened/closed counts

## Limitations

- Google Calendar API requires enabling in GCP project (the user's work project blocks this; personal GCP project in progress)
- If the broad `google-workspace` OAuth flow fails with `invalid_scope` or the main Docs/Drive token lacks Calendar scope, use a separate read-only Calendar token instead of overwriting the Docs token. Generate a PKCE URL for `https://www.googleapis.com/auth/calendar.readonly`, save the result separately (for example `~/.hermes/google_calendar_token.json`), then query events for the report week in `Asia/Jakarta`.
- Google Chat API same limitation
- Until APIs enabled, bug metrics come from screenshots or Pamela emails

## Token / OAuth troubleshooting (Jun 2026 update)

**Scope mismatch: `drive.file` vs `drive`** — The `google_token.json` often has `drive.file` scope only (files created by this app). It cannot see weekly reports owned by `agent@gdplabs.id` and cannot copy docs to a different owner. For Drive search across all files AND for copying the master/template doc to a TEST preview, the token needs full `https://www.googleapis.com/auth/drive` scope. If the main token only has `drive.file`, use `google_workspace_full_token.json` (which has full `drive` scope) or run the full OAuth flow.

If Drive metadata/copy returns 404 under `documents` + `drive.file` but `documents.get` succeeds for a Gmail-discovered doc ID, do not treat the report as inaccessible. Keep a local pre-edit Docs JSON backup, write through `documents.batchUpdate`, and export a QA PDF with bearer-authenticated `https://docs.google.com/document/d/{id}/export?format=pdf`. Read the live Doc back after writing and visually inspect the exported PDF.

**Expired/invalid refresh tokens** — Both `google_workspace_full_token.json` and `google_forms_token.json` may have refresh tokens that return `400 Bad Request` or `401 Unauthorized` on refresh. This happens when the user revoked access or the token expired beyond recovery.

**Recovery: run the full OAuth flow** — Use the PKCE script with all needed scopes:

```bash
~/.hermes/venvs/google-workspace/bin/python3 ~/.hermes/scripts/gmail_auth_v3.py url
# Visit the printed URL, authorize, copy the redirect URL (contains code=...)
~/.hermes/venvs/google-workspace/bin/python3 ~/.hermes/scripts/gmail_auth_v3.py exchange "<redirect_url_with_code>"
```

The script writes to `~/.hermes/google_token.json` with scopes: Gmail (readonly/modify/send/labels/settings), Documents, Drive, Calendar, Chat (spaces/messages readonly).

**If Calendar scope is missing** — generate a separate minimal Calendar token (`~/.hermes/google_calendar_token.json`) instead of overwriting the main Docs/Drive token:

```bash
# Copy and modify gmail_auth_v3.py SCOPES to only calendar.readonly, or use a one-off PKCE flow
```

**If Gmail/Chat scope is missing for metrics** — generate a separate metrics token (`~/.hermes/google_metrics_token.json`) with only `gmail.readonly`, `chat.spaces.readonly`, `chat.messages.readonly`. Keep PKCE pending state separate (`~/.hermes/google_metrics_oauth_pending.json`).

**Writable Docs token for live edits** — Before `replace-section` / `docs_api.py`, verify the token has `https://www.googleapis.com/auth/documents` and `https://www.googleapis.com/auth/drive` (not `drive.file`). If `google_token.json` lacks them, copy a writable token:

```bash
mkdir -p ~/.google-docs-skill
cp ~/.hermes/google_forms_token.json ~/.google-docs-skill/google_token.json
# (ensure google_forms_token.json was refreshed successfully)
python3 ./hermes-skills/google-docs/scripts/docs_api.py headings DOC_ID
```

**Quick token scope check**:

```bash
python3 -c "
import json
from pathlib import Path
data = json.loads((Path.home() / '.hermes/google_token.json').read_text())
print('Scopes:', data.get('scopes'))
print('Expiry:', data.get('expiry'))
"
```
