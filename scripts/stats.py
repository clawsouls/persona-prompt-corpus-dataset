#!/usr/bin/env python3
"""records.jsonl → 논문 표·수치 재생성 (논문 숫자의 단일 소스)
사용: python3 scripts/stats.py [--md]
"""
import json, pathlib, statistics, sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
recs = [json.loads(l) for l in open(ROOT / "data/records.jsonl")]

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

print(f"## 코퍼스 통계 (records.jsonl, N={N})\n")
print("### 표 1 — 검색 경로별 분포")
print("| search path | files | repos |\n|---|---|---|")
for p in ["persona", "agent", "role", "identity", "soul"]:
    print(f"| path:{p} | {by_path.get(p,0)} | {len(repos_by_path.get(p,set()))} |")
print(f"| **합계** | **{N}** | **{len(set(r['source']['repo'] for r in recs))}** |\n")
print("### 표 2 — 형식·구조 특징")
print(f"- 형식: " + ", ".join(f"{k} {v} ({v/N:.0%})" for k, v in fmt.most_common()))
print(f"- 언어: " + ", ".join(f"{k} {v}" for k, v in lang.most_common()))
print(f"- 분량(단어): 중앙값 {statistics.median(words):.0f} · 평균 {statistics.mean(words):.0f} · 최소 {min(words)} · 최대 {max(words)}")
print(f"- 헤더 없음(구조 부재): {no_hdr} ({no_hdr/N:.0%}) · 코드블록 {code} ({code/N:.0%}) · 표 {table} ({table/N:.0%})")
print(f"\n### 표 3 — 라이선스 (게이트)")
print(f"- 원문 공개수록 가능: {inc}/{N} ({inc/N:.0%})")
for k, v in lic.most_common(8):
    print(f"  - {k}: {v}")
print(f"- provenance(commit_sha) 확보: {sha}/{N}")
