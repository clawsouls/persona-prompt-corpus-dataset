#!/usr/bin/env python3
"""Label-independent corpus figures of the paper (Table I and Sec. IV-A) from data/records.jsonl.

    python3 scripts/stats.py
"""
import json, pathlib, statistics
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
recs = [json.loads(l) for l in open(ROOT / "data/records.jsonl", encoding="utf-8")]

by_path = Counter(r["source"]["search_path"] for r in recs)
repos_by_path = {}
for r in recs:
    repos_by_path.setdefault(r["source"]["search_path"], set()).add(r["source"]["repo"])
fmt = Counter(r["stats"]["format"] for r in recs)
lang = Counter(r["stats"]["lang"] for r in recs)
words = [r["stats"]["words"] for r in recs]
no_hdr = sum(1 for r in recs if r["stats"]["headers_max_depth"] == 0)
code = sum(1 for r in recs if r["stats"]["has_code_block"])
table = sum(1 for r in recs if r["stats"]["has_table"])
lic = Counter(r["license"]["spdx"] for r in recs)
inc = sum(1 for r in recs if r["license"]["content_included"])
sha = sum(1 for r in recs if r["source"]["commit_sha"])
N = len(recs)

print(f"## Corpus statistics (records.jsonl, N={N})\n")
print("### Yield by search path")
print("| search path | files | repos |\n|---|---|---|")
for p in ["persona", "agent", "role", "identity", "soul"]:
    print(f"| {p} | {by_path.get(p, 0)} | {len(repos_by_path.get(p, set()))} |")
print(f"| total | {N} | {len(set(r['source']['repo'] for r in recs))} |\n")
print("### Format and structure")
print("- format: " + ", ".join(f"{k} {v} ({v / N:.0%})" for k, v in fmt.most_common()))
print("- language: " + ", ".join(f"{k} {v}" for k, v in lang.most_common()))
print(f"- words: median {statistics.median(words):.0f}, mean {statistics.mean(words):.0f}, min {min(words)}, max {max(words)}")
print(f"- no header {no_hdr} ({no_hdr / N:.0%}), code block {code} ({code / N:.0%}), table {table} ({table / N:.0%})")
print("\n### License gate")
print(f"- full text shipped: {inc}/{N} ({inc / N:.0%})")
for k, v in lic.most_common():
    print(f"  - {k}: {v}")
print(f"- commit SHA pinned: {sha}/{N}")
