# Persona Prompt Corpus

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23230144.svg)](https://doi.org/10.5281/zenodo.23230144)

A dataset of **281 AI agent persona prompts** collected from public GitHub repositories.
These are files such as `SOUL.md`, `persona.md`, and `IDENTITY.md` that declare an agent's
identity, values, tone, and behavioral limits. Every record is pinned to a repository,
path, and commit SHA.

- **281 records from 168 repositories**
- **Provenance pinned for every record** (281/281) — repository, path, and the commit SHA at collection time
- Full text included for **179**, metadata only for **102** (see "License gate" below)

한국어 설명: [README.ko.md](README.ko.md)

> The figures in this README are counted from the data by the build script.
> They are not written by hand, so they cannot drift from the dataset.

---

## What is in here

```
data/
  records.jsonl        281 records (JSON Lines)
  content/             179 source files — only where redistribution is permitted
schema/
  record.schema.json   record schema
docs/
  COLLECTION_METHOD.md how the corpus was collected
scripts/
  stats.py             regenerate corpus statistics
```

### One record

```json
{
  "id": "gh-000001",
  "source": {
    "repo": "HLR/DomiKnowS",
    "path": "Agent.md",
    "commit_sha": "d3fb1904b602f69e654986d6add27cc18db7312f",
    "url": "https://github.com/HLR/DomiKnowS/blob/HEAD/Agent.md",
    "collected_at": "2026-08-09"
  },
  "license": { "spdx": "MIT", "redistributable": true, "content_included": true },
  "full_text_ref": "content/gh-000001.md",
  "content_sha256": "…",
  "summary": "Two-phase DomiKnowS graph-builder agent: …",
  "tags": ["coding-assistant", "domain-expert", "structured-output"],
  "refetch": "same",
  "refetched_at": "2026-09-06",
  "stats": { "chars": 7335, "words": 980, "lang": "en", "format": "md",
             "headers_max_depth": 3, "has_code_block": true, "has_table": true }
}
```

When `full_text_ref` is `null`, the source file is not bundled. That record still carries
`source.commit_sha`, so **you can fetch the original yourself.**

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

## Licensing

- **What this repository produced** — metadata, schema, documentation, scripts:
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
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
- **Classification labels used for inter-rater agreement are not included yet.** They will be
  added in a later release once agreement can be reported.

---

## Citation

If you use this dataset, please cite it by its Zenodo DOI:

> **10.5281/zenodo.23230144** — https://doi.org/10.5281/zenodo.23230144

This is the *concept* DOI: it always resolves to the latest version. To cite a
specific version instead, use that release's own DOI from the Zenodo record.

## Contact

Please open an issue. If you reclassify or extend this corpus, we would be glad to hear about it.
