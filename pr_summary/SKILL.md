---
name: pr_summary
description: "Generate a weekly PR activity summary report using GitHub API search queries. Searches org:GDP-ADMIN for a user's authored, reviewed, and commented PRs with bot filtering and role detection."
---

# PR Summary

Generates a Pull Request activity summary report for a GitHub user across specified repositories within the org.

## Context

This works in both OpenCode (`~/.opencode/command/pr-summary.md` origin) and Hermes.
All queries target `org:GDP-ADMIN` using the GitHub API via `gh` CLI or `curl` + GitHub REST API.
User identity: `raychrisgdp`.

## Workflow

### 1. Determine Cutoff Date

Default: 7 days before today. Calculate:
```bash
date -d "7 days ago" +%Y-%m-%d  # Linux
```

### 2. Query Authored PRs (GraphQL)

**Use `gh api graphql` not `gh search prs`**. The REST/CLI search returns truncated data and lacks `isMerged`. GraphQL gives full fields in one call.

```bash
gh api graphql -f query='
query($q: String!) {
  search(query: $q, type: ISSUE, first: 100) {
    edges {
      node {
        ... on PullRequest {
          number
          title
          url
          state
          createdAt
          updatedAt
          repository { nameWithOwner }
          mergedAt
        }
      }
    }
  }
}
' --field q="org:GDP-ADMIN author:raychrisgdp is:pr created:>=$CUTOFF"
```

**Important**: Use `mergedAt` to detect merged PRs (don't look for `isMerged` — it doesn't exist in the GraphQL schema; `mergedAt: null` = not merged).

### 3. Query Reviewed/Commented PRs (GraphQL)

Run **two** separate queries. The `reviewed-by:` filter only catches formal reviews, but the user often leaves non-review comments and closure comments that are equally important.

**Query A — Reviewed:**
```bash
--field q="org:GDP-ADMIN reviewed-by:raychrisgdp is:pr updated:>=$CUTOFF"
```

**Query B — Commented:**
```bash
--field q="org:GDP-ADMIN commenter:raychrisgdp is:pr updated:>=$CUTOFF"
```

Merge both result sets (deduplicate by URL).

**Critical audit step:** `reviewed-by:` / `commenter:` combined with `updated:>=...` proves the PR was updated recently, not that Raymond's review/comment happened recently. After the search, inspect each PR's `comments.nodes.createdAt`, `reviews.nodes.createdAt`, and authored `createdAt`; include the PR only if Raymond has a visible event at or after the cutoff. Sort by that event timestamp, not `updatedAt`. If this strict pass removes entries from a previously generated report, update the report rather than hand-waving.

**IMPORTANT:** EXCLUDE "Close:" entries entirely. If the user's ONLY activity on a PR is a closure comment (no code review, no review), skip it. Do not list it, do not count it, do not include it in the report. Only include:
- "Review": user left an actual code review at/after cutoff, or a non-close comment at/after cutoff
- "Review & Implement": user reviewed/commented at/after cutoff AND contributed code (check Co-authored-by below)
- "Implement": user is the PR author and the PR was created at/after cutoff

### 4. Filter Bot Activity

For authored PRs created near cutoff (within 3 days), verify recent activity is from the user, not bots. Exclude comments/reviews from:
- `github-actions[bot]`
- `sonarqubecloud[bot]`
- `sca-gdplabs[bot]`
- Any user with `[bot]` suffix

### 5. Detect Roles

- **Implement**: User is the PR author
- **Review**: User reviewed/commented but did not author
- **Review & Implement**: User is not author but contributed code (`Co-authored-by: Raymond Christopher` in commit messages, or commits with author login `raychrisgdp`)

Add `(WIP)` for open PRs.

## Sort & Format

Sort all PRs globally by user's last activity date descending (most recent first). Do NOT group by repo — single continuous numbered list.

```
# PR Summary (since YYYY-MM-DD)

Cutoff date: YYYY-MM-DD

1. Role[(WIP)]: PR title [#number](link)
2. Role: PR title [#number](link)
...
```

## Strict Timestamp Audit Recipe

For weekly reports, build the candidate set with authored/reviewed/commented searches, then filter it again in code:

```python
CUTOFF = "YYYY-MM-DDT00:00:00Z"

def ge_cut(ts):
    return bool(ts and ts >= CUTOFF)

def user_events(pr):
    events = []
    if pr["author"]["login"] == USER and ge_cut(pr["createdAt"]):
        events.append(("created", pr["createdAt"], ""))
    for c in pr["comments"]["nodes"]:
        if c["author"] and c["author"]["login"] == USER and ge_cut(c["createdAt"]):
            events.append(("comment", c["createdAt"], c.get("body") or ""))
    for r in pr["reviews"]["nodes"]:
        if r["author"] and r["author"]["login"] == USER and ge_cut(r["createdAt"]):
            events.append(("review", r["createdAt"], r.get("body") or ""))
    return events
```

Include authored PRs only when the `created` event is at/after cutoff. Include reviewed/commented PRs only when there is a non-close comment or review event at/after cutoff. Use `max(event_timestamp)` for sorting. Never use PR `updatedAt` as a fallback user activity timestamp in the final report.

## Outside Normal Business Hours Variant

Use this when the user wants a last-7-days activity report filtered to non-working time instead of a PR-level summary. A supporting workflow note lives in `references/outside-hours-gh-activity.md`.

Default interpretation for Raymond:
- timezone: `WIB` (`UTC+7`)
- normal business hours: `09:00` through `17:59` Monday-Friday
- outside-hours: weekdays before 09:00 or at/after 18:00, plus all Saturday/Sunday events

Event sources to inspect:
- Authored PRs: GraphQL search for `author:<user> is:pr created:>=<cutoff>`.
- PR reviews: `contributionsCollection.pullRequestReviewContributions` for exact review timestamps; optionally fetch `/repos/{repo}/pulls/{num}/reviews` for full bodies and state.
- PR comments: fetch `/repos/{repo}/issues/{num}/comments` because search only proves the PR was active, not when the comment happened.
- Issue creations: `contributionsCollection.issueContributions` gives exact creation timestamps.
- Issue comments: fetch `/repos/{repo}/issues/{num}/comments` and filter by author login + timestamp.
- PR commits: fetch `/repos/{repo}/pulls/{num}/commits`, then filter commit authorship carefully.

Filtering rules:
- Sort by the event timestamp, not PR `updatedAt`.
- Exclude closure-only activity: comments whose body starts with `Close:` should not count unless another non-close comment/review exists on the same PR.
- Deduplicate by a stable key such as `(repo, url, event_type, timestamp, body/sha)`.
- Keep bot noise out of the report when the user asks for human activity.
- For commit fetches, guard `c.get('author') or {}` because GitHub can return null authors on some entries.

Presentation:
- Prefer a flat, newest-first list of outside-hours events.
- Add a compact summary by type and by repo if the list is long.
- When the user asks for a daily breakdown, put a summary table before the detail sections.
- In that table, include date, day, event count, active time summary, and a one-line description of what the work mostly was that day.
- Derive the description from the dominant repos, PR titles, and event types on that day.
- For daily summaries, group timestamps into active windows and split separate work sessions when gaps exceed roughly 90 minutes.
- This usually produces a better human summary than listing every timestamp.
- Save the full report to a markdown file when the result would be noisy in-chat.

## Save & Report

- Save to `pr_activity_report.md` (or `{filename}_summary.md` if filename specified)
- Display breakdown:
  - Total PRs count
  - By repository
  - By role (Implement vs Review vs Review & Implement)
  - WIP (open) PRs list

## Constraints

- **CRITICAL**: For authored PRs, always use `created:>=<date>`, NOT `updated:>=<date>`. The `updated:` filter includes activity from ANY user (bots, reviewers, SonarCloud) causing false positives.
- For reviewed/commented PRs, `reviewed-by:` and `commenter:` identify candidate PRs only. They are not enough for weekly reporting because `updated:>=<date>` can be caused by someone else. Inspect the returned comments/reviews and require a Raymond-authored event timestamp at/after cutoff before including it.
- Sort by Raymond's last event timestamp, not PR `updatedAt`. If an item has no qualifying user event at/after cutoff, exclude it even if it appeared in GitHub search.
- Exclude PRs where only bots were active recently.
- Deduplicate PRs appearing in multiple search results.
- Check commit history for `Co-authored-by` to detect "Review & Implement" cases.
- **GraphQL note**: `isMerged` doesn't exist on PullRequest type. Use `mergedAt` (null = open/closed, non-null = merged).
- **Auth requirement**: Must be authenticated via `gh auth login` on the machine.
- **"Close:" role**: EXCLUDED. The user does not want closure-only activity in reports. Skip PRs where the user's only interaction was closing the PR.
- **Comparison baseline**: The original OpenCode command at `~/.opencode/command/pr-summary.md` includes ~17 Close-only entries. The expected output WITHOUT Close entries is ~45-48 PRs for a 7-day window; counts vary by week, but strict timestamp audit is mandatory.

## Origin

The canonical definition lives at `~/.opencode/command/pr-summary.md` as an OpenCode custom slash command (`/pr-summary`).
This skill adapts that command's logic for execution outside the OpenCode TUI (Hermes sessions, cron jobs, shell scripts).
