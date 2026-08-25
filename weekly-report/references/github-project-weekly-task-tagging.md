# GitHub Project weekly finished-task tagging

Use this when the user asks to tag/list finished weekly tasks, especially for AI Agents work.

## Source of truth

Issue labels may not contain sprint/story metadata. For GDP-ADMIN AI Agents work, check the GitHub ProjectV2 board fields first:

- Project: `GDP-ADMIN/projects/231` (AI Agents)
- Sprint field: `Sprint Name` single-select, not repo labels and not the text field named `Sprint`
- Status field: `Status`
- Story field: `Story Point`
- Date fields: `Start Date`, `Due Date`

If the initial issue/label scan shows missing sprint or points, do not stop at that audit. Query the project board fields before reporting gaps.

## Required fields for every finished task

For each closed/completed task in the weekly window:

1. Ensure the report subject is represented as assignee: `raychrisgdp`.
2. Set/verify `Status = Done`.
3. Set/verify the specific `Sprint Name` option for the reporting week.
4. Set/verify `Story Point`.
5. Set/verify `Start Date` and `Due Date` for the reporting window.
6. Verify the mutation by reading the issue/project item back; do not rely on mutation responses only.

## Sprint boundary pitfall

Month-boundary weeks can have two plausible sprint labels. In the 2026-05-26 to 2026-06-02 window, both `2026-Q2-May-W4` and `2026-Q2-Jun-W1` appeared on the board. When the user asks for June reporting, use `2026-Q2-Jun-W1`; mention the board oddity only if it affects the choice.

## Story points

GDP-ADMIN ProjectV2 story points are single-select values. Common options observed:

- `0`
- `0.5`
- `1`
- `2`
- `3`
- `5`
- `8`
- Larger options may exist (`13`, `20`, `40`, `100`), but do not invent estimates. If uncertain, leave an audit gap or ask the user rather than assigning arbitrary values.

Roadmap/parent tracking items may be `0`; small cleanup/superseded/meta tasks are often `0.5`; implementation tasks are commonly `1+`. Treat those as heuristics only and verify project conventions where possible.

## Final handoff format

Keep the user-facing report operational and compact:

- State total processed, verified OK count, and mismatch/error count.
- State the exact fields applied to every item.
- Explicitly say whether any items were only assigned. If items merely needed the report subject added as assignee, list those separately as "Added the report subject as assignee" while confirming sprint/status/date/story were also set.
- List each item with repo/issue, title, sprint tag, story point, and any assignment note.
- Do not expose tokens or raw auth output.

## Verification shape

A good final verification summary looks like:

```text
Applied to every item:
◆ Assignee includes raychrisgdp
◆ Status = Done
◆ Sprint Name = 2026-Q2-Jun-W1
◆ Start Date = YYYY-MM-DD
◆ Due Date = YYYY-MM-DD
◆ Story Point filled
◆ Verified after mutation: N/N OK, 0 mismatches
```

Then provide the tagged list.