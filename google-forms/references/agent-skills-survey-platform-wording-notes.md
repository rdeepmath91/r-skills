# Agent Skills survey platform wording notes

Use this when designing surveys about "Agent Skills" adoption.

## Why wording matters
Users can confuse:
- built-in assistant behavior in an app, vs
- intentionally selecting/installing/creating reusable skills.

For adoption diagnostics, question stems should explicitly say:
- "intentionally used Agent Skills"

## Platform naming guidance
Prefer interface-based labels over brand buckets, especially for mixed PM/engineering audiences. Brands can appear as examples inside the interface option.

Recommended quick-intake options:
- Not yet
- Web chat / browser app (for example Claude web)
- IDE / editor agent (for example Cursor or VS Code)
- CLI / terminal agent (for example Claude Code, Codex CLI, OpenCode, or Hermes CLI)
- AIP / GLChat
- Other

Recommended stricter diagnostic options:
- IDE with skills support (e.g., Cursor)
- CLI agents with skills support (e.g., Claude Code, Codex CLI, OpenCode)
- Other
- I have not intentionally used Agent Skills yet

Avoid broad "Chat UI" wording unless your org confirms explicit Agent Skills support there; when the user wants PM-friendly options, use "Web chat / browser app" and give a concrete example such as Claude web.

## Lightweight evidence captured during session
- OpenCode skills doc is explicit:
  - Title: "Agent Skills | OpenCode"
  - URL: https://opencode.ai/docs/skills/
- Cursor docs navigation/metadata explicitly includes "Skills":
  - Title: "Cursor Docs — Agent, Rules, MCP, Skills & CLI"
  - URL: https://docs.cursor.com/context/rules
- Claude Code docs describe coding agent surfaces (terminal/IDE/etc.), but naming may differ from internal "Agent Skills" terminology:
  - Title: "Claude Code overview - Claude Code Docs"
  - URL: https://docs.anthropic.com/en/docs/claude-code/overview
- ChatGPT terminology is often "GPTs" and can be interpreted differently from explicit skill-install workflows:
  - Title: "Explore GPTs"
  - URL: https://chatgpt.com/gpts

## Question-structure pattern for mixed users (users + non-users)
- Benefit question should be multi-select, not single-select.
- Include both:
  - "No clear benefit yet"
  - "Not applicable (I have not intentionally used Agent Skills yet)"

## Two-session skill-sharing / brownbag survey pattern
Use this when an Agent Skills presentation is split into a general cross-functional session plus a technical AIP/GLConnector/custom-skills session.

Keep the existing adoption diagnostic core:
1. role
2. behavior-based familiarity/adoption stage
3. usage frequency window, phrased as "intentionally used Agent Skills"
4. where the user intentionally used skills
5. use cases
6. benefits with non-user option
7. primary blocker

Add session-planning questions:
- "Which session are you most interested in?" (single-select)
  - Session 1: General overview and use cases
  - Session 2: Technical usage with AIP + GLConnector
  - Both
  - Not sure yet
- "What do you want to learn from the general session?" (multi-select)
  - What Agent Skills are
  - How skills differ from prompts, tools, and MCP
  - Examples of useful skills
  - How my team can identify good skill candidates
  - How skills improve consistency and governance
  - Other
- "What do you want to learn from the technical session?" (multi-select)
  - How to use skills in AIP
  - How to discover/use skills from GLConnector
  - How to create a custom skill
  - Skill folder hierarchy and `SKILL.md` structure
  - Best practices for lean `SKILL.md` + references/scripts
  - Validation/testing before sharing
  - Versioning and production usage
  - Other
- "What repeated workflow should your team convert into a skill?" (paragraph). This is usually the highest-value planning input.
- Confidence ratings, 1-5:
  - use an existing Agent Skill today
  - create or request a custom skill

If the form API returns a blank title for an otherwise readable form, treat that as a form-quality issue before sharing; set a clear title such as "Agent Skills Sharing Session Survey".
