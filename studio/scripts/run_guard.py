#!/usr/bin/env python3
"""Persistent local-stage guard. Not suitable for remote writes or publication."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def atomic(path, data):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state-dir", required=True)
    p.add_argument("--stage", required=True)
    p.add_argument("--input", action="append", default=[])
    p.add_argument("--output", action="append", required=True)
    p.add_argument("--timeout", type=float, default=180)
    p.add_argument("--reset-reason")
    p.add_argument("command", nargs=argparse.REMAINDER)
    a = p.parse_args()
    if not a.stage.replace("-", "").replace("_", "").isalnum(): p.error("Invalid stage")
    cmd = a.command[1:] if a.command[:1] == ["--"] else a.command
    if not cmd or a.timeout <= 0: p.error("Command and positive timeout required")
    d = Path(a.state_dir); d.mkdir(parents=True, exist_ok=True)
    lock = (d / (a.stage + ".lock")).open("w")
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("BUSY: stage already running"); return 75
    path = d / (a.stage + ".json")
    state = json.loads(path.read_text()) if path.exists() else {"failures":0,"history":[]}
    fingerprint = hashlib.sha256(json.dumps({"command":cmd, "cwd":os.getcwd(),"inputs":{str(Path(f).resolve()):sha(f) for f in a.input}},sort_keys=True).encode()).hexdigest()
    outputs = [str(Path(f).resolve()) for f in a.output]
    valid = state.get("fingerprint") == fingerprint and state.get("status") == "success" and set(state.get("outputs",{})) == set(outputs) and all(Path(f).is_file() and Path(f).stat().st_size > 0 and sha(f) == h for f,h in state.get("outputs",{}).items())
    if valid:
        print("SKIP: unchanged inputs and verified outputs"); return 0
    if a.reset_reason:
        state["history"].append({"reset_reason":a.reset_reason,"at":time.time()})
        state["failures"] = 0
    if state.get("fingerprint") != fingerprint:
        state["failures"] = 0
    if state.get("failures",0) >= 2:
        print("BLOCKED: two failures; diagnose and record --reset-reason"); return 78
    state.update(fingerprint=fingerprint,status="running",started=time.time())
    # Reserve an attempt before launch. Crashes/interruption cannot create an unbounded loop.
    state["failures"] = state.get("failures",0) + 1
    atomic(path,state)
    code = 1
    log = d / (a.stage + ".log")
    try:
        with log.open("wb") as out:
            proc = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT,start_new_session=True)
            try: code = proc.wait(timeout=a.timeout)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGTERM)
                try: proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid,signal.SIGKILL); proc.wait()
                code = 124
    except OSError as e:
        log.write_text(str(e)); code = 127
    if code == 0 and not all(Path(f).is_file() and Path(f).stat().st_size > 0 for f in outputs):
        code = 66
    state["history"].append({"code":code,"at":time.time()})
    state["status"] = "success" if code == 0 else "failed"
    if code == 0:
        state["outputs"] = {f:sha(f) for f in outputs}; state["failures"] = 0
    atomic(path,state)
    # Keep the diagnostic tail, not unbounded repeated logs.
    if log.stat().st_size > 2_000_000:
        with log.open("rb") as f: f.seek(-2_000_000,2); tail=f.read()
        log.write_bytes(tail)
    print(f"{state['status'].upper()}: exit={code}; log={log}")
    return code if code >= 0 else 128 - code

if __name__ == "__main__": sys.exit(main())
