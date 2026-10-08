# Collection Method

## Population and search

We searched public GitHub repositories by path, using five patterns: `persona`, `agent`,
`role`, `identity`, and `soul`.

**Why path search rather than a popularity sample.** In a sample that filters for mature
engineering projects (non-fork, two or more contributors, an OSI license, at least 271
commits), these files are structurally absent. Scanning 9,975 such repositories, filename
patterns matched 42 (0.42%), and only **3 (0.03%)** survived intent screening. Persona files
in the wild live in agent workspaces and personal repositories.

Filename matching alone carries a 93% false-positive rate (identity/role in feature
documentation, Persona UI components, UX persona documents). A **human intent-screening
step** is therefore necessary.

## Steps

1. **Search** — collect candidates by the five path patterns
2. **Intent screening** — manually exclude files that are not persona declarations
   (reason recorded per file)
3. **Pin the SHA** — store the commit SHA that last touched the file at collection time,
   together with repository and path
4. **Byte-level refetch** — fetch again at the pinned SHA and compare byte for byte
   (the outcome is recorded in the `refetch` field)
5. **License gate** — check the SPDX license of every repository and record whether
   redistribution is permitted

Collection closed **2026-09-30**.

## Records dropped during refetch

A refetch of every file at its pinned SHA on 2026-09-06 reduced 284 records to 281.
280 were byte-identical, one was corrected to the pinned revision, and three were dropped
because the upstream repository had disappeared.

## Why provenance is pinned

The dataset does not shift when an upstream repository edits or deletes a file. Each record's
`source.commit_sha` points at the content as it was, and even records without bundled text can
be retrieved from that SHA.
