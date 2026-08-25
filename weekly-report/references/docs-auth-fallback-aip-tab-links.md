# Docs-auth fallback: AIP tab links

When weekly-report discovery cannot access Google Docs/Drive but a recent session has an AIP Current Issues URL:

1. Label it as the canonical/root AIP document link, not the current-week tab.
2. Do not infer or invent a `?tab=` value. A week-specific tab link requires a live `includeTabsContent=true` read and a matched child-tab title/tabId.
3. State that the live weekly report was not read or modified, then provide any locally generated fallback payload separately.
4. Name the concrete recovery: reauthorize Google with Docs and full Drive scopes, then re-run discovery/export before filling or validating the live report.

This prevents a historical document URL from being presented as verified current-week source state.
