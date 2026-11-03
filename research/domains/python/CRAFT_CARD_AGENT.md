# Card agent — coding craft (branch `craft` of domain `python`)

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your leaves' cards. Scratch in `/tmp/craft_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a leaf that already has its cards.

Chi's goal is much stronger core coding and deeper Python, connecting what different problems share. He describes his fundamentals as weak and treats himself as a senior who wants logic, trade-offs and best practice, never syntax tours. Do not open `sources/local/hello-interview/premium/` or `cards/premium/`. This work is public.

## Input

Your leaves are listed in your group file. Each entry is in `research/domains/python/craft_map.json`. Open the code it cites, at the cited lines.

## Output

`vault/domains/python/cards/craft/<branch>/<leaf>/`, one file per card, 3–6 cards per leaf. Frontmatter exactly:

```
---
id: craft-<leaf>-<n>-<short-slug>
node: craft.<branch>.<leaf>
type: qa
step: <n>
---
```

- **First card opens from zero:** the problem, what the naive version does and where it hurts, then the technique on a tiny example. Introduce every term you use.
- **Idioms:** what it does underneath, what the plainer version costs, when not to use it.
- **Patterns:** one mechanism, then how it appears across problems. Quote 2–3 real short excerpts side by side, naming each problem, and say what stays the same and what changes. End with `**见于。**` listing the problems, and `**信号。**`: what in a new problem should make you think of this.
- **Architecture:** the decision, both options, what each costs, and a real problem where it went each way.
- **Tie the scales together** when `scales` is filled: the same mechanism in a LeetCode problem, a low-level design and a distributed system, and what changes at each step (one process and a lock → many machines and a lease). Include one card like that where it fits.
- **Code:** Python 3.11+, type hints, comments carry the reasoning, prose never repeats the code. Keep excerpts under about 25 lines. Run every snippet longer than 5 lines in your scratch folder, and show real output.
- **Quoted output must match the code on the card:** every line of output comes from code the reader can see. Do not show output of snippets you cut.
- The front never says 参考解 or 这份解法: describe the situation itself, naming the problem (分账, 库存预留) where it helps.
- Every claim about CPython behaviour must be true for 3.11+; state the version where it matters. Do not invent numbers.

## Style

Chinese, technical terms in English in parentheses on first use. Front: header `**<leaf name> · <要点>**｜<写法|模式|架构>`, then a self-contained question built on a scenario: a why or a when, not a definition. Back: `**要点。**` first, then label chips as they fit (`**为什么。**`, `**代价。**`, `**易错。**`), about 150–300 Chinese characters plus code. Phone width. No citations, no process talk. The style checker rejects 这道题, 本题, 本书, 抓取 and 面经 (even inside 页面经常).

## Gate

`uv run python scripts/plain_style.py <your files>`, `python3 scripts/phone_diagrams.py <your folder>`, `uv run trellis --domain python validate` 0 errors with no `not_self_contained` or `leans_on_source` on your cards.
Reply in ≤ 5 lines: leaves done, cards, snippets run, least sure claims.
