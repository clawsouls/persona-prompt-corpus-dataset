# How the form scale came to have three levels

The current `structure_form` field has three ordered levels (2 full-pack, 1 flat, 0 prose).
It replaced a four-level nominal scale used in a pilot. This note records why, so that
anyone re-coding the corpus can see which distinctions were tried and dropped.

**The figures below belong to the replaced scale. They are not the reliability of the
current scheme**, which is reported by `scripts/agreement.py` (ordinal α = 0.84).

## The four-level pilot scale

The pilot scale had four levels: full-pack, flat, prose ("wild" in the coding sheets), and
minimal. The levels were first defined as stimulus conditions for a planned persona-fidelity
experiment, and grounded afterwards in published ways of measuring prompt and context-file
structure (element-level rubrics, header depth and word counts, content checklists). No
prior work derives these four levels; we defined them first and looked for support second.

Its boundaries were set by three questions:

1. Are there conventional section markers (Markdown headers, or custom markers such as
   `[ROLE]`)? If yes, full-pack or flat.
2. Do the markers have hierarchy (header depth ≥ 2) and lists or code blocks? If yes,
   full-pack; otherwise flat.
3. With no markers, does the file cover two or more items (character, voice, rules, …)?
   If yes, prose; if it is a single undivided declaration, minimal.

A first pass by rater 1 over 100 files checked that the levels line up with measurable
features: a simple rule on word count and header depth (fewer than 60 words → minimal;
header depth ≥ 2 → full-pack) decided 65 of the 100 files and agreed with the human label
on 64. The remaining 35 sat on the flat / prose / minimal boundaries, which is where human
judgment, and therefore an agreement measure, was needed.

## What the two-rater pilot showed

Both raters coded all 281 files on the four-level scale.

- **Order was reliable.** Ordinal Krippendorff's α = 0.92 and quadratic-weighted Cohen's
  κ = 0.83 (n = 245 files where both raters gave a single level).
- **Exact levels were not.** Nominal α = 0.46 and κ = 0.47 over all 281 files; α = 0.56
  and κ = 0.57 over the 248 files where both raters gave a single level.
- **Disagreements sat on adjacent levels, mostly the flat / prose boundary**: 22 direct
  swaps and 24 compound labels (a rater giving two levels to one file).
- **Full-pack agreed almost perfectly** (183 files).

## What changed

1. **The axis became ordinal with three levels** (2 full-pack, 1 flat, 0 prose). High
   ordinal agreement with low nominal agreement says the axis carries order but its
   interior cut points are fuzzy, so the scale should be read as ordered.
2. **Minimal was dropped.** A short persona is a matter of length, which `stats.words`
   already records, not of form.
3. **Element-level distinctions moved to content facets.** The distinctions behind the
   compound labels were element-level rather than about overall shape, so they were taken
   out of the form scale and coded as nine binary content facets plus `conditions_count`,
   leaving `structure_form` to describe shape only.

The current labels (`labels/rater1.csv`, `labels/rater2.csv`) were coded under the
three-level scale and the nine facets described in [ANNOTATION_GUIDE.md](ANNOTATION_GUIDE.md).
