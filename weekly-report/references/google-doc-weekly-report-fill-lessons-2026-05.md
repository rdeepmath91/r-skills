# Google Docs weekly report fill lessons — May 2026

Use this when filling the report subject's weekly report in an existing Google Doc.

## Workflow lessons

- Preserve the current template structure. Do not add explanatory labels or new prose wrappers unless the template already has them.
- For `Key Metrics / OMTM`, combine the current week's metrics block with the previous week's performance baseline when current performance numbers are missing. Keep the metric headings/plain-text structure rather than converting it to bullets.
- `Next Actions` should be concise and plain. Prefer short action phrases over long implementation-detail sentences.
- Technology section should favor current agent-space/developer-agent/model-release items over generic AI/business news.
- When multiple articles are about the same model release, include the official introduction once instead of repeating launch coverage from multiple outlets.
- Use linked titles only; avoid visible raw URLs.
- When the user asks whether edits landed in the live report, verify the exact live Google Doc instead of relying on a local export or prior script output: list matching Drive files, compare title/doc ID/owner/parents/createdTime/modifiedTime, then read back the same `DOC_ID` via Docs API and Drive text export. Call out same-title duplicates or Master Data docs explicitly.

## Verification checklist

After editing the doc, verify:

- target doc title and `DOC_ID` match the intended live weekly report, not a preview/copy; 
- placeholders remaining is zero unless a section truly lacks data;
- raw URL count in plain-text export is zero;
- PR/article link count matches inserted linked items;
- body text remains Proxima Nova 11 pt;
- headings remain native Google Docs headings;
- numbered/bulleted sections remain native Google Docs lists where the template uses lists.

## Style examples

Simplified `Next Actions` style:

1. Finalize GLChat agent management policy and dashboard alignment.
2. Follow up token streaming and file-link fixes.
3. Continue A2UI, GL Runner, and GitHub agent action reviews.
4. Finish /goal orchestration follow-ups and defaults cleanup.
5. Continue Agent Skills sharing and adoption follow-ups.

Agent-space technology item pattern:

- Introducing Claude Opus 4.8 — Anthropic
- Cisco and OpenAI redefine enterprise engineering with Codex — OpenAI
- Bringing AI agents to Chrome Enterprise security management — Google
