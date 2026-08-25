# Neutral comparison section editing

Use this when editing an existing Google Doc section that compares systems, tools, vendors, or architectural layers and the user asks for a strong but non-adversarial tone.

## Goal

Make the boundary clear without implying one option is globally better than the other.

Preferred framing:
- complementary layers
- boundary / ownership / center of gravity
- inner execution vs outer operations
- where each tool belongs
- what state or lifecycle each layer owns

Avoid framing:
- replaces / replaced by
- better / worse
- right tool / wrong tool when the user wants neutrality
- falls short / insufficient / adds no value
- cannot / has no, unless a precise hard limitation is necessary

## Workflow

1. Export the doc section first and inspect the exact text around the target heading.
2. If the user asks to improve/review/suggest wording, produce a draft change list or separate Markdown draft first. Do not edit the live doc unless the user explicitly says to apply the change.
3. Draft a short executive summary that states the boundary in 2-4 sentences.
4. Preserve headings the reviewer explicitly requested, even if they contain charged terms like `replaces`; add a clarification note under the heading instead. Example: `In this section, “replaces” means “is used instead of for this responsibility”; it does not mean one component is generally better.`
5. If headings are not explicitly required, rename charged headings before editing table cells. Example: change `X Replaces Y` to `When X Is the Inner Execution Layer` or `When Y Is the Operations Layer`.
6. Rewrite table columns toward ownership language:
   - `Why X is better` -> `Why this belongs in X`
   - `Why Y falls short` -> `Operational boundary`
7. Use targeted `replaceAllText` for simple visible-text edits when preserving existing native tables matters.
8. Re-export the section and scan only that section for charged comparison terms before handing off.

## Executive-reader pattern

For boss-facing appendices, reduce cognitive load before the tables:

- Add one simple concept diagram near the start when the distinction is layered or architectural.
- Use 2-4 high-level bullets only; avoid long vertical bullet stacks for details that belong inline or in tables.
- Put alternative phrasings in the Markdown draft so the user can choose emphasis before the live doc is touched.

## GL Runner / Prefect / GL Pipeline terminology pattern

When explaining this specific class of architecture comparison, prefer:

- **GL Runner**: product/runtime boundary that manages runnable execution.
- **Prefect**: operational orchestration backend used inside GL Runner.
- **Runnable**: unit of execution known to GL Runner.
- **GL Pipeline**: one possible runnable type that orchestrates the internal sequence of agent tasks.

Preferred one-liner: `GL Runner uses Prefect to run and manage runnables. GL Pipeline can be one of those runnables. Prefect orchestrates the runnable’s operational lifecycle; GL Pipeline orchestrates the runnable’s internal agent workflow.`

## Verification scan

After editing, search the edited section for terms like:

`replaces`, `better`, `worse`, `right tool`, `wrong tool`, `falls short`, `insufficient`, `adds no value`, `cannot`, `has no`, `not suited`

If a charged term remains, either neutralize it or make sure it is an intentional hard constraint rather than rhetorical comparison.
