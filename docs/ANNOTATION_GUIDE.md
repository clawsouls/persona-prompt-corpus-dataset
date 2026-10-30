# Annotation Guide (labeling scheme v3.2)

This is the guide behind `labels/rater1.csv` and `labels/rater2.csv`. Every record was coded
on two axes: **content** (what the file declares) and **form** (what shape it takes). The
same questions were given to both raters. They were written down from rater 1's coding,
so that the second rater would apply the same lines, and handed to rater 2 during coding
(see "Limits of this guide" below).

All example records cited here ship with full text in this release (MIT or Apache-2.0).

## How to judge

- Every field asks one question: **"does this file give the agent this?"**
- Code every cell. If a case is ambiguous, decide and write the reason in a memo; a blank
  cannot be told apart from "absent".
- Code independently. Raters do not discuss files while coding, and nothing is pre-filled
  by a script or a model. What is measured is whether independent judgments agree.

## Content facets (0/1)

### identity_declared and rule_declared

- `identity_declared` = 1 if the file says **who the agent is**: a name, role, character,
  voice, or values.
- `rule_declared` = 1 if the file says **what the agent should or should not do**:
  instructions or constraints on behavior.

Together they give four content types: both, identity only, rules only, neither.
The hardest boundary in practice is a file that names a role ("You are a code reviewer")
and then lists rules but gives no personality or voice. Whether a role name alone is an
identity declaration is exactly where the two raters split (see the paper, Sec. III).

### has_role

Is a job or functional role **named**? "You are a/an ___" with a job or function is 1.
A file with rules and instructions but no role name is 0.

- 1: `ceciliomichael/echode` `identity/ask.md` (gh-000013): "You are an expert Codebase Analyst."
- 0: `Crawlith/crawlith` `AGENT.MD` (gh-000002): project instructions with no role statement.

### has_goal

Does the file state a **goal the agent pursues**, a state to reach ("Your goal is to …")?
Role, character, and rules without a goal statement are 0.

- 1: gh-000013: "Your goal is to provide factually accurate answers based strictly on the current code."
- 0: gh-000002: much structure, commands, and rules, but no goal statement.

### has_context

Does the file give **background on the project, the user, or the environment** in advance
(repository layout, tech stack, who the user is, where the agent runs)?

- 1: gh-000002: a package layout table and build commands.
- 0: gh-000013: a role and an answer format, no project background.

### has_output_spec

Does the file **enforce or demonstrate the form of what the agent will produce**? An example
that shows the expected shape counts, not only explicit wording. The deciding question is
whether the format is **something the agent will write** or **something that already exists
in the project**. Do not decide by whether the word "format" appears.

- 1: gh-000002: "Title format: `feat(scope): short description`" (the commit messages the agent writes).
- 1: gh-000013: answers structured as Direct Answer, Evidence, Context, Caveats.
- 0: `cursey/regenny` `AGENT.md` (gh-000004): describes the project's existing `.genny`
  file format, unrelated to the agent's output.

### structured_relation

Are **order, dependency, or priority among elements** declared ("this first, then that";
"if these conflict, follow this order"; "do not do B before A")? A plain list of items
with no relation between them is 0.

- 1: gh-000013: the answer's parts are fixed in the order 1 → 2 → 3 → 4.
- 0: `dmzoneill/redhat-ai-workflow` `personas/database.yaml` (gh-000074): roles and
  conditions, but no relation declared between items.

### multi_step

Does the file tell the agent to split **its working procedure** into two or more ordered
steps ("first do X, then do Y")?

This is the facet most often confused with `structured_relation`:

| field | order of what |
|---|---|
| `multi_step` | the procedure the agent follows while working |
| `structured_relation` | relations among elements: output layout, priority, dependency |

The deciding case is gh-000013: `structured_relation` = 1 (fixed answer layout) but
`multi_step` = 0 (no procedure split into steps).

- 1: gh-000002: a planning step before writing any code, test-first work, then PR requirements.
- 0: gh-000013.

### has_conditions

Is there **at least one conditional instruction** (if, when, unless, once), a premise that
changes what the agent does?

- Conditions inside example dialogues, code blocks, or backstory do not count.
- This field asks only whether one exists; `conditions_count` counts them.
- 1: gh-000004: what to do on failure ("`proc:read_*` methods return `nil` on failure … Always nil-check in loops").
- 0: a file that only describes role and character, with unconditional instructions.

## conditions_count (integer)

Count the **distinct premises** (if / when / unless / once) that change what the agent does.

- Exclude premises inside example dialogues, code blocks, or backstory.
- A bulleted list under one premise counts once.

The raters agreed on the ranking of files (Spearman ρ = 0.69) but not on the counting unit:
rater 2 counted four fewer at the median. Users who need a count should re-derive it under
their own unit rather than average the two.

## structure_form (ordinal 0–2)

| level | rule | example |
|---|---|---|
| 2 full-pack | conventional section markers **with hierarchy** (header depth ≥ 2) and lists or code blocks | `mthalman/agent-personas` `personas/sre.md` (gh-000136): YAML front matter, nested headers, lists, code blocks |
| 1 flat | section markers **without hierarchy**; custom markers such as `[ROLE]` count as markers | `WhoIsMrSentry/HollowKnightRAG` `persona.txt` (gh-000043): one header, then `[ROLE]`, `[VOICE / STYLE]` and bullet rules |
| 0 prose | no conventional markers; prose, possibly with inline pseudo-headings | `AbhiGodara/jarvis` `persona.txt` (gh-000040): no headers, inline cues such as "Your personality:" |

Two cautions:

1. **Custom markers are structure.** A file with a single Markdown header can still be cleanly
   divided by markers like `[ROLE]` and `[LANGUAGE]`. Do not judge by header count alone.
2. The line between flat and prose is whether the markers are **conventional**, formalized
   enough that a section name could be copied into another file as is. Sentence-style cues
   ("Your personality:") inside running text are prose.

How this scale replaced an earlier four-level one is in [SCHEME_HISTORY.md](SCHEME_HISTORY.md).

## Limits of this guide

- The boundary cases were reconstructed from rater 1's coding and given to rater 2 during
  coding, not before. This is a likely source of the one-directional disagreements in
  `labels/disagreements.csv`.
- All nine content facets fell below α = 0.667 (`scripts/agreement.py`). Treat facet labels
  as two readings of the same file under one guide, not as ground truth. The form scale
  reached α = 0.84 and can be used as a reference label.
