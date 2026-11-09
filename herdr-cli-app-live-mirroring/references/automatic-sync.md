# Automatic CLI-to-native-app views

## Scope and components

This opt-in compatibility layer preserves the running legacy agents. It does not merge registries or copy conversations. The graphical app runs on the viewing Windows computer, not on every remote machine.

- `scripts/legacy_hc_bridge.py`: PTY relay around `herdr agent attach`; forwards input, terminal output and resize, polls the source, and emits OSC 7501. Only Hermes and Codex are accepted. Status-query failures report error, never fake idle. The source detector can still be wrong.
- `scripts/wait_for_agent.py`: explicitly labelled, noninteractive waiting screen for an ordinary source shell. It discards input, emits no fake agent status, polls positional `pane get PANE`, and execs the neighbouring bridge when a supported agent is recognized. It never starts an AI agent.
- `scripts/watcher.py`: observes configured legacy source sessions and native core/app metadata, adopts existing attachments, adds missing/new views, and propagates source labels. It does not submit prompts, restart source servers, or close source panes.

Linux/POSIX Python 3 with stdlib is required on source hosts and for the watcher; this implementation runs the watcher inside WSL and calls the Windows executables. Verify compatible installed `herdr`, `hc`/`herdr-core.exe`, and `herdr-app.exe` help. The rollout used legacy Herdr 0.9.5 and native core 0.1.18; treat that as a tested version pair, not a guarantee for later versions.

## Before installation

1. Obtain authorization for the exact source machines/sessions, native layout changes, and any persistent startup registration. Respect the installed Herdr caller-context rule; never fabricate `HERDR_ENV` to authorize interactive pane/agent control.
2. Read the generated native app guide. Inventory both machine catalogs and verify each remote alias really reaches the intended legacy session and native endpoint. Machine connections alone do not import panes.
3. Reconstruct existing native attachments from live metadata. Recognized forms include direct legacy attach, the supplied bridge/waiter, validated staged Python launchers, and WSL/PowerShell wrappers. Do not read login or credential screens to discover bindings.
4. Save a private source/native mapping outside scratch, with directory mode 0700 and files 0600. Back up an existing helper installation, config, state and startup entry before replacing them.
5. Run the bundled tests from `scripts/`: `python3 -m unittest -v test_bridge test_wait_for_agent test_watcher`. Record the actual collected count and result rather than carrying forward an old total; live-machine acceptance is separate.

## Install and configure

Install these two files together on every selected Linux source host:

    ~/.local/share/herdr-native-status-bridge/legacy_hc_bridge.py
    ~/.local/share/herdr-native-status-bridge/wait_for_agent.py

Use discovered absolute home paths and the existing legacy executable. Copying the helpers must not replace Herdr, its server, or any agent. Verify deployed hashes against the tested files. Executable mode 0700 is appropriate for a private installation. The helpers run within each native viewer; no separate remote discovery daemon or graphical app is required.

Install `scripts/watcher.py` on the viewing WSL host. Copy `templates/auto-sync-config.example.json` to a private configuration location and substitute every placeholder with verified absolute paths. JSON values are literal: `~`, environment variables, and placeholder names are not expanded.

Each `machines` entry provides:

- `id`: stable unique local identity used in source keys; changing it changes identity.
- `nativeName`: null for this computer, otherwise the exact saved native machine name.
- `sourcePrefix`: argv for the existing legacy session. Local form is an absolute `herdr` path plus `--session SESSION`; remote form uses the saved `--machine LABEL` selector and must not also specify `--session`.
- `session`: the actual source session; remote saved profiles may select a non-default session, so discover it.
- `home`, `herdr`: absolute paths on that source host. Helpers are expected in the fixed relative directory above.
- `distro`: required for a local WSL source, using the exact installed distribution name.

Global `app` and `hc` paths point to Windows executables as seen from WSL; `windowsCwd` is a real Windows directory, not a Linux source cwd. `stateDir` must be a private, durable directory. `interval` is the sleep between scans, not a maximum detection-latency guarantee: network latency and per-terminal metadata reads add scan time. `timeout` bounds individual subprocess calls.

Do not publish the populated configuration, durable state, inventories, logs, or startup scripts containing personal paths.

## Baseline, start and controls

A first normal scan adopts existing views but suppresses other already-existing sources. That protects tabs the user intentionally closed. If the user explicitly requests mapping every current source, bootstrap once with:

    python3 /absolute/path/watcher.py --config /private/config.json --once --include-existing

Read back exact targets before retrying. Then run the long-lived watcher:

    python3 /absolute/path/watcher.py --config /private/config.json

Controls, using the same config:

    python3 /absolute/path/watcher.py --config /private/config.json --status
    python3 /absolute/path/watcher.py --config /private/config.json --pause
    python3 /absolute/path/watcher.py --config /private/config.json --resume

Pause stops discovery/renaming, not existing agent viewers or source agents. Resume removes the pause marker; it does not start a stopped daemon. Status includes the last successful scan, recorded worker PID, online machines and record counts. `source_absent` means absent in an online source inventory, not an active mapped agent. Offline machines retain their last-known mappings; counts can be stale during outages. Verify the exact live process command line and a fresh scan before claiming daemon health.

The private state directory is protected by a nonblocking process lock and atomic fsync/rename writes. A durable creation intent is saved before external writes. A deterministic per-source native `--name` is a server-side uniqueness fence for timeout/restart retries; ambiguous launches reuse the same space/tab intent after a cooldown rather than generating new IDs. Verify uniqueness behavior on the installed core before deploying.

The watcher adds views with `hc run --bg --no-parent --no-notify --keep`, labels `herdr.space`, `herdr.tab`, `sync.key`, and `sync.source`; app adoption creates the actual tab without selecting it. Renames use explicit app IDs and are retried after transient failures. Source identity includes machine, session, pane and original terminal ID. Native-only tabs remain untouched. Closing a mapped native tab while its source remains present records a dismissal rather than reopening it automatically. Preserve state across restarts; deleting it changes baseline/dismissal behavior.

Each source pane is a logical view; exact recreation of arbitrary split geometry is not promised. Unknown source workspaces get a new background-labelled space. Check app names and actual membership after adoption; a successful core launch alone is insufficient.

## Windows sign-in startup

With authorization, register a per-user Startup-folder shortcut to a hidden launcher. The verified mechanism is `wscript.exe //B //Nologo` running a small VBS file whose `WScript.Shell.Run(command, 0, False)` starts:

    C:\Windows\System32\wsl.exe --distribution VERIFIED_DISTRO --cd /absolute/wsl/home --exec /usr/bin/python3 /absolute/path/watcher.py --config /private/config.json

Quote the executable and arguments correctly; do not paste placeholders into a live startup entry. Keep the launcher on Windows, with the watcher/config in the intended WSL distribution. Read back the exact `.lnk` target/arguments, invoke that same launcher, then verify the new worker process and a completed scan. Do not claim an actual logoff/reboot test from a launcher-only test. A duplicate watcher must fail its lock without creating views.

Optional status/pause/resume shortcuts can call the controls through WSL. For a PowerShell shortcut, use an outer quoted `-Command` string and a single-quoted executable path inside it, e.g. `& 'C:\Windows\System32\wsl.exe' ...`; doubled empty quotes around a path can produce a broken command. Parse and execute the exact fixed control command, then read back pause state. Do not run it against arbitrary user-provided shell text.

If Windows Script Host is disabled, report that limitation and agree an alternative startup mechanism; do not weaken policy. This launcher can start WSL at sign-in. It does not restore source AI processes after a remote reboot or WSL shutdown, nor run while the laptop is suspended.

## Live acceptance gates

1. Re-inventory sources and native views; join bindings in code and check every intended source has exactly one live native view in the correct machine/space/tab.
2. Verify every recognized Hermes/Codex view has actual `reported` status and matching `status.app` in core, and the same status-bearing terminal appears in app metadata. Shell waiting views must have no fake app/status. Test activity accuracy separately: compare an authorized actual working/ready viewport with source detection and bridged state. Matching idle values on both APIs can still be an inaccurate source fallback; count attachment, reporting presence and reporting accuracy as different results.
3. For an actor-driven test, obtain authorized contact, verify the chosen agent is ready and has no unsent user draft or unrelated approval UI, and ask it to load its Herdr skill and verify its own caller context/control access. Require that actor to perform the requested source creation and agent startup, then read its actual reply and returned IDs. Do not substitute controller actions for either requested stage. If the requested exercise is only a shell-placeholder test, leave the new shell agent-free until that stage is observed.
4. Without manually running a reconciliation or creating a native tab, observe the running watcher create that source tab's app view. Read only the nonsensitive waiting screen and verify its warning.
5. For a separate shell-to-agent exercise, start an authorized idle test agent in that same owned shell; for an actor-driven creation/startup exercise, require the selected actor to start it. Do not resume an existing conversation, submit real work or create another writer. Verify the same native terminal switches to the bridge and reports the agent kind. If authentication/approval appears, do not inspect secrets or bypass the UI.
6. Rename the owned source tab and verify the same native tab receives the label, without duplication. Compare selection over a controlled short interval. Unrelated user navigation invalidates broad before/after focus assertions; it is not proof of watcher focus theft.
7. Repeat shell discovery for the other selected hosts; verify no duplicate AI processes are created. Pause/resume, restart only the verified watcher process, and confirm exact existing tab/terminal bindings survive without duplicate launches.
8. Recheck the test pane's current viewport/task, queued input and ownership before cleanup; an idle API badge can be stale. If the user has begun real work there, preserve the agent and both views, record the ownership transfer, and obtain fresh closure authorization instead of treating its test name as disposable. Otherwise gracefully exit the owned idle test agent, close only exact test source tabs, and verify absence. Native helper exit can remove its tab automatically; inspect before explicit close and treat an already-missing exact target as cleanup success. Never repeat a broad close after an ambiguous failure.
9. Re-inventory after cleanup. Compare original terminal identities and source survival with the baseline, recalculate counts, and inspect sidebar/screens only where nonsensitive and authorized. Report metadata verification and actual visual inspection separately.

### Actor access and readiness decisions

Keep a per-machine acceptance record with the selected actor, requested agent kind, actual creator/starter, source and native bindings, creation/detection result, activity-accuracy result, and any concrete blocker. Refresh current catalog counts independently; unrelated user closures or new panes can change totals while testing.

- If a worker cannot access its Herdr control socket, record the actor-driven exercise as blocked before tab creation, not as a watcher failure. Controller SSH/API access and supported agent kinds do not establish the worker's sandbox permissions. Request narrowly scoped approval, or obtain explicit permission to use a different already-authorized actor; do not weaken the worker's sandbox or silently substitute controller creation.
- If the approved actor is working or waiting on an unrelated user question, leave its work and UI untouched. For an authorized deferred check, use the installed blocking wait, for example `herdr --machine SOURCE_LABEL agent wait MAIN_PANE --until idle --until done --timeout 30000`; then re-read `agent get` and a bounded visible viewport before sending anything. A wait result is not an atomic reservation, and live background jobs are not completed merely because the parent shows a ready prompt.
- If a prompt returns `agent_prompt_stalled` or times out, inspect the actor's actual reply and source tab/agent inventories before retrying. Delivery and creation may already have succeeded while the activity detector missed the transition. Reuse the exact test label and agent name when a retry is authorized; never interpret the error alone as proof of no side effects.
- If the requested tests remain blocked or waiting, report that state plainly alongside the already-working mappings. Do not present a started waiter, queued prompt or background job as a completed test, and do not publish an unverified waiting harness as a proven installation recipe.

## Displaced or exited attachment viewers

When a source agent exists but its native tab is missing, inspect the exact former core terminal, its retained output and the source mapping before creating anything. Compare the original source terminal identity, core `state`/`exit_code`/`reason`, app membership and watcher record. An old viewer output of `herdr: server shut down: terminal attach taken over` can mean the attachment was displaced while the original source server and agent remain alive; verify those separately rather than interpreting the prefix as proof of server shutdown.

The current watcher classifies a missing tab from an active mapping as `dismissed` without distinguishing a user close from automatic removal after the viewer exits. It consequently will not restore such a view on its own. Record this limitation; do not describe arbitrary viewer-exit recovery as tested or implemented. Do not automatically add `--takeover` or repeatedly reconnect against another attachment owner.

With explicit authorization to restore only the missing viewer, verify there is no other live native viewer for the same source, back up private state, and use an ordinary attachment without `--takeover`. Refusal is a blocker, not permission to force ownership. Preserve the original agent and never launch another AI against its conversation. Reuse the intended native space/tab identity when valid, verify stable live attachment and status, then repair only that source's mapping. The daemon pause flag does not acknowledge an already-running scan: establish quiescence or exclusive access before editing state so a stale scan cannot overwrite the repair. Restore the prior pause state in a cleanup path, then re-read the exact tab, original source identity and active mapping. This manual recovery is not a fix to the watcher's disappearance classification.

## Failure boundaries

Do not restart source servers or agents for watcher failures. An unavailable machine is not an empty source catalog. The watcher does not promise automatic AI session resurrection, perfect source status detection, unified notification/seen-state behavior, or a shared interactive shell. Raw attach traffic is not a security boundary; authorized users with an attached viewer can interact with the source agent, so avoid simultaneous typing from two clients.

Keep test logs and private manifests outside the shared skill. Publish only reviewed code, synthetic fixtures, templates and reusable instructions. Re-run tests from the actual packaged scripts, not merely from an earlier build directory.
