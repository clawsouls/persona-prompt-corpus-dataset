# Persona Prompt Corpus

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23230144.svg)](https://doi.org/10.5281/zenodo.23230144)

A dataset of **281 AI agent persona prompts** collected from public GitHub repositories.
These are files such as `SOUL.md`, `persona.md`, and `IDENTITY.md` that declare an agent's
identity, values, tone, and behavioral limits. Every record is pinned to a repository,
path, and commit SHA.

- **281 records from 168 repositories**
- **Provenance pinned for every record** (281/281) — repository, path, and the commit SHA at collection time
- Full text included for **179**, metadata only for **102** (see "License gate" below)
- **Two raters' labels for every record** (v1.1): nine content facets, a count of conditional
  clauses, and an ordinal form scale, with the annotation guide and per-field disagreements

한국어 설명: [README.ko.md](README.ko.md)

> The figures in this README are counted from the data by the build script.
> They are not written by hand, so they cannot drift from the dataset.

---

## What is in here

```
data/
  records.jsonl          281 records (JSON Lines)
  content/               179 source files — only where redistribution is permitted
  dup_clusters.csv       cross-repository near-duplicate clusters (kept in the corpus, listed here)
labels/
  rater1.csv             rater 1's labels, one row per record
  rater2.csv             rater 2's labels, coded independently
  disagreements.csv      every record × field where the two raters differ (1017 rows)
schema/
  record.schema.json     record schema
docs/
  COLLECTION_METHOD.md   how the corpus was collected
  ANNOTATION_GUIDE.md    the labeling questions and boundary cases
  SCHEME_HISTORY.md      why the form scale has three levels (pilot figures)
scripts/
  stats.py               corpus statistics (label-independent)
  label_stats.py         label-dependent figures, per rater
  agreement.py           inter-rater agreement (Krippendorff's alpha, Cohen's kappa)
  refetch_pinned.py      re-fetch every record at its pinned commit and compare
  license_gate.py        audit the license gate; optionally re-read SPDX ids from GitHub
  find_duplicates.py     near-duplicate detection (re-run covers the shipped texts)
requirements.txt
```

### One record

```json
{
  "id": "gh-000013",
  "source": {
    "repo": "ceciliomichael/echode",
    "path": "identity/ask.md",
    "commit_sha": "e1dc45961bf4ffebf7d8a3696c3bc2b5de7c180e",
    "url": "https://github.com/ceciliomichael/echode/blob/HEAD/identity/ask.md",
    "collected_at": "2026-08-09",
    "search_path": "identity"
  },
  "license": { "spdx": "MIT", "redistributable": true, "copyleft_review": false, "content_included": true },
  "full_text_ref": "content/gh-000013.md",
  "content_sha256": "…",
  "summary": "Excerpt of a coding-assistant app's 'Ask Mode' identity + communication-style prompt sections: …",
  "tags": ["coding-assistant", "documentation-excerpt"],
  "stats": { "chars": 937, "words": 125, "lang": "en", "format": "md",
             "headers_max_depth": 1, "has_code_block": true, "has_table": false },
  "refetch": "same",
  "refetched_at": "2026-09-06"
}
```

When `full_text_ref` is `null`, the source file is not bundled. That record still carries
`source.commit_sha`, so **you can fetch the original yourself while the upstream repository
still exists.** Repositories can be deleted or made private after collection, and some already
have; for those records only the metadata remains.

---

## License gate — why 102 records have no text

Redistributing a source file republishes someone else's work. We checked the SPDX license of
every repository in the corpus and bundled the text only where redistribution is permitted.

| | Records |
|---|---|
| Text included | **179** |
| Metadata only | **102** |

Licenses of the included records: MIT 138 · Apache-2.0 31 · CC-BY-4.0 7 · BSD-3-Clause 2 · CC0-1.0 1

Most of the 102 excluded records come from **repositories with no declared license**.
No license does not mean "free to use" — copyright remains with the author, so the text is
not bundled. The rest are copyleft repositories, kept as metadata to keep the archive's
licensing simple.

This judgment lives **in the data, not in prose** — the fields `license.redistributable` and
`license.content_included` let you audit every record one by one. The bundle is regenerated
from those fields by a build script; no one hand-picks the files.

---

## Labels

Both raters coded all 281 records independently, without discussion and without any
machine pre-filling. Each row of `labels/rater1.csv` and `labels/rater2.csv` has:

| field | type | question |
|---|---|---|
| `identity_declared` | 0/1 | does the file say who the agent is (name, role, character, voice, values)? |
| `rule_declared` | 0/1 | does it say what the agent should or should not do? |
| `has_role` | 0/1 | is a job or functional role named? |
| `has_goal` | 0/1 | is a goal stated? |
| `has_context` | 0/1 | is project, user, or environment background given? |
| `has_output_spec` | 0/1 | is the form of the agent's own output enforced or demonstrated? |
| `has_conditions` | 0/1 | is there at least one conditional instruction? |
| `multi_step` | 0/1 | is the agent's procedure split into ≥2 ordered steps? |
| `structured_relation` | 0/1 | are order, dependency, or priority among elements declared? |
| `conditions_count` | integer | distinct premises that change what the agent does |
| `structure_form` | 0–2 | 2 full-pack · 1 flat · 0 prose |

Definitions and boundary cases are in [docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md).

**Read the reliability before using a label.** `structure_form` is reliable (ordinal
Krippendorff's α = 0.84). All nine facets fall below α = 0.667, and most disagreements run
in one direction: the raters drew the boundaries of concepts such as identity and goal in
different places. We release both raters' labels and the disagreement list instead of an
adjudicated single label, so that others can re-code with their own definitions. Treat
facet figures as a range across raters, and use only patterns that hold for both.

```bash
pip install -r requirements.txt
python3 scripts/agreement.py        # alpha, kappa, disagreement directions
python3 scripts/label_stats.py      # content types, form x content, per-path figures
```

---

## Licensing

- **Metadata, labels, schema, and documentation** produced by this project:
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Scripts under `scripts/`**: MIT (see `scripts/LICENSE`)
- **Source files under `data/content/`** — each remains under its original author's license.
  Per-record SPDX identifiers are in `records.jsonl` under `license.spdx`.

When using a source file, check that record's license and attribute the original author.

---

## Usage

```python
import json, pathlib

recs = [json.loads(l) for l in open("data/records.jsonl", encoding="utf-8")]

with_text = [r for r in recs if r["full_text_ref"]]          # records that include text
text = pathlib.Path("data", with_text[0]["full_text_ref"]).read_text(encoding="utf-8")
```

Regenerate statistics:

```bash
python3 scripts/stats.py
```

---

## Limitations

- Collection is limited to GitHub, so the corpus skews toward personas written by developers.
- Path-based search **also misses conventional naming.** Scanning the same population found
  three repositories using the `.agents/` convention that did not enter this corpus.
- This is a single point-in-time snapshot (collection closed 2026-09-30).
- Almost everything is in English (280 of 281 — a character-based estimate).
- `summary` and `tags` were **written by the dataset author during collection.** They are not
  extracted from the source text; they exist for browsing and filtering.
- Content-facet labels did not reach the usual reliability threshold (see "Labels" above).
  Definitions were not revised and disagreements were not re-coded in this version.
- Both raters are dataset authors, and rater 1 also wrote `summary` and `tags`.
- Candidate counts and intent-screening records from before the 2026-09-06 re-fetch are not
  part of the release, and agreement on the inclusion decision was not measured.

---

## Citation

If you use this dataset, please cite it by its Zenodo DOI:

> **10.5281/zenodo.23230144** — https://doi.org/10.5281/zenodo.23230144

This is the *concept* DOI: it always resolves to the latest version. To cite a
specific version instead, use that release's own DOI from the Zenodo record.

### Versions

- **v1.1.0** — adds both raters' labels, the disagreement list, the annotation guide, the
  scheme history, the near-duplicate cluster list, and the agreement, label-statistics,
  re-fetch, license-gate, and duplicate scripts. Records and texts are unchanged.
- **v1.0.0** — 281 records, 179 with source text.

## Contact

Please open an issue. If you reclassify or extend this corpus, we would be glad to hear about it.
