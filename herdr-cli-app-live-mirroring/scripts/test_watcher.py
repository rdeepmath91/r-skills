import copy
import tempfile
import unittest
from pathlib import Path
import watcher as w


M = dict(id='local', nativeName=None, sourcePrefix=['/home/tester/.local/bin/herdr', '--session', 'default'],
         session='default', home='/home/tester', herdr='/home/tester/.local/bin/herdr', distro='Ubuntu')
S = dict(machine='local', session='default', pane='w1:p1', terminal='term_1', workspace='w1',
         tab='w1:t1', workspaceName='master', name='setup', cwd='/home/tester')


class Fake:
    def __init__(self):
        self.sources = [copy.deepcopy(S)]
        self.native = []
        self.app = {'spaces': []}
        self.writes = []
        self.offline = False
        self.timeout = False
        self.save_check = lambda: None

    def snapshot(self, config):
        if self.offline:
            raise w.Unavailable('app')
        return self.app, {'local': (self.sources, self.native)}

    def spawn(self, machine, source, record):
        self.save_check()
        self.writes.append(('spawn', copy.deepcopy(record)))
        if self.timeout:
            raise w.Unavailable('timeout')

    def rename(self, kind, target, name):
        self.writes.append((kind, target, name))
        for sp in self.app['spaces']:
            for obj in [sp] + sp['tabs']:
                if obj['id'] == target:
                    obj['name'] = name

    def publish(self, record, source=S):
        self.native.append(dict(address='t9', labels={'sync.key': w.source_key(source),
            'herdr.space': record['space'], 'herdr.tab': record['tab']}, argv=[]))
        self.app['spaces'] = [dict(id=record['space'], machine=None, name='old space', tabs=[
            dict(id=record['tab'], name='old tab', terminals=[{'terminal': 't9'}])])]


class WatcherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = w.Store(Path(self.temp.name) / 'state')
        self.io = Fake()
        self.config = {'machines': [copy.deepcopy(M)]}
        self.engine = w.Watcher(self.config, self.store, self.io)

    def tick(self, include=False):
        self.engine.tick(include_existing=include)
        return self.store.load()

    def test_adopts_direct_viewer_and_follows_names_not_labels(self):
        self.io.native = [dict(address='t9', labels={}, argv=[M['herdr'], '--session', 'default', 'agent', 'attach', S['pane']])]
        self.io.app = {'spaces': [dict(id='sp-old', machine=None, name='native space', tabs=[
            dict(id='tb-old', name='native tab', terminals=[{'terminal': 't9'}])])]}
        state = self.tick()
        record = state['sources'][w.source_key(S)]
        self.assertEqual('active', record['status'])
        self.assertEqual('tb-old', record['tab'])
        self.assertNotIn('spawn', [x[0] for x in self.io.writes])
        self.assertEqual('setup', self.io.app['spaces'][0]['tabs'][0]['name'])
        self.io.sources[0]['name'] = 'renamed'
        self.tick()
        self.assertEqual('renamed', self.io.app['spaces'][0]['tabs'][0]['name'])

    def test_timeout_intent_is_durable_reconciles_after_restart_without_retry(self):
        self.io.timeout = True
        self.io.save_check = lambda: self.assertEqual('ambiguous', self.store.load()['sources'][w.source_key(S)]['status'])
        self.tick(include=True)
        record = self.store.load()['sources'][w.source_key(S)]
        self.assertIn('retryAfter', record)
        self.engine = w.Watcher(self.config, self.store, self.io)
        self.tick()
        self.assertEqual(1, len(self.io.writes))
        self.io.publish(record)
        state = self.tick()
        self.assertEqual('active', state['sources'][w.source_key(S)]['status'])
        self.assertEqual(1, len([x for x in self.io.writes if x[0] == 'spawn']))

    def test_closed_target_is_dismissed_even_if_core_terminal_survives(self):
        self.tick(include=True)
        record = self.store.load()['sources'][w.source_key(S)]
        self.io.publish(record)
        self.tick()
        self.io.app['spaces'] = []
        state = self.tick(include=True)
        self.assertEqual('dismissed', state['sources'][w.source_key(S)]['status'])
        self.io.publish(record)
        self.tick(include=True)
        self.assertEqual('dismissed', self.store.load()['sources'][w.source_key(S)]['status'])
        self.assertEqual(1, len([x for x in self.io.writes if x[0] == 'spawn']))

    def test_workspace_group_reuses_adopted_space_and_explicit_baseline_override(self):
        self.tick()
        self.tick(include=True)
        first = self.store.load()['sources'][w.source_key(S)]
        self.assertEqual('ambiguous', first['status'])
        self.io.publish(first)
        self.tick()
        new = dict(S, pane='w1:p2', terminal='term_2', tab='w1:t2')
        self.io.sources.append(new)
        state = self.tick()
        self.assertEqual(first['space'], state['sources'][w.source_key(new)]['space'])
        self.assertNotEqual(first['tab'], state['sources'][w.source_key(new)]['tab'])

    def test_offline_app_and_paused_ticks_do_not_query_or_mutate(self):
        self.io.offline = True
        self.tick()
        self.assertEqual([], self.io.writes)
        self.assertEqual([], self.store.load()['baseline'])
        self.store.set_paused(True)
        self.io.snapshot = lambda _: self.fail('paused watcher queried live systems')
        self.tick()
        self.assertTrue(self.store.paused())
        self.store.set_paused(False)
        self.assertFalse(self.store.paused())

    def test_missing_source_only_records_absence_and_remote_failure_preserves_mapping(self):
        self.tick(include=True)
        record = self.store.load()['sources'][w.source_key(S)]
        self.io.publish(record)
        self.tick()
        self.io.sources = []
        state = self.tick()
        self.assertFalse(state['sources'][w.source_key(S)]['present'])
        self.assertEqual('active', state['sources'][w.source_key(S)]['status'])
        self.io.snapshot = lambda _: (self.io.app, {'local': None})
        self.tick()
        self.assertEqual(state['sources'], self.store.load()['sources'])
        self.assertFalse(any(x[0] in ('close', 'kill') for x in self.io.writes))

    def test_existing_viewer_without_app_tab_is_never_duplicated(self):
        self.io.native = [dict(address='t9', labels={}, argv=[M['herdr'], 'agent', 'attach', S['pane']])]
        self.tick(include=True)
        self.assertEqual([], self.io.writes)
        self.assertEqual('unmapped', self.store.load()['sources'][w.source_key(S)]['status'])

    def test_status_separates_absent_sources_from_active_coverage(self):
        import contextlib
        import io
        import json
        self.io.native = [dict(address='t9', labels={}, argv=[M['herdr'], 'agent', 'attach', S['pane']])]
        self.io.app = {'spaces': [dict(id='sp-old', machine=None, name='master', tabs=[
            dict(id='tb-old', name='setup', terminals=[{'terminal': 't9'}])])]}
        self.tick()
        self.io.sources = []
        self.tick()
        config = Path(self.temp.name) / 'status-config.json'
        config.write_text(json.dumps(dict(stateDir=str(self.store.path))))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(0, w.main(['--config', str(config), '--status']))
        counts = json.loads(output.getvalue())['counts']
        self.assertEqual(0, counts.get('active', 0))
        self.assertEqual(1, counts['source_absent'])

    def test_ambiguous_launch_retries_same_intent_only_after_cooldown(self):
        self.io.timeout = True
        self.tick(include=True)
        key = w.source_key(S)
        before = self.store.load()['sources'][key]
        self.tick()
        self.assertEqual(1, len(self.io.writes))
        state = self.store.load()
        state['sources'][key]['retryAfter'] = 0
        self.store.save(state)
        self.tick()
        self.assertEqual(2, len(self.io.writes))
        retried = self.io.writes[-1][1]
        self.assertEqual(before['tab'], retried['tab'])
        self.assertEqual(before['space'], retried['space'])

    def test_failed_rename_is_retried_without_stopping_or_duplicating(self):
        self.io.native = [dict(address='t9', labels={}, argv=[M['herdr'], 'agent', 'attach', S['pane']])]
        self.io.app = {'spaces': [dict(id='sp-old', machine=None, name='master', tabs=[
            dict(id='tb-old', name='old label', terminals=[{'terminal': 't9'}])])]}
        original = self.io.rename
        def failed(*args):
            raise w.Unavailable('transient')
        self.io.rename = failed
        state = self.tick()
        self.assertEqual('active', state['sources'][w.source_key(S)]['status'])
        self.io.rename = original
        self.tick()
        self.assertEqual('setup', self.io.app['spaces'][0]['tabs'][0]['name'])
        self.assertFalse(any(x[0] == 'spawn' for x in self.io.writes))

    def test_cold_start_suppresses_existing_then_creates_only_new_identity(self):
        state = self.tick()
        self.assertEqual('suppressed', state['sources'][w.source_key(S)]['status'])
        self.assertEqual([], self.io.writes)
        self.io.sources.append(dict(S, pane='w1:p2', terminal='term_2'))
        state = self.tick()
        self.assertEqual(1, len(self.io.writes))
        self.tick()
        self.assertEqual(1, len(self.io.writes))


class IdentityTests(unittest.TestCase):
    def test_staged_wsl_root_and_current_foreground_bridge_are_adopted(self):
        bridge = M['home'] + '/.local/share/herdr-native-status-bridge/legacy_hc_bridge.py'
        argv = ['/usr/bin/python3', bridge, '--herdr', M['herdr'], '--session', 'default', S['pane']]
        staged = [r'C:\Windows\System32\wsl.exe', '--distribution', 'Ubuntu', '--exec',
                  '/usr/bin/python3', '-c', 'opaque staging code', '/gate', *argv]
        self.assertEqual(('default', S['pane']), w.attachment(staged, M))
        with tempfile.TemporaryDirectory() as directory:
            store, fake = w.Store(directory), Fake()
            fake.native = [dict(address='t9', labels={}, argv=['/bin/bash'], foreground={'argv': argv})]
            fake.app = {'spaces': [dict(id='sp', machine=None, name='master', tabs=[
                dict(id='tb', name='setup', terminals=[{'terminal': 't9'}])])]}
            w.Watcher({'machines': [M]}, store, fake).tick()
            self.assertEqual('active', store.load()['sources'][w.source_key(S)]['status'])

    def test_recognizes_only_supported_attachment_argv_not_native_agents(self):
        bridge = M['home'] + '/.local/share/herdr-native-status-bridge/legacy_hc_bridge.py'
        waiter = bridge.replace('legacy_hc_bridge.py', 'wait_for_agent.py')
        python = ['/usr/bin/python3', bridge, '--herdr', M['herdr'], '--session', 'default', S['pane']]
        wrapped = [r'C:\Windows\System32\wsl.exe', '--distribution', 'Ubuntu', '--exec'] + python
        shell = ['powershell.exe', '-NoProfile', '-Command', '& wsl.exe --distribution Ubuntu --exec ' + ' '.join(python)]
        for argv in [python, [x.replace(bridge, waiter) for x in python], wrapped, shell,
                     [M['herdr'], 'agent', 'attach', S['pane']]]:
            with self.subTest(argv=argv):
                self.assertEqual(('default', S['pane']), w.attachment(argv, M))
        for argv in [['codex', 'resume', S['pane']], [M['herdr'], 'agent', 'start', S['pane']],
                     ['echo'] + python, [x.replace('Ubuntu', 'Other') for x in wrapped],
                     [M['herdr'], '--machine', 'unapproved', 'agent', 'attach', S['pane']]]:
            self.assertIsNone(w.attachment(argv, M))


class ControlTests(unittest.TestCase):
    def test_controls_and_single_instance_lock_never_launch_live_commands(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as directory:
            config = dict(machines=[M], app='app', hc='hc', windowsCwd='C:/Users/TestUser', stateDir=directory + '/state')
            path = Path(directory) / 'config.json'
            path.write_text(__import__('json').dumps(config))
            def forbidden(_):
                self.fail('control mode constructed transport')
            for flag in ['--pause', '--status', '--resume']:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(0, w.main(['--config', str(path), flag], transport_factory=forbidden))
                self.assertIn('paused', output.getvalue())
            store = w.Store(config['stateDir'])
            with store.lock():
                with self.assertRaises(w.Unavailable):
                    with store.lock():
                        self.fail('second lock acquired')
            with store.lock():
                pass
            fake = Fake()
            self.assertEqual(0, w.main(['--config', str(path), '--once'], transport_factory=lambda _: fake))
            self.assertEqual([], fake.writes)


class CommandTests(unittest.TestCase):
    def test_real_transport_plans_waiter_only_nonfocus_launch_with_exact_source_ids(self):
        calls = []
        def run(argv):
            calls.append(argv)
            if argv == ['app', 'ls']:
                return {'spaces': []}
            if argv == ['hc', 'ls', '--json']:
                return {'terminals': [], 'machines': []}
            if argv[-2:] == ['workspace', 'list']:
                return {'result': {'workspaces': [{'workspace_id': 'w1', 'label': 'master'}]}}
            if argv[-4:] == ['tab', 'list', '--workspace', 'w1']:
                return {'result': {'tabs': [{'tab_id': 'w1:t1', 'label': 'setup'}]}}
            if argv[-4:] == ['pane', 'list', '--workspace', 'w1']:
                return {'result': {'panes': [dict(pane_id=S['pane'], terminal_id=S['terminal'],
                    tab_id=S['tab'], workspace_id='w1', cwd=S['cwd'])]}}
            if argv[:2] == ['hc', 'run']:
                return {'address': 't8'}
            self.fail('unexpected command ' + repr(argv))
        config = {'machines': [M], 'app': 'app', 'hc': 'hc', 'windowsCwd': 'C:\\Users\\TestUser'}
        transport = w.Transport(config, run=run)
        with tempfile.TemporaryDirectory() as directory:
            store = w.Store(Path(directory) / 'state')
            w.Watcher(config, store, transport).tick(include_existing=True)
        launch = next(c for c in calls if c[:2] == ['hc', 'run'])
        for flag in ['--bg', '--no-parent', '--no-notify', '--keep']:
            self.assertIn(flag, launch)
        self.assertIn('sync.key=' + w.source_key(S), launch)
        self.assertIn('herdr.tab=', ' '.join(launch))
        self.assertEqual([r'C:\Windows\System32\wsl.exe', '--distribution', 'Ubuntu', '--cd', S['cwd'], '--exec',
            '/usr/bin/python3', M['home'] + '/.local/share/herdr-native-status-bridge/wait_for_agent.py',
            '--herdr', M['herdr'], '--session', 'default', S['pane']], launch[launch.index('--')+1:])
        self.assertFalse(any('tab.new' in c or 'space.new' in c for c in calls))


if __name__ == '__main__':
    unittest.main()
