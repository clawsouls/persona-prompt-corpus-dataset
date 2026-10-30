#!/usr/bin/env python3
"""Audit the license gate from the record fields, optionally against GitHub today.

    python3 scripts/license_gate.py            # recount the gate from records.jsonl
    python3 scripts/license_gate.py --requery  # also re-read each repository's SPDX id
                                               # (uses $GITHUB_TOKEN if set; 168 API calls)

The gate is a rule over two fields. `license.redistributable` records whether the upstream
SPDX license permits redistribution; `license.content_included` records whether the text
was shipped. Text ships only for permissive licenses; copyleft repositories are kept
metadata-only to keep the archive's licensing simple, and repositories without a license
are never shipped. This script checks that every shipped file has content_included = true,
that no other record has a file, and prints the SPDX breakdown.
"""
import argparse, json, os, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def spdx_now(repo):
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}', headers={'Accept': 'application/vnd.github+json'})
    if os.environ.get('GITHUB_TOKEN'):
        req.add_header('Authorization', f"Bearer {os.environ['GITHUB_TOKEN']}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return ((json.load(r).get('license') or {}).get('spdx_id')) or 'NOASSERTION'
    except Exception as e:
        return f'error: {getattr(e, "code", type(e).__name__)}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--requery', action='store_true')
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(ROOT / 'data/records.jsonl', encoding='utf-8')]
    files = {p.name for p in (ROOT / 'data/content').glob('*')}
    shipped = [r for r in recs if r['license'].get('content_included')]
    bad = [r['id'] for r in recs if bool(r.get('full_text_ref')) != bool(r['license'].get('content_included'))]
    missing = [r['id'] for r in shipped if Path(r['full_text_ref']).name not in files]
    print(f'records {len(recs)} · text shipped {len(shipped)} · metadata only {len(recs) - len(shipped)} · files {len(files)}')
    print('shipped by SPDX:', dict(Counter(r['license']['spdx'] for r in shipped).most_common()))
    print('withheld by SPDX:', dict(Counter(r['license']['spdx'] for r in recs if not r['license'].get('content_included')).most_common()))
    repos = {r['source']['repo']: r['license']['spdx'] for r in recs}
    print(f'repositories {len(repos)}:', dict(Counter(repos.values()).most_common()))
    ok = not bad and not missing and len(files) == len(shipped)
    if bad:
        print('full_text_ref and content_included disagree:', bad)
    if missing:
        print('shipped records without a file:', missing)
    if a.requery:
        changed = [(repo, was, now) for repo, was in repos.items() if (now := spdx_now(repo)) != was]
        print(f'SPDX changed or unreachable since collection: {len(changed)}')
        for repo, was, now in changed:
            print(f'  {repo}: {was} -> {now}')
    print('gate OK' if ok else 'gate FAILED')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
