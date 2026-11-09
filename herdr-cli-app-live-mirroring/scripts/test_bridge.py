import importlib.util
import json
import os
import pty
import select
import signal
import subprocess
import sys
import termios
import tempfile
import threading
import time
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'legacy_hc_bridge.py'


def load_bridge(test):
    test.assertTrue(SCRIPT.exists(), 'bridge implementation is missing')
    spec = importlib.util.spec_from_file_location('legacy_hc_bridge', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StatusTests(unittest.TestCase):
    def test_documented_states_become_exact_safe_osc(self):
        bridge = load_bridge(self)
        for state in ('idle', 'working', 'done', 'blocked', 'error'):
            for app in ('codex', 'hermes'):
                with self.subTest(state=state, app=app):
                    report = bridge.parse_status(json.dumps({'result': {'agent': {
                        'agent_status': state, 'agent': app, 'completion_seq': 7}}}))
                    self.assertEqual(report, (state, app, 7))
                    self.assertEqual(bridge.encode_status(report),
                                     f'\x1b]7501;state={state}:app={app}\x1b\\'.encode())

    def test_status_boundary_tracks_chunked_terminal_controls_and_utf8(self):
        bridge = load_bridge(self)
        self.assertTrue(hasattr(bridge, 'OutputBoundary'), 'safe insertion tracking is missing')
        for start, middle, end in [
            (b'\x1b', b'[12;', b'4H'),
            (b'\x1b]', b'2;title', b'\x07'),
            (b'\x1b]', b'2;title\x1b', b'\\'),
            (b'\x1bP', b'dcs\x07', b'\x1b\\'),
            (b'\x1b_', b'apc', b'\x1b\\'),
            (b'\x1b^', b'pm', b'\x1b\\'),
            (b'\x1bX', b'sos', b'\x1b\\'),
            (b'\x1b(', b'', b'B'),
            (b'\xe2', b'\x82', b'\xac'),
            (b'\x1b[', b'123', b'\x18'),
        ]:
            with self.subTest(start=start, end=end):
                boundary = bridge.OutputBoundary()
                self.assertTrue(boundary.safe)
                boundary.feed(start)
                self.assertFalse(boundary.safe)
                boundary.feed(middle)
                self.assertFalse(boundary.safe)
                boundary.feed(end)
                self.assertTrue(boundary.safe)
                boundary.feed(b'plain\xff\r\n')
                self.assertTrue(boundary.safe)

    def test_untrusted_status_never_injects_or_claims_completion(self):
        bridge = load_bridge(self)
        invalid = ['not json', 'null', '[]', '{}',
                   json.dumps({'result': {'agent': None}})]
        for state, app in [('unknown', 'codex'), (None, 'codex'),
                           ('working:state=done', 'codex'),
                           ('idle', 'codex\x1b\\\x1b]7501;state=done'),
                           ('done', 'other'), ([], 'hermes')]:
            invalid.append(json.dumps({'result': {'agent': {
                'agent_status': state, 'agent': app}}}))
        for payload in invalid:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    bridge.parse_status(payload)
        self.assertEqual(bridge.encode_status(('error', None, None)),
                         b'\x1b]7501;state=error\x1b\\')
        for seq in (None, -1, True, '1:state=done', {}, 1.5):
            report = bridge.parse_status(json.dumps({'result': {'agent': {
                'agent_status': 'working', 'agent': 'codex',
                'completion_seq': seq}}}))
            self.assertEqual(report, ('working', 'codex', None))
        report = bridge.parse_status(json.dumps({'result': {'agent': {
            'agent_status': 'idle', 'agent': 'hermes'}}}))
        self.assertEqual(report, ('idle', 'hermes', None))


class RelayTests(unittest.TestCase):
    def test_backpressured_write_preserves_all_bytes_and_is_cancellable(self):
        bridge = load_bridge(self)
        self.assertTrue(hasattr(bridge, 'write_all'), 'complete cancellable writes are missing')
        read_fd, write_fd = os.pipe()
        os.set_blocking(write_fd, False)
        received = bytearray()
        payload = bytes(range(256)) * 4096
        stop = threading.Event()
        def read_bytes():
            while len(received) < len(payload):
                received.extend(os.read(read_fd, 4096))
        reader = threading.Thread(target=read_bytes, daemon=True)
        reader.start()
        try:
            self.assertTrue(bridge.write_all(write_fd, payload, stop))
            reader.join(timeout=2)
            self.assertFalse(reader.is_alive())
            self.assertEqual(bytes(received), payload)
            while True:
                try:
                    os.write(write_fd, b'x' * 4096)
                except BlockingIOError:
                    break
            timer = threading.Timer(0.05, stop.set)
            timer.start()
            started = time.monotonic()
            self.assertFalse(bridge.write_all(write_fd, b'not sent', stop))
            self.assertLess(time.monotonic() - started, 0.5)
            timer.join()
        finally:
            os.close(write_fd)
            os.close(read_fd)


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fixture-', dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.state = self.path / 'state.json'
        self.log = self.path / 'calls.jsonl'
        self.set_state('working')
        self.fake = self.path / 'herdr'
        self.fake.write_text('#!' + sys.executable + '\n' +
                             (ROOT / 'fixture_child.py').read_text().split('\n', 1)[1])
        self.fake.chmod(0o700)
        self.env = dict(os.environ, FIXTURE_STATE=str(self.state),
                        FIXTURE_LOG=str(self.log),
                        FIXTURE_QUERY_PID=str(self.path / 'query.pid'))
        self.data = b''

    def set_state(self, state):
        temp = self.path / 'state.new'
        temp.write_text(json.dumps({'result': {'agent': {
            'agent_status': state, 'agent': 'codex'}}}))
        temp.replace(self.state)

    def start(self, mode='quiet', terminal=False):
        self.outer_master = self.outer_slave = None
        if terminal:
            self.outer_master, self.outer_slave = pty.openpty()
            termios.tcsetwinsize(self.outer_slave, (37, 112))
            self.original_terminal = termios.tcgetattr(self.outer_slave)
        command = [sys.executable, str(SCRIPT), '--herdr', str(self.fake),
                   '--poll-interval', '0.08']
        if mode is not None:
            command += ['--session', 'fixture-session']
        command += ['w4:p4']
        if mode is not None:
            command += ['--', sys.executable, str(ROOT / 'fixture_child.py'), mode]
        if getattr(self, 'partial_writes', False):
            wrapper = ("import os,runpy,sys; original=os.write; "
                       "os.write=lambda fd,data:original(fd,data[:7]); "
                       "sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')")
            command = [sys.executable, '-c', wrapper] + command[1:]
        self.proc = subprocess.Popen(command,
            stdin=self.outer_slave if terminal else subprocess.PIPE,
            stdout=self.outer_slave if terminal else subprocess.PIPE,
            stderr=subprocess.PIPE, env=self.env)
        self.output_fd = self.outer_master if terminal else self.proc.stdout.fileno()
        self.addCleanup(self.stop)

    def stop(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=4)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=2)
        for stream in (self.proc.stdin, self.proc.stdout, self.proc.stderr):
            if stream:
                stream.close()
        for fd in (self.outer_master, self.outer_slave):
            if fd is not None:
                os.close(fd)

    def until(self, needle, timeout=3):
        deadline = time.monotonic() + timeout
        while needle not in self.data and time.monotonic() < deadline:
            readable, _, _ = select.select([self.output_fd], [], [], 0.05)
            if readable:
                chunk = os.read(self.output_fd, 65536)
                if not chunk:
                    break
                self.data += chunk
        self.assertIn(needle, self.data, f'bridge output: {self.data!r}')

    def test_relay_preserves_output_and_reports_when_kernel_writes_are_partial(self):
        self.partial_writes = True
        self.start(mode='quiet')
        self.until(b'FIXTURE_READY')
        self.until(b'\x1b]7501;state=working:app=codex\x1b\\')

    def test_invalid_cli_options_fail_before_launch(self):
        for options in (['--poll-interval', '0'], ['--poll-interval', '-1'],
                        ['--poll-interval', 'nan'], ['--poll-interval', 'inf'],
                        ['--']):
            with self.subTest(options=options):
                command = [sys.executable, str(SCRIPT), '--herdr', str(self.fake)]
                if options == ['--']:
                    command += ['w4:p4', '--']
                else:
                    command += options + ['w4:p4']
                result = subprocess.run(command, input=b'', capture_output=True,
                                        env=self.env, timeout=3)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse(self.log.exists(), 'invalid CLI launched a subprocess')

    def test_cli_defaults_attach_to_same_session_and_literal_target(self):
        self.start(mode=None)
        self.until(b'FIXTURE_READY')
        self.until(b'\x1b]7501;state=working:app=codex\x1b\\')
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertIn(['--session', 'default', 'agent', 'attach', 'w4:p4'], calls)
        self.assertIn(['--session', 'default', 'agent', 'get', 'w4:p4'], calls)

    def test_status_never_splits_attachment_escape_sequence(self):
        self.env['FIXTURE_GATE'] = str(self.path / 'output-started')
        self.start('split-osc')
        self.until(b'END_SPLIT')
        self.until(b'\x1b]7501;state=working:app=codex\x1b\\')
        self.assertIn(b'\x1b]2;HELLOWORLD\x07END_SPLIT', self.data)

    def test_query_errors_are_explicit_and_recover_without_false_idle(self):
        self.start()
        self.until(b'FIXTURE_READY')
        self.until(b'\x1b]7501;state=working:app=codex\x1b\\')
        failure_with_result = json.dumps({'ok': False, 'result': {'agent': {
            'agent_status': 'idle', 'agent': 'codex'}}})
        for payload in (failure_with_result, 'not json', '!fail', '!hang',
                        json.dumps({'result': {'agent': {
                            'agent_status': 'unrecognized', 'agent': 'codex'}}})):
            with self.subTest(payload=payload):
                self.data = b''
                temp = self.path / 'bad.new'
                temp.write_text(payload)
                temp.replace(self.state)
                self.until(b'\x1b]7501;state=error\x1b\\', timeout=3)
                self.assertNotIn(b'state=idle', self.data)
                self.assertNotIn(b'state=done', self.data)
                self.data = b''
                self.set_state('working')
                self.until(b'\x1b]7501;state=working:app=codex\x1b\\')
                self.assertIsNone(self.proc.poll())

    def test_shutdown_reaps_only_owned_children_even_during_hung_query(self):
        sentinel = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
        def cleanup_sentinel():
            sentinel.terminate()
            sentinel.wait(timeout=2)
        self.addCleanup(cleanup_sentinel)
        attach_pid_file = self.path / 'attachment.pid'
        query_pid_file = self.path / 'query.pid'
        self.env.update(FIXTURE_ATTACH_PID=str(attach_pid_file),
                        FIXTURE_QUERY_PID=str(query_pid_file))
        self.state.write_text('!hang')
        self.start('stubborn', terminal=True)
        self.until(b'FIXTURE_READY')
        deadline = time.monotonic() + 2
        while not query_pid_file.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(query_pid_file.exists())
        attachment_pid = int(attach_pid_file.read_text())
        query_pid = int(query_pid_file.read_text())
        self.proc.terminate()
        self.proc.wait(timeout=1.5)
        self.assertFalse(Path(f'/proc/{attachment_pid}').exists(), 'attachment was not reaped')
        self.assertFalse(Path(f'/proc/{query_pid}').exists(), 'query was not reaped')
        self.assertIsNone(sentinel.poll(), 'unrelated legacy-agent stand-in was stopped')
        self.assertEqual(termios.tcgetattr(self.outer_slave), self.original_terminal)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertTrue(all(call[2:4] == ['agent', 'get'] for call in calls))

    def test_initial_size_and_resize_reach_controlling_child_terminal(self):
        self.start('size', terminal=True)
        self.until(b'CONTROLLING_TTY')
        self.until(b'SIZE[37,112]')
        termios.tcsetwinsize(self.outer_slave, (53, 143))
        self.proc.send_signal(signal.SIGWINCH)
        self.until(b'SIZE[53,143]')

    def test_raw_terminal_preserves_control_bytes_without_automatic_input(self):
        payload = b'\x00\x03\x04\x1a\r\n\xff\x1b[A\x1b]2;title\x07\x1b[?25l'
        self.env['FIXTURE_PAYLOAD'] = payload.hex()
        self.start('raw', terminal=True)
        self.until(b'NO_AUTOMATIC_INPUT')
        self.assertIn(b'RAW_OUTPUT[' + payload + b']END_OUTPUT', self.data)
        self.assertNotIn(b'UNEXPECTED_INPUT', self.data)
        os.write(self.outer_master, payload)
        self.until(b'INPUT[' + payload + b']END_INPUT')
        self.assertIsNone(self.proc.poll())

    def test_poll_changes_reach_output_while_attachment_is_quiet(self):
        self.start()
        self.until(b'FIXTURE_READY')
        self.until(b'\x1b]7501;state=working:app=codex\x1b\\')
        self.set_state('blocked')
        self.until(b'\x1b]7501;state=blocked:app=codex\x1b\\')
        self.assertIsNone(self.proc.poll())
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertGreaterEqual(len(calls), 2)
        self.assertTrue(all(call == ['--session', 'fixture-session', 'agent',
                                     'get', 'w4:p4'] for call in calls))


if __name__ == '__main__':
    unittest.main()
