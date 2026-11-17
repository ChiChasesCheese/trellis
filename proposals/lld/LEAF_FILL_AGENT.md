# Filling the coding-craft leaves that LeetCode Project misses route to

Every LeetCode Project quick card names 1–3 knowledge-tree leaves (`leaves` in
`sources/local/lc-project/quick/points/<slug>.json`). When Chi misses a card, the plan sends him to those leaves
(`8 LC Project::00 补弱`). On 2026-11-17, 82 of the 118 leaves named there had no cards, and 80% of the routes went to
an empty leaf. You fill those leaves, most-routed first.

Repository root: `/Users/chiserver/sessions/trellis`. The vault is public: write in your own words; never quote a
LeetCode workspace (`sources/local/lc-project/workspaces/`, read-only, for context only). No git, no other agents. Python
runs use `uv run --no-project --python 3.11`; never touch the repo `.venv`.

## Input, per leaf

- The leaf in `skeleton/low-level-design.yaml` (`grep -n -A4 "id: <leaf>$"`): its `title` and `summary` say what it
  covers; `requires` says what it builds on.
- The LCP points that route to it: `grep -l '"<leaf>"' sources/local/lc-project/quick/points/*.json`, then read those
  points' titles. They are the concrete situations a card must prepare Chi for (a miss on 「`True` 被当成 1 收下」 lands
  on `errors.boundary-validation`).
- The LCP articles `vault/domains/low-level-design/readings/problems/solution-lcp-<slug>.md` for worked examples.

## Output, per leaf: 4–8 cards

Files `vault/domains/low-level-design/cards/<root>/<root>-<short-slug>.md` (root = the part of the leaf id before the
dot), frontmatter `id`, `node: <leaf id>`, `type: qa`, `step: <n>`; body `## Q` and `## A`. Write them by hand in the
format of existing cards in `vault/domains/low-level-design/cards/python/` (read two first), or through
`uv run trellis grow --leaf low-level-design:<leaf> --count 6 -o /tmp/<leaf>.prompt.md` → JSON →
`uv run trellis grow --import /tmp/<leaf>.cards.json --leaf low-level-design:<leaf>`.

**Card mix:** the principle (what and why), the mechanism in Python (code), the decision against the nearest
alternative, the failure (what breaks and how it shows up), and one or two **applied** cards that put the principle into
an LCP-style situation in your own words (a service, its input, the wrong and right handling). `step` 1…n in teaching
order; a card that uses a term comes after the card that defines it.

**Layout of `## A` (Chi, 2026-11-16: dense, laid out, code over prose, no filler):**

1. First line: the conclusion in bold, ≤ 30 characters.
2. 3–6 bullets, each `**短语**：一句`.
3. A ```python block ≤ 15 lines that runs on 3.11 (run it), or a mermaid diagram ≤ 8 nodes when the point is a flow.
   At least half the leaf's cards carry code.
4. Optional `<details class="pt"><summary>延伸</summary>…</details>`: the next thing a senior engineer would say.
5. Last line `**知识点：**` with the leaf title.

## Rules (from `proposals/lld/CONCEPT_AGENT.md` "Card rules" and the LCP verifiers' findings)

- Self-contained, one idea per card, Chinese prose with English terms of art, questions that ask for reasoning.
- No meta sentences (「本卡讲」「需要注意」); spoken Chinese.
- Every fact is run or is standard documented behaviour; a version-dependent fact names the version.
- No strawmen: the wrong way on a card is a mistake a real engineer makes.
- Python facts people get wrong are listed in CONCEPT_AGENT.md; respect them.

## Gate, per leaf

`uv run python scripts/check_lld_concepts.py <root>` (it checks the whole root; only your leaf's lines matter, other
leaves of a new root may still be empty), `python3 scripts/plain_style.py <your cards>`,
`python3 scripts/phone_diagrams.py <your cards>`, `python3 -B scripts/check_wikilinks.py domains/low-level-design`,
and `uv run trellis --domain low-level-design validate` with no error naming your files. Do not run
`trellis --domain low-level-design sync` (it would generate map notes for every empty leaf).

## Report

Per leaf: card ids with their one-line question, which LCP points they prepare for, and the three statements you are
least sure of.
