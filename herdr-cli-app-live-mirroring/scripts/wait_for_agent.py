#!/usr/bin/env python3
"""Show a safe placeholder until a legacy Herdr pane has a supported agent."""


import argparse
import json
import math
import os
from pathlib import Path
import re
import select
import subprocess
import sys
import termios
import time


def classify(payload):
    if not isinstance(payload, dict):
        return 'unavailable'
    if payload.get('error'):
        error = payload['error']
        return 'missing' if isinstance(error, dict) and error.get('code') == 'pane_not_found' else 'unavailable'
    result = payload.get('result')
    pane = result.get('pane') if isinstance(result, dict) else None
    if not isinstance(pane, dict):
        return 'unavailable'
    if pane.get('agent') in ('hermes', 'codex') and pane.get('agent_status') in ('idle', 'working', 'done', 'blocked', 'error'):
        return 'attach'
    return 'waiting'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--herdr', required=True)
    parser.add_argument('--session', default='default')
    parser.add_argument('--bridge', default=str(Path(__file__).with_name('legacy_hc_bridge.py')))
    parser.add_argument('--interval', type=float, default=4)
    parser.add_argument('target')
    args = parser.parse_args()
    if not math.isfinite(args.interval) or args.interval <= 0:
        parser.error('--interval must be finite and positive')
    if not re.fullmatch(r'w[0-9A-Za-z]+:p[0-9A-Za-z]+', args.target):
        parser.error('expected an exact legacy workspace-qualified pane ID')
    print('Waiting for an agent in CLI pane ' + args.target + '.', flush=True)
    print('This is not a shared shell. Start Hermes or Codex in the original CLI tab.', flush=True)
    print('Typed commands here are discarded until the agent is attached; Ctrl+C closes only this view.', flush=True)
    input_open = True
    last_message = None
    while True:
        try:
            query = subprocess.run([args.herdr, '--session', args.session, 'pane', 'get', args.target],
                                   capture_output=True, text=True, timeout=3)
            payload = json.loads(query.stdout)
            decision = classify(payload)
            if query.returncode and decision not in ('missing', 'unavailable'):
                decision = 'unavailable'
        except (OSError, ValueError, subprocess.SubprocessError):
            decision = 'unavailable'
        if decision == 'attach':
            if os.isatty(0):
                termios.tcflush(0, termios.TCIFLUSH)
            else:
                # Never deliver queued shell-placeholder input to the real agent.
                for _ in range(32):
                    if not select.select([0], [], [], 0)[0] or not os.read(0, 4096):
                        break
            os.execv(sys.executable, [sys.executable, args.bridge,
                     '--herdr', args.herdr, '--session', args.session, args.target])
        if decision == 'missing':
            print('The original CLI pane no longer exists. No agent was started.', flush=True)
            return 0
        message = 'Source temporarily unavailable; waiting safely.' if decision == 'unavailable' else 'Waiting for the original CLI tab to start an agent.'
        if message != last_message:
            print(message, flush=True)
            last_message = message
        deadline = time.monotonic() + args.interval
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            if input_open:
                if select.select([0], [], [], remaining)[0]:
                    input_open = bool(os.read(0, 4096))
            else:
                time.sleep(remaining)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
