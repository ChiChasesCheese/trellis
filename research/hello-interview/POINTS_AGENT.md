# Card agent — granular cards for the design questions (要点卡)

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your files. Scratch in
`/tmp/pts_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a slug whose folder already
has cards.

Chi (2026-11-01): each design question keeps its one complete answer card (the main entry, a foldable outline), and
also gets small cards, one knowledge point each, under the question's deck, so he can review a single point at random
and still know where it comes from.

## Input

Your slugs are in your group file. Each body is `vault/interviews/core/design-questions/<slug>.md` — the single source of
truth. Take facts only from it (numbers, choices, reasons); do not add claims the body does not make, do not contradict it.

## Output

Folder `vault/domains/hello-interview/cards/points/<slug>/`, one file per card, 6–12 cards per question:

```
---
id: hi-pt-<slug>-<n>-<short-slug>
node: points.<slug>
type: qa
step: <n>
---
## Q
**<中文题名> · <要点名>**｜出自：<中文题名> › <部分（需求 / 核心实体与接口 / 整体设计 / 深入 n / 取舍与追问 / 级别期望）>

<one self-contained question in Chinese: the situation and what to decide or recall>

## A
<the answer in ≤ 250 Chinese characters: label chips such as **要点。** **为什么。** **数字。** **取舍。** **易错。**; a short
```python block for a key method of a low-level design question is fine>
```

Pick the points an interviewer probes: the scale numbers and what they force, each deep dive's problem → chosen option
and why it beats the alternative, the key failure / consistency mechanism, the core entity or API decision, the
follow-up that changes the design, and for low-level design the class responsibilities and the key method. One point
per card; no card that only says "see the answer". The generator rewrites `node:` to the question's leaf.

Chinese, English terms in parentheses on first use; no URLs, no process talk; style checker rejects 这道题, 本题, 本书,
抓取 and 面经 (even inside 页面经常).

## Gate

`uv run python scripts/plain_style.py <your files>` ok; then `uv run python research/hello-interview/gen_skeleton.py && uv run trellis --domain hello-interview validate`
— 0 errors, no `not_self_contained` / `leans_on_source` on your cards. Reply in ≤ 5 lines: questions done, cards written.
