# Drill agent — HFT domain

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never switch branches, never spawn agents. You own
`vault/domains/hft/drills/` only.

Write **one drill per top-level branch** of `skeleton/hft.yaml` (15 files), named `<branch>-<short-slug>.md`. A drill makes
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
- <5–8 bullets; each ends with 1–3 wikilinks to the card ids that hold the answer, e.g. ([[hft-java-gc-choices-gen-zgc]])>

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
```

Rules: Chinese, English terms in full-width parentheses on first use; no provenance; `proposals/WRITING_RULES.md` rules
1–6, 12. Every wikilink must be an existing card id: `ls vault/domains/hft/cards/*/` and grep before linking. Make at
least one drill (in `java` or `java-at-hft`) an interview-style "explain to the interviewer" for a Java SWE at an HFT firm,
and link related practice in `vault/interviews/companies/headlands/` by note name where it fits.

Gate: `uv run trellis --domain hft validate` 0 errors; `uv run python scripts/check_wikilinks.py domains/hft` 0 dead
links; `uv run python scripts/plain_style.py vault/domains/hft/drills/*.md` ok; `git checkout uv.lock` if changed.
Reply ≤ 8 lines.
