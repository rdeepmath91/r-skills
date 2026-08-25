# Scheduled weekly report handoff checklist

Use this reference for autonomous weekly report cron jobs. The run should complete as much of the report as the available data supports, then make the uncertainty explicit instead of silently guessing.

## Required handoff shape

```markdown
Weekly report update: <doc title>
<doc link>

Filled:
- Issues: <source tab/doc>
- Accomplishments/Pull Requests: <count> PRs from strict the report subject activity audit
- Meetings/Events: <count> deduped calendar items, or not filled because <reason>
- Key Metrics / OMTM: filled from <Pamela/Bugle/pasted block>, or left for confirmation
- Next Actions: adapted from previous report + current issue/PR themes
- Technology/Business: inserted selected/current items, or candidates listed for choice
- Out of Office: <observed status>

Needs confirmation / decision:
- <section>: <specific missing data or decision the report subject must make>

Validation:
- target doc ID: <id>
- previous report used for formatting: <title/link>
- placeholders: <n>
- raw URLs visible: <n>
- PR links: <linked>/<expected>
- article links: <linked>/<expected>
- previous-report formatting comparison: passed / needs manual check (<reason>)
```

## Confirmation/decision triggers

Add an item under `Needs confirmation / decision` when any of these are true:

- Multiple same-title weekly report docs exist and the target is not unambiguous.
- Calendar scope is unavailable, or OOO/leave status was inferred without an explicit Calendar event.
- Key Metrics / OMTM source is unavailable; do not fabricate or summarize metrics from memory.
- Technology/Business article choices were not explicitly selected and there is no stable auto-selection rule.
- Previous report formatting comparison could not be completed through export + Docs API readback.
- A mobile screenshot or user report appears to show a different blank copy than the exported doc.

## Formatting gates before delivery

- Compare against the immediately previous report for the subject, not only the template.
- Preserve native list types: recent Technology/Business uses bullets; Out of Office uses numbering.
- Keep metrics as plain paragraphs with the previous report's spacing and no new indentation.
- Link PR numbers only on final trailing `#N` markers inside Accomplishments.
- Link article title text directly; avoid standalone raw URLs unless the user explicitly asks for them.
