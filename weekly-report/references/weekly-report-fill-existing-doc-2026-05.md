# Weekly report fill-existing-doc notes — 2026-05 session

Use this as a concrete reference when filling the report subject's weekly report Google Doc without breaking formatting.

## What worked

- Locate the current weekly report Google Doc, then modify only the target section bodies under stable headings.
- Preserve native Google Docs structure:
  - keep existing heading paragraphs/styles;
  - replace section body text only;
  - apply `NORMAL_TEXT` to inserted bodies;
  - use Proxima Nova 11 pt for body text;
  - convert inserted list text to native Docs bullets/numbered lists rather than leaving plain `1.` markers when possible;
  - use linked PR/article titles or `#PR` markers, not raw URLs in visible text.
- Good section sources:
  - Issues: copy from the corresponding `AIP Current Issues` week tab when available.
  - Accomplishments: GitHub PR audit for the report subject's work account over the current week; include reviewed and implemented PRs, link final `#PR` markers.
  - Meetings: Google Calendar for the week, deduped, labeled `[Weekly]`, `[Biweekly]`, `[Monthly]`, or `[One-time]`.
  - Out of Office: Google Calendar OOO events.
  - Next Actions: synthesize from current issues + PR themes; keep concise.
- Validation checks after editing:
  - export/read back the doc as plain text and check remaining `(please insert here)` placeholders;
  - verify raw visible URL count is 0;
  - inspect Docs API text styles for inserted body ranges: Proxima Nova 11 pt;
  - verify PR/article link count matches inserted linked items;
  - verify headings still appear as native Google Docs headings.

## User preference from this session

For the `Technology, Business, Communication, Leadership, Management & Marketing` section, the user prefers new agent-space items, especially model/coding-agent releases and agent infrastructure/security. Avoid multiple duplicate articles about the same release. For example, when Claude Opus 4.8 appears, use Anthropic's introduction as the single Opus item, then diversify with Codex/enterprise agents, Chrome/Google agents, Workday/enterprise agents, MCP/sandbox/agent-governance items, etc.

## Pitfalls

- Do not invent Key Metrics / OMTM if the source metrics block is not available; leave the placeholder and ask/prompt for the metrics.
- Do not insert raw article URLs into the visible doc body. Link the article titles.
- If a public X search or X CLI is unavailable in the current environment, use official/vendor/news sources rather than unreliable scraped mirrors. Do not store the transient setup failure as a durable rule.
