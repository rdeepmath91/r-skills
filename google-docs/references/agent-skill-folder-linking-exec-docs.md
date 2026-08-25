# Agent skill-folder linking executive docs

Use this reference when drafting or revising boss-facing docs about agent skills, SkillBuilder/skill-creator flows, or parent-folder skill linking.

## Recommended approach

- Do not use the word `framing` in the stakeholder-facing doc; keep that as behind-the-scenes thinking only.
- Lead with the operational problem: an agent can use multiple skills, but one URL per skill makes skill-set changes require repeated agent configuration.
- Make two executive messages explicit and non-conflicting:
  1. Datasaur can provide a reusable skill-building skill, similar to Anthropic's skill-creator.
  2. AIP already supports agents using skills today; top-level folder linking is the code-level improvement that makes skill sets easier to manage.
- State the proposal plainly: each agent links once to one top-level GitHub skills folder; the runtime discovers child skill folders inside it.
- Explain that the improvement must be achieved through code, not manual doc/process convention: runtime resolves the parent folder, finds valid child skill folders, and loads them as the agent's resolved skill set.
- Make the current-vs-goal distinction explicit: AIP agents can already connect to skills stored in GitHub; the requested improvement is syncing new or updated child skills from the linked folder without another per-skill URL update or service redeploy.
- Explain the benefit in non-technical terms: Datasaur uses GitHub as the skill repository; the agent keeps one stable link while the skills inside that repo/folder can evolve.
- Describe the skill-building workflow as a skill, not an extra product surface. Use wording like “Datasaur can provide a SkillBuilder skill, similar to Anthropic’s skill-creator, so the team can build and improve new skills inside the same GitHub folder.”
- For this doc class, prefer the title `Datasaur Agent Skill Linking Improvement` over implementation-only titles like `Parent Folder Skill Linking`, unless the user explicitly wants the lower-level mechanism as the document title.
- Avoid making PR review the main executive message unless the user explicitly asks for governance. For this doc class, the main point is GitHub-as-skill-repo plus AIP runtime folder expansion.
- If comparing to Anthropic's pattern, link the phrase “skill-creator skill” cleanly; do not paste a raw URL into executive prose.
- Link the actual related repo when named. For Digital Employee, use `GDP-ADMIN/digital-employee` linked to `https://github.com/GDP-ADMIN/digital-employee`.

## Copy pattern

Problem: Datasaur team manages their skills in a GitHub repository, and AIP agents can already connect to skills stored in GitHub. The gap is that skill-set changes still require updating configured skill URLs and redeploying the service.

Recommendation: give each agent one top-level skills folder in GitHub, then link the agent once to that folder. The runtime can discover child skill folders inside it automatically and sync new or updated skills without another per-skill URL change or service redeploy.

Expected benefit: Datasaur uses GitHub as the skill repository while the agent link stays stable. The workflow stays code-controlled rather than relying on manual per-skill URL updates.

SkillBuilder note: one of Datasaur's agent skills can be a SkillBuilder skill, similar to Anthropic's skill-creator, so the team can draft, improve, and maintain new skills inside the same folder.

## Agent SDK code-change section

Use this when the user wants the implementation point made clear without adding a heavy technical section. Replace redundant comparison prose with a compact current/proposed SDK snippet. The important diff is the direct `Agent(..., skills=[...])` value: many child skill URLs today, one parent skills-folder URL after the improvement.

Link the actual repo name in the context line when known, for example `GDP-ADMIN/digital-employee` -> `https://github.com/GDP-ADMIN/digital-employee`. In the code block itself, prefer generic placeholders such as `https://github.com/<org>/<agent-skills-repo>` unless the user explicitly wants the concrete repo URL shown there.

```python
# Current: attach skill URLs one by one
agent = Agent(
    name="datasaur-digital-employee",
    skills=[skill1_url, skill2_url, skill3_url],
)

# Proposed: attach the parent skills repo once
skill_repo_url = "https://github.com/<org>/<agent-skills-repo>"

agent = Agent(
    name="datasaur-digital-employee",
    skills=[skill_repo_url],
)
```

Follow with one short implementation sentence: `AIP resolves skill_repo_url, discovers the child skill folders inside it, and runs the agent with the resolved skill set.` Do not make PR review the main activation message unless the user explicitly asks for governance.

## Agent SDK example pattern

When the doc needs a code example, use the visible GitBook-style `Agent(..., skills=[...])` shape rather than internal wrapper/config classes.

Current:
```python
agent = Agent(
    name="datasaur-digital-employee",
    skills=[skill1_url, skill2_url, skill3_url],
)
```

Proposed:
```python
skill_repo_url = "https://github.com/GDP-ADMIN/digital-employee/tree/main/skills"

agent = Agent(
    name="datasaur-digital-employee",
    skills=[skill_repo_url],
)
```

Keep the point narrow: the code still passes a skills list; the diff is many child skill URLs versus one parent skills-folder URL. Do not use `SkillConfig` in executive docs when the public/GitBook sample shows direct `Agent(..., skills=[...])`.

## Layout and formatting pitfalls

- Preserve the narrative distinction: AIP agents can already connect to GitHub-hosted skills; the requested improvement is syncing changes from one parent GitHub skills folder without per-skill URL edits or service redeploys.
- Spell out `Datasaur`; do not abbreviate it as `DS` in stakeholder docs.
- When explaining how new skills are created, say one of Datasaur's agent skills can be a `SkillBuilder` skill that builds or maintains new skills inside the same GitHub folder.
- For explanation-heavy summary sections, keep lists compact but add visible breathing room between explanatory paragraphs (`Skill repository approach`, `AIP improvement`, `Expected result`, SDK runtime notes). Too-tight paragraph spacing reads cramped even when the page count is correct.
- Prefer compact prose or a tiny hierarchy over a code block/tree when page budget matters.
- Under a `Summary` heading, do not add another `Problem statement` subheading unless the user explicitly asks for that structure. Use short executive prose paragraphs instead, with bold lead phrases only where they clarify the narrative.
- Avoid adding a third diagram when existing before/after diagrams already explain the mechanism.
- Avoid redundant bottom comparison sections. If diagrams already show before/after, use the bottom section for the concrete SDK call-shape diff instead.
- After `replace-section --no-simple-lists`, inspect export/PDF for literal Markdown such as `**Problem:**` or `[link](url)`. If it appears, rewrite as plain text and apply bold/link styling via the Docs API.
- Re-export to PDF and render contact sheets after section replacement; watch for code snippet spacing spilling a small tail onto a third page. Tighten the snippet or shorten surrounding prose rather than accepting a sparse spillover page.
- Link real repositories in the document context instead of leaving plain repo names. For Digital Employee, use `https://github.com/GDP-ADMIN/digital-employee` when that repo is the stated target.
- When the user says paragraph or explanation spacing is too tight, do not globally loosen every paragraph. Add breathing room only around explanatory paragraphs and labeled explanation blocks, while keeping numbered lists, captions, and code compact enough to preserve the page budget.
- After tightening or loosening spacing, re-export to PDF and render contact sheets again. Verify the intended readability change visually plus page count, diagrams, code readability, no blank pages, no clipping, no `SkillConfig`, and no unwanted PR-review/governance wording.