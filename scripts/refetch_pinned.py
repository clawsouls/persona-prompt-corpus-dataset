#!/usr/bin/env python3
"""Re-fetch every record at its pinned commit and compare with the release.

    python3 scripts/refetch_pinned.py [--workers 8]

For each record, downloads https://raw.githubusercontent.com/<repo>/<commit_sha>/<path>.
Records with bundled text are compared byte for byte (SHA-256) with data/<full_text_ref>;
metadata-only records report whether the pinned bytes are still reachable. Nothing is
written. Outcomes: same, differs, reachable (metadata-only), gone (HTTP 404), or other.

This is the check that produced the `refetch` field (2026-09-06: 280 same, 1 replaced by
the pinned version, 3 gone). Upstream repositories keep disappearing, so a later run will
report more `gone` records; the release itself does not change.

If every record comes back as `other` with CERTIFICATE_VERIFY_FAILED, Python cannot find CA
certificates (common with the python.org installer on macOS). Run its "Install
Certificates.command", or point SSL_CERT_FILE at a CA bundle such as /etc/ssl/cert.pem.
"""
import argparse, hashlib, json, urllib.error, urllib.parse, urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fetch(r):
    s = r['source']
    url = f"https://raw.githubusercontent.com/{s['repo']}/{s['commit_sha']}/{urllib.parse.quote(s['path'])}"
    try:
        with urllib.request.urlopen(url, timeout=40) as resp:
            return r, 200, resp.read()
    except urllib.error.HTTPError as e:
        return r, e.code, b''
    except Exception as e:
        return r, str(getattr(e, 'reason', e))[:120], b''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(ROOT / 'data/records.jsonl', encoding='utf-8')]
    out = Counter()
    with ThreadPoolExecutor(a.workers) as ex:
        for r, code, body in ex.map(fetch, recs):
            ref = r.get('full_text_ref')
            if code == 200 and ref:
                local = (ROOT / 'data' / ref).read_bytes()
                k = 'same' if hashlib.sha256(local).digest() == hashlib.sha256(body).digest() else 'differs'
            elif code == 200:
                k = 'reachable'
            elif code == 404:
                k = 'gone'
            else:
                k = 'other'
            out[k] += 1
            if k not in ('same', 'reachable'):
                print(f"  {k:<8} {r['id']} {r['source']['repo']}/{r['source']['path']} ({code})")
    print(json.dumps(dict(out), sort_keys=True))


if __name__ == '__main__':
    main()
