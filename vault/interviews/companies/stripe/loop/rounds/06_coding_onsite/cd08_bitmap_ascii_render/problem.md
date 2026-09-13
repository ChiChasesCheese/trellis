# cd08 · Convert Bitmap into ASCII Characters — bitmap font → ASCII grid renderer

**Type:** onsite coding · **Stage:** Onsite（PracHub 明确标注 `interview_round: "Onsite"`）·
**Difficulty:** Medium · **Last updated:** 2026-03-29（PracHub `updated_at`）；`created_at`
2025-07-29
**来源（Sources）：** 本轮（2026-09-03）直接 `curl` 抓取
`https://prachub.com/coding-questions/convert-bitmap-into-ascii-characters` 的原始 HTML，在
Next.js 的 `self.__next_f.push` 数据块里找到该题完整的结构化 JSON（`problem_statement` /
`constraints` / `examples` / `function_signature` / `test_cases` / `hints` 全部齐全，非登录墙
锁住的摘要）——这是 `catalog/discovery/2026-09/C_batchB.md` `## C27` 与
`catalog/discovery/2026-09/C_batchA.md` "新发现 N1" 都提到但**没有真正抓到正文**的那道题，
本轮把它抓全了。
**Confidence（置信度）：high** —— Rules / Worked examples 两节下面的规则文字和两个样例都是
PracHub 原文的逐字迻录（下方逐条标注"原文"）；本仓库自己加工的部分**只有两处**，都在下面
明确标出：(1) 把 PracHub 原本的单一函数 `render_bitmap_text(...)` 按仓库惯例拆成了 Part 1→2→3
三级递进（PracHub 原题不分 part）；(2) "空格字符即使 font 里出现同名 key 也必须按空白字形处理"
这条属于本仓库对原文空隙的显式补全（原文没有讨论 font 是否可能包含 `' '` 这个 key）。

> **说明（非"重建题"警示，仅供对照）**：这道题拿到的证据在整个 "Bitfont" 题目家族三个变体
> 里是**最硬的一个**——PracHub 原文包含函数签名、完整规则文本、两个带解释的样例和约束列表，
> 不是标题或一句话概述。但请仍然读一遍下面的"这个家族的其他版本"一节：同一个 "Bitfont" /
> "bitmap font" 题名下，本仓库还建了另外两道规则完全不同、互不兼容的题（`cd09`、`cd10`），
> 说明现实中这个题库位置至少被三种不同内容复用过。**拿到这道题原文不代表面试时真的会考这一个
> 版本**——只能说它是三者里唯一被完整核实过的一个。

## Context
Stripe's internal debugging tools sometimes need to render structured data as plain-text ASCII
art for terminals and log files — one recurring example is a tiny "bitmap font" renderer: given
a dictionary that maps single characters to fixed-size pixel grids, render arbitrary text as a
block of ASCII characters that a human can read directly in a terminal, without any graphics
library.

## Problem statement (verbatim from source)
> You are given a bitmap font and a text to render. The font is a mapping from single characters
> to a row-major bitstring of length `width * height`. Each bit `'1'` renders as `'#'`, and each
> bit `'0'` renders as `'.'`. Render the given text by placing glyphs side-by-side, inserting
> exactly one `'.'` column between adjacent characters. The space character `' '` is treated as
> a blank glyph of `width` columns (all `'.'`). If any non-space character in `text` is missing
> from the font or has an invalid bitstring length, raise a `ValueError`. Return the rendered
> result as a list of `height` strings (top to bottom).

Original (unsplit) function signature, PracHub Python stub:
```python
def render_bitmap_text(font: dict[str, str], width: int, height: int, text: str) -> list[str]:
```

## Constraints (verbatim)
- `1 <= width <= 32`
- `1 <= height <= 32`
- `1 <= len(text) <= 10000`
- Each font entry's bitstring length is exactly `width * height`
- Bits are only `'0'` or `'1'`
- Space `' '` renders as a blank glyph of `width` columns (all `'.'`)

## This repo's Part split (not in the source — PracHub gives one function)
Per this repo's convention (`CONVENTIONS.md`), the single function above is broken into three
incremental parts so a candidate can lock correct behavior in stages:

- **Part 1 — single glyph decode.** `part1(bitstring: str, width: int, height: int) -> list[str]`
  decodes one already-known-good bitstring into its `height`-row ASCII grid. This is the
  low-level primitive `render_bitmap_text` uses internally, isolated so its row-major /
  bit-mapping logic can be locked before touching text layout.
- **Part 2 — happy-path text layout.** `part2(font: dict[str, str], width: int, height: int,
  text: str) -> list[str]` renders full `text` by calling Part 1 per character and joining
  glyphs with a single `'.'` separator column, handling the space-is-blank rule. **Assumes**
  every non-space character in `text` is present in `font` with a valid-length bitstring —
  behavior is undefined (may raise `KeyError`/produce garbage) otherwise; that's Part 3's job.
- **Part 3 — full contract with validation.** `part3(font, width, height, text) -> list[str]` is
  functionally equal to the source's `render_bitmap_text`: same as Part 2, but raises
  `ValueError` for a missing character or a wrong-length bitstring, exactly per the "If any
  non-space character in text is missing from the font or has an invalid bitstring length,
  raise a ValueError" sentence above. Part 3 must not need to change Part 1's or Part 2's code —
  only add a check before delegating.

**Clarification (this repo's addition, not in the source):** the space character is *always*
rendered as a blank glyph, even if `font` happens to contain a `' '` key — the source text never
says whether `font[' ']` should be consulted, so this repo picks the simpler, unambiguous rule
and tests it explicitly (see the `fmt` test below).

## Input (stdin, for `main()`)
```
PART n
<one JSON object on the rest of stdin>
```
- `n == 1`: JSON is `{"bitstring": "...", "width": W, "height": H}`.
- `n == 2` or `n == 3`: JSON is `{"font": {...}, "width": W, "height": H, "text": "..."}`.

## Output
Print each of the `height` returned strings on its own line, in order, no trailing blank line
beyond the final `\n`.

## Worked examples (verbatim from source `test_cases`)

**Example 1** — `font = {"A": "010101111101101", "B": "110101110101110"}`, `width = 3`,
`height = 5`, `text = "AB"`:
```
.#..##.
#.#.#.#
###.##.
#.#.#.#
#.#.##.
```
(A and B, 3×5 each, rendered and concatenated with one `'.'` separator column.)

**Example 2** — same font, `text = "A A"`:
```
.#.......#.
#.#.....#.#
###.....###
#.#.....#.#
#.#.....#.#
```
(Space renders as a blank 3-column glyph; one `'.'` column still separates every pair of
adjacent characters, including the two separators around the space glyph.)

## Edge cases hidden tests are known to target
- `text` is a single character (0 separators, output width == `width`).
- A glyph's bitstring is entirely `'0'` or entirely `'1'` (all-blank / all-filled grid).
- A character used in `text` is missing from `font` entirely (Part 3 only: `ValueError`; Part 2
  is not required to guard this).
- A font entry exists for a used character but its bitstring length is `!= width * height`
  (Part 3 only: `ValueError`).
- `font` contains an (irrelevant, distractor) entry keyed `' '` — must still render blank per the
  Clarification above, never consulting that entry.
- Repeated characters in `text` (e.g. `"AAAA"`) — glyph decode result must be identical and
  correctly re-placed at each position, not accidentally cached/mutated across calls.
- Large `text` (up to 10<sup>4</sup> characters) with a small font — output row length must be
  exactly `len(text) * width + (len(text) - 1)`.

## Variants seen in the wild
- 090 号 popular 帖（`stripe/coding/090__...bit_font_renderer__popular_7100088.py`，仅标题）用的
  是四段式命名（"Draw One Character / Draw a Word / Compressed Fonts (RLE) / Bonus: Multiple Font
  Types"）——本题的 Part 1/2 与那份标题列表的前两段主题相同，但**没有 RLE 压缩段**，因为本题
  抓到的 PracHub 原文里根本没有压缩/字体切换这两块内容。见 `cd10` 获取那个四段式版本的重建。
- 032 号文件（`stripe/coding/032__...bitfont_render_letters_by_converting_bitmap_symbols_and_printing_wrapped_text__oj_24423292.py`）
  是同一题名下的另一份**互不兼容**的规则：符号是 `*`/`&` 而非 `0`/`1`，渲染规则是简单字符替换
  （不是逐字形 8-bit 解码），而且额外要求"长文本按固定宽度 W 换行"——这个"按 W 换行"的行为
  **在本题（PracHub 原文）里完全不存在**。该文件本身也自陈"原帖没给精确 I/O 格式，样例是自己
  编的"，置信度低，本仓库不采信其规则，只在此处交叉引用。

## 这个家族的其他版本
同一个 "Bitfont" 题名在 `catalog/discovery/2026-09/C_batchB.md` `## C27` 记录了至少三个互不
兼容的版本；本仓库把它们分别建成三道独立的题：
- **本题（cd08）**：ASCII 位图字符集渲染，`font: dict[str,str]` + 逐字形拼接 + `.` 分隔列 —
  证据最硬（PracHub 完整题面）。
- **cd09_bitfont_binary_frames**：自定义二进制帧格式（`FRAME`/`FLAGS`/RLE/COMPACT），置信度
  low-medium，唯一来源怀疑是二次创作。
- **cd10_bitfont_render_compress_invert**：四段式（画字符→画单词→RLE 压缩→翻转），仅有标题级
  证据，规则全部本仓库自拟。
面试当场可能拿到这三个版本中的任意一个，也可能是第四个、本仓库完全没见过的版本——**做完这道题
不代表你已经准备好了整个 "Bitfont" 家族**，请三道都练。

## Sources
- https://prachub.com/coding-questions/convert-bitmap-into-ascii-characters （本轮 2026-09-03
  curl 抓取，`interview_round: Onsite`, `difficulty: medium`, `updated_at: 2026-03-29`, 完整
  `problem_statement`/`constraints`/`examples`/`function_signature`/`test_cases`/`hints`）
- https://prachub.com/companies/stripe?page=4 （标题列表页，用于定位上面的详情页 URL）
- `catalog/discovery/2026-09/C_batchB.md` `## C27`（记录了这题所属的家族证据全貌）
- `catalog/discovery/2026-09/C_batchA.md` "新发现 N1"（上一轮排查已经指出这题证据最硬，但当时
  没有真正把正文抓下来，本轮补上）

## What this tests
- **S09** — byte/character-exact output formatting: the `.` separator column, `#`/`.` mapping,
  and exact row lengths are all graded precisely (this is the primary skill this problem drills).
- **S02** — parsing a font dictionary of fixed-length bitstrings and reasoning about row-major
  layout.
- **S18** — validation/error paths (missing font entry, wrong-length bitstring → `ValueError`).
- **S19** — incremental design: Part 1 (glyph decode) → Part 2 (layout) → Part 3 (validation)
  without touching earlier parts' code.
- **S24** — awareness that the same interview title can hide multiple, non-interchangeable real
  questions (see "这个家族的其他版本" above) — a form of domain/process literacy specific to how
  this OA/onsite question bank gets reused.
