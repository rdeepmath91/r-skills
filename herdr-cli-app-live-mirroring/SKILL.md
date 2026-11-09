---
name: herdr-cli-app-live-mirroring
description: "Use when mirroring Herdr CLI agents in the native app."
version: 2.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [herdr, windows, wsl, ssh, live-mirroring]
    related_skills: [herdr-control]
---

# Herdr CLI → native app live mirroring

Expose existing terminal-Herdr agent panes as individual native-app tabs without restarting the agents, copying their conversations, or starting a second writer.

This is a compatibility workflow, not backend migration or a shared agent registry. Terminal `herdr` owns the original agents; native `herdr-core` (`hc`) owns attachment viewers. Direct attachment alone normally lacks native Agents-panel status. The optional tested status bridge and automatic watcher below add lifecycle reporting and discovery without starting replacement conversations.

## When to Use

Use when a user asks to expose existing terminal-Herdr panes in the native app, keep future tabs discoverable, forward agent status, make machine names consistent, or reconcile an interrupted rollout. Choose manual attachment for a bounded one-off operation; use the optional watcher only with explicit automation authorization. Never promise a unified backend or detection independent of the legacy source.

## Preconditions and scope

- Obtain authorization for the machines and tabs to expose. Manual `space.new`/`tab.new` can change selection; the optional watcher uses verified background label adoption instead. Persistent startup registration requires authorization too.
- Keep the original client, source panes, and servers intact. Never stop agents to populate a sidebar.
- Load `herdr-control` if available. Read each installed binary's help/skill; names and APIs differ between the terminal TUI and native app.
- Before legacy pane/agent control, follow the installed `herdr --skill` caller-context rules. Check `HERDR_ENV`; do not fabricate context or act on another client's focused pane.
- Discover actual executable paths. Native Windows installs may expose `herdr-core.exe`, not an `hc` alias. WSL tools can invoke Windows executables through `/mnt/c/...`.
- Read the native app's generated `AGENTS.md` before changing its layout. Typical locations: `~/.config/herdr-app/AGENTS.md` and the Windows user's equivalent. Do not edit generated guides or application-owned layout documents.

## Acceptance and reporting contract

- Establish the exact live exercise for each requested machine before dispatch: which existing agent must create the source tab, which fresh agent kind it must start, and what the watcher must detect without manual reconciliation. A controller-created tab, or an agent-created shell followed by a controller-started AI, does not satisfy an actor-created-agent-tab test.
- Report deployment, current one-to-one mappings, actor-driven end-to-end tests, activity-status accuracy, fresh-machine installation and reboot recovery separately. Mark each machine's requested exercise passed, blocked, waiting or untested; never turn a passing unit suite or one host's result into “all tested.”
- Before cleaning up a test pane or viewer, recheck its current task and queued input. Preserve it if the user has begun real work there; a test label or original creation authority is not continuing permission to close it.

## Naming domains: inspect the actual selected view

For a reported rename mismatch, identify the exact terminal and its app space/tab from the screenshot and live app membership before comparing legacy CLI labels. A native-only terminal can have a descriptive OSC terminal `title` shown in the Agents row while its app tab is still unnamed and displayed as `1`; core `name`, terminal `title`, legacy tab `label`, app-tab `name`, and space `name` are separate fields. Confirm each relevant field with `hc get` and `herdr-app ls`. A correct terminal title does not prove an app-tab rename occurred.

Do not treat this as a watcher failure when the terminal has no legacy attachment or `sync.key`: native-only tabs are deliberately outside the CLI watcher's naming scope. For a user-authorized app-tab rename, use explicit `herdr-app do tab.rename` IDs and preserve the requested spelling exactly. Read back the exact app tab and verify its terminal and live foreground process are unchanged. Never enable broad title-to-tab synchronization or mutate unrelated native-only tabs as a one-off fix. An inspection request alone is not authorization to choose and apply a new name.

## Read-only audit or interrupted rollout

For a request to inspect, simulate from a fresh context, or reconstruct existing mappings, do not install, register, rename, create views, focus tabs, send input, or change settings. Start with the existing catalogs and live metadata. Use [read-only discovery and mapping](references/read-only-reconstruction.md) to discover missing executable aliases and reconstruct exact source/destination bindings without historical manifests.

A metadata-only audit can verify process and pane bindings without reading screens. It does not satisfy conversation-screen, input-delivery, or full setup acceptance. Keep recognized agents, ordinary/unclassified panes, live native views and status-reporting views as separate counts. For a disputed mirrored status, join the exact source pane to `hc get` and app membership, inspect `herdr agent explain` and an authorized bounded source viewport, then resample both sides; a bridge can faithfully forward an incorrect source idle fallback. A screenshot shows only the current rendered sidebar region, not the entire inventory. Do not recreate an unmatched source view without authorization; a view may have been intentionally closed.

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

For a production rollout, save each batch to a private, durable manifest outside disposable scratch directories (directory mode 0700, files 0600). For a read-only audit, an explicitly scoped private scratch report is sufficient; do not publish it with the reusable skill. Record source machine/profile ID, session, workspace/tab labels, pane ID, agent kind/name, cwd, conversation reference when available, and destination identifiers/readback. Count/deduplicate with code; inventory is time-sensitive. Distinguish agent panes from ordinary shells, and do not read credential/setup panes without checking their purpose.

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
2. For authorized nonsensitive panes, `hc read RETURNED_TERMINAL --lines 0`: an actual source conversation screen appears, not a shell prompt, startup error, or ownership refusal. This returns the complete viewport; `--lines 0` is not a secrecy safeguard. Skip screens and screenshots for credential/setup panes or metadata-only audits, and report that visual acceptance is untested. Keep output bounded and private. Do not send a task or submit draft input merely to test attachment.
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
- Shared native agent registry: no. The optional bridge translates legacy detection into OSC 7501; direct attachment alone does not.
- Future source panes: automatic discovery only when the optional watcher is installed, running, unpaused, and both inventories are reachable. Manual mode requires explicit reconciliation.
- Shell-only panes: waiting views, not shared shells and not fake agents. A waiting view discards typed commands, then attaches when Hermes or Codex is recognized.
- Closed/dismissed views: do not blindly recreate them. The watcher preserves dismissal records; it does not deliberately close user tabs when a source disappears. A helper exiting may cause the native app itself to remove its finished tab.
- True backend migration: no. Existing processes remain owned by terminal Herdr.
- A verified startup entry can relaunch the watcher at Windows sign-in. This does not restore killed AI processes, prove an actual reboot test, or establish notification sounds. Core may recover a lost viewer into a shell; automatic source-agent restoration remains out of scope.
- Never resume a second agent against a live conversation as a workaround for missing sidebar status.
- Stop only an authorized viewer after checking its exact argv/identity, supported lifecycle and current ownership. If a user has adopted a test view for real work, leave it open unless closure is freshly authorized. Never use broad process kills or stop the source server. Verify original agents survive any viewer cleanup.
- To add a custom status bridge, obtain scope, implement/test separately, and verify actual native status transitions. A bridge that merely forwards legacy API state inherits legacy detector errors. Do not deploy unfinished helpers or imply their existence means synchronization works.

Final report: machine naming changes; verified live-view count by workspace; original-agent survival; remaining status/automation limits; durable manifest location. Do not claim full migration.

## 8. Optional status bridge and automatic discovery

For user-authorized ongoing mapping, follow [automatic watcher installation and acceptance](references/automatic-sync.md). The self-contained `scripts/` directory contains the actual bridge, safe shell waiter, watcher, and executable unit tests. Start from `templates/auto-sync-config.example.json`, substitute discovered absolute paths, and keep the real configuration/state private.

Do not count a shell waiting view as an agent. After rollout, independently join the current source inventory, native attachment argv/labels, app tab membership, and actual reported status; the watcher's bookkeeping count is not sufficient evidence of sidebar coverage. Reconcile any changes during the audit. Keep screenshots, operational manifests, addresses, and conversation IDs outside this public skill.

## Upstream compatibility context

At the time this workflow was checked, a project contributor explicitly stated the backends were separate and could not share agents. Recheck current support before concluding this workaround is still necessary:

- https://github.com/herdrdev/herdr-app/issues/63#issuecomment-6508292436
- https://github.com/herdrdev/herdr-core/issues/115
- https://github.com/herdrdev/herdr-app/issues/96
