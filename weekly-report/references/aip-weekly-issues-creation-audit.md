# AIP weekly Issues creation audit

Use this when Raymond asks whether AIP issues were already created for a prior weekly-report period, especially after a cron run filled Pull Requests but left `Issues` blank.

## Workflow

1. Identify the report week precisely in Asia/Jakarta.
   - User phrases like "4th week of June" may mean the existing weekly report title range, not ISO week numbering.
   - Check both likely windows when needed, e.g. `2026-06-21..2026-06-27` and `2026-06-22..2026-06-28`.
2. Locate the current and immediately previous `[Weekly Report: Raymond Christopher]` Docs in Drive.
   - Export both as plain text.
   - Read the previous report's `Issues` section first; this gives the actual issue themes and any referenced issue/PR numbers.
   - Also check whether the current report's `Issues` section is still `(please insert here)` before implying the cron filled it.
3. Search GitHub issues in `GDP-ADMIN/ai-agent-platform` for the target creation window.
   - `gh search issues` only supports `--state open` or `--state closed`, not `--state all`; query both and dedupe by URL.
   - Capture total created issues and Raymond-authored subset separately.
4. Verify referenced numbers individually.
   - In GitHub, `#N` can refer to an issue or PR in the same number namespace. Do not assume a weekly-report `#1022` is an issue; `gh issue view` can return a PR-shaped object if that number is a PR.
   - If the title does not match the weekly-report item, flag it as suspicious/wrong reference and search by exact title/keywords across GDP-ADMIN before reporting.
5. For roadmap items, verify native sub-issues through GraphQL:
   - Query `repository.issue(number:N).subIssues(first:100)`.
   - Report open/closed child counts and list the important children, not just the parent URL.
6. Final answer shape:
   - Short answer first: created / not created / partially created.
   - Table mapping each weekly-report Issues item to GitHub evidence.
   - Call out wrong or suspicious refs explicitly.
   - If the current report's Issues section is blank, state that separately from whether issues exist in GitHub.

## Example findings from Jun 21–27 2026

- Previous report `21 June 2026 - 27 June 2026` contained three Issues items: BYOK/admin-dashboard registration, Code Execution Security `#2114`, and standardize Agent building requirements `#1022`.
- `#2114 Roadmap: Code Execution Security` was created on 2026-06-25 and had native sub-issues such as `#2115`, `#2117`, `#2118`, `#2119`, `#2120`, `#2122`, `#2136`, and `#2137`.
- `#1022` in `GDP-ADMIN/ai-agent-platform` was not the named standardization issue; it resolved to a merged PR about `BOSA_API_BASE_URL`, so it should be flagged as likely wrong/stale reference unless another repo/source proves otherwise.
- The following week's report `28 June 2026 - 04 July 2026` had `Issues` still equal to `(please insert here)` even though the cron filled Pull Requests.