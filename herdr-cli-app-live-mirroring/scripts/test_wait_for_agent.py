import importlib.util
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'wait_for_agent.py'

class WaiterTests(unittest.TestCase):
    def load(self):
        self.assertTrue(SCRIPT.exists(), 'waiting-view launcher is not implemented')
        spec = importlib.util.spec_from_file_location('wait_for_agent', SCRIPT)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    def test_plain_shell_is_waiting_not_a_fake_agent(self):
        m = self.load()
        self.assertEqual(m.classify({'result': {'pane': {'pane_id': 'w1:p2'}}}), 'waiting')
        self.assertEqual(m.classify({'result': {'pane': {'agent': 'codex', 'agent_status': 'unknown'}}}), 'waiting')

    def test_supported_recognized_agent_is_attachable(self):
        m = self.load()
        for app in ['codex', 'hermes']:
            self.assertEqual(m.classify({'result': {'pane': {'agent': app, 'agent_status': 'idle'}}}), 'attach')

    def test_error_or_unrecognized_payload_cannot_be_attached(self):
        m = self.load()
        self.assertEqual(m.classify({'error': {'code': 'pane_not_found'}}), 'missing')
        self.assertEqual(m.classify({'error': {'code': 'connection_error'}}), 'unavailable')
        self.assertEqual(m.classify({'result': {'pane': {'agent': 'injected:state=done', 'agent_status': 'working'}}}), 'waiting')
        for payload in [None, [], {}, {'result': {'pane': None}}]:
            self.assertEqual(m.classify(payload), 'unavailable')

class LiveWaiterTests(unittest.TestCase):
    def test_shell_view_transitions_to_attachment_without_automatic_input(self):
        self.assertTrue(SCRIPT.exists(), 'waiting-view launcher is not implemented')
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            d=Path(tmp);state=d/'state.json';calls=d/'calls.jsonl'
            state.write_text(json.dumps({'result': {'pane': {'pane_id': 'w1:p2'}}}))
            fake=d/'herdr'
            fake.write_text('#!'+sys.executable+'\nimport os,sys,pathlib\np=pathlib.Path(os.environ["TEST_STATE"])\nwith open(os.environ["TEST_CALLS"],"a") as f:f.write(repr(sys.argv[1:])+"\\n")\nprint(p.read_text())\n')
            fake.chmod(0o700)
            bridge=d/'bridge.py'
            bridge.write_text('import os,sys\nprint("ATTACHED "+repr(sys.argv[1:]),flush=True)\nimport select\nprint("NO_QUEUED_INPUT" if not select.select([0],[],[],.1)[0] else "HAS_INPUT",flush=True)\n')
            env=dict(os.environ,TEST_STATE=str(state),TEST_CALLS=str(calls))
            p=subprocess.Popen([sys.executable,str(SCRIPT),'--herdr',str(fake),'--bridge',str(bridge),'--interval','.05','--session','fixture','w1:p2'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
            data=b'';deadline=time.monotonic()+4
            try:
                while b'Waiting for an agent' not in data and time.monotonic()<deadline:
                    if select.select([p.stdout],[],[],.1)[0]:data+=os.read(p.stdout.fileno(),4096)
                self.assertIn(b'Waiting for an agent',data)
                self.assertNotIn(b'7501;',data)
                state.write_text(json.dumps({'result': {'pane': {'agent':'codex','agent_status':'working'}}}))
                output,err=p.communicate(timeout=5)
                self.assertEqual(p.returncode,0,err)
                self.assertIn(b'ATTACHED',output)
                self.assertIn(b"'--session', 'fixture', 'w1:p2'",output)
                self.assertTrue(all("'pane', 'get', 'w1:p2'" in l for l in calls.read_text().splitlines()))
            finally:
                if p.poll() is None:p.kill();p.wait()
                for f in [p.stdin,p.stdout,p.stderr]:
                    if f and not f.closed:f.close()

if __name__=='__main__':unittest.main()
