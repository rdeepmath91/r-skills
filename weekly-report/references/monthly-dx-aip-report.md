# Monthly Developer Experience / AIP report workflow

Use this when the user asks to fill the monthly `[Monthly Report: Developer Experience (DX)]` Google Doc, especially the GLAIR / AIP section.

## Safety workflow

1. Never edit the live monthly report directly unless the user explicitly asks. Create or use a preview/copy first.
2. Before writing, export the live doc and the preview/copy and compare structure:
   - page count from PDF export
   - headings / named styles
   - native bullet/list count
   - paragraph spacing
   - raw URL count
3. If preview formatting is broken, reset the preview from the live doc/template before editing further. Preserve a backup copy of the broken preview if it contains useful draft text.
4. Avoid whole-section markdown/plain-text replacement for nested list sections. It often destroys Google Docs native bullets, spacing, and heading/list hierarchy. Prefer editing inside the existing list structure or manually paste copy into the preview.

## Content sourcing

1. Use org/repo-level contribution data, not only the report subject's authored PRs.
2. For AIP-focused reporting, inspect relevant repos across the AIP surface, commonly:
   - `glaip-sdk`
   - `ai-agent-platform`
   - `gl-runner`
   - `gl-sdk`
   - `glchat`
   - `glchat-agents`
   - `glchat-sdk`
   - `glchat-messaging`
   - `glchat-mobile-app`
   - `gl-connectors`
   - `gl-smart-search`
   - `gl-smart-crawl`
   - `model-accuracy-benchmarking`
   - `prompt-template`
3. Aggregate into outcomes and implemented capabilities, not PR lists.

## Style the report subject accepted in this session

Keep the report executive-readable and top-level:

- Do not mention specific PR numbers in the copy.
- Do not make it a the report subject-only achievement list; write team/product-level outcomes.
- Keep achievements grouped per team/product area, matching the existing template style.
- Use bold emphasis sparingly for concepts executives should scan: `**model usage telemetry**`, `**streaming and final-response reliability**`, `**uploaded image attachments**`.
- Avoid overly internal implementation phrasing unless it explains a practical developer outcome.
- Remove items that are only in-progress from Achievements. Put unfinished/stabilization work under Issues or Next Steps.
- For unfinished `/goal` work, do not present it as implemented. Use broader wording such as “agent workflows” or “multi-step agent work” unless the user explicitly wants `/goal` mentioned.
- Treat roadmap/preview-only work conservatively. If A2UI, model usage telemetry, session resume, realtime/session support, or similar roadmap items are not clearly complete, omit them from Achievements or soften them into Next Steps.
- Make implemented items specific enough to be credible: e.g. “Added **context compaction integration**” rather than “Improved orchestration”.
- When reporting documentation, distinguish live/published docs from preview/sync/internal docs. the report subject rejected “preview docs” / “GitBook sync support” framing; verify merged live GitBook/docs PRs and write “Published live GitBook coverage…” or “Updated live onboarding docs…” only for docs that are actually published/merged. Do not treat a source PR in `glaip-sdk` as live GitBook publication until the corresponding page exists on `gl-sdk:docs/gitbook-sync` and the public URL returns HTTP 200.

### Live vs preview GitBook verification

Use this concrete check before claiming docs achievements:

1. Fetch `gl-sdk` docs branch and inspect the canonical GitBook tree:
   - `git fetch origin docs/gitbook-sync`
   - `git show origin/docs/gitbook-sync:gitbook/SUMMARY.md`
   - `git cat-file -e origin/docs/gitbook-sync:gitbook/<path>.md`
2. Derive live URLs from `gitbook/SUMMARY.md` paths under `https://gdplabs.gitbook.io/sdk/`, dropping `.md` and `README` where GitBook does so. Verify with `curl -L -A 'Mozilla/5.0' -s -o /dev/null -w '%{http_code}' <url>`; plain urllib/HEAD may get 403 from GitBook even when the browser URL is live.
3. Preview URLs come from GitHub PR `statusCheckRollup` contexts named `GitBook (gitbook)` / `GitBook (gitbook) - gdplabs.gitbook.io`, not from the final live page path. Use them only as preview evidence and label them as preview.
4. If a guessed live URL returns 404 or the file is absent from `origin/docs/gitbook-sync:gitbook/`, remove that item from live-documentation achievements or reword it as source/internal docs only.

## Recommended GLAIR / AIP achievement grouping

Use this grouping unless the live template has changed:

1. `GL AIP`
   - Context compaction integration
   - Model usage telemetry / usage deltas / aggregation helpers
   - Token streaming final-response fixes
   - Uploaded image attachments and generated image artifacts
   - Safe runtime trace metadata / read-image contract
   - A2UI event emission and platform routing, if implemented
   - Tool/MCP reliability, trusted identity, namespace/shared-resource handling
   - CLI/TUI reliability
2. `Gen AI SDK`
   - `GLLM Inference`
   - `GLLM Pipeline`
   - `GLLM Retrieval / Datastore`
   - `GLLM Evals`
   - `GLLM DocProc / Multimodal`
   - `Computer-use`
3. `GL Runner`
   - Tenant access boundary
   - Runnable dependency isolation
   - Run history / stream integration
   - SDK examples, quick-start guidance, demo setup, environment creation
   - Do not describe docs work as “GitBook sync support” unless the actual completed work was sync tooling; prefer developer-facing outcome wording.
4. `GLChat / GL Connectors`
   - Connector-backed tool/agent setup
   - Shared runtime resource handling
   - Local/onboarding guidance and integration points used by AIP
5. `Live Documentation / Developer Enablement`
   - Live GitBook/docs coverage for AIP agent filesystem environment propagation, sandbox filesystem behavior, and file-processing/read-image usage when the pages are present on `gl-sdk:docs/gitbook-sync` and live URLs return 200
   - Live GL SDK GitBook/docs coverage for GL Computer Use, GLLM Evals, GLLM Inference, GLLM DocProc/OCR, Computer Vision migrations, when supported by merged PRs and live URLs
   - Live ai-agent-platform onboarding docs for gcloud prerequisites, installation Definition of Done, health-check expectations, and local application startup
   - Tool/MCP/filesystem/multimodal/runner workflow guidance that is published or merged, not merely previewed
   - Do not claim `agent-evaluations` as live AIP GitBook coverage unless `gitbook/gl-ai-agent-package/guides/agent-evaluations.md` or equivalent appears on the docs branch and its public URL verifies; a source-only `glaip-sdk` PR is insufficient

## Verification before handoff

- Confirm only the preview/copy changed unless live editing was explicitly requested.
- Export the changed doc and verify the page count did not unexpectedly expand.
- Compare heading and bullet/list counts against the live template.
- Check that Executive Summary remains top-level and compact.
- Check that Achievements do not contain WIP-only items or raw PR references unless the report subject asked for them.
