#!/usr/bin/env python3
"""Conservative legacy Herdr viewer synchronizer; never starts an AI writer."""
import argparse
from collections import Counter
from contextlib import contextmanager
import fcntl
import hashlib
import math
import json
import os
from pathlib import Path
import shlex
import subprocess
import time
import uuid


class Unavailable(Exception):
    pass


def source_key(source):
    identity = [source[k] for k in ('machine', 'session', 'pane', 'terminal')]
    return hashlib.sha256(json.dumps(identity, separators=(',', ':')).encode()).hexdigest()


class Store:
    def __init__(self, directory):
        self.path = Path(directory)
        self.path.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(self.path, 0o700)

    @contextmanager
    def lock(self):
        fd = os.open(self.path / 'watcher.lock', os.O_RDWR | os.O_CREAT, 0o600)
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Unavailable('already-running') from None
            yield
        finally:
            os.close(fd)

    def load(self):
        path = self.path / 'state.json'
        return json.loads(path.read_text()) if path.exists() else {'sources': {}, 'baseline': [], 'groups': {}}

    def paused(self):
        return (self.path / 'paused').exists()

    def set_paused(self, paused):
        if paused:
            fd = os.open(self.path / 'paused', os.O_WRONLY | os.O_CREAT, 0o600)
            os.close(fd)
        else:
            (self.path / 'paused').unlink(missing_ok=True)

    def save(self, state):
        path = self.path / ('state.' + uuid.uuid4().hex)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(state, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(path, self.path / 'state.json')
        fd = os.open(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def attachment(argv, machine):
    if not argv or not all(isinstance(a, str) for a in argv):
        return None
    argv = list(argv)
    base = argv[0].replace('\\', '/').split('/')[-1].lower()
    if base in ('powershell.exe', 'pwsh.exe'):
        try:
            index = next(i for i, a in enumerate(argv) if a.lower() == '-command')
            argv = shlex.split(argv[index + 1].removeprefix('& '))
        except (ValueError, IndexError, StopIteration):
            return None
        return attachment(argv, machine)
    if base == 'wsl.exe':
        if machine.get('nativeName') is not None:
            return None
        try:
            distro = argv[argv.index('--distribution') + 1]
            if distro != machine['distro']:
                return None
            argv = argv[argv.index('--exec') + 1:]
        except (ValueError, IndexError):
            return None
        return attachment(argv, machine)
    bridges = [machine['home'] + '/.local/share/herdr-native-status-bridge/' + name
               for name in ('legacy_hc_bridge.py', 'wait_for_agent.py')]
    if base in ('python3', 'python') and len(argv) > 1:
        # The validated staging launcher keeps the eventual argv after its gate.
        if argv[1] == '-c' and len(argv) > 5:
            return attachment(argv[4:], machine)
        if argv[1] not in bridges:
            return None
        args = argv[2:]
        if len(args) == 5 and args[:2] == ['--herdr', machine['herdr']] and args[2] == '--session':
            return args[3], args[4]
        return None
    if argv[0] not in (machine['herdr'], 'herdr'):
        return None
    args = list(argv[1:])
    session = 'default'
    if args[:1] == ['--session'] and len(args) >= 2:
        session, args = args[1], args[2:]
    if len(args) == 3 and args[:2] == ['agent', 'attach']:
        return session, args[2]
    return None


def app_targets(app, machine):
    targets = {}
    for space in app['spaces']:
        if space.get('machine') != machine.get('nativeName'):
            continue
        for tab in space['tabs']:
            for terminal in tab['terminals']:
                targets[terminal['terminal']] = (space, tab)
    return targets


class Transport:
    def __init__(self, config, run=None):
        self.config = config
        self.run = run or self.command

    def command(self, argv):
        try:
            result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL, timeout=self.config.get('timeout', 8), check=True)
            value = json.loads(result.stdout)
            if not isinstance(value, dict) or value.get('error') or value.get('ok') is False:
                raise ValueError('failed response')
            return value
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            raise Unavailable(type(exc).__name__) from None

    def sources(self, machine):
        prefix = machine['sourcePrefix']
        workspaces = self.run(prefix + ['workspace', 'list'])['result']['workspaces']
        sources = []
        for workspace in workspaces:
            wid = workspace['workspace_id']
            tabs = self.run(prefix + ['tab', 'list', '--workspace', wid])['result']['tabs']
            panes = self.run(prefix + ['pane', 'list', '--workspace', wid])['result']['panes']
            tabs = {t['tab_id']: t for t in tabs}
            for pane in panes:
                tab = tabs[pane['tab_id']]
                sources.append(dict(machine=machine['id'], session=machine['session'],
                    pane=pane['pane_id'], terminal=pane['terminal_id'], tab=pane['tab_id'],
                    workspace=wid, name=tab.get('label') or pane['tab_id'],
                    workspaceName=workspace.get('label') or wid, cwd=pane['cwd']))
        return sources

    def snapshot(self, config):
        # Never call hc (which can auto-start a core) unless a window answers first.
        try:
            app = self.run([config['app'], 'ls'])
            if not isinstance(app['spaces'], list):
                raise ValueError('invalid layout')
            inventory = self.run([config['hc'], 'ls', '--json'])
            rows = inventory['terminals']
            connected = {m['name'] for m in inventory.get('machines', []) if m['state'] == 'connected'}
        except (KeyError, TypeError, ValueError) as exc:
            raise Unavailable(type(exc).__name__) from None
        result = {}
        for machine in config['machines']:
            mid, name = machine['id'], machine.get('nativeName')
            result[mid] = None
            if name and name not in connected:
                continue
            try:
                sources = self.sources(machine)
                terminals = []
                for row in rows:
                    address = row['address']
                    owner = address.split('/')[0] if '/' in address else None
                    if owner != name or row['state'] != 'live':
                        continue
                    raw = self.run([config['hc'], 'get', address, '--json'])
                    terminals.append({k: raw.get(k) for k in ('address', 'labels', 'argv', 'foreground')})
                result[mid] = sources, terminals
            except (Unavailable, KeyError, TypeError, ValueError):
                continue
        return app, result

    def spawn(self, machine, source, record):
        args = ['/usr/bin/python3', machine['home'] + '/.local/share/herdr-native-status-bridge/wait_for_agent.py',
                '--herdr', machine['herdr'], '--session', source['session'], source['pane']]
        cwd = source['cwd']
        if machine.get('nativeName') is None:
            args = [r'C:\Windows\System32\wsl.exe', '--distribution', machine['distro'],
                    '--cd', cwd, '--exec'] + args
            cwd = self.config['windowsCwd']
        command = [self.config['hc'], 'run', '--json', '--bg', '--no-parent', '--no-notify', '--keep',
                   '--name', 'sync-' + source_key(source)[:24], '--cwd', cwd]
        if machine.get('nativeName'):
            command += ['--on', machine['nativeName']]
        for key, value in {'herdr.space': record['space'].split('/')[-1],
                           'herdr.tab': record['tab'].split('/')[-1],
                           'sync.key': source_key(source), 'sync.source': machine['id']}.items():
            command += ['--label', key + '=' + value]
        self.run(command + ['--'] + args)

    def rename(self, kind, target, name):
        self.run([self.config['app'], 'do', kind + '.rename', json.dumps({'id': target, 'name': name})])
        app = self.run([self.config['app'], 'ls'])
        objects = app['spaces'] if kind == 'space' else [t for s in app['spaces'] for t in s['tabs']]
        if not any(o['id'] == target and o['name'] == name for o in objects):
            raise Unavailable('rename-unverified')


class Watcher:
    def __init__(self, config, store, transport):
        self.config, self.store, self.io = config, store, transport

    def tick(self, include_existing=False):
        if self.store.paused():
            return
        state = self.store.load()
        try:
            app, machines = self.io.snapshot(self.config)
        except Unavailable:
            return
        for machine in self.config['machines']:
            mid = machine['id']
            if machines.get(mid) is None:
                continue
            sources, native = machines[mid]
            keys = {source_key(s) for s in sources}
            for key, record in state['sources'].items():
                if record['source']['machine'] == mid:
                    record['present'] = key in keys
            cold = mid not in state['baseline']
            targets = app_targets(app, machine)
            for source in sources:
                key = source_key(source)
                group = json.dumps([mid, source['session'], source['workspace']])
                record = state['sources'].get(key)
                tabs = {tab['id'] for _, tab in targets.values()}
                if record and record['status'] == 'active' and record['tab'] not in tabs:
                    record['status'] = 'dismissed'
                if record and record['status'] == 'dismissed':
                    continue
                match = next((t for t in native if
                    t.get('labels', {}).get('sync.key') == key or
                    (not t.get('labels', {}).get('sync.key') and
                     (attachment((t.get('foreground') or {}).get('argv', []), machine) or
                      attachment(t.get('argv', []), machine)) == (source['session'], source['pane']))), None)
                if match and match['address'] in targets:
                    space, tab = targets[match['address']]
                    record = dict(source=source, status='active', space=space['id'], tab=tab['id'])
                    state['sources'][key] = record
                    state['groups'][group] = space['id']
                    try:
                        if tab['name'] != source['name']:
                            self.io.rename('tab', tab['id'], source['name'])
                        if space['name'] != source['workspaceName']:
                            self.io.rename('space', space['id'], source['workspaceName'])
                    except Unavailable:
                        state['last_error'] = 'rename-unavailable'
                    continue
                if match:
                    state['sources'].setdefault(key, dict(source=source, status='unmapped'))
                    continue
                if record and record['status'] == 'ambiguous' and time.time() >= record.get('retryAfter', float('inf')):
                    # The deterministic hc --name is a second, server-side uniqueness fence.
                    # Reuse the durable tab/space intent even if an earlier reply was lost.
                    record['retryAfter'] = time.time() + 60
                    self.store.save(state)
                    try:
                        self.io.spawn(machine, source, record)
                    except Unavailable:
                        pass
                    continue
                if record and not (record['status'] == 'suppressed' and include_existing):
                    continue
                record = dict(source=source, status='suppressed')
                state['sources'][key] = record
                if cold and not include_existing:
                    continue
                space = state['groups'].setdefault(group, uuid.uuid4().hex)
                record.update(status='ambiguous', retryAfter=time.time() + 60,
                              space=space, tab=uuid.uuid4().hex)
                self.store.save(state)
                try:
                    self.io.spawn(machine, source, record)
                except Unavailable:
                    pass
            if cold:
                state['baseline'].append(mid)
        state['last_scan'] = time.time()
        state['worker_pid'] = os.getpid()
        state['online_machines'] = [m for m, value in machines.items() if value is not None]
        self.store.save(state)


def main(argv=None, transport_factory=Transport):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True)
    modes = parser.add_mutually_exclusive_group()
    for flag in ('once', 'status', 'pause', 'resume'):
        modes.add_argument('--' + flag, action='store_true')
    parser.add_argument('--include-existing', action='store_true')
    args = parser.parse_args(argv)
    try:
        config = json.loads(Path(args.config).read_text())
        store = Store(config['stateDir'])
        if args.pause or args.resume:
            store.set_paused(args.pause)
        if args.status or args.pause or args.resume:
            state = store.load()
            print(json.dumps(dict(paused=store.paused(), baseline=state['baseline'],
                worker_pid=state.get('worker_pid'), last_scan=state.get('last_scan'),
                online_machines=state.get('online_machines', []),
                counts=dict(Counter(r['status'] if r.get('present') is not False else 'source_absent'
                                    for r in state['sources'].values())))))
            return 0
        with store.lock():
            watcher = Watcher(config, store, transport_factory(config))
            while True:
                watcher.tick(include_existing=args.include_existing)
                if args.once:
                    return 0
                time.sleep(config.get('interval', 5))
    except (Unavailable, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': type(exc).__name__}))
        return 1
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
