# Google OAuth profile routing

## Canonical Google Docs profile

Use the following profile for Google Docs read, review, export, preview, and publication work:

```bash
HERMES_HOME=/home/raymond-christopher/.hermes
```

It is paired with this skill's helpers:

```bash
python3 /home/raymond-christopher/.hermes/skills/productivity/google-docs/scripts/setup.py --check
python3 /home/raymond-christopher/.hermes/skills/productivity/google-docs/scripts/docs_api.py get DOC_ID --md
```

The profile is intentionally limited to the Docs and full Drive scopes required by this skill:

- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/drive`

## Do not cross-route Docs tasks

The broad `productivity/google-workspace` helper requests a wider scope set for Gmail, Calendar, Contacts, Sheets, Forms, and Drive. Do not invoke it with the canonical Docs profile for a Docs-only task. A refresh request that includes scopes the token never received can fail with `invalid_scope`, even though the Docs token is valid.

## Alternate profiles

Other local Google OAuth profiles are retained for recovery or account-specific work. Do not auto-discover and select them. Test or re-authorize an alternate profile only when the user explicitly needs a different Google account or broader Workspace capabilities.

## Verification

Before a Docs operation, run:

```bash
HERMES_HOME=/home/raymond-christopher/.hermes \
python3 /home/raymond-christopher/.hermes/skills/productivity/google-docs/scripts/setup.py --check
```

If that fails, use the Docs skill's re-authentication flow in `references/auth-and-setup.md`. Never copy or symlink token files into another profile as a workaround.
