# Card agent — cross-question pattern cards (跨题模式)

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your files. Scratch in
`/tmp/cross_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a pattern whose folder has cards.

Chi (2026-11-01): many design questions share one mechanism used differently per scenario. These cards connect the
questions so he sees the relationships and the differences; they sit in the course part of the deck as its shared core.

## Input

Your pattern ids are in your group file; each pattern (title, summary, the questions it connects with a `how` and a
`differs` line) is in `research/hello-interview/patterns.json`. **Verify every `how`/`differs` line against the
question's body** `vault/interviews/core/design-questions/<slug>.md` (the single source of truth) and use what the body
says; drop a question from your cards if its body does not support the claim.

## Output

Folder `vault/domains/hello-interview/cards/cross/<sd|lld>/<pattern-id>/` (`sd` for track sd and both), 3–5 cards:

```
---
id: hi-x-<pattern-id>-<n>-<short-slug>
node: <sd|lld>.cross.<pattern-id>
type: qa
step: <n>
---
## Q
**<模式名>**｜跨题模式 · <card kind: 共性 / 对比 / 怎么选 / 易错>

<a self-contained question>

## A
...
```

The kinds, in this order:
1. **共性** — the mechanism and the invariant every use shares; why it is needed at all (what breaks without it).
2. **对比** — a table: 题 | 在这里怎么用 | 为什么和别的题不同 (4–8 rows, the questions with the sharpest contrasts). Name
   each question as a wikilink to its body: `[[<slug>|<中文题名>]]` (the title is the bold header of the body).
3. **怎么选** — given a new prompt, how to decide which variant applies (the deciding signals: money vs not, ordering
   needed or not, read-heavy vs write-heavy …), with one example per branch drawn from the questions.
4. **易错** (optional) — the mistake candidates make across these questions, with the concrete failure.
5. A second **对比** only when the pattern truly has two axes.

Prose short; a table is the backbone of the 对比 card. Chinese, English terms in parentheses on first use; no URLs, no
process talk; the style checker rejects 这道题, 本题, 本书, 抓取 and 面经 (even inside 页面经常).

## Gate

`uv run python scripts/plain_style.py <your files>` ok, `python3 -B scripts/check_wikilinks.py | tail -1` no dead link
of yours, then `uv run python research/hello-interview/gen_skeleton.py && uv run trellis --domain hello-interview validate`
0 errors and no `not_self_contained` / `leans_on_source` on your cards. Reply in ≤ 5 lines.
