# Card brief, wave 2 (2026-11-21) — everything left

Chi: 「全部搞完」. Every leaf of seven domains gets cards: the non-core leaves of k8s, sr-craft, ai-eng, and all leaves
(core first, then non-core) of tech-comm, career, ai-dev, ai-industry.

**All rules of `research/agents/new-domains-cards.md` apply unchanged** (read it first): self-contained with a
`research/domains/<d>/terms.yaml` (term → first teaching leaf; one term per line, quote keys that contain a colon),
English terms + Chinese prose, content not talk, ≥ 25% diagrams (`flowchart TD`, labels ≤ 16 chars), every number
verified and logged in `research/domains/<d>/claims.md`, `**出处：**` last line, generic (no employer names), gates.
Add one gate: `uv run python scripts/term_order.py <d>` must end with `0 used before taught, 0 bad entries` for the
cards you wrote (fix by moving a definition earlier or defining the term in one line on the card; never by deleting
the term from terms.yaml when the card really uses it).

Leaf citations: `research/domains/<d>/leaves.yaml`. Books in `sources/local/<corpus>/` (gitignored, never copy text):
`se-guidebook`, `never-split-the-difference` (career); `minto-pyramid` (tech-comm; 8-page runs, cite `Minto p. N–M`
plus the chapter heading); `ai-engineering` (ai-dev/ai-industry where relevant). Free sources: the URL in the leaf's
citation — fetch and read it before writing; if it is dead, find the official replacement and log it.

## Card mix for the four new domains (their outline's `## 卡片格式建议` refines this)

- **tech-comm** — 原则 cards for structure and writing (**原则** / **怎么做** / **常见错法** / **改写示例**: a short
  before → after rewrite). For the English-phrase leaves (marked 惯用说法): a situation question, then **可以这么说**
  (3–5 natural English sentences), **别这么说** (1–2 with why), **语气** (one line). Mark them `tags: [惯用说法]`;
  no invented "research says".
- **career** — decision-scenario cards: **原则** / **怎么做（含示例措辞，英文原句）** / **常见错法** / **对方在想什么**.
  Compensation and tax facts only from official pages (IRS, USCIS, company filings) or the cited essays, with year;
  no salary numbers for specific companies. Visa leaves: general rules with the official URL, no advice framed as legal.
- **ai-dev** — 摘要 / 考点 / 实践 like ai-eng. Ground in official docs (Claude Code, Codex, Cursor), the METR study,
  DORA 2025, Stack Overflow 2025 survey, Simon Willison. Terms like token, context window, prompt injection may be
  defined in one line (ai-eng teaches them in another deck; this deck must stand alone).
- **ai-industry** — 摘要 / 考点 / **怎么读** (a method card: how to read a 10-K, a benchmark claim, a capex headline).
  Numbers go stale: every number carries its year and source in the text (「2025 年，…（Stanford AI Index 2025）」) and
  the card gets `tags: [时效]`; prefer cards that teach structure and mechanisms over cards that are mostly numbers.

## Wave 2 for the built domains

- Same format as their wave-1 cards (read three of them first). Non-core leaves only: `core: false` in the skeleton.
- **k8s:** also write the chapter article for any theme that has cards but no `vault/domains/k8s/readings/<theme-id>.md`
  yet (e.g. p4.t02 Ingress), and append a section to an existing article when a new leaf needs explaining there.
  Parts p5–p9 of k8s are local-only by Chi's choice (git-excluded); write them the same way, nothing else changes.
- Resume rule as before: skip leaves that already have cards.
