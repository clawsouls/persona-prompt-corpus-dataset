#!/usr/bin/env python3
"""Inter-rater agreement from the released label tables.

    python3 scripts/agreement.py [--disagreements labels/disagreements.csv]

Reads labels/rater1.csv and labels/rater2.csv (281 records each, same ids) and reports,
for each coded field, raw agreement, Cohen's kappa, and Krippendorff's alpha at the
matching level of measurement:

  nine content facets   nominal alpha, unweighted kappa
  structure_form        ordinal alpha, quadratic-weighted kappa
  conditions_count      interval alpha, Spearman rho

95% intervals come from 1,000 bootstrap resamples of records (seed 20261021). Point
estimates match the paper exactly; bootstrap intervals can differ in the second decimal
across library versions. With --disagreements, every record where the raters differ on a
field is written as one row: id, field, rater1, rater2.
"""
import argparse, csv, random
from collections import Counter
from pathlib import Path

import numpy as np
import krippendorff

ROOT = Path(__file__).resolve().parent.parent
FACETS = ['identity_declared', 'rule_declared', 'has_role', 'has_goal', 'has_context',
          'has_output_spec', 'has_conditions', 'multi_step', 'structured_relation']
FIELDS = FACETS + ['structure_form', 'conditions_count']


def load(name):
    with open(ROOT / 'labels' / name, encoding='utf-8') as f:
        return {r['id']: {k: int(v) for k, v in r.items() if k != 'id'} for r in csv.DictReader(f)}


def kappa(a, b, weights=None):
    cats = sorted(set(a) | set(b)); k = len(cats); ix = {c: i for i, c in enumerate(cats)}
    o = np.zeros((k, k))
    for x, y in zip(a, b):
        o[ix[x], ix[y]] += 1
    o /= o.sum(); e = np.outer(o.sum(1), o.sum(0))
    if weights is None:
        w = 1 - np.eye(k)
    else:
        d = np.subtract.outer(np.arange(k), np.arange(k)) / max(k - 1, 1)
        w = d ** 2 if weights == 'quadratic' else np.abs(d)
    return 1 - (w * o).sum() / (w * e).sum()


def alpha(a, b, level):
    return krippendorff.alpha(reliability_data=np.array([a, b], dtype=float), level_of_measurement=level)


def ranks(x):
    x = np.asarray(x, float); order = x.argsort(); r = np.empty(len(x)); r[order] = np.arange(len(x))
    for v in np.unique(x):
        m = x == v; r[m] = r[m].mean()
    return r


def spearman(a, b):
    return np.corrcoef(ranks(a), ranks(b))[0, 1]


def boot(fn, a, b, rng, n=1000):
    N = len(a); v = []
    for _ in range(n):
        s = [rng.randrange(N) for _ in range(N)]
        try:
            v.append(fn([a[j] for j in s], [b[j] for j in s]))
        except Exception:
            pass
    return np.percentile(v, 2.5), np.percentile(v, 97.5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--disagreements', help='write per-field disagreement rows to this CSV')
    args = ap.parse_args()
    A, B = load('rater1.csv'), load('rater2.csv')
    if sorted(A) != sorted(B):
        raise SystemExit('rater tables cover different ids')
    ids = sorted(A); N = len(ids); rng = random.Random(20261021)
    col = lambda f, L: [L[i][f] for i in ids]
    print(f'n = {N}\n')
    print(f"{'field':<22}{'agree':>7}{'kappa':>8}{'alpha':>8}  alpha 95% CI     r1=1  r2=1  1/0  0/1")
    for f in FACETS:
        a, b = col(f, A), col(f, B)
        k = kappa(a, b); boot(kappa, a, b, rng)
        x = alpha(a, b, 'nominal'); lo, hi = boot(lambda p, q: alpha(p, q, 'nominal'), a, b, rng)
        c = Counter(zip(a, b))
        print(f"{f:<22}{sum(p == q for p, q in zip(a, b)) / N:>7.0%}{k:>8.2f}{x:>8.2f}  [{lo:5.2f}, {hi:5.2f}]  "
              f"{sum(a) / N:>4.0%}  {sum(b) / N:>4.0%}  {c[(1, 0)]:>3}  {c[(0, 1)]:>3}")
    a, b = col('structure_form', A), col('structure_form', B)
    kq = kappa(a, b, 'quadratic'); boot(lambda p, q: kappa(p, q, 'quadratic'), a, b, rng)
    x = alpha(a, b, 'ordinal'); lo, hi = boot(lambda p, q: alpha(p, q, 'ordinal'), a, b, rng)
    far = sum(abs(p - q) > 1 for p, q in zip(a, b)); dis = sum(p != q for p, q in zip(a, b))
    print(f"\nstructure_form        agree {sum(p == q for p, q in zip(a, b)) / N:.0%}  quadratic kappa {kq:.2f}  "
          f"ordinal alpha {x:.2f} [{lo:.2f}, {hi:.2f}]  disagreements {dis} ({dis - far} one level apart)")
    a, b = col('conditions_count', A), col('conditions_count', B)
    x = alpha(a, b, 'interval'); lo, hi = boot(lambda p, q: alpha(p, q, 'interval'), a, b, rng)
    d = sorted(q - p for p, q in zip(a, b))
    print(f"conditions_count      exact {sum(p == q for p, q in zip(a, b)) / N:.0%}  Spearman rho {spearman(a, b):.2f}  "
          f"interval alpha {x:.2f} [{lo:.2f}, {hi:.2f}]  median(rater2 - rater1) {np.median(d):g}")
    if args.disagreements:
        with open(args.disagreements, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['id', 'field', 'rater1', 'rater2']); n = 0
            for fld in FIELDS:
                for i in ids:
                    if A[i][fld] != B[i][fld]:
                        w.writerow([i, fld, A[i][fld], B[i][fld]]); n += 1
        print(f'\n{n} disagreement rows → {args.disagreements}')


if __name__ == '__main__':
    main()
