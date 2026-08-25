# Weekly AIP Issues: status reconciliation, links, and native list parity

Use before copying a previous AIP week into a new nested month/week tab.

## Reconcile first

1. Extract every visible issue/PR reference and its existing link target from the prior child tab.
2. Resolve each reference against its exact repository. Do not infer a bare `#N` repository from an old sentence: the same number can belong to different GDP repos and may be unrelated.
3. Remove a carry-over that is truly complete (closed issue or merged/closed implementation set) instead of retaining a `[SOLVED]` weekly item.
4. Keep roadmap/umbrella items only if the tracker itself remains open; describe completed child work as context, never as proof that the whole roadmap is solved.
5. When an operational source says a problem is solved but its GitHub tracker remains open, inspect the newest source entry and separate the core rollout from residual work. Keep `[WIP]` when implementation or validation remains. Use `[OPERATIONAL — UNDER MONITORING]` when the core implementation is complete and only latency monitoring, template verification, rollout confirmation, or final closure evidence remains. State the open tracker and exact closure action instead of treating either source as the whole truth.

## Link rule

Every repo-qualified `GDP-ADMIN/<repo>#N` visible in the weekly AIP tab must be a direct URL to the exact GitHub issue or PR. After writing, scan each text run containing a repo-qualified reference and assert it has a `link.url`.

## Native-list parity

Previous AIP tabs use native `NUMBERED_DECIMAL_ALPHA_ROMAN` lists, not typed `1.` / `a.` text. Manual prefixes create duplicated or invalid mobile formatting.

- Preserve the `Issues` heading.
- Top-level issue paragraphs: native list level 0, bold, `indentStart: 36pt`, `indentFirstLine: 18pt`.
- Detail paragraphs: native list level 1, normal weight, `indentStart: 72pt`, `indentFirstLine: 54pt`.
- When using leading tabs to encode nesting, do **not** also pre-apply the final list indents before `createParagraphBullets`; Docs can combine both signals and turn one-tab detail rows into nesting level 2. Reset issue-row indents to zero, insert exactly one leading tab for each intended level-1 detail, create one list across the tab, then apply the exact 36/18 pt and 72/54 pt indents after list creation.
- If repairing a bad list, run `deleteParagraphBullets`, reset indents, reinsert nesting tabs bottom-to-top, recreate one native list, then reapply final indents.
- Read back the exact target child tab. Assert no paragraph text starts with typed `1.` / `2.` / `a.` / `b.` labels, and verify the exact `bullet.nestingLevel` sequence, not only the visual indent.

## Capacity-issue wording

For Raymond's AIP capacity issue:

- State the demand as an ownership fact: AIP now supports critical GLChat projects, Developer Experience, internal automations, and other production use cases.
- Do not enumerate internal component surfaces merely to make the issue sound larger.
- Do not add headcount targets, ownership-plan language, hiring/internal-transfer workflows, or onboarding plans unless requested.
- It is acceptable to prioritize adding a senior engineer for architecture, technical reviews, mentoring, incident response, release support, and long-term reliability.

## Weekly-report transfer

For a full current-week synchronization, copy only reconciled current child-tab items into the weekly report's `Issues` section. Preserve links there, but reset all copied body/list paragraphs to `NORMAL_TEXT`; do not let the preceding `Issues` heading make every issue paragraph a `HEADING_2`.

When Raymond asks to “mirror this” immediately after revising one issue, default to a bounded mirror of that issue only. Re-read the weekly report, add or replace the matching top-level item and its details, and leave unrelated issue wording unchanged. Rebuild the section's single native list only when necessary to continue numbering, then verify the top-level/detail counts, exact `bullet.nestingLevel` sequence, Proxima Nova body style, heading styles, placeholder count, and raw-URL count.
