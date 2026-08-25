# AIP Current Issues tab update pattern

Use when Raymond asks to add or correct AIP issue status in the `AIP Current Issues` Google Doc, especially for a specific week/month tab.

## Trigger

- User references AIP weekly issues, previous weekly report issue mappings, or asks to fill/update the AIP issues Google Doc.
- User gives GitHub issue links and asks for a rephrased status update.

## Workflow

1. Verify source issues first.
   - Use GitHub issue metadata for every referenced issue: repo, number, title, state, URL, labels, created/updated time.
   - Do not rely on a bare `#1234` from a report; it may resolve to a PR or a different repo.
2. Locate the canonical `AIP Current Issues` Google Doc.
   - Drive search for `name contains 'Current Issues'` and confirm the title is exactly `AIP Current Issues`.
3. Read with `includeTabsContent=true`.
   - Parent month tabs can be empty; the real content is often in child tabs such as `Week 4 Jun 2026`.
   - Walk `tabs[]` and `childTabs[]`; match the requested week by tab title and keep the `tabId`.
4. Insert into the target child tab only.
   - Use Docs `batchUpdate` with `insertText.endOfSegmentLocation.tabId`.
   - Avoid whole-doc section replacement; this doc is tabbed and stable URLs matter.
5. Match existing AIP issue style.
   - If the surrounding tab uses visible numbered issues with alpha subpoints, continue that format. Do not append a detached bold paragraph block after a blank line.
   - Preferred mobile-readable shape: `4. [WIP] ...` as the title, then indented `a.`, `b.`, `c.` subpoints.
   - First/title line: status prefix such as `[WIP]`, bold.
   - Body subpoints: normal text, not bold.
   - Link GitHub refs directly on the visible repo/issue text, e.g. `GDP-ADMIN/glaip-sdk#1500`.
   - If native Docs bullets produce bad nesting or mobile rendering, use visible manual `4.` / `a.` labels with paragraph indents matching the prior entries; see `references/aip-current-issues-tab-update-pattern.md`.
6. Read back and verify.
   - Re-fetch the same `tabId` with `includeTabsContent=true`.
   - Confirm the inserted text, both issue refs, and link targets are present.
   - Inspect text runs if styling matters: title bold, body not bold, links attached only to issue refs.

## Wording pattern

Use concise status-forward language:

```text
[WIP] <issue title / theme> (<repo>#<issue>, <repo>#<issue>)
AIP needs changes across <surface A> and <surface B> so <deployment/runtime goal> can work.
The <first surface> work is tracked in <repo>#<issue>, and the <second surface> work is tracked in <repo>#<issue>.
<Current validation status>.
Next step: deploy to <first environments>, then promote to <later environments> after tests pass.
```

## Pitfalls

- Do not ask for confirmation if the user named the exact week and provided the issue links; verify and update.
- Do not append to the parent month tab; it may contain only a newline.
- Do not leave body paragraphs bold because the preceding title style can bleed into inserted text.
- Do not assume `#N` belongs to `ai-agent-platform`; include the repo-qualified issue reference in the doc when ambiguity exists.
