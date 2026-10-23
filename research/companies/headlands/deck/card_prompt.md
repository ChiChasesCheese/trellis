# Card agent — Headlands deck, group {GROUP}

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents, never
edit the source pages. You write only card files for **your leaves**: {LEAVES}

Cards go to `vault/interviews/companies/headlands/deck/cards/<branch>/` where `<branch>` is the part of the leaf id before
the dot (e.g. leaf `java21.j01-record` → folder `java21/`).

## 0. Resume rule (do this first)

`uv run trellis --domain headlands stats` and `ls` your folders. Skip leaves that already have their cards. If uv touches
`uv.lock`, run `git checkout uv.lock`.

## 1. Inputs

- `research/companies/headlands/deck/plan.json` — for each of your leaves: the source files (a `#[X]` suffix means only
  section `## [X] …` of that file) and `min_cards`.
- `skeleton/headlands.yaml` — leaf titles.
- `proposals/WRITING_RULES.md` rules 1, 3, 5, 6, 10, 11, 12.
- Format example: `vault/domains/hft/cards/java/hft-java-gc-choices-gen-zgc.md`.

**Read every source file of a leaf completely before writing its cards.**

## 2. The goal: completeness

Chi (preparing for the Headlands Java SWE phone screen on 2026-10-26) wants to study this kit **in Anki alone**, so the
cards of a leaf must carry **every key point of its sources**: each concept, mechanism, rule, number, API, pitfall,
comparison, interview question and follow-up the source teaches. `min_cards` is a floor, not a target — write as many as
the source needs. Do not skip a point because another deck may cover it. Do not invent facts the source does not support;
keep the source's numbers.

Per kind of source:
- **Lecture (J01–J19, C01–C16, foundations, company pages)**: one card per key point; include "写出 / 补全这段代码"
  cards for the syntax that must be typed in CoderPad (short snippets ≤ 10 lines in a fenced block).
- **Question bank section (`questions.md#[X]`)**: every question `### Qnn` gets **at least one card** whose front is the
  interview question (Chinese, plus the original English wording on its own line), and whose back is the answer's
  skeleton: the 3–6 points to say, bolded keywords, a number or example. Long answers become 2–3 cards (main answer,
  follow-up, trap).
- **Problem (problem.md + REPORT.md + articles)**: cards for: what the problem asks (restated plainly, with a tiny
  example), the key idea, data-structure choice and why, complexity, the Java implementation detail that matters, the
  C++ difference when there is a C++ article, edge cases and bugs, each follow-up question with its answer. A card may
  show the core 5–10 lines of code.
- **System design**: requirements and numbers, components, each design decision with its reason, each follow-up with
  its answer, rubric points.
- **Behavioral (rule 10 style)**: question cards — front: the question; back: which story, the 3–4 beats in bullets with
  **bold keywords**, time limit, likely follow-ups with one-line cues. Story cards — front: "讲 <story id> 故事"; back:
  one-line headline then S / T / A / R / L bullets with bold keywords and numbers. Keep 【待补：…】 placeholders as they
  appear in the source.

## 3. Card format

One file per card, `<id>.md`:

```
---
id: hl-<leaf-slug>-<card-slug>
node: <leaf id>
type: qa
step: <1..n inside the leaf, in the order the source teaches>
---
## Q
<question>

## A
<answer>
```

- `id`: lowercase ASCII and hyphens, starts with `hl-`, globally unique; file name = `<id>.md`. No `source:`, no `tags:`.
- `step`: 1, 2, 3 … no repeats, prerequisite order (definition before use).
- Everything Chinese; English terms in full-width parentheses on first use on each card; code identifiers in backticks.
- **Self-contained**: the front names its subject (never starts with 它 / 这 / this / it); the back defines what it
  relies on, gives the why, and a concrete number or example. Never "如上所述 / 见讲义 / 本文 / 本题 / 这道题 / 作者",
  never where a fact came from, never file names or lesson numbers as the thing to recall (say "Java 的 record", not
  "J01 讲了什么").
- Length: back about 100–400 Chinese characters (+ a short code block when useful). Split rather than exceed. No ASCII
  diagrams; tables ≤ 4 rows.

## 4. Gate (before replying)

1. `uv run trellis --domain headlands validate` — 0 errors; no `not_self_contained` / `leans_on_source` warnings on your
   cards.
2. `uv run python scripts/plain_style.py <your card files>` — ok.
3. `uv run trellis --domain headlands stats` — each of your leaves ≥ its `min_cards`.
4. `git checkout uv.lock` if changed. Leave no scripts in the repo.

## 5. Reply (≤ 12 lines)

Cards per leaf (or per branch with totals), gate results, any source point you could not turn into a card and why.
