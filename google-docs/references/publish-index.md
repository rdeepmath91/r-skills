# Publish and Refresh Index

Use this index for Markdown-to-Docs publishing and repeat refreshes.

## Primary
- `command-recipes.md` — command-level entry points for publish/update workflows.
- `markdown-pipeline.md` — source shaping and conversion behavior.
- `publishing-scope.md` — bound scope to requested subtree/doc family.

## Related
- `refresh-wrapper-pattern.md` — wrapper pattern for repeated refresh operations.
- `mermaid-images.md` — render/insert diagram assets during publish.
- `live-doc-promotion-and-page-audit.md` — safe preview->live promotion.

## Suggested sequence
1. Confirm scope via `publishing-scope.md`.
2. Run publish flow from `command-recipes.md` and `markdown-pipeline.md`.
3. Add assets (`mermaid-images.md`) as needed.
4. For repeated runs, apply `refresh-wrapper-pattern.md`.
5. If promoting, follow `live-doc-promotion-and-page-audit.md`.
