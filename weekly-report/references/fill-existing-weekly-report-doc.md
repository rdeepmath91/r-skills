# Fill an existing weekly report Google Doc

Use this when the user asks to fill the current weekly report from existing sources while preserving prior report formatting.

## Source order

1. Locate the target weekly report doc in Drive by exact title/date range. If running from a Saturday cron job, compute the date range in `Asia/Jakarta` first.
2. Locate and export the immediately previous filled report for the subject. Treat it as the formatting baseline, not just content inspiration.
3. Fill only sections with grounded data or explicit report-subject-provided content. For unavailable/ambiguous sections, leave the placeholder or write a clear `No ... found` line only when backed by an observable source such as Calendar.
4. Keep a running handoff list of sections that need the report subject's confirmation or decision.

## Automated Saturday run

For recurring Saturday 1 PM WIB runs:

1. Search Drive for the current report title and previous report title. If multiple matching current reports exist, compare doc IDs, owners, modified times, placeholder counts, and first-page text before choosing; report ambiguity instead of silently writing to multiple copies.
2. Fill confident sections autonomously:
   - Issues from the current AIP issue tab when accessible.
   - Pull Requests from strict `pr_summary` timestamp audit.
   - Meetings and Out of Office from Calendar when the calendar token has scope.
   - Key Metrics only from Pamela/Bugle/GLChat source or a pasted block; otherwise leave for confirmation.
   - Technology/Business only from current-week candidates if there is an established auto-selection rule; otherwise present candidates for the report subject's choice.
   - Next Actions from previous report baseline adapted to current issues/PRs.
3. Preserve placeholders for any section that cannot be grounded, unless the previous-report pattern uses an explicit `No ... found` line and the relevant source was checked.
4. After validation, send the user a short Telegram report with the doc link plus `Needs confirmation / decision` bullets.

## Issues section from a tabbed Google Doc

the report subject's issue source can be a multi-tab Google Doc such as "AIP Current Issues".

- Fetch with the Docs API using `includeTabsContent=true`.
- Top-level month tabs may have no body text; inspect `childTabs`.
- Use the latest/current child tab under the current month, e.g. `May 2026 -> Week 1 May 2026`.
- Preserve nested numbered-list structure from the source tab.
- When the user asks to copy from the latest issue tab, copy all top-level issues from that tab, not only the item currently discussed in chat.
- If the source tab mixes native Docs bullets with manual visible labels like `4.` / `a.` / `b.`, parse those labels into nesting levels and recreate native `NUMBERED_DECIMAL_ALPHA_ROMAN` bullets in the weekly report.
- Preserve bold on top-level issue titles.
- Carry source wording through, but fix obvious typos only when safe, e.g. `GPD Labs` -> `GDP Labs`.
- After replacing `Issues`, verify `Accomplishments` is still a section heading parallel to `Issues` and `Pull Requests` is still the subsection heading. See `references/weekly-report-section-replacement-guardrails.md`.

## Meetings section from Calendar

- Use the separate calendar token if the main Workspace token lacks Calendar scope: `~/.hermes/google_calendar_token.json`.
- If the token fails refresh or was created with a stale client secret, regenerate a separate read-only Calendar OAuth flow instead of modifying the Docs/Drive token. Validate OAuth `state`, exchange with the stored PKCE verifier, save the token to `google_calendar_token.json`, and verify `calendarList` before fetching events.
- Query the primary work calendar for the report week in `Asia/Jakarta`, using an inclusive week start and exclusive next-week start.
- Exclude `workingLocation`, `outOfOffice`, and routine prep blocks such as `Daily Prep` from Meetings. Fill `outOfOffice` events in the dedicated Out of Office section.
- Deduplicate by event summary.
- Label recurring meetings based on recurrence metadata:
  - `[Weekly]` for recurring weekly-looking events.
  - `[Biweekly]` for summaries containing `biweekly` / `bi-weekly` or recurrence indicating biweekly cadence.
  - `[Monthly]` for monthly recurrence metadata or monthly-looking summaries.
- Keep scheduled calendar meetings/events even when the invite response is declined if matching Raymond's prior weekly-report calendar-summary style; do not recast the section as attendance proof unless the user asks.
- Keep the previous report's simple numbered-line format; do not include date/time/duration unless the reference report does.

## Out of Office from Calendar

- Fill from `eventType=outOfOffice` Calendar events.
- Preserve hourly and multi-day leave in readable prose, e.g. `Monday June 29th, 18:30–19:30 WIB — hourly leave`.
- If there is no sentinel/guide paragraph after `Out of Office`, replace only the placeholder paragraph after the heading rather than relying on an end-heading search.

## Accomplishments / Pull Requests

- Add a `Pull Requests` subsection under Accomplishments.
- Populate it from the `pr_summary` workflow for `raychrisgdp`, using the report week cutoff.
- Before writing or defending the PR list, run the strict per-event audit from `pr_summary`: authored PRs must be created at/after cutoff; reviewed/commented PRs must contain a report-subject-authored review/comment event at/after cutoff; closure-only comments do not count.
- Do not rely on PR `updatedAt` as evidence that the report subject touched it this week. GitHub search candidates can be updated by other users/bots after the report subject's older activity.
- Keep a single continuous numbered list sorted by the report subject's last qualifying activity timestamp.
- Format entries as `Role[(WIP)]: title #number`, with `#number` linked to the PR URL when writing via Docs API.
- Link PR numbers only inside the Accomplishments section and only on the final trailing `#number` marker per PR paragraph; never scan/link all `#N` in the document because numbered lists in Issues/Meetings/Next Actions can be corrupted.
- If a later audit finds false positives already inserted into the weekly report, tell the user which entries are questionable and offer to replace the section with the strict list.

## Formatting details

Previous reports use Google Docs native styles with Proxima Nova applied by explicit text style, not only named styles.

- Main title: keep existing `HEADING_1`.
- Section headings: `HEADING_2`, bold, Proxima Nova, 16 pt.
- Subsection headings such as `Pull Requests`: `HEADING_2`, Proxima Nova, 16 pt; match previous report boldness (often not bold for subsection headings).
- Body/list text: `NORMAL_TEXT`, Proxima Nova, 11 pt, line spacing 100.
- Issue top-level titles: bold.
- Issue children and PR/meeting list bodies: not bold.
- Prefer Docs API `createParagraphBullets` for native numbered lists. Verify with Drive text export after writing.
- When the user says the mobile/phone view still looks blank, treat it as a verification problem rather than insisting the export is right. Search Drive for same-title copies, compare doc IDs/links, check owner and modified time, export the exact requested doc, and ask the user to copy the link from the phone if the screenshot may be a different same-title doc. Google Docs mobile cache can be stale, but same-title weekly reports are common enough to rule out first.
- When the user asks to match the previous weekly report's formatting, compare against the immediately previous report for the subject using both plain-text export and Docs API structure/style readback. Mirror native list choices, not only visible text: recent Technology/Business sections use native bullets; Out of Office uses native numbering; Key Metrics uses plain paragraphs with the previous report's blank-line rhythm and no extra indentation before P0/P1/P2 lines.

## Key Metrics / OMTM

When the user provides a GLChat weekly metrics block, paste it into `Key Metrics / OMTM` using the previous report's plain-text structure rather than inventing a new summary format. If Raymond loosely says "for accomplishments" but the pasted content is clearly a metrics/OMTM block (`📊 GLChat Weekly Report`, bug counts, performance report, GL AIP report), place it in `Key Metrics / OMTM`, not under `Accomplishments`.

If the current Docs/Drive token lacks Gmail or Chat scopes, do not overwrite or narrow the working Docs token just to fetch metrics. Generate a separate minimal metrics OAuth token instead, e.g. `~/.hermes/google_metrics_token.json`, with only `gmail.readonly`, `chat.spaces.readonly`, and `chat.messages.readonly` as needed. Save any PKCE pending state separately, e.g. `~/.hermes/google_metrics_oauth_pending.json`, so a failed/expired re-auth cannot break Docs/Drive editing. If the report subject does not re-auth, leave the metrics placeholder and ask for the Pamela/Bugle/GLChat block to paste.

- Keep the supplied headings and values exactly unless the user asks for cleanup.
- Match the previous report structure: `📊 GLChat Weekly Report`, Month-to-Date, bug report subsections, performance report, and GL AIP report.
- Use `NORMAL_TEXT`, Proxima Nova 11 pt, line spacing 100 for the whole metrics block.
- Bold only the metrics headings/subheadings, e.g. `📊 GLChat Weekly Report`, `Month-to-Date (...)`, `🐛 Weekly Bug Report`, `Bugs from Internal Report`, `Bugs from External Report`, `⏱️ Performance Report`, model/concurrency lines, `🏃 GL AIP Report`.
- Be careful with line breaks when using `replace-section` / `insertText`: blank lines in the source text can expand into visually excessive spacing in Drive text export because each paragraph break is preserved. For compact weekly-report metrics, prefer no blank-only lines between headings/subsections unless the reference report visibly requires them; verify by Drive text export before handoff.

## Technology / business reading candidates

When the user asks for recent items for `Technology, Business, Communication, Leadership, Management & Marketing` and says they will filter them:

- Do not write directly to the report yet. Present a candidate list first with bullet/numbered items and URLs.
- Prefer current-week items matching the report week/date range.
- If the user asks for OpenAI/Anthropic additions, run targeted Google News RSS queries such as `OpenAI AI agents May 2026 when:7d`, `Anthropic AI agents May 2026 when:7d`, and `OpenAI Anthropic financial agents May 2026`; filter for OpenAI, Anthropic, ChatGPT, Claude, Codex, agents, enterprise services, or finance agents.
- If `web_search` fails, Google News RSS is a reliable fallback:

```python
import urllib.request, urllib.parse, xml.etree.ElementTree as ET
queries = ['AI agents generative AI when:7d', 'agentic AI May 2026', 'generative AI agents enterprise']
for q in queries:
    url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({
        'q': q, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'
    })
    data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
    root = ET.fromstring(data)
    for item in root.findall('.//item'):
        print(item.findtext('title'), item.findtext('link'), item.findtext('pubDate'))
```

- Include source names and dates when available. Google News RSS URLs are acceptable as a fallback when canonical article URLs are not easily recoverable.
- When writing selected items into the Google Doc, link the article title text directly and do not leave standalone URLs visible in the body. Verify via Docs API readback that each selected title has a `link.url`, and via Drive text export that raw URLs are not visible.
- If the user asks for “anything related to OpenAI or Gemini,” add 1-2 current-week OpenAI/Gemini-relevant candidates to the chosen list, still keeping the section short and report-ready.
- If the user asks for Sonnet/Fable or multiple variants from the same vendor, merge them into one report bullet unless they represent genuinely separate business themes. For Claude Sonnet/Fable-style items, one stronger bullet should cover external model availability plus any internal model-catalog sync evidence, instead of producing separate bullets that feel repetitive.
- For Google AI-agent news, prefer the most enterprise-relevant/domain-specific item over generic product-update news. Strong candidates are partnerships or deployments that show governed enterprise workflows, e.g. Google Cloud + finance/industry agents, rather than a broad Gemini release unless the user specifically asks for Gemini.
- When the user asks to “check other AI agent news,” widen beyond OpenAI/Anthropic/Google to Microsoft, GitHub, AWS, Salesforce, ServiceNow, Dataverse/data-platform, agent-security, and agent-observability items. Rank for weekly-report impact: enterprise agent adoption, governed data/action surfaces, coding-agent productivity, and relevance to GL AIP runtime/model-selection work.
- Keep final suggested wording compact: usually 3–4 bullets, each one sentence plus source links. If the user asks for candidates, do not write directly to the doc yet; give a shortlist and a “shorter version for the report.”
- For this section, the user prefers skimmable bullets over paragraphs. When filling the final doc, use native Google Docs bullets to match recent previous reports; do not leave literal `*` markers as plain text.

## Google Docs API editing pitfalls

- When deleting trailing notes/placeholders near the end of a Google Doc segment, do not include the segment-ending newline in `deleteContentRange`; Docs API returns `Invalid requests[0].deleteContentRange: The range cannot include the newline character at the end of the segment.` Use `endIndex - 1` when necessary.
- If Python Google API calls repeatedly time out, refresh the token with the Google Workspace venv and use direct `curl`/raw HTTP batchUpdate for small edits.

## Raw API fallback

If the `google-workspace` scripts fail because `hermes_constants` is missing or the token lacks a scope, use raw HTTP with the stored OAuth tokens instead of blocking:

```python
import json, urllib.request, urllib.parse
from pathlib import Path
TOKEN = json.loads((Path.home()/'.hermes/google_token.json').read_text())['token']
req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN})
data = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
```

Use `google_token.json` for Docs/Drive and `google_calendar_token.json` for Calendar when available.

## Verification

After updating, export the target doc as `text/plain` via Drive API and verify:

- Requested sections no longer contain `(please insert here)` unless intentionally left for the report subject.
- Remaining placeholders correspond only to sections in the `Needs confirmation / decision` handoff.
- Numbered list nesting is visible in export.
- A Docs API readback confirms Proxima Nova is applied to filled body text and headings.
- PR number text runs contain `link.url` for GitHub URLs.
- The target section structures match the previous report for the subject's section structures:
  - `Key Metrics / OMTM`: plain paragraphs, same blank-line rhythm, no added indentation before P0/P1/P2 lines.
  - `Technology, Business, Communication, Leadership, Management & Marketing`: native decimal-numbered Google Docs lists for Raymond, never bullet dots or literal `*` text.
  - `Out of Office`: native Google Docs numbering, not literal `1.` text.
  - `Meetings/Events/Training/Conferences`: previous report's numbered-list style and cadence labels.
- The Drive text export has no raw article URLs if the report subject asked for direct article-title links.
- If the user reports a blank phone/mobile view, search Drive for same-title copies and ask the user for the phone doc link before assuming cache.

Handoff shape for scheduled runs:

```markdown
Weekly report update: <doc title>
<doc link>

Filled:
- ...

Needs confirmation / decision:
- Key Metrics / OMTM: missing Pamela/Bugle metrics block
- Technology/Business: choose from candidate articles
- Out of Office: confirm no leave if Calendar scope was unavailable

Validation:
- placeholders: <n>
- raw URLs visible: <n>
- previous-report formatting comparison: passed/needs manual check
```

### PR link verification / relink pitfall

When linking PR numbers in `Accomplishments`, do not globally link every `#N` occurrence in the document. Numbered issue/meeting/action lines can contain `#1`, `#2`, etc. and may be accidentally linked if the script scans all paragraphs. Safer pattern:

1. Locate the `Accomplishments` section range only.
2. Clear existing `link` styles in that section before relinking, in case an earlier broad pass linked wrong markers.
3. For each PR paragraph, link only the final trailing `#<number>` marker, not any incidental number elsewhere in the line.
4. Verify `linked_final_markers == PR_count` and `missing_count == 0`.

### Confidence-gated sections

If the user asks to fill the report but a section requires unavailable data or approval, fill only the confident sections and leave the placeholder rather than inserting speculative text. This is still a successful partial fill when the handoff names the remaining decisions clearly.

- `Key Metrics / OMTM`: leave placeholder unless the GLChat/Bugle/Pamela metrics block is available from Gmail/Chat scope or pasted by the report subject. If Gmail/Chat scope is missing, generate a separate metrics re-auth URL and continue filling every other grounded section first.
- `Technology, Business, Communication, Leadership, Management & Marketing`: present current-week candidate links first; do not insert until the report subject selects items.
- `Out of Office`: if Calendar has no explicit OOO/leave events, it is acceptable to write a short “No out of office / leave entries found in Google Calendar this week” line, then mention it in handoff.
