# Map LeetCode Project onto the low-level-design tree — instructions for one agent

LeetCode Project (leetcode.com/project, launched 2026-10) has 31 projects done with a coding agent in a real workspace:
build a component, repair a broken service, or handle an incident. Chi wants to ace all of them and become a much
stronger coder, learning through the existing knowledge tree `skeleton/low-level-design.yaml` (domain
`low-level-design`, about 330 nodes). Your job is the research layer: what the projects test, where the tree already
teaches it, what the tree lacks, and in which order to study the projects.

Repository root: `/Users/chiserver/sessions/trellis`. Run one plain command at a time. Do not run git, do not start
agents, do not edit the skeleton or any card. Write only the two output files below.

## Inputs

- `sources/local/lc-project/raw/list.json` and `raw/<slug>.json`: LeetCode's public list and per-project overview
  (`description` holds Background, Task and "What This Problem Tests"; `topicTags`, `difficulty`, `paidOnly`,
  `estimatedSolvingMin`). Read all 31. Never copy their sentences into your output: the repository is public; restate.
- `skeleton/low-level-design.yaml`: the tree. `docs/explanation/coding-craft-framework.md` explains its shape (abilities →
  round playbooks → problems). The root `lcproject` is new and holds three pilot leaves.
- Cards per leaf: `uv run trellis --domain low-level-design stats` (run `git checkout -q uv.lock` afterwards if uv touched
  it). Card files are under `vault/domains/low-level-design/cards/`; read a few of a leaf before calling it covered.
- Classic problems already in the bank: `vault/domains/low-level-design/problems/` (rate-limiter, pub-sub, ttl-cache,
  thread-pool, digital-wallet …) with articles in `readings/problems/solution-<slug>.md`.

## Method

1. **Exam points per project.** For each project: kind (build / repair / incident), the 5–10 exam points it tests in
   your own Chinese phrasing with the English term in full-width parentheses (幂等键（idempotency key）), and the
   product-rule ambiguities a hidden test is likely to pin (error precedence, boundary inclusivity, tie-breaking order,
   what a failed batch leaves behind).
2. **Union and frequency.** Merge the exam points across projects into one list of canonical points (merge synonyms:
   "snapshot isolation", "detached copies", "data isolation" and "defensive copying" are one point unless a project
   clearly means something else). Count how many projects need each point. Sort by count: this is the 80/20 table.
3. **Map each canonical point to leaves.** For each point: the existing leaf ids that teach it, how many cards each
   has, and a verdict: *covered* (cards exist and actually teach this angle; quote one card question as evidence),
   *thin* (leaf exists, cards miss this angle; say what is missing), or *gap* (no leaf). Also list the classic bank
   problems a project extends.
4. **Survey before proposing leaves (GitHub first).** For the gap and thin points, search GitHub
   (`gh api -X GET search/repositories -f q="<topic>"`, `search/code` sparingly) and the web for the best readable,
   mechanism-level source per point: official docs first (docs.python.org threading / sqlite3 / datetime / decimal,
   Stripe's idempotency docs, the SQLite and PostgreSQL docs on transactions and isolation, RFC 9110 for HTTP status
   semantics), then strong engineering blogs. Also search for anything written about LeetCode Project itself
   (announcements, Reddit or Discuss write-ups, candidate reports) and record what it says about format and scoring.
5. **Propose new leaves** only for gaps a proposal of yours can justify: needed by at least two projects, or one project
   plus at least two independent outlines. Put each under the root where it belongs (`errors`, `concurrency-depth`,
   `data`, `api`, `structure`, `testing`, `debugging`, `ai`, `parsing-io`, `fluency` …), never under `lcproject`. Give
   each: `id` (root.kebab-name, not already used), Chinese `title` with the English term, one-line Chinese `summary`,
   `requires` (existing leaf ids it truly depends on), the projects that need it, and its best source URL.
6. **Study order for the 31 projects.** Rank by coverage gain: the next project is the one whose exam points add the
   most not-yet-covered weight (weight = the point's project count), ties broken by difficulty (easier first) and by
   `paidOnly` false first. Also mark which projects are mostly the same skills as an earlier one (study as a pair).

## Output

1. `research/domains/low-level-design/lc-project/MAP.md` with these sections:
   - `## Projects` — one row per project: slug, kind, difficulty, minutes, free/paid, exam points (canonical names),
     likely hidden-test ambiguities (2–4).
   - `## Exam points (80/20)` — canonical point, project count, the projects, leaves, verdict, evidence card question or
     what is missing.
   - `## Gaps and proposed leaves` — the table from step 5 with sources.
   - `## Study order` — the ranked list with the cumulative weight covered after each project, the pairs, and the cut
     line where about 80% of the exam-point weight is covered.
   - `## About LeetCode Project` — what public sources say about the format, the agent in the workspace, scoring, time
     limits; each fact with its URL and date. Say plainly what you could not find.
   - `## Not reached` — sources or searches that failed.
2. `research/domains/low-level-design/lc-project/new_leaves.yaml`: the proposed leaves as skeleton YAML fragments, grouped
   by parent root, in the skeleton's own format (`- id:`, `title:`, `summary:`, `requires:`), ready to paste.

## Report (≤ 15 lines)

The number of canonical exam points, how many are covered / thin / gap, the top ten points by project count, the proposed
leaves (ids only), the first ten projects of the study order, and the three conclusions you are least sure of.
