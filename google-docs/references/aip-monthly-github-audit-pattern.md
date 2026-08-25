# AIP Monthly GitHub Audit Pattern

Use this as the evidence-gathering pattern before filling Raymond's monthly Developer Experience / AIP report.

## Principle

Do not treat the report as Raymond-only activity. Raymond explicitly expects the AIP/GLAIR monthly report to reflect what happened across the relevant repos and contributors in May/month scope, then use Raymond's PRs only where they define direction or are central examples.

## Scope shape

1. Start broad: list GDP-ADMIN repos updated during the report month.
2. Fetch PRs updated during the month across those repos, then classify rather than dumping everything into the report.
3. Separate:
   - report-wide repo activity: all touched repos and PR counts;
   - AIP/GLAIR-relevant subset: repos whose work affects agent platform, SDK, runner, tools, model/runtime, GLChat/agent apps, connectors, evaluation, retrieval, or prompt templates;
   - core AIP subset: usually `glaip-sdk`, `ai-agent-platform`, `gl-runner`, and `gl-sdk`.
4. Use created/merged-in-month PRs for achievement evidence. Use updated-in-month PRs to discover active work and open risks, but do not call every updated PR an achievement.
5. Count/inspect authors across the relevant subset so the summary is team-level, not only user-level.

## Repos to consider first

Core:
- `GDP-ADMIN/glaip-sdk`
- `GDP-ADMIN/ai-agent-platform`
- `GDP-ADMIN/gl-runner`
- `GDP-ADMIN/gl-sdk`

Common adjacent AIP/GLAIR surfaces:
- `GDP-ADMIN/glchat`
- `GDP-ADMIN/glchat-agents`
- `GDP-ADMIN/glchat-sdk`
- `GDP-ADMIN/glchat-mobile-app`
- `GDP-ADMIN/glchat-messaging`
- `GDP-ADMIN/glchat-custom-services`
- `GDP-ADMIN/gl-connectors`
- `GDP-ADMIN/gl-smart-search`
- `GDP-ADMIN/gl-smart-crawl`
- `GDP-ADMIN/model-accuracy-benchmarking`
- `GDP-ADMIN/prompt-template`

Include or exclude adjacent repos based on PR titles and whether they materially affect AIP/GLAIR runtime, developer workflow, or product surface.

## Theme buckets for report wording

Group the final report by outcomes/themes, not by repo or by every PR:

- `/goal` and command orchestration contracts
- context compaction, memory, long-running session safety
- model usage, model routing, provider/runtime configuration
- token streaming, final-response correctness, streamed links/media rewriting
- image/vision/multimodal attachments and generated artifacts
- A2UI / human-in-the-loop interaction events
- tools, MCP, filesystem, connectors, identity/namespace isolation
- CLI/TUI/developer workflow reliability
- GL Runner runnable/scheduler/tenant isolation foundations
- GL SDK pipeline state/resume, retrieval, evals, datastore, document processing, computer-use, realtime/multimodal inference
- GLChat/agent application integration only when it connects to AIP/GLAIR platform behavior

## Report-use guidance

- Use PR counts and repo counts as grounding for yourself; include only small headline numbers in the doc if they improve credibility.
- Prefer compact bullets such as “Added model usage contract, deltas, aggregation helpers, and platform run-detail/backfill work” over long PR lists.
- Cite representative PR numbers only when the user asks for auditability or when a concrete item is important.
- Open PRs and WIP work are useful for `Issues` / `Next Steps`; merged PRs are better for `Achievements`.
- Before writing the doc, answer “what are you aiming to fill?” with the proposed sections/themes so Raymond can correct scope before formatting-sensitive edits.
