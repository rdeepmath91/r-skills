# AIP Current Issues tab update pattern

Use this when Raymond asks to update the `AIP Current Issues` Google Doc for a weekly tab, especially when the target is a nested tab such as `June 2026 → Week 4 Jun 2026`.

## Source and target resolution

1. Search Drive for `AIP Current Issues`; the canonical doc observed in this workflow was a multi-tab Google Doc.
2. Fetch with `includeTabsContent=true`; top-level month tabs may contain only a newline while useful content lives in `childTabs`.
3. Match the exact child tab by title, e.g. `Week 4 Jun 2026`, and keep its `tabId` for all reads/writes.
4. Verify GitHub issue titles/states before writing if the user gives issue URLs.

## Tab-aware write mechanics

For multi-tab docs, all insertion, deletion, styling, and link ranges must include `tabId`:

```json
{"range": {"tabId": "t...", "startIndex": 123, "endIndex": 456}}
```

For appending to a tab, use:

```json
{"insertText": {"endOfSegmentLocation": {"tabId": "t..."}, "text": "..."}}
```

Then re-read with `includeTabsContent=true` and verify the target tab, not just the document export.

## Formatting preference for weekly issue items

Raymond expects each new week to preserve the previous tab’s visual hierarchy exactly. First inspect the source tab’s Docs API `bullet.listId`, `nestingLevel`, `indentStart`, and `indentFirstLine`.

When the source uses native numbered lists, preserve that structure rather than typing markers:

1. Copy source paragraph text **without** visible `1.` / `a.` prefixes.
2. Apply the source hierarchy: top-level issue titles at `indentStart: 36pt`, `indentFirstLine: 18pt`; child details at `72pt` / `54pt`.
3. Create one native `NUMBERED_DECIMAL_ALPHA_ROMAN` list over the whole issue range so Docs supplies `1. / a. / b.` numbering.
4. Keep top-level titles bold and child detail/status lines normal-weight.
5. Add a sandbox item as the next top-level issue, not as detached paragraphs. Its status must clearly separate solved items from WIP/unresolved items and link only verified repo-qualified references.

Manual visible `4.` / `a.` text is an emergency fallback only when a native list has been proven to render incorrectly. Never combine manual markers with native bullets: it creates duplicate or misaligned numbering, especially on mobile.

After writing, re-read the target tab and require:

- exact target month/week tab and expected top-level/child counts
- native bullets at nesting levels 0 and 1
- zero manual numeric/alpha prefixes in paragraph text
- bold top-level titles, normal child lines, and the matching indent pattern
- verified GitHub links attached only to intended issue/PR references

## Copy style

Keep text concise and status-oriented. Example wording that fit the existing doc style:

```text
4. [WIP] Self-hosted E2B support for AIP cloud rollout (GDP-ADMIN/glaip-sdk#1500, GDP-ADMIN/ai-agent-platform#2267)
a. AIP needs changes across the GL AIP SDK / aip-agents runtime and the ai-agent-platform runner so cloud deployments can use the self-hosted E2B endpoint.
b. The SDK/aip-agents support is tracked in GDP-ADMIN/glaip-sdk#1500, and the cloud runner wiring is tracked in GDP-ADMIN/ai-agent-platform#2267.
c. AIP has already connected to the self-hosted E2B endpoint successfully in local validation.
d. Next step: deploy to dev and testing first, then promote to staging, beta, and production after the tests pass.
```
