# Multi-Doc Architecture Preview Packages

Use this when a user asks to refresh a family of live Google Docs (for example Architecture, Design, Implementation) from current repo evidence, but wants preview docs first.

## Workflow

1. Load the relevant docs skill plus any domain skills before inspecting sources.
2. Confirm source repos/branches and live doc IDs/tab IDs from user-provided links.
3. Read live doc headings first, not full exports, to understand current structure without swamping the terminal.
4. Inspect local repos and roadmap/issues for current facts. Separate:
   - implemented/current code paths,
   - valid roadmap/adoption items,
   - explicit non-goals or cautions.
5. Create local Markdown previews and diagram sources in a separate working folder.
6. Render diagrams to PNG and run fit/heuristic checks before uploading.
7. Create preview Google Docs only; do not overwrite live docs without explicit promotion approval.
8. Insert diagrams/images in a second pass after all preview docs exist.
9. Verify each preview doc through the Docs API:
   - title and first headings,
   - paragraph count roughly non-empty,
   - inline image count where diagrams were inserted.
10. Handoff with preview links, local paths, validation notes, and a clear “live docs not touched” statement.

## Content split pattern

For architecture/design/implementation packages, keep the main three docs readable and propose small linked docs when details grow large.

Main docs:
- Architecture: system boundaries, layers, primary flows, cross-cutting architecture lanes.
- Design: contracts, runtime mechanics, component responsibilities, data/event shapes at a summary level.
- Implementation: code-owned seams, endpoint inventory, rollout phases, tests, security/reliability notes.

Small docs candidates:
- context engineering/compaction,
- vision and image artifacts,
- usage reporting contract,
- A2UI/HITL user-gated interaction contract,
- SDK/CLI roadmap and platform convergence,
- test harness/evaluation/benchmark strategy.

## Pitfalls

- Do not turn roadmap issues into implemented facts. Mark them as planned/adoption until code confirms them.
- Do not claim a named “Harness” class exists unless code confirms it. It is often the execution envelope across SDK, backend, runner, runtime builder, event processor, tools, files, HITL, usage, and persistence.
- Do not put all exact schemas and roadmap slices into the main architecture doc; propose focused docs when the main narrative gets heavy.
- If `docs_api.py create --md` fails with 429 after creating the doc, recover the created doc from the traceback document ID instead of recreating it.
