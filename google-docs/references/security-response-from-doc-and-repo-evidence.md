# Security response drafts from Google Doc + repo evidence

Use when Raymond asks to check or improve a pasted email/reply against a Google Doc security finding and the local `ai-agent-platform` repo.

## Workflow

1. Read the pasted reply/email thread first and identify the exact question being answered.
2. Export the Google Doc as Markdown (`docs_api.py export DOC_ID --format md`) and review the finding, impact, and remediation sections.
3. If the claim depends on current implementation, verify it in the repo before drafting:
   - search for relevant env vars, toggles, guards, loaders, or sandbox code;
   - inspect the implementation path and docs;
   - use git history for origin/default changes when the reply references prior behavior.
4. Avoid reproducing exploit payload values or secret-like output. Use names/categories only.
5. Draft the reply as paste-ready text. Keep it concise, accountable, and security-aligned.
6. Include a short evidence note after the draft only if useful, with exact file paths/commits but no secret values.

## Framing rules for security-toggle replies

- Do not frame disabling a guard as a normal business requirement.
- Acknowledge the security concern directly: users should not be able to unmask/extract sensitive environment values.
- Describe toggles such as `ENABLE_SECURITY_GUARD` as temporary compatibility or break-glass exceptions when repo evidence supports that history.
- State the desired production/shared-deployment posture clearly: guard enabled, exceptions reviewed explicitly.
- Separate short-term remediation (enable guard, rotate/revoke exposed credentials, audit affected deployments) from longer-term remediation (isolated execution with clean/minimal environment).
- If prior wording says “disable if necessary,” rewrite it to “temporary compatibility exception” or equivalent bounded language.

## Evidence pattern from AIP custom-tool env exposure

Useful repo evidence pattern:

- Google Doc finding: custom tool execution can read server-side `os.environ` and expose credentials.
- Runner loader path: `applications/ai-agent-platform-runner/runner/loader/custom_tool_loader.py`.
- Environment guard path: `applications/ai-agent-platform-runner/runner/security/environment_guard.py`.
- Docs path: `applications/ai-agent-platform-backend/docs/custom-tools.md`.
- Git history can show when the guard was added, made configurable, or default behavior changed.

Preferred reply shape:

1. Thank/acknowledge the concern.
2. State there is no normal business requirement to expose secrets.
3. Explain the guard/toggle context briefly.
4. Give the current position as numbered points.
5. Close with remediation direction.
