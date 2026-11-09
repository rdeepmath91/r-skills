#!/usr/bin/env python3
"""Observe legacy Herdr status while relaying its attachment through a PTY."""
import argparse
import errno
import json
import math
import os
import pty
import queue
import select
import signal
import subprocess
import sys
import termios
import threading
import tty
import time


STATES = ('idle', 'working', 'done', 'blocked', 'error')
APPS = ('codex', 'hermes')


def parse_status(payload):
    """Accept only explicit legacy detection, never infer from missing data."""
    try:
        response = json.loads(payload)
        if not isinstance(response, dict):
            raise ValueError('invalid legacy response envelope')
        if (response.get('ok', True) is not True or
                response.get('success', True) is not True or
                response.get('error') is not None):
            raise ValueError('legacy query reported failure')
        agent = response['result']['agent']
        state, app = agent['agent_status'], agent['agent']
        seq = agent.get('completion_seq')
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError('invalid legacy agent response') from exc
    if state not in STATES or app not in APPS:
        raise ValueError('unsupported legacy status or agent kind')
    if type(seq) is not int or seq < 0:
        seq = None
    return state, app, seq


def encode_status(report):
    state, app, _ = report
    if state not in STATES or (app is not None and app not in APPS):
        raise ValueError('unsafe status report')
    fields = f'state={state}' + (f':app={app}' if app else '')
    return f'\x1b]7501;{fields}\x1b\\'.encode('ascii')


class OutputBoundary:
    """Track safe insertion points without buffering or changing child bytes.

    ESC-based VT controls and UTF-8 are expected; no terminal emulation occurs.
    An unfinished string/control defers status, not attachment output.
    """
    def __init__(self):
        self.state = 'ground'
        self.utf8 = 0

    @property
    def safe(self):
        return self.state == 'ground' and self.utf8 == 0

    def feed(self, data):
        for byte in data:
            if self.utf8:
                if 0x80 <= byte <= 0xbf:
                    self.utf8 -= 1
                    continue
                self.utf8 = 0
            if byte in (0x18, 0x1a):
                self.state = 'ground'
            elif self.state.startswith(('osc', 'str')):
                kind = self.state[:3]
                if (kind == 'osc' and byte == 7) or (
                        self.state.endswith('-esc') and byte == 0x5c):
                    self.state = 'ground'
                else:
                    self.state = kind + ('-esc' if byte == 27 else '')
            elif byte == 27:
                self.state = 'esc'
            elif self.state == 'esc':
                if byte == 0x5b:
                    self.state = 'csi'
                elif byte == 0x5d:
                    self.state = 'osc'
                elif byte in (0x50, 0x58, 0x5e, 0x5f):
                    self.state = 'str'
                elif 0x30 <= byte <= 0x7e:
                    self.state = 'ground'
            elif self.state == 'csi':
                if 0x40 <= byte <= 0x7e:
                    self.state = 'ground'
            elif 0xc2 <= byte <= 0xf4:
                self.utf8 = 1 if byte < 0xe0 else (2 if byte < 0xf0 else 3)


def write_all(fd, data, stop):
    """Preserve partial writes and remain interruptible under backpressure."""
    view = memoryview(data)
    while view:
        if stop.is_set():
            return False
        _, writable, _ = select.select([], [fd], [], 0.05)
        if not writable:
            continue
        try:
            count = os.write(fd, view[:1024])
        except (BlockingIOError, InterruptedError):
            continue
        view = view[count:]
    return True


def poll_status(command, interval, stop, reports):
    while not stop.is_set():
        try:
            with subprocess.Popen(command, stdin=subprocess.DEVNULL,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL) as query:
                deadline = time.monotonic() + 2
                while True:
                    try:
                        output, _ = query.communicate(timeout=0.05)
                        break
                    except subprocess.TimeoutExpired:
                        if stop.is_set() or time.monotonic() >= deadline:
                            query.kill()
                            query.communicate()
                            raise subprocess.TimeoutExpired(command, 2)
                if query.returncode:
                    raise subprocess.CalledProcessError(query.returncode, command)
            report = parse_status(output)
        except (OSError, ValueError, subprocess.SubprocessError):
            report = ('error', None, None)
        reports.put(report)
        stop.wait(interval)


def reap_attachment(pid):
    """Signal only the forked attachment, never a process group or agent PID."""
    found, status = os.waitpid(pid, os.WNOHANG)
    if found:
        return os.waitstatus_to_exitcode(status)
    os.kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + 0.5
    while time.monotonic() < deadline:
        found, status = os.waitpid(pid, os.WNOHANG)
        if found:
            return os.waitstatus_to_exitcode(status)
        time.sleep(0.01)
    os.kill(pid, signal.SIGKILL)
    _, status = os.waitpid(pid, 0)
    return os.waitstatus_to_exitcode(status)


def run_bridge(args, command):
    stop = threading.Event()
    reports = queue.SimpleQueue()
    size = termios.tcgetwinsize(0) if os.isatty(0) else (24, 80)
    pid, master = pty.fork()
    if pid == 0:
        try:
            termios.tcsetwinsize(0, size)
            os.execvp(command[0], command)
        except OSError:
            os.write(2, b'legacy-hc-bridge: cannot execute attachment\r\n')
            os._exit(127)
    saved_terminal = termios.tcgetattr(0) if os.isatty(0) else None
    if saved_terminal is not None:
        tty.setraw(0)
    def resize(*_):
        if os.isatty(0):
            termios.tcsetwinsize(master, termios.tcgetwinsize(0))

    previous = {signal.SIGWINCH: signal.signal(signal.SIGWINCH, resize)}
    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        previous[sig] = signal.signal(sig, lambda *_: stop.set())
    worker = threading.Thread(target=poll_status, args=(
        [args.herdr, '--session', args.session, 'agent', 'get', args.target],
        args.poll_interval, stop, reports), daemon=True)
    worker.start()
    last = pending = None
    boundary = OutputBoundary()
    try:
        while not stop.is_set():
            while not reports.empty():
                pending = reports.get()
            if pending is not None and pending != last and boundary.safe:
                write_all(1, encode_status(pending), stop)
                last = pending
            readable, _, _ = select.select([master, 0], [], [], 0.05)
            if 0 in readable:
                typed = os.read(0, 65536)
                if not typed:
                    break
                write_all(master, typed, stop)
            if master in readable:
                try:
                    data = os.read(master, 65536)
                except OSError as exc:
                    if exc.errno != errno.EIO:
                        raise
                    break
                if not data:
                    break
                boundary.feed(data)
                write_all(1, data, stop)
    finally:
        stop.set()
        code = reap_attachment(pid)
        os.close(master)
        worker.join(timeout=3)
        if saved_terminal is not None:
            termios.tcsetattr(0, termios.TCSANOW, saved_terminal)
        for sig, handler in previous.items():
            signal.signal(sig, handler)
    return code if code >= 0 else 128 - code


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    command = None
    if '--' in argv:
        index = argv.index('--')
        command, argv = argv[index + 1:], argv[:index]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--herdr', default='herdr')
    parser.add_argument('--session', default='default')
    parser.add_argument('--poll-interval', type=float, default=4.0)
    parser.add_argument('target')
    args = parser.parse_args(argv)
    if not math.isfinite(args.poll_interval) or args.poll_interval <= 0:
        parser.error('--poll-interval must be finite and positive')
    if command == []:
        parser.error('-- requires an attachment command')
    if command is None:
        command = [args.herdr, '--session', args.session,
                   'agent', 'attach', args.target]
    return run_bridge(args, command)


if __name__ == '__main__':
    raise SystemExit(main())
