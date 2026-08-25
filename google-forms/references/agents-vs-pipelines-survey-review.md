# Agents vs Pipelines survey review pattern

Use this when reviewing or designing a Google Form intended to learn how teams choose between agents, deterministic pipelines, and hybrid architectures.

## Core principle

Make one response represent one project/feature/architecture decision, not one respondent. If a respondent has multiple projects with different choices, ask them to submit the form once per project.

This enables a project registry and a decision-mechanism analysis at the same time.

## Recommended structure

### A. Project index

Use structured fields so the responses sheet can become a list of projects:

1. Project / feature / service name — short answer
2. Team — short answer or dropdown
3. Respondent role — dropdown
4. Project stage — single-select
   - Design / planning
   - Prototype / PoC
   - Internal use
   - Production
   - Replaced / deprecated
5. Architecture choice — single-select
   - Pure pipeline
   - Pure AI agent
   - Hybrid: agent orchestrates pipeline tools
   - Hybrid: pipeline calls an agent for one step
   - Still undecided
   - Other

### B. Decision mechanism

Capture why the decision happened in analyzable fields before asking for prose:

6. What triggered this architecture choice? — multi-select
   - Existing pipeline was enough
   - Needed LLM reasoning/judgment
   - Needed flexible tool orchestration
   - Needed strict schema / deterministic output
   - Needed low latency
   - Needed auditability/reproducibility
   - Needed human approval
   - Requirements were still changing
   - Team already had template/SDK support
   - Other

7. Which factors mattered most? — select up to 3
   - Reliability
   - Flexibility
   - Speed to build
   - Maintainability
   - Cost/token usage
   - Latency
   - Security/access control
   - Evaluation/testing ease
   - Observability/debugging
   - Existing SDK/template availability
   - User experience

8. Which factor was the deciding factor? — single-select using the same list.

Multi-select reveals what mattered; single-select reveals what won.

### C. Context

9. What kind of task was it? — multi-select
   - Data extraction/parsing
   - Document processing
   - RAG/search
   - Workflow automation
   - Decision support
   - Code/developer workflow
   - Chat/user interaction
   - QA/evaluation
   - Reporting/analytics
   - Other

10. What was true about the task? — multi-select
   - Input was structured
   - Input was messy/open-ended
   - Output schema was strict
   - Execution flow was predictable
   - Execution flow depended on context
   - Errors were high risk
   - Low latency was required
   - Cost/token budget was tight
   - Needed multiple tools/APIs
   - Needed human review

### D. Outcome / lesson

11. How well did the choice work? — rating 1-5
12. If restarting today, would you choose the same architecture? — single-select
   - Yes
   - Mostly yes, with changes
   - No
   - Not sure
13. Why? — optional paragraph

## Review checklist

- Fix visible numbering bugs before distribution.
- Avoid packing many subquestions into one required paragraph. Split repeated dimensions into structured fields.
- Keep only one required free-text rationale question if response friction matters.
- Add a project-stage option so PoCs and experiments are not forced into “production.”
- Prefer simple hybrid labels:
  - “Hybrid: agent orchestrates pipeline tools”
  - “Hybrid: pipeline calls an agent for one step”
- Include outcome questions so the audit can identify which decision patterns actually worked.

## Analysis views this enables

Project list view:
- Project
- Team
- Stage
- Architecture choice
- Deciding factor
- Outcome rating
- Would choose again?

Decision-mechanism view:
- Architecture choice → common deciding factors
- Task conditions → architecture choice
- Team → patterns
- Outcome rating → which decisions worked
- Restart answer → architecture regrets
