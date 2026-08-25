# Outside-hours GitHub activity reporting

Use this when the user wants a last-7-days or weekly report of GitHub activity outside normal working hours.

Timezone + business-hours rule
- Default to WIB / UTC+7 for Raymond unless the user says otherwise.
- Working hours: Monday-Friday 09:00-17:59 local time.
- Outside-hours: weekdays before 09:00 or at/after 18:00, plus all Saturday/Sunday events.

Event sources to inspect
- Authored PRs: GraphQL search for `author:<user> is:pr created:>=<cutoff>`.
- PR reviews: `contributionsCollection.pullRequestReviewContributions` for exact review timestamps, then optionally fetch `/repos/{repo}/pulls/{num}/reviews` for richer per-review bodies.
- PR comments: fetch `/repos/{repo}/issues/{num}/comments` because search only proves the PR was active, not when the comment was made.
- Issue creations: `contributionsCollection.issueContributions` or issue search when you need repo context.
- Issue comments: fetch `/repos/{repo}/issues/{num}/comments` and filter by author login + timestamp.
- PR commits: fetch `/repos/{repo}/pulls/{num}/commits`, then filter commit authorship carefully.

Filtering rules
- Sort by the event timestamp, not PR `updatedAt`.
- Exclude closure-only activity: comments whose body starts with `Close:` should not count unless another non-close comment/review exists on the same PR.
- Deduplicate by a stable key such as `(repo, url, event_type, timestamp, body/sha)`.
- Keep bot noise out of the report when the user asks for human activity.

Commit-authorship pitfall
- GitHub REST `pulls/{num}/commits` can return entries with `author: null`.
- Guard with `c.get('author') or {}` before reading `login`.
- Count a commit only if the commit author login matches the user or the message contains `Co-authored-by: <user>`.

Recommended output
- Flat, newest-first event list.
- A short summary by type and by repo.
- For large weeks, save the full list to a markdown file and print a digest in-chat.
- If the user asks for a daily view, put a table first with columns: date, day, event count, active time summary, and a one-line explanation of the day's work.
- Derive the explanation from the dominant repos, PR titles, and event types on that day.
- Cluster day-level timestamps into active windows and split windows when gaps exceed about 90 minutes; this usually reads better than raw timestamps.
