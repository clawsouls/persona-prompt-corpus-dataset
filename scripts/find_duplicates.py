#!/usr/bin/env python3
"""Duplicate / template-reuse detection over the raw collected corpus.

Tiers (calibrated 2026-08-11; positive control: file vs itself with 10% of
lines dropped gives 5-gram Jaccard 0.799 — an 0.8 threshold FAILS it, so
near-dup uses 0.5):

  exact            — SHA-256 of whitespace-normalized text.
  near             — word 5-gram shingle Jaccard >= 0.50 (clustered, union-find).
  template-related — containment |A∩B|/min(|A|,|B|) >= 0.50 (clustered):
                     catches template + additions where Jaccard dilutes.
  phrase-reuse     — pair shares >= 30 distinct 5-gram shingles (a few
                     sentences) without reaching the cluster tiers. Pairwise
                     list, quantifies the goldset pilot's "identical phrases
                     in unrelated files" observation.

Nothing is deleted: outputs are analysis labels.
  dup_clusters.recomputed.csv       — one row per member of a cluster (>=2 files)
  phrase_reuse_pairs.recomputed.csv — pairwise phrase-reuse below cluster tiers

The released data/dup_clusters.csv was computed over all 281 files. This release ships
text for 179 of them, so a re-run here covers only those; fetch the other files at their
pinned SHAs (raw.githubusercontent.com/<repo>/<commit_sha>/<path>) to reproduce the full run.

Usage: python3 scripts/find_duplicates.py
"""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "data" / "records.jsonl"
OUT_CLUSTERS = ROOT / "dup_clusters.recomputed.csv"
OUT_PHRASES = ROOT / "phrase_reuse_pairs.recomputed.csv"
JACCARD_THRESHOLD = 0.50
CONTAINMENT_THRESHOLD = 0.50
PHRASE_SHINGLES = 30
SHINGLE_N = 5


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    out, blank = [], False
    for ln in lines:
        if ln == "":
            if not blank:
                out.append(ln)
            blank = True
        else:
            out.append(ln)
            blank = False
    return "\n".join(out).strip()


def shingles(text: str) -> set:
    words = re.findall(r"[a-z0-9가-힣]+", text.lower())
    if len(words) < SHINGLE_N:
        return {tuple(words)} if words else set()
    return {tuple(words[i : i + SHINGLE_N]) for i in range(len(words) - SHINGLE_N + 1)}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def containment(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def main() -> None:
    docs = []
    missing = 0
    for line in open(RECORDS, encoding="utf-8"):
        r = json.loads(line)
        ref = r.get("full_text_ref")
        p = ROOT / "data" / ref if ref else None
        if not p or not p.exists():
            missing += 1
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        norm = normalize(raw)
        docs.append(
            {
                "id": r["id"],
                "repo": r["source"]["repo"],
                "path": r["source"]["path"],
                "sha": hashlib.sha256(norm.encode()).hexdigest(),
                "sh": shingles(norm),
            }
        )
    print(f"loaded {len(docs)} raw files ({missing} records without a resolvable file)")

    # self-check: positive control (drop 10% of shingles) must pass at current thresholds
    base = docs[0]
    sh = list(base["sh"])
    mut = set(sh[: int(len(sh) * 0.9)])
    pc = jaccard(base["sh"], mut)
    assert pc >= JACCARD_THRESHOLD, f"positive control failed: {pc:.3f} < {JACCARD_THRESHOLD}"
    print(f"positive control: jaccard(self, 90% of self)={pc:.3f} >= {JACCARD_THRESHOLD} OK")

    parent = {d["id"]: d["id"] for d in docs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    pair_stats = {}  # (id_a, id_b) -> dict
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            a, b = docs[i], docs[j]
            inter = len(a["sh"] & b["sh"])
            if not inter:
                continue
            jc = inter / len(a["sh"] | b["sh"])
            ct = inter / min(len(a["sh"]), len(b["sh"]))
            exact = a["sha"] == b["sha"]
            if exact or jc >= JACCARD_THRESHOLD or ct >= CONTAINMENT_THRESHOLD:
                union(a["id"], b["id"])
            pair_stats[(a["id"], b["id"])] = {
                "inter": inter, "jaccard": jc, "containment": ct, "exact": exact,
                "a": a, "b": b,
            }

    clusters = {}
    for d in docs:
        clusters.setdefault(find(d["id"]), []).append(d)

    by_id = {d["id"]: d for d in docs}
    rows = []
    n_cluster = cross_repo_clusters = 0
    clustered_ids = set()
    for _, members in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
        if len(members) < 2:
            continue
        n_cluster += 1
        cid = f"dup-{n_cluster:03d}"
        repos = {m["repo"] for m in members}
        cross = len(repos) > 1
        if cross:
            cross_repo_clusters += 1
        sha_counts = {}
        for m in members:
            sha_counts[m["sha"]] = sha_counts.get(m["sha"], 0) + 1
        for m in members:
            clustered_ids.add(m["id"])
            kind = "exact" if sha_counts[m["sha"]] > 1 else "near-or-template"
            rows.append(
                {
                    "cluster_id": cid, "record_id": m["id"], "repo": m["repo"],
                    "path": m["path"], "kind": kind, "cluster_size": len(members),
                    "cross_repo": "yes" if cross else "no",
                }
            )

    phrase_rows = []
    for (ia, ib), st in sorted(pair_stats.items(), key=lambda kv: -kv[1]["inter"]):
        if st["exact"] or st["jaccard"] >= JACCARD_THRESHOLD or st["containment"] >= CONTAINMENT_THRESHOLD:
            continue
        if st["inter"] < PHRASE_SHINGLES:
            continue
        a, b = st["a"], st["b"]
        phrase_rows.append(
            {
                "record_id_a": ia, "repo_a": a["repo"], "path_a": a["path"],
                "record_id_b": ib, "repo_b": b["repo"], "path_b": b["path"],
                "shared_shingles": st["inter"],
                "jaccard": f"{st['jaccard']:.3f}",
                "containment": f"{st['containment']:.3f}",
                "cross_repo": "yes" if a["repo"] != b["repo"] else "no",
            }
        )

    with open(OUT_CLUSTERS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["cluster_id", "record_id", "repo", "path", "kind", "cluster_size", "cross_repo"],
        )
        w.writeheader()
        w.writerows(rows)
    with open(OUT_PHRASES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "record_id_a", "repo_a", "path_a", "record_id_b", "repo_b", "path_b",
                "shared_shingles", "jaccard", "containment", "cross_repo",
            ],
        )
        w.writeheader()
        w.writerows(phrase_rows)

    cross_phrase = sum(1 for r in phrase_rows if r["cross_repo"] == "yes")
    print(f"clusters (>=2 files): {n_cluster} covering {len(clustered_ids)}/{len(docs)} files")
    print(f"cross-repo clusters: {cross_repo_clusters}")
    print(f"phrase-reuse pairs (>= {PHRASE_SHINGLES} shared shingles, below cluster tiers): "
          f"{len(phrase_rows)} ({cross_phrase} cross-repo)")
    print(f"unique-content estimate: {len(docs) - len(clustered_ids) + n_cluster}")
    print(f"wrote {OUT_CLUSTERS.relative_to(ROOT)}, {OUT_PHRASES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
