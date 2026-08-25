# GL AIP weekly update from GitHub when the Google Doc is inaccessible

Use when Raymond asks to update the GL AIP weekly/current-issues list, but the linked Google Doc cannot be read or written because OAuth is expired/revoked, browser access requires sign-in, or public export is unauthorized.

## Pattern

1. State the Docs blocker plainly, but do not stop there.
   - Say which access path failed: Docs API token refresh, browser sign-in, public export, etc.
   - Do not frame this as "can't do it" if GitHub evidence can still produce the update candidates.
2. Ground the update from GitHub activity in the relevant AIP repos.
   - Include both `GDP-ADMIN/ai-agent-platform` and `GDP-ADMIN/glaip-sdk` unless Raymond narrows scope.
   - Use the strict weekly-report / PR-summary timestamp rule: search authored/reviewed/commented candidates, then require a Raymond-authored event at or after the cutoff. Sort by Raymond's event timestamp, not PR `updatedAt`.
3. Choose the report window explicitly.
   - Default for "this week" can be Monday 00:00 WIB through now.
   - If the target weekly report/list may use a Saturday-to-Saturday window, also check Saturday/Sunday as an "optional weekend carry-in" section rather than silently excluding it.
4. Collapse the PR list into issue/status themes instead of dumping every PR first.
   - Good GL AIP groupings from this session: provider-managed sandbox migration, PTC/custom-tool timeout and metadata handoff, browser-use/computer-use extras adoption, runtime compatibility surfaces (DOCUMENT/A2UI/image registry), model/provider catalog updates, eval/report-automation/security validation.
   - Mark status conservatively: `[Done]` only for merged/completed themes; `[Testing]` when fixes landed but validation/rollout is active; `[WIP]` for open implementation PRs; `[Review/WIP]` for open review tracks.
5. Include PR links under each themed point.
   - Use repo-qualified refs plus direct URLs, e.g. `GDP-ADMIN/glaip-sdk#1552` and `https://github.com/GDP-ADMIN/glaip-sdk/pull/1552`.
   - Preserve a full evidence list in a local draft if the chat summary would be too long.
6. If the Doc cannot be edited, produce a copy-paste-ready local draft and name the path.
   - Keep it mobile-readable: numbered themes, alpha subpoints, PR links below each point.
   - Tell Raymond the exact reauth/share condition needed before writing to the live Google Doc.

## Pitfalls

- Do not only report the Google Docs auth failure. The useful deliverable is still the GL AIP update candidate list.
- Do not query only one repo. Recent GL AIP work often spans `ai-agent-platform` and `glaip-sdk` in paired PRs.
- Do not use GitHub `updatedAt` as evidence of Raymond's activity; bot/reviewer updates cause false positives.
- Do not bury the grouped update points under a raw PR dump. Raw PR evidence belongs after the summarized points or in a local file.
- Do not silently mix Monday and Saturday report windows. Label weekend carry-in separately so Raymond can decide whether to include it.
