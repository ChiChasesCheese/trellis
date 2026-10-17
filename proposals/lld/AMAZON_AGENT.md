# Amazon 专项（`amazon` branch of low-level-design) — instructions for one agent

Chi has an Amazon onsite on 2026-10-20/21. The `amazon` branch of `skeleton/low-level-design.yaml` holds the OOD problems
reported for Amazon on 1point3acres and Hello Interview between 2026-09-16 and 2026-10-16. In Anki they become the deck
`低层设计（LLD）::10 Amazon 专项（Amazon OOD）`, studied **in card order, beginner first**.

> **`proposals/WRITING_RULES.md` overrides everything below** (Chi, 2026-10-16): provenance only in the last section, textbook voice to the reader, cause → effect, self-contained, diagrams `flowchart TB` that fit the page. `scripts/plain_style.py` enforces it inside the gate.

**Follow `proposals/lld/PROBLEM_AGENT.md` in full**, with the changes below. Where the two disagree, this file wins.

## Changes to PROBLEM_AGENT.md

1. **Leaf ids and slugs.** Leaves are `amazon.amz-<name>`; the slug is `amz-<name>` (e.g. `amz-train-fare`), so the
   folder is `vault/domains/low-level-design/problems/amz-train-fare/`, the article `solution-amz-train-fare.md`, the
   drill `design-amz-train-fare.md`. **Card ids start with `<slug>-`** (`amz-train-fare-…`), not `problems-<slug>-`.
   The gate is `uv run python scripts/check_lld_problems.py --branch amazon <leaf id>`.
2. **The prompt, in plain words, first.** `## 题目与澄清` opens by stating the problem the way an interviewer would
   pose it to you (no quotes, no source, no labels). Stage 1 of the drill and of `## 需求与分级` is the first ask the
   brief reports; later stages are its follow-ups, then yours. *Which* stages were reported and which are
   reconstructed, with the URLs and dates, is said once, in `## 来源与延伸` (the last section).
3. **The reader is a beginner on this problem** (Chi: "for beginner 并且逐步深入"). The article still meets the senior bar,
   but every term of art is explained the first time it appears, and `## 核心对象与职责` starts with a two-sentence plain
   description of the system before any class.
4. **Cards: 7–9, every one with a `step`, and the steps form a ladder** — card order is study order. Write them so a
   learner meeting this problem for the first time can go 1 → n:

   | step | the card asks | the answer gives |
   |---|---|---|
   | 1 | 「<题名>要你设计什么？开场先问哪三个澄清问题？」 | the problem in one sentence + three questions and what each answer changes |
   | 2 | the 3–5 objects and the one job of each | one line per class; the invariant that decides the split |
   | 3 | the stage-1 flow in code | ≤ 15 lines of Python, the core method only |
   | 4 | the data structure / algorithm that makes the key operation right or fast | the choice, its complexity, a concrete input → output |
   | 5 | the central design decision | two real options, what each costs, the choice |
   | 6 | the first reported follow-up: what changes, where | the class added / the line changed, what stays untouched |
   | 7 | the second follow-up, or the failure path / edge case interviewers probe | concrete case and the fix |
   | 8 | concurrency or scale (the senior question) | what races, the lock / structure that prevents it |
   | 9 (optional) | the most common mistake on this problem | the mistake, a concrete input that exposes it, the fix |

   Answers ≤ 220 Chinese characters plus at most one ≤ 15-line code block. Step 1–3 answers define every term they use.
   Write the order to `proposals/steps/low-level-design/<slug>.json` and import it (PROBLEM_AGENT.md §6).
5. **Sources.** At least two readings: a pointer to the Amazon report (`src-1p3a-<slug>.md` or `src-hellointerview-<slug>.md`,
   always `tags: [no-archive]`), plus one free source (docs.python.org, a permissively licensed repo). Hello Interview
   breakdowns that Chi's membership unlocks are saved as plain text under
   `/Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/hi_lld/` — read them to calibrate the follow-up order and to say in
   `## 来源与延伸` where you disagree; **never copy a sentence, diagram or line of code from them**.
6. **Reuse what the repo already has.** Your task brief names kit files (`vault/interviews/companies/amazon/lld/…`) and
   bank problems this one stands on. Adapt our own code freely; link bank problems by wikilink
   (`[[solution-parking-lot]]`) instead of re-teaching them.
7. **Cards-only leaves** (`amazon.amz-round`, `amazon.amz-locker-onsite`) have no problem folder, article or drill:
   write 5–7 stepped cards through `trellis grow` and the steps file, plus the readings your brief asks for. The gate
   checks them with `--branch amazon` (≥ 4 cards, every card stepped).

## Defects found in earlier batches (each is a rule)

- 「本题」「这道题」「上一张卡」on a card: name the system every time (「在 Amazon 火车票价设计里，…」).
- Process talk in an article or card (「我验证过」「对拍 300 组通过」): show the concrete input and output instead.
- Numbers typed from memory: every complexity bound, example output and size in prose is computed by running code.
- An invented interviewer requirement presented as reported: the final source section lists which stages were reported and which were added.

## Report (≤ 12 lines)

Per leaf: the gate line, tests, solution code lines, article characters, cards — and the three claims you are least sure
of. Do not run git; do not start agents; touch only your leaves' files.
