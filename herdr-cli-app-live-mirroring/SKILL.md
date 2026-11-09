---
name: herdr-cli-app-live-mirroring
description: "Use when mirroring Herdr CLI agents in the native app."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [herdr, windows, wsl, ssh, live-mirroring]
    related_skills: [herdr-control]
---

# Herdr CLI → native app live mirroring

Expose existing terminal-Herdr agent panes as individual native-app tabs without restarting the agents, copying their conversations, or starting a second writer.

This is a compatibility workflow, not backend migration or automatic catalog synchronization. Terminal `herdr` owns the original agents; native `herdr-core` (`hc`) owns attachment viewers. Native app Agents-panel status is normally absent for these viewers.

## When to Use

Use when a user asks to expose existing terminal-Herdr tabs or agents in the native Herdr app, make their machine names consistent, or reconcile an interrupted live-mirroring rollout. Do not use to promise a unified backend, independent native lifecycle reporting, or automatic synchronization of future tabs.

## Preconditions and scope

- Obtain authorization for the machines and tabs to expose. Creating spaces/tabs changes the visible native app selection.
- Keep the original client, source panes, and servers intact. Never stop agents to populate a sidebar.
- Load `herdr-control` if available. Read each installed binary's help/skill; names and APIs differ between the terminal TUI and native app.
- Before legacy pane/agent control, follow the installed `herdr --skill` caller-context rules. Check `HERDR_ENV`; do not fabricate context or act on another client's focused pane.
- Discover actual executable paths. Native Windows installs may expose `herdr-core.exe`, not an `hc` alias. WSL tools can invoke Windows executables through `/mnt/c/...`.
- Read the native app's generated `AGENTS.md` before changing its layout. Typical locations: `~/.config/herdr-app/AGENTS.md` and the Windows user's equivalent. Do not edit generated guides or application-owned layout documents.

## 1. Distinguish and inventory both runtimes

Read-only discovery:

    herdr --help
    herdr --skill
    herdr --version
    hc --help
    hc --skill
    hc --version
    herdr-app --skill
    hc machine ls
    hc ls
    herdr-app ls
    herdr machine list --json

For the verified source machine/session, collect:

    herdr [--machine SOURCE_LABEL] [--session SESSION] agent list
    herdr [--machine SOURCE_LABEL] workspace list
    herdr [--machine SOURCE_LABEL] tab list --workspace LIVE_WORKSPACE_ID

These bracketed portions denote optional arguments, not literal shell syntax. `--machine` and `--session` cannot be combined in the legacy CLI; a saved machine already selects its remote session.

Save each batch to a private, durable manifest outside disposable scratch directories. Record source machine/profile ID, session, workspace/tab labels, pane ID, agent kind/name, cwd, conversation reference when available, and destination identifiers/readback. Count/deduplicate with code; inventory is time-sensitive. Distinguish agent panes from ordinary shells, and do not read credential/setup panes without checking their purpose.

One manifest row per source pane; retain original spelling. Preserve the source names unless the user requests changes. A tab's title may describe old work, not its current agent type.

## 2. Connect native core to a remote machine

See `references/connection-and-naming.md` for Windows SSH prerequisites and renaming.

Use the installed syntax:

    hc machine add VERIFIED_SSH_ALIAS --name VALID_NATIVE_NAME --install
    hc machine ls

Only use `--install` with installation authorization. Core must be installed alongside, not in place of, existing terminal Herdr. Native machine registration does not import legacy spaces or agents.

Verify a successful connection and actual endpoint version by reading back `hc machine ls`. Do not repeatedly add a machine after a timeout without checking whether registration succeeded.

## 3. Pilot one remote live view

Resolve the legacy executable on the source host. Noninteractive SSH PATH can omit `~/.local/bin`; inspect known absolute paths before declaring installation missing. Verify:

    /absolute/path/herdr agent attach --help

Read the source agent again immediately before attaching. Never add `--takeover` by default.

Create a native space with this payload shape:

    {
      "name": "SOURCE_WORKSPACE_LABEL",
      "machine": "NATIVE_MACHINE_NAME",
      "folder": "/source/working/directory",
      "tab": "SOURCE_TAB_LABEL",
      "argv": [
        "/absolute/path/herdr", "--session", "SOURCE_SESSION",
        "agent", "attach", "SOURCE_PANE_ID"
      ]
    }

Pass it as one JSON argument to `herdr-app do space.new`. Do not interpolate shell text or assume JSON escaping is shell quoting. A safe Python invocation is:

    result = subprocess.run(
        [app_executable, "do", "space.new", json.dumps(payload)],
        text=True, capture_output=True, timeout=30, check=True,
    )
    created = json.loads(result.stdout)

The native app may wrap remote argv in a login-shell launcher; root `sh` is not proof of failure. Save the returned `space`, `tab`, and `terminal` IDs before continuing.

## 4. Verify before expanding

For every attachment:

1. `hc get RETURNED_TERMINAL`: terminal is live; foreground argv identifies the intended legacy session/pane attachment.
2. `hc read RETURNED_TERMINAL --lines 0`: an actual source conversation screen appears, not a shell prompt, startup error, or ownership refusal. Keep output bounded and private. Do not send a task or submit draft input merely to test attachment.
3. Read source `agent list/get` again: original source pane still exists. Compare conversation identity where available. No replacement agent should have been launched.
4. `herdr-app ls`: intended machine/space/tab contains the exact destination terminal.
5. `herdr-app shot CHOSEN_PATH`: inspect the image before claiming visual verification. The app can return the last frame from a different selected space; a screenshot file alone does not prove the intended tab is shown.

Native `status: null`, `reported: false`, or an empty Agents panel can coexist with a working live terminal view. That is expected for this workflow; do not call it synchronized lifecycle status.

If any gate fails, preserve the manifest, report the exact blocker, and inspect actual state before retrying. A successful space-creation reply is not proof the attachment launched correctly.

## 5. Mirror the remaining panes one at a time

Group views by source workspace. Reuse the space ID returned by the first creation. Add subsequent tabs through `herdr-app do tab.new` with:

    {
      "space": "EXACT_RETURNED_SPACE_ID",
      "name": "SOURCE_TAB_LABEL",
      "folder": "/source/working/directory",
      "argv": ["/absolute/path/herdr", "--session", "SOURCE_SESSION", "agent", "attach", "SOURCE_PANE_ID"]
    }

Persist each destination mapping immediately, then verify it. Batch several short operations if useful, but never recreate an unverified success blindly. Inspect existing native spaces/terminals and recorded argv to avoid duplicate viewers when resuming interrupted work.

Re-inventory the source after rollout; agents can move or close during a long run. Declare exactly which inventory was mirrored and whether new/unmatched panes appeared. Machine connections, source-to-view mappings, and native lifecycle status coverage are separate totals.

## 6. Local WSL panes in the Windows native app

See `references/local-wsl.md`. Do not start Windows-native Hermes/Codex to imitate Linux sessions. Launch a viewer through `wsl.exe` that attaches to the actual WSL agent pane.

Keep the existing outer tab containing the nested TUI as fallback. Do not close it or switch off its server merely because direct views exist.

## 7. Limits, recovery, and report

- Same screen and input target: yes, verified by binding the viewer to the existing pane. Avoid simultaneous typing from two clients.
- Shared native agent registry: no. Legacy detection state does not automatically become OSC 7501 status in core.
- New or closed source tabs automatically mirrored: no. Refresh the inventory and reconcile explicitly.
- True backend migration: no. Existing processes remain owned by terminal Herdr.
- Reboot recovery, notification sounds, and automatic reattachment: not established by this workflow. Verify separately; core may recover a lost viewer into a shell rather than replaying the command.
- Never resume a second agent against a live conversation as a workaround for missing sidebar status.
- Stop only a viewer you created, after checking its exact argv/identity and supported lifecycle. Never use broad process kills or stop the source server. Verify original agents survive any viewer cleanup.
- To add a custom status bridge, obtain scope, implement/test separately, and verify actual native status transitions. A bridge that merely forwards legacy API state inherits legacy detector errors. Do not deploy unfinished helpers or imply their existence means synchronization works.

Final report: machine naming changes; verified live-view count by workspace; original-agent survival; remaining status/automation limits; durable manifest location. Do not claim full migration.

## Upstream compatibility context

At the time this workflow was checked, a project contributor explicitly stated the backends were separate and could not share agents. Recheck current support before concluding this workaround is still necessary:

- https://github.com/herdrdev/herdr-app/issues/63#issuecomment-6508292436
- https://github.com/herdrdev/herdr-core/issues/115
- https://github.com/herdrdev/herdr-app/issues/96
