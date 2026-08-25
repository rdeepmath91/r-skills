# Setup Index

Use this index when onboarding a new environment or fixing auth/runtime preconditions.

## Primary
- `setup-and-dependencies.md` — Python env, package installs, API enablement, smoke checks.
- `auth-and-setup.md` — OAuth bootstrap/re-auth/token troubleshooting.

## Related
- `reliability-and-timeouts.md` — transport/retry/timeouts and flaky behavior during setup runs.
- `api-lessons.md` — durable pitfalls and API behavior notes.

## Suggested sequence
1. Run `setup-and-dependencies.md` checks.
2. Complete OAuth flow from `auth-and-setup.md`.
3. Validate with script help/compile checks.
4. If unstable, apply `reliability-and-timeouts.md` mitigations.
