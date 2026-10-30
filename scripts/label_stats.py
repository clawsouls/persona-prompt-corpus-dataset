#!/usr/bin/env python3
"""Annotation-dependent figures of the paper (Sec. IV-B), regenerated per rater.

    python3 scripts/label_stats.py

Reads data/records.jsonl and labels/rater{1,2}.csv. For each rater it prints content
types, facet prevalence, conditional clauses, the form distribution, form x content type
(Table III) with Fisher's exact test, and the per-search-path figures for RQ3 at file
level and averaged per repository. Path figures join on source.search_path.
"""
import csv, json, statistics as st
from collections import Counter
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACETS = ['identity_declared', 'rule_declared', 'has_role', 'has_goal', 'has_context',
          'has_output_spec', 'has_conditions', 'multi_step', 'structured_relation']
FORM = {2: 'full-pack', 1: 'flat', 0: 'prose'}
TYPES = ['both', 'identity', 'rules', 'neither']
R = {r['id']: r for r in map(json.loads, open(ROOT / 'data/records.jsonl', encoding='utf-8'))}


def load(name):
    with open(ROOT / 'labels' / name, encoding='utf-8') as f:
        return {r['id']: {k: int(v) for k, v in r.items() if k != 'id'} for r in csv.DictReader(f)}


def ctype(x):
    return {(1, 1): 'both', (1, 0): 'identity', (0, 1): 'rules', (0, 0): 'neither'}[(x['identity_declared'], x['rule_declared'])]


def fisher(a, b, c, d):
    """Two-sided Fisher's exact test for [[a, b], [c, d]]."""
    r1, c1, n = a + b, a + c, a + b + c + d
    p = lambda k: comb(c1, k) * comb(n - c1, r1 - k) / comb(n, r1)
    obs = p(a)
    return min(1.0, sum(p(k) for k in range(max(0, r1 + c1 - n), min(r1, c1) + 1) if p(k) <= obs * (1 + 1e-9)))


def pct(k, n):
    return f'{k / n:.1%} ({k}/{n})'


def report(name):
    L = load(name); ids = [i for i in R if i in L]; n = len(ids); out = [f'## {name} (n={n})']
    ct = Counter(ctype(L[i]) for i in ids)
    out.append('content type: ' + ', '.join(f'{t} {pct(ct[t], n)}' for t in TYPES))
    prev = sorted(FACETS, key=lambda f: -sum(L[i][f] for i in ids))
    out.append('facet prevalence: ' + ', '.join(f"{f} {sum(L[i][f] for i in ids) / n:.0%}" for f in prev))
    cc = [L[i]['conditions_count'] for i in ids]; pos = [c for c in cc if c > 0]
    out.append(f'conditions_count >= 1: {pct(len(pos), n)}; median among those {st.median(pos)}, '
               f'mean {st.mean(pos):.1f}, max {max(pos)}')
    m1 = [i for i in ids if L[i]['has_conditions'] == 0 and L[i]['conditions_count'] >= 1]
    m2 = [i for i in ids if L[i]['has_conditions'] == 1 and L[i]['conditions_count'] == 0]
    out.append(f'has_conditions=0 but count>=1: {len(m1)} {m1}; has_conditions=1 but count=0: {len(m2)} {m2}')
    fd = Counter(L[i]['structure_form'] for i in ids)
    out.append('form: ' + ', '.join(f'{s} {FORM[s]} {pct(fd[s], n)}' for s in (2, 1, 0)))
    out.append('\n| form | ' + ' | '.join(TYPES) + ' | total |\n|---|---|---|---|---|---|')
    for s in (2, 1, 0):
        c = Counter(ctype(L[i]) for i in ids if L[i]['structure_form'] == s)
        out.append(f'| {s} {FORM[s]} | ' + ' | '.join(str(c[t]) for t in TYPES) + f' | {sum(c.values())} |')
    full = [i for i in ids if L[i]['structure_form'] == 2]; rest = [i for i in ids if L[i]['structure_form'] != 2]
    a = sum(ctype(L[i]) == 'neither' for i in full); c = sum(ctype(L[i]) == 'neither' for i in rest)
    out.append(f'\nneither: full-pack {pct(a, len(full))} vs rest {pct(c, len(rest))}; '
               f"Fisher's exact (full-pack x neither) p = {fisher(a, len(full) - a, c, len(rest) - c):.2g}")
    out.append('\n| path | files | repos | full-pack | conditions | both | full-pack (repo avg) | conditions (repo avg) | both (repo avg) |'
               '\n|---|---|---|---|---|---|---|---|---|')
    for sp in ['soul', 'persona', 'identity', 'agent', 'role']:
        g = [i for i in ids if R[i]['source']['search_path'] == sp]
        if not g:
            continue
        repos = {}
        for i in g:
            repos.setdefault(R[i]['source']['repo'], []).append(i)
        ind = [('full-pack', lambda i: L[i]['structure_form'] == 2), ('conditions', lambda i: L[i]['has_conditions'] == 1),
               ('both', lambda i: ctype(L[i]) == 'both')]
        fl = [sum(map(f, g)) / len(g) for _, f in ind]
        ra = [st.mean(sum(map(f, m)) / len(m) for m in repos.values()) for _, f in ind]
        out.append(f'| {sp} | {len(g)} | {len(repos)} | ' + ' | '.join(f'{v:.0%}' for v in fl + ra) + ' |')
    return '\n'.join(out)


if __name__ == '__main__':
    print('\n\n'.join(report(n) for n in ('rater1.csv', 'rater2.csv')))
