# Card brief — k8s, sr-craft, ai-eng (wave 1, 2026-11-21)

Chi approved samples for these three decks; this brief is the standard they set. Read it whole, then your assignment
block. Also read `.claude/skills/building-study-domains/SKILL.md` (section **Card agents**) and look at the approved
samples: `sources/local/plan/samples-src/{k8s,sr-craft,ai-eng}/*.md` — copy their shape exactly.

## Inputs per domain

- Tree: `skeleton/<d>.yaml` (ids, titles, summaries, `core`, `requires`). **Wave 1 = leaves with `core: true` only.**
- Citations and chapter notes: `research/domains/<d>/leaves.yaml` (`cite:` per leaf id; k8s theme ids also have
  `notes:` = the diagrams each chapter must draw and the 2026 features to fold in).
- Books, ingested locally (read them; they are gitignored and must never be copied into the repo):
  `sources/local/<corpus>/` — k8s: `k8s-in-action-2e`, `kubernetes-book-2026`; sr-craft: `se-guidebook`,
  `crafting-engineering-strategy`; ai-eng: `ai-engineering` (and `ai-engineering-zh` only to understand, never for
  terms). Google SRE book chapters: URLs in `corpora/sre-book.yaml` and sre.google.
- k8s version facts: only from the verified table and the orchestrator check in `research/domains/k8s/BUILD.md`.
  Anything else about versions must be checked in the kubernetes.io release blogs before it goes on a card.

## Rules Chi set (all binding)

1. **Self-contained, textbook order.** A card may use a term only if an earlier leaf in deck order teaches it, or the
   card defines it in one line (e.g. "etcd（control plane 里存放所有对象的数据库）"). Foundations are written for
   someone who knows nothing about the field. **First step:** write `research/domains/<d>/terms.yaml` — every
   technical term your cards will use → the leaf id that first teaches it (in skeleton order). Keep it updated.
2. **English terms, Chinese prose.** Technical terms stay English as-is (Pod, reconcile loop, design doc, eval,
   guardrails, LLM-as-judge, chunking). Explanations in plain spoken Chinese. No Chinese translations of terms.
3. **Content, not talk.** Lay things out: tables, short lists, code/YAML, diagrams. No meta sentences ("本卡介绍…"),
   no "本题" (say "回到题目："), no filler. Bold labels as in the samples (**一句话：** **规则：** **怎么做：** …).
4. **Diagrams:** at least 25% of cards carry one (mermaid). `flowchart TD/TB` only (never LR), every node label
   ≤ 16 characters, ≤ ~8 nodes. Tables and YAML also help; code blocks never wrap (they scroll sideways).
5. **Every number and version is verified** in the book or an official page, and logged in
   `research/domains/<d>/claims.md` (card id | claim | source with chapter/section or URL). Unconfirmed → leave it off.
   Never copy book paragraphs; rewrite in Chinese; short quoted terms or command names are fine.
6. **Last line of every answer:** `**出处：**` the book chapter/section (or official URL) the card rests on.
7. **Generic.** Never mention Chi's employers or his own projects (Braintree examples are a separate private pass).

## Card file format

`vault/domains/<d>/cards/<top-node-id>/<card-id>.md`:

```
---
id: <prefix>-<short-slug>
node: <leaf id from the skeleton>
type: qa
step: <1..4, order among this leaf's cards>
tags: [<kind>]
---
## Q
**<Term> · <角度>**｜<kind> · <必会|追问|加分>

<the question: a concrete situation, not "what is X">

## A
...
**出处：** …
```

Prefixes: `k8s-`, `src-`, `aie-`. Ids unique across the repo (`grep -r "^id: <id>$" vault` before using one).

## Per-domain card mix

- **k8s** (layout of the system-design deck): each core leaf gets 2–4 cards from the kinds **先修** (foundation leaves
  only: definitions the rest depends on), **摘要** (what happens / how it works), **考点** (a probe: predict, compute,
  debug, compare — like the maxSurge walk-through), **拓展** (2026 practice, version-tagged; only where the chapter's
  `2026：` note has a verified item). Plus one **article per chapter (theme)** that has a core leaf:
  `vault/domains/k8s/readings/<theme-id>.md` with frontmatter `nodes: [<that chapter's leaf ids>]` and **no `url:`**;
  Chinese, from zero, the chapter's `图：` diagrams drawn in mermaid, worked YAML + `kubectl` examples rewritten from
  the books, 800–1800 characters, sections matching the leaves. The article teaches; cards test.
- **sr-craft**: each core leaf gets 1 **原则** card (a situation question; answer in five parts exactly as the sample:
  **原则** / **怎么做** / **常见错法** / **回到题目** (when the question is a scenario) / **面试官在考什么** / **适合配哪类故事**
  — a story *type*, never a specific story) and, when the leaf has a classic follow-up, 1 **追问** card.
- **ai-eng**: the `t01` foundations leaves get **先修** cards written for someone who knows no ML. Other core leaves
  get 2–3 cards from **摘要** / **考点** / **实践** (how to do it in production), like the LLM-as-judge samples.

## Gates (run before you report)

```
uv run trellis --domain <d> validate          # 0 errors; no not_self_contained / leans_on_source warnings for your cards
uv run python scripts/plain_style.py <your card files>
uv run python scripts/phone_diagrams.py <your card files>
uv run python scripts/check_mermaid.py <your card files>
uv run python scripts/diagram_share.py <d>    # ≥ 25%
```

## Working rules

- **Resume rule:** start by listing `vault/domains/<d>/cards/` and `uv run trellis --domain <d> stats`; skip leaves that
  already have cards. Work part by part in skeleton order, running the gates after each part.
- Write only inside your assigned folders plus `research/domains/<d>/{terms.yaml,claims.md}`. No skeleton edits (if a
  leaf is wrong or missing, report it), no Anki, no git commits, no subagents.
- Final message: cards and articles written per part, diagram share, the 5 claims you are least sure of, any term-order
  problem you could not solve, and leaves you think are misplaced.
