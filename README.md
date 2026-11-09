# r-skills

A collection of reusable skills and workflows I use with AI coding assistants.

This repository is not limited to Hermes. Skills use a `SKILL.md` entry point with supporting references, scripts, or templates. Some workflows depend on a particular assistant, command-line tool, or service; read each skill's prerequisites before using it.

## Skills

| Skill | What it covers |
| --- | --- |
| [google-docs](google-docs/SKILL.md) | Create, edit, format, and publish Google Docs. |
| [google-forms](google-forms/SKILL.md) | Create and manage Google Forms through Google Apps Script. |
| [herdr-cli-app-live-mirroring](herdr-cli-app-live-mirroring/SKILL.md) | Preserve existing Herdr sessions while exposing remote/WSL views, forwarding Hermes/Codex sidebar status, and optionally discovering future CLI tabs automatically. |
| [pr_summary](pr_summary/SKILL.md) | Generate weekly GitHub pull-request activity summaries. |
| [weekly-report](weekly-report/SKILL.md) | Prepare weekly reports from work activity and reporting sources. |

## Use a skill

1. Open its `SKILL.md` and check the scope, prerequisites, permissions, and supporting files.
2. Clone or download this repository.
3. Install the entire selected skill folder into your assistant's supported skills directory. Keep `references/`, `scripts/`, and `templates/` with it.
4. Ask your assistant to load the skill. Adapt account names, paths, and project-specific assumptions to your environment.

For Hermes, the usual destination is `$HERMES_HOME/skills/`, or `~/.hermes/skills/` for the default profile. For other assistants, use their documented skill installation mechanism. Back up an existing same-name skill before replacing it.

Example request:

> Use herdr-cli-app-live-mirroring to expose my existing Herdr CLI agent tabs in the native app. Preserve the original running sessions and verify each attachment.

## Herdr mirroring: what is and is not shared

The Herdr skill documents a live-attachment workaround. Terminal Herdr and the native app use different backends. The workflow opens views of existing agent terminals without restarting those agents or duplicating their conversations.

Optional, explicitly authorized helpers now add Hermes/Codex Agents-panel status and automatic discovery of future CLI panes. The skill includes the tested bridge, safe shell waiting view, deduplicating watcher, configuration template, and unit tests. Plain shells are not misrepresented as agents. This is still **not** a unified backend or automatic restoration of killed AI processes; source detection errors can propagate into reported status. Read the installation, verification, and recovery limits before enabling automation.

## Sharing and safety

1. Publish only reviewed skill folders, not an entire assistant home directory.
2. Do not commit credentials, OAuth state, private keys, session transcripts, or machine inventories.
3. Keep reusable instructions separate from private operational records.
4. Treat scripts and instructions as code to review, not as an automatic grant of permission to change accounts or machines.

The newly added Herdr skill uses placeholders rather than personal machine addresses or session IDs. Existing skills may contain project-specific assumptions; review them before reuse.

## Repository history and licensing

This repository was previously named `hermes-skills`; it is now `r-skills` to reflect its broader scope.

Check each skill's license and attribution. A license declared by one skill does not automatically license every other folder in this repository.
