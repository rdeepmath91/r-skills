#!/usr/bin/env python3
"""Isolated subprocess fixture. Never contacts Herdr or existing agents."""
import json
import os
from pathlib import Path
import select
import signal
import sys
import termios
import tty
import time

if sys.argv[1:] == ['split-osc']:
    os.write(1, b'\x1b]2;HELLO')
    Path(os.environ['FIXTURE_GATE']).touch()
    time.sleep(0.4)
    os.write(1, b'WORLD\x07END_SPLIT')
    time.sleep(60)
elif sys.argv[1:] == ['size']:
    def emit_size(*_):
        rows, cols = termios.tcgetwinsize(0)
        os.write(1, f'SIZE[{rows},{cols}]'.encode())
    with open('/dev/tty', 'rb', buffering=0):
        os.write(1, b'CONTROLLING_TTY')
    signal.signal(signal.SIGWINCH, emit_size)
    emit_size()
    while True:
        signal.pause()
elif sys.argv[1:] == ['raw']:
    tty.setraw(0)
    payload = bytes.fromhex(os.environ['FIXTURE_PAYLOAD'])
    os.write(1, b'RAW_OUTPUT[' + payload + b']END_OUTPUT')
    if select.select([0], [], [], 0.15)[0]:
        os.write(1, b'UNEXPECTED_INPUT')
    else:
        os.write(1, b'NO_AUTOMATIC_INPUT')
    received = b''
    while len(received) < len(payload):
        received += os.read(0, len(payload) - len(received))
    os.write(1, b'INPUT[' + received + b']END_INPUT')
    time.sleep(60)
elif sys.argv[1:] == ['stubborn']:
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    Path(os.environ['FIXTURE_ATTACH_PID']).write_text(str(os.getpid()))
    os.write(1, b'FIXTURE_READY')
    time.sleep(60)
elif sys.argv[1:] == ['quiet']:
    os.write(1, b'FIXTURE_READY')
    time.sleep(60)
else:
    with open(os.environ['FIXTURE_LOG'], 'a') as log:
        log.write(json.dumps(sys.argv[1:]) + '\n')
    if sys.argv[3:5] == ['agent', 'attach']:
        os.execv(sys.executable, [sys.executable, __file__, 'quiet'])
    if os.environ.get('FIXTURE_GATE'):
        while not Path(os.environ['FIXTURE_GATE']).exists():
            time.sleep(0.01)
    state = Path(os.environ['FIXTURE_STATE']).read_text()
    if state == '!hang':
        Path(os.environ['FIXTURE_QUERY_PID']).write_text(str(os.getpid()))
        time.sleep(60)
    if state == '!fail':
        sys.exit(7)
    os.write(1, state.encode())
