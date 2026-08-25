# PR GraphQL Query for Weekly Report

## Working Query Structure

```graphql
query {
  user(login: "raychrisgdp") {
    pullRequests(first: 100, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        number
        title
        url
        repository { nameWithOwner }
        createdAt
        updatedAt
        author { login }
        timelineItems(first: 30, itemTypes: [PULL_REQUEST_REVIEW, ISSUE_COMMENT, MERGED_EVENT, CLOSED_EVENT]) {
          nodes {
            __typename
            ... on PullRequestReview { author { login }; createdAt; state }
            ... on IssueComment { author { login }; createdAt }
            ... on MergedEvent { actor { login }; createdAt }
            ... on ClosedEvent { actor { login }; createdAt }
          }
        }
      }
    }
  }
}
```

## Filtering Logic (in post-processing)

1. **Collect all timeline items** where author/actor = `raychrisgdp`
2. **Filter by week** — Keep PRs where at least one event timestamp falls in target week:
   - Target week: Saturday 00:00 to Saturday 23:59 Asia/Jakarta (UTC+7)
   - In UTC: Friday 17:00 to Friday 17:00
3. **Determine role**:
   - Has `PullRequestReview` → "Review" (or "Review & Implement" if also authored)
   - Only authored/other events → "Implement"
   - Title contains "WIP" → append " (WIP)"
4. **Sort** by latest qualifying event timestamp (descending)
5. **Format**: `Role: title #number` with only final `#N` linked

## Week Boundary Calculation

```python
# Asia/Jakarta = UTC+7
week_start = datetime(2026, 6, 7, 0, 0, 0, tzinfo=timezone(timedelta(hours=7)))
week_end = datetime(2026, 6, 14, 0, 0, 0, tzinfo=timezone(timedelta(hours=7)))
# In UTC:
week_start_utc = datetime(2026, 6, 6, 17, 0, 0, tzinfo=timezone.utc)
week_end_utc = datetime(2026, 6, 13, 17, 0, 0, tzinfo=timezone.utc)
```

## Common Mistakes

- ❌ Using `updatedAt` — reflects bot/other-user activity after Raymond's touch
- ❌ Using `gh search prs` — missing timeline details
- ❌ Not converting to Asia/Jakarta timezone — includes wrong PRs
- ❌ Including Close-only/Merge-only events — these don't count as "touched"
- ❌ Not normalizing duplicate `#N` refs in PR titles before linking