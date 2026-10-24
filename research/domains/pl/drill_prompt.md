# Drill agent — programming-languages domain (`pl`)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never switch branches, never spawn agents. You own
`vault/domains/pl/drills/` only.

Write **one drill per top-level branch** of `skeleton/pl.yaml` (one per branch), named `<branch>-<short-slug>.md`. A drill makes
the learner *produce* the mechanism, not recall it: predict behaviour ("this order book uses std::map — where will p99
come from?"), debug a symptom ("p99.9 jumps every 4 seconds — list causes in order of likelihood"), or explain a design
to a peer ("explain to a new teammate why the risk check sits inline").

Format (copy the shape of `vault/domains/system-design/drills/design-rate-limiter.md`, but in Chinese):

```
---
nodes: [<2–6 leaf ids this drill exercises>]
tags: [drill]
---
# 练习：<title>

<2–4 sentences setting the scene, concrete numbers>

**要你给出的**
- <2–4 bullets: what to produce>

**评分要点**
- <5–8 bullets; each ends with 1–3 wikilinks to the card ids that hold the answer, e.g. ([[pl-memory-escape-analysis-best-practice]])>

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
```

Drills for a senior engineer (Chi: logic, philosophy, trade-offs, best practice): e.g. predict what a snippet prints
in each of the four languages and why; diagnose a production symptom (a goroutine leak, a virtual thread pinned on
`synchronized`, an asyncio loop blocked by CPU work, a borrow-checker fight that hides a real aliasing bug); defend a
language choice for a given system to a sceptical peer; redesign an API so it is idiomatic in each language. Each drill
spans Go, Java, Rust and Python.

Rules: Chinese, English terms in full-width parentheses on first use; no provenance; `proposals/WRITING_RULES.md` rules
1–6, 12. Every wikilink must be an existing card id: `ls vault/domains/pl/cards/*/` and grep before linking. Make the `signatures` drill a "choose and defend a language" exercise.

Gate: `uv run trellis --domain pl validate` 0 errors; `uv run python scripts/check_wikilinks.py domains/pl` 0 dead
links; `uv run python scripts/plain_style.py vault/domains/pl/drills/*.md` ok; `git checkout uv.lock` if changed.
Reply ≤ 8 lines.
