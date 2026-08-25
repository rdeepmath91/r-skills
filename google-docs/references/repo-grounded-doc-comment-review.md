# Repo-grounded Google Doc comment review

Use this when a Google Doc review comment asks Raymond to review a section and the user provides a repository URL as reference/context.

## Workflow

1. Fetch current doc comments first.
   - Identify the exact unresolved thread that tags Raymond.
   - Use the comment anchor/quoted content to define scope.
   - If the comment is anchored to an appendix/section, keep the review scoped there unless the user explicitly broadens it.
2. Export/read the live document section.
   - Extract the section outline and line ranges.
   - Identify any cross-referenced sections, but label them as supporting context, not primary scope.
3. Inspect the referenced repo before drafting review comments.
   - Verify repo access, default branch, and current commit.
   - Check actual paths/imports/dependencies mentioned by the doc.
   - Prefer exact evidence from files over generic architecture advice.
4. Adjust review comments to repo reality.
   - Drop generic comments when the repo shows a more concrete concern.
   - Promote comments that point to mismatches between the doc and current repo structure.
   - If a path in the doc does not exist, make that a direct comment.
5. Return simple paste-ready comments.
   - Sort by impact.
   - For each item include only: `Highlight`, `Comment`, and optionally a short `Why` if the user asks for evaluation.
   - Keep comments short enough to paste into Google Docs.

## Comment quality bar

Good comments are specific and anchored:

- Highlight: `Create the registry at applications/glchat-be/glchat_be/plugin_registry.py exactly as in Section 3`
- Comment: `The repo already uses bosa_core.PluginManager / glchat_plugin in app startup. Can we align this with the existing plugin system instead of adding a separate registry?`

Avoid broad comments that could apply to any migration plan unless there is no repo-specific evidence.

## Common findings to check

- Existing plugin framework vs proposed new registry.
- Direct imports that contradict the proposed boundary, such as Community code importing Enterprise/AIP implementations.
- Directory-level split descriptions that hide route/service-method/DTO-level coupling.
- Private/internal dependencies and package indexes that block public OSS publishing.
- UI/backend paths in the doc that are stale relative to the repo.
- Public release checks beyond secret scanning: license compliance, private indexes, internal URLs, cert/key directories, generated artifacts, and customer/project identifiers.

## Scope discipline

If the tagged comment is anchored to Appendix A, keep the final list Appendix A-only. Related sections can be used as evidence, but do not include comments on those sections unless the user approves broader review.
