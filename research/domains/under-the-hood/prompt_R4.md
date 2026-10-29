# Revise agent — domain `under-the-hood`, group R4: pictures and worked examples

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only the card files of
your branches: os-net, devtools (in `vault/domains/under-the-hood/cards/<branch>/`). Scratch in `/tmp/uthr_R4/`.
`git checkout uv.lock` whenever uv touches it. Read `research/domains/under-the-hood/CARDS.md` §2b for the card layout.

Chi read the deck and said: reading is hard — add pictures (e.g. a Huffman tree); and the example problems should be
ones already in his decks, with the problem and the **full code** right under the card. Do both, for every card.

## 1. Pictures (```svg blocks)

Give **every leaf at least one figure** (usually on its first card) and add one to any other card where a picture
beats a sentence: hash buckets and probing, a skip list's levels, a heap as a tree over an array, a ring buffer with
head / tail, B+ tree pages, LSM levels, a consistent-hash ring, a timing wheel, a Huffman tree, a Merkle DAG,
an epoll red-black tree + ready list, a TCP window over a byte stream … Then shorten the text the picture now explains.

Write the figure as a fenced block with language `svg`; the template inlines it so it follows day / night colours:

- One `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H">` with W 300–360 and H ≤ 260; no width / height
  attributes; no blank line anywhere inside the block; no external images, fonts, scripts or `<style>` elements.
- Colours only through the theme: lines and text `currentColor`; highlight `style="stroke:var(--accent,#3b6fd4)"` or
  `fill:var(--accent,#3b6fd4)`; soft fill `fill:var(--chip,rgba(59,111,212,0.12))`; secondary text
  `fill:var(--dim,#6b7280)`. Shapes otherwise `fill="none"`.
- Text: `font-size="12"` or `13`, `font-family="sans-serif"`, short labels (a number, a key, 2–6 Chinese characters),
  never full-width punctuation inside the SVG. Nothing may overlap or run outside the viewBox.
- Check each figure: it must parse as XML (`python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" f.svg`),
  and render it with `qlmanage -t -s 700 -o /tmp/uthr_R4/png f.svg`, then **look at the PNG** (Read tool) and fix
  overlaps, clipped text and cramped spacing before you move on.

## 2. Worked example under every card

Replace the last line `**对应 LeetCode：** …` with a folded example (the template folds everything from the label to
the end of the card, so the card stays short):

```
**例题：** LC 146 LRU 缓存（同类：LC 460 LFU 缓存）

<题目：2–4 行中文，含关键约束与一个例子>

```python
<完整 Python 解答，原样照抄牌组里的代码>
```
```

- The problem **must already be in Chi's decks**: `sources/local/lc-in-decks.json` maps every LeetCode number in the
  decks to its card (a TikTok whole-answer card path under `vault/interviews/core/leetcode/tiktok/cards/`, or an Anki
  export with `front` / `back`). Pick the deck problem that uses the same structure or algorithm as the card; prefer one
  whose code shows the mechanism most directly. Copy the statement (shortened) and the **complete** code from that card
  without changing it (comments included). Different cards of one leaf may use different problems.
- If no problem in the decks truly uses the card's idea, keep one line `**对应 LeetCode：** 无直接对应的题` and no example.
  Do not force a match.

## 3. Keep

The facts already verified (do not change numbers or versions; `claims-*.md` holds their sources), the §2b layout, all
Chinese. Read every answer once as Chi would: a sentence that needs two reads gets split or replaced by the picture.

## 4. Gate (before replying)

`uv run python scripts/plain_style.py <files>` ok · `uv run python scripts/phone_diagrams.py <files>` ok ·
`uv run trellis --domain under-the-hood validate` 0 errors (long-answer warnings caused by the folded example are fine) ·
`uv run python scripts/check_wikilinks.py` 0 dead links · every SVG parses.

## 5. Reply (≤ 10 lines)

Cards touched, figures added (count per branch), examples added and cards left with 无直接对应的题, gate results.
