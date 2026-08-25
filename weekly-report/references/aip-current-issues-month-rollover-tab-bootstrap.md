# AIP Current Issues month-rollover tab bootstrap

Use when the current reporting week has no matching parent month / child-week tab in the canonical `AIP Current Issues` Google Doc.

## Preconditions

- The user has explicitly asked to create the missing period tab(s), or creation is part of the established weekly-report workflow.
- Verify a refreshable OAuth token with Docs and Drive scopes first. Do not create anything from stale tab metadata.

## Procedure

1. Fetch the document with `includeTabsContent=true` and walk both `tabs[]` and every `childTabs[]`.
2. Match the parent naming convention exactly (`July 2026`) and the child convention exactly (`Week 2 Jul 2026`). For the Saturday 5–11 July 2026 report window, use `Week 2 Jul 2026`.
3. If the month parent is missing, call `documents.batchUpdate` with `addDocumentTab` and `tabProperties.title` set to the month label.
4. Re-read or use the `addDocumentTab` reply to obtain the parent `tabId`.
5. If the week child is missing, create it with `addDocumentTab` and `tabProperties` containing its title and `parentTabId`.
6. Re-fetch with `includeTabsContent=true`; verify the child title, `tabId`, and `parentTabId`, and confirm it is initially empty before inserting issue content.
7. Build the stable share URL as `https://docs.google.com/document/d/<DOC_ID>/edit?tab=<TAB_ID>`.

## Guardrails

- Never create a second month/week tab merely because a shallow top-level search did not show a nested child.
- Do not populate an empty newly created tab until issue/PR sources have been verified.
- Use `addDocumentTab`; `updateDocumentTabProperties` is for rename/reparent/reorder only.
- Report both the parent and the child URL/ID verification after creation.
