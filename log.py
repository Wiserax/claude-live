#!/usr/bin/env python3
"""Append log lines / update fields in progress.json, then commit + push (Pages redeploys)."""
import json, sys, subprocess, datetime, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
p = json.load(open('progress.json')) if os.path.exists('progress.json') else {"log": [], "top": [], "sofa": []}
now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).strftime('%H:%M')
args = sys.argv[1:]
if args and args[0] == '--json':          # merge a JSON file (top / sofa) into progress
    p.update(json.load(open(args[1]))); args = args[2:]
for m in args:
    p["log"].append({"t": now, "m": m})
json.dump(p, open('progress.json', 'w'), ensure_ascii=False, indent=0)
if os.path.isdir('.git'):
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-q', '-m', 'progress ' + now + '\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01BqUiUCQeviQV8aYrTZesxX'], check=False)
    subprocess.run(['git', 'push', '-q'], check=False)
print('ok', len(p['log']), 'lines')
