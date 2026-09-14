# cd10 · Implement Bitmap Font Render/Compress/Invert — four-part glyph render + RLE + invert

**Type:** onsite coding (claimed title) · **Stage:** unclear — see Sources below (two
conflicting stage labels across sources) · **Last asked:** section headings dated 2025-12-03
(GitHub scrape date); PracHub entry `created_at` unknown, `updated_at` 2026-05-30
**Frequency:** 2 independent-looking sources, both title/heading-level only, **zero shared rule
text** between them · **Confidence（置信度）：low（题面级别，仅标题/一句话证据）**

**Sources（来源）：**
1. GitHub `divyavenn/coding_problems`，文件
   `stripe/coding/090__20251203__bit_font_renderer__popular_7100088.py`（来源标注
   `https://www.1point3acres.com/interview/problems/post/7100088`）——本轮通过
   `raw.githubusercontent.com` 读取，文件**只有一段 docstring**，列出"Public Section
   Headings"：`Bit Font Renderer Problem / Problem Summary / Part 1: Draw One Character /
   Part 2: Draw a Word / Part 3: Compressed Fonts (RLE) / Solution Details / Bonus Question:
   Multiple Font Types`。**没有任何规则文本、函数签名或样例**——这份文件本身承认只抓到了
   1p3a 帖子的目录结构（大概率是页面锚点/小标题），正文完全没有。
2. `https://prachub.com/coding-questions/implement-bitmap-font-render-compress-invert`——本轮
   （2026-09-03）重新 `curl` 抓取原始 HTML，确认 `"is_locked":true`、`"content":null`、
   `"schema_data":null`（正文和结构化题面**都被登录墙锁住**，与上一轮 `C_batchB.md` `## C27`
   的记录一致，本轮没有绕过登录墙）；唯一可读的字段是 `"title":"Implement bitmap font
   render/compress/invert"`、`"interview_round":"Online Assessment"`（**注意**：与来源 1 的
   "onsite popular 帖"标签不一致——两个来源对"这题出现在哪个阶段"都各执一词）、
   `"meta_description"`/`"seo_summary"`："Evaluates proficiency in bitmap and matrix
   manipulation, lossless compression/decompression techniques, and modular code reuse for
   transformations such as inversion, targeting skills in data representation, algorithmic
   correctness, and space-time trade-offs."

> ⚠️ **重建题（证据仅到标题/小标题级别，规则全部本仓库自拟）**：把上面两个来源合起来看，能
> 确定的只有：(a) 这是一道关于"位图字体"的题；(b) 它按某种方式分成至少 3 个 part，某个 part
> 明确叫 "Draw One Character"、下一个叫 "Draw a Word"、再下一个和"RLE 压缩"有关；(c) 题目
> 标题本身还提到 "invert"（翻转）这个第四个操作，但**没有任何一个来源给出"翻转"具体是翻转
> 什么、怎么翻转**；(d) meta_description 提到"modular code reuse for transformations such as
> inversion"，暗示"翻转"应该复用已有的渲染代码而不是重新实现一遍，但同样没有规则细节。
>
> **除了这四条"主题存在性"信息之外，下面 problem.md 里的字体数据结构、渲染符号、RLE 压缩的
> 具体编码方式、invert 的精确语义、每个 part 的函数签名、约束数字、worked examples ——
> 全部是本仓库自己编的，不是任何来源的原文**。而且，同一个 "Bitfont" 题名下，本仓库还建了
> 另外两道规则完全不同的题（`cd08`、`cd09`），三者互不兼容——本题面在"哪个才是真题"这个问题
> 上给不出答案，只能保证"如果真题真的是'渲染+压缩+翻转'这个方向，覆盖的技能点大致是对的"。
>
> 为了和 `cd08`（已经占用了"ASCII 位图字符渲染"这个具体编码：`font: dict[str,str]` +
> `#`/`.` + 单列分隔符）区分开、避免两道题字面上撞车，本题**故意选择了不同的字体数据结构**
> （每行一个 8-bit 整数，而不是字符串），这是本仓库为避免重复而做的设计选择，不代表真题真的
> 用这种结构。
>
> 练它是为了覆盖 **S09**（逐字节精确输出，本题族共同核心考点）、**S19**（Part 1→4 递进，
> 后面的 part 复用前面的渲染函数而不是重新实现——直接对应 meta_description 里的"modular code
> reuse for transformations such as inversion"这句话）、**S02**（解析定长位图数据）。
> **不要把这里的具体规则/函数签名/样例当成任何形式的"真题原文"去背**，它们是本仓库按主题
> 存在性证据自拟的训练内容。

## Context
A small internal Stripe tool renders glyphs for a custom 8x8 bitmap font — used for status
displays on hardware terminals with no graphics library available. This problem builds that tool
up in four stages: draw a single character, draw a full word, compress/decompress a font using
run-length encoding (so many near-identical glyphs can ship in a small binary), and invert a
glyph for a "negative" (highlighted / selected) rendering — reusing the same draw routine rather
than writing a second renderer.

## Font representation (this repo's own design — see warning above)
A font is `dict[str, list[int]]` mapping a single character to a list of exactly 8 ints, one per
row, each in `0..255`. Bit 7 (MSB) of a row is the leftmost pixel, bit 0 (LSB) is the rightmost.
(This is the same bit convention as `cd09`'s raw frame encoding, deliberately, so a candidate who
has practiced one recognizes the other — but the *data structure* here is `list[int]` rows, not
framed bytes, and there is no separate "font" concept in `cd09` at all.)

## Part 1 — Draw One Character
```python
part1(font: dict[str, list[int]], ch: str) -> list[str]
```
Render a single glyph as 8 strings of 8 characters: `'#'` for a set bit, `'.'` for a clear bit,
most-significant-bit first (leftmost column = bit 7). Raise `KeyError` if `ch` is not in `font`
(this repo's choice: `KeyError`, not `ValueError`, since this is a plain dict lookup and Part 1
does no other validation — Part 3/4 build validated wrappers on top where noted).

## Part 2 — Draw a Word
```python
part2(font: dict[str, list[int]], word: str, sep: int = 1) -> list[str]
```
Render every character of `word` left to right, calling Part 1 per character and placing `sep`
columns of `'.'` between adjacent glyphs (default `sep=1`; `sep=0` is legal — glyphs touch with
no gap). The space character `' '` always renders as a blank glyph (`[0]*8`, i.e. all `'.'`)
without ever being looked up in `font` — same rule this repo used for `cd08`, kept consistent
across the family for the parts of the rules this repo does control. Part 2 must call Part 1 for
each character's rendering rather than re-deriving pixels itself.

## Part 3 — Compressed Fonts (RLE)
```python
part3_compress(rows: list[int]) -> str
part3_decompress(s: str) -> list[int]
```
`rows` is one glyph: 8 ints, each `0..255`. Compress each row independently into a run-length
string of `"<count>:<bit>"` tokens separated by `;` (each token's `count` is a positive int,
`bit` is `'0'` or `'1'`, reading the row MSB-first; consecutive equal bits merge into one token),
then join the 8 per-row strings with `|`. `part3_decompress` is the exact inverse: given the
`"|"`-joined, `";"`-joined token string, rebuild the 8-int row list. `part3_decompress(part3_
compress(rows)) == rows` for every valid 8-int-row list.

## Part 4 — Invert
```python
part4(font: dict[str, list[int]], ch: str) -> list[str]
```
Render the *inverse* of glyph `ch`: flip every bit in every row (`row ^ 0xFF`, keeping the
result an 8-bit value), then render it **by building a one-entry temporary font and calling
Part 1 on it** — Part 4 must not duplicate Part 1's `'#'`/`'.'`/bit-order rendering logic. This
"invert by reusing the renderer on transformed data" structure is this repo's best-effort
reconstruction of the PracHub `meta_description` phrase "modular code reuse for transformations
such as inversion."

## Input (stdin, for `main()`) — this repo's own encoding
```
PART n
<JSON object — shape depends on n>
```
- `n == 1`: `{"font": {...}, "ch": "A"}` (font values are lists of 8 ints).
- `n == 2`: `{"font": {...}, "word": "...", "sep": 1}` (`sep` optional, defaults to 1).
- `n == 3`: `{"op": "compress", "rows": [...]}` or `{"op": "decompress", "s": "..."}`.
- `n == 4`: `{"font": {...}, "ch": "A"}` (same shape as Part 1).

## Output
- Parts 1/2/4: print the returned list of 8 strings, one per line.
- Part 3 `compress`: print the returned string on one line. `decompress`: print the returned
  8-int list as one line, ints comma-separated (e.g. `12,0,255,...`).

## Worked examples
Font: `A = [0b01100110, 0b10011001, 0b10000001, 0b11111111, 0b10000001, 0b10000001, 0b10000001,
0b00000000]` (an 8x8 "A"-ish glyph; picked by this repo, not from any source).

**Part 1** — `part1(font, "A")`:
```
.##..##.
#..##..#
#......#
########
#......#
#......#
#......#
........
```

**Part 2** — `part2(font, "A A", sep=1)` (space renders blank, one `.` separator column on
either side of it, same as every other gap — 8-column `A` + 1-column sep + 8-column blank +
1-column sep + 8-column `A` = 26 columns per row):
```
.##..##............##..##.
#..##..#..........#..##..#
#......#..........#......#
########..........########
#......#..........#......#
#......#..........#......#
#......#..........#......#
..........................
```

**Part 3** — compress row `0b01100110` (`= [0,1,1,0,0,1,1,0]` MSB-first) → runs: `1:0`, `2:1`,
`2:0`, `2:1`, `1:0` → token string `"1:0;2:1;2:0;2:1;1:0"`. Compressing all 8 rows of the `A`
glyph above and joining with `|` gives:
```
1:0;2:1;2:0;2:1;1:0|1:1;2:0;2:1;2:0;1:1|1:1;6:0;1:1|8:1|1:1;6:0;1:1|1:1;6:0;1:1|1:1;6:0;1:1|8:0
```
`part3_decompress` must invert this exactly, recovering `[102, 153, 129, 255, 129, 129, 129, 0]`
(== the original `A` row ints) from that string.

**Part 4** — `part4(font, "A")` inverts every bit of every row, then renders the result:
```
#..##..#
.##..##.
.######.
........
.######.
.######.
.######.
########
```
(Row `0b01100110` → `0b10011001`, `0b11111111` → `0b00000000`, `0b10000001` → `0b01111110`,
etc. — i.e. Part 4's output is exactly Part 1's rendering of `[row ^ 0xFF for row in font[ch]]`,
swapping every `'#'` for `'.'` and vice versa across the whole 8x8 grid.)

## Edge cases hidden tests are known to target
- `sep=0` in Part 2 — glyphs touch directly, no separator column, output row length is exactly
  `8 * len(word)`.
- A row that is entirely one bit (`0` or `255`) compresses to a single RLE token (`"8:0"` or
  `"8:1"`).
- `part3_decompress(part3_compress(rows)) == rows` round-trip for an arbitrary random 8-row
  glyph, not just the worked example (round-trip property test, not a single fixed example).
- `part4` on an all-zero glyph (`[0]*8`) must produce an all-`'#'` grid (`"########"` x8) — the
  "everything was off, now everything is on" boundary.
- `part4` must **not** mutate the original `font` dict entry (`font[ch]` before and after must be
  unchanged) — a naive implementation that inverts rows in place breaks this.
- A word containing a character missing from `font` — Part 2 propagates whatever Part 1 raises
  (`KeyError`), it does not add its own validation layer (this repo picked "no double validation
  across parts" to keep Part 2 a thin composition of Part 1, mirroring the "later parts must not
  need to change earlier ones" principle used across this problem family).

## Variants seen in the wild
- `cd08_bitmap_ascii_render`'s PracHub source (fully verified) has **no RLE and no invert step
  at all** — it is a strict subset of what this title's headings imply, using a completely
  different font data structure (`dict[str,str]` bitstrings, not `dict[str,list[int]]` row
  ints).
- `cd09_bitfont_binary_frames`'s source has its own, unrelated RLE scheme (binary
  `(count_byte, value_byte)` pairs inside a framed byte stream, not a human-readable
  `"count:bit"` text token) — "RLE" appearing in both this problem and `cd09` is **not** evidence
  they're the same question; it's a common enough compression technique to show up independently
  in two different bitmap-font-flavored questions.
- The "Bonus Question: Multiple Font Types" heading in source 1 above is **not implemented
  here** — there is no rule text for it anywhere, and this repo did not want to invent a fifth
  part with zero constraint on what "multiple font types" would even mean.

## 这个家族的其他版本
- **cd08_bitmap_ascii_render**：ASCII 位图字符集渲染，`font: dict[str,str]` + 单函数（本仓库
  拆成 3 part），置信度 **high**——PracHub 完整题面已核实，是三者中唯一被验证过规则细节的。
- **cd09_bitfont_binary_frames**：自定义二进制帧格式（`FRAME`/`FLAGS`/RLE/COMPACT），置信度
  **low-medium**，唯一来源怀疑是二次创作，同样无法在原始页面核实。
- **本题（cd10）**：四段式（画字符→画单词→RLE 压缩→翻转），置信度**低**，只有 6 个小标题
  + 一句 meta_description，规则/数据结构/函数签名/样例全部本仓库自拟。
三道题**互不兼容**，本仓库都建出来只是为了最大化覆盖面——面试当场可能拿到任意一个变体，
也可能是一个和这三者都不一样的第四个版本。做完这三道不代表"背下了 Bitfont 真题"，只代表
"练熟了这类题共同需要的技能（位图解析、逐字节精确输出、渐进式模块化设计）"。

## Sources
- GitHub `divyavenn/coding_problems`：
  `stripe/coding/090__20251203__bit_font_renderer__popular_7100088.py`（本轮 2026-09-03 读取，
  仅含小标题列表，来源标注 `https://www.1point3acres.com/interview/problems/post/7100088`，
  1p3a 原页本轮和上一轮均因 Cloudflare 拦截无法访问核实）
- https://prachub.com/coding-questions/implement-bitmap-font-render-compress-invert （本轮
  2026-09-03 重新 curl 抓取原始 HTML，确认 `is_locked:true`、`content:null`、
  `schema_data:null`，只有 title/meta_description/interview_round/updated_at 可读）
- `catalog/discovery/2026-09/C_batchB.md` `## C27`（记录了 090 号文件与 PracHub 锁定条目两处
  证据，判定"仅标题级信息"）

## What this tests
- **S09** — byte-exact output: `'#'`/`'.'` mapping, separator columns, RLE token string format
  (`"count:bit"` joined by `;` then `|`), all graded on exact string equality.
- **S02** — parsing a fixed-size (8-row, 8-bit) bitmap representation.
- **S19** — incremental design across 4 parts: Part 2 composes Part 1 without re-deriving pixel
  logic; Part 4 reuses Part 1 on transformed data instead of writing a second renderer — this is
  the one design principle this repo is fairly confident the real question also cares about,
  since it's the one specific enough phrase in the (otherwise generic) PracHub meta_description.
- **S18** — round-trip correctness as its own test category (`decompress(compress(x)) == x`),
  distinct from output-formatting correctness.
