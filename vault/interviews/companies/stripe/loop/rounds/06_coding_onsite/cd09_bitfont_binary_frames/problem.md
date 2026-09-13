# cd09 · Bitfont Repository: Implement Decoders and Compose Them — binary frame format decoder

**Type:** onsite coding (claimed) · **Stage:** onsite, "small made-up binary format" round ·
**Last asked:** 2026-04-23（该转述文件的抓取/生成日期戳，非确证的候选人经历日期）
**Frequency:** 1 个来源，无法交叉验证 · **Confidence（置信度）：low-medium**

**Sources（来源）：** GitHub `divyavenn/coding_problems` 仓库，文件
`stripe/coding/004__20260423__bitfont_repository_implement_decoders_and_compose_them__oj_c3826719.py`
（本轮通过 `raw.githubusercontent.com` 直接读取全文），该文件自己标注的来源是
`https://www.1point3acres.com/interview/problems/c3826719-e927-4380-9e5e-e54bd82496c4`。1p3a
全站对本环境的 WebFetch/curl 均返回 Cloudflare 拦截页，**本轮和上一轮排查都没能访问那个原始
URL**，无法核实这份 GitHub 文件是不是对 1p3a 原帖的忠实转录。

> ⚠️ **重建题（证据强度不足，不代表真题）**：这道题面的**唯一**来源是上面这份 GitHub 文件，而
> 且 `catalog/discovery/2026-09/C_batchB.md` `## C27` 对它的判定是——内容详实到"面试官逐字
> 讲稿 + 验收标准 + 一份能通过全部隐藏测试的参考实现"的程度，风格更像仓库作者（或某个 agent）
> **基于一个真实存在的题目标题做的合理重构**，而不是逐字候选人转录；因为原始 1point3acres 页面
> 完全无法访问，**本仓库无法判断这份规格里有多少是真、多少是编的**。同时，`## C27` 里明确记录
> 了**同一个 "Bitfont" 题名下至少还有另外两个互不兼容的版本**（见本文件"这个家族的其他版本"
> 一节）——本仓库把三个版本都建成了题，这**不代表其中任何一个是"标准版"**，只代表三者都值得
> 练，因为面试当场可能拿到其中任意一个，甚至一个都不是。
>
> 本题下面的 FRAME 格式、FLAGS 位定义、RLE/COMPACT 编码规则、三个 Part 的函数签名、约束数字，
> **全部原样保留自这份低-中置信度来源**，一个字都没有改（因为这份来源本身已经细到函数签名和
> 参考实现的程度，没有留"仓库需要自己拟"的空白）；本仓库自己新增的只有 stdin/stdout 的具体
> 编码方式（见下方 Input/Output 一节，源文件本身是用 pytest 直接调函数，没有 stdin/stdout 格式）
> 和 Part 拆分保持不变（源文件本身已经是三段式）。
>
> 练它是为了覆盖 **S02**（结构化二进制解析）、**S09**（逐字节精确输出）、**S19**（Part 间边界
> 不可越界的递进设计——源文件明确写了"Part 3 不应该需要改 Part 1/2 的代码"）、以及一个现有
> 编号体系里**完全没有**的技能点——见下方"建议新增技能 S25"（`REPORT.md` 里详细展开）。
> **不要把这份规格当成"背下来准考"的真题**，它更适合当"练手的二进制协议解析题"来用。

## Context (as delivered by the interviewer, per source)
> Hey — in this round we're going to look at a small, made-up binary format called "Bitfont".
> Don't worry, no actual font expertise is required. The format is just a vehicle for the real
> exercise: writing two small decoders and then composing them so the output of one feeds the
> input of the other.

## The wire format (verbatim from source)
A Bitfont file is a sequence of **FRAMES** on the wire. Each frame represents one glyph. The wire
format is a stream of bytes; assume **big-endian** throughout.

```
FRAME (variable length):
  +--------+--------+--------+- - - - - - - - - - +
  | LEN_HI | LEN_LO | FLAGS  |    PAYLOAD ...     |
  +--------+--------+--------+- - - - - - - - - - +

    LEN_HI, LEN_LO  : 16-bit unsigned big-endian length of PAYLOAD, in BYTES.
                      (Header bytes are not included.)
    FLAGS           : 8-bit. Bit 0 (LSB) is RLE, bit 1 is COMPACT.
                      Other bits are reserved -- ignore.
    PAYLOAD         : LEN bytes. The interpretation depends on FLAGS.
```

The end of stream is just EOF — there's no trailer or sentinel.

A PAYLOAD encodes an **8x8 monochrome glyph**: 64 pixels, each 1 bit, where 1 = "on" and 0 =
"off". The encoding depends on FLAGS:

- **If `FLAGS == 0` (raw):** PAYLOAD is exactly 8 bytes. Row 0 is byte 0, row 1 is byte 1, etc.
  Within a byte, the most significant bit is the leftmost pixel.
- **If FLAGS bit 0 is set (RLE):** PAYLOAD is a sequence of `(count, value)` pairs, each one
  byte. `count` is 1..255 and `value` is 0 or 1. The total of all counts across pairs is exactly
  64. Decode left-to-right, top-to-bottom.
- **If FLAGS bit 1 is set (COMPACT):** PAYLOAD is exactly 4 bytes. Each byte encodes two rows:
  the high nibble is row `2k`, the low nibble is row `2k+1`. A nibble's leftmost pixel is its
  most significant bit. (So COMPACT only works for glyphs whose rightmost 4 columns are all
  zero — decode always fills those 4 columns with `0`.)
- **If both RLE and COMPACT bits are set:** that's invalid; raise `ValueError`.

## Part 1 — Glyph decoder ("Decoder A")
```python
part1(payload: bytes, flags: int) -> list[list[int]]
```
Returns an 8x8 grid of 0s and 1s (a list of 8 lists of 8 ints). This is the inner decoder — it
does **not** know about frames or lengths, it's handed a payload and the flags byte and produces
the grid. Raise `ValueError` for: a raw payload whose length isn't 8; an RLE payload whose length
is odd, whose total pixel count isn't 64, whose count is 0, or whose value isn't 0/1; a COMPACT
payload whose length isn't 4; or both RLE and COMPACT bits set.

## Part 2 — Stream decoder ("Decoder B")
```python
part2(data: bytes) -> list[tuple[int, bytes]]
```
Parses `data` (the full byte content of a Bitfont file, already read into memory — see
Clarifications below) into a list of `(flags, payload)` tuples, one per frame, in stream order.
Does **not** decode the payload — only parses the framing. Raise `EOFError` if the stream ends
mid-frame (a header shorter than 3 bytes when a new frame was expected, or a payload shorter
than its declared `LEN`).

## Part 3 — Compose
```python
part3(data: bytes) -> list[list[list[int]]]
```
Returns the list of glyphs in the file, in order. Must be the obvious composition of Part 1 and
Part 2 — `[part1(payload, flags) for flags, payload in part2(data)]` — **without** changing
anything in Part 1 or Part 2's logic. If Part 3 requires touching Part 1/2's code, the module
boundary was drawn in the wrong place (this is stated explicitly in the source material as the
thing the interviewer is grading for).

## Constraints (verbatim from source)
- Each frame's PAYLOAD is at most 65535 bytes (the `LEN` field is 16-bit).
- Glyphs are always 8x8.
- (Source additionally says files may be up to 100MB and `iter_frames` should be a generator
  that never loads the whole file into memory — see Clarifications for why this repo's Part 2
  signature does not preserve that streaming property.)

## Input (stdin, for `main()`) — this repo's own encoding, NOT from the source
The source problem is graded by calling Python functions directly (`pytest -q` against a starter
repo) — it has no stdin/stdout format. This repo adds one so the problem fits the drill harness:
```
PART n
<line 2, format depends on n — see below>
```
- `n == 1`: line 2 is `<flags_int> <payload_hex>` (payload as a hex string, even length).
- `n == 2` or `n == 3`: line 2 is `<data_hex>` — the entire byte stream as one hex string.

## Output
- **Part 1**: print the 8x8 grid as 8 lines, each a string of 8 characters `'0'`/`'1'`
  (row-major, top row first).
- **Part 2**: print one line per parsed frame, `"<flags> <payload_hex>"` (decimal flags, then a
  space, then the payload re-encoded as lowercase hex), in stream order.
- **Part 3**: print each glyph as 8 lines of `'0'`/`'1'` (same format as Part 1), with exactly
  one blank line between consecutive glyphs and no trailing blank line after the last glyph.

## Worked examples
Grids below are shown with `#`/`.` for human readability only — the actual `part1` return value
is `list[list[int]]` (1/0 ints), and the stdout rendering (see Output above) prints each row as
a literal `'0'`/`'1'` string, e.g. row `"##......"` below is `"11000000"` on stdout.

**Raw glyph** — `payload = bytes([0b11000000, 0, 0, 0, 0, 0, 0, 0b00000011])`, `flags = 0`:
```
##......   (11000000)
........   (00000000)
........   (00000000)
........   (00000000)
........   (00000000)
........   (00000000)
........   (00000000)
......##   (00000011)
```

**RLE glyph**, all-off — `payload = bytes([64, 0])`, `flags = 1` (bit 0 set): 8 rows of
`"00000000"` (64 zero pixels total, one run).

**RLE glyph**, checkerboard-ish stripes — `payload = bytes([8, 1, 8, 0, 8, 1, 8, 0, 8, 1, 8, 0,
8, 1, 8, 0])`, `flags = 1`: alternates 8 pixels on / 8 off, i.e. rows 0,2,4,6 are `"11111111"`
and rows 1,3,5,7 are `"00000000"` (each run is exactly one full row of 8 pixels; total
`8*8 = 64`).

**COMPACT glyph** — `payload = bytes([0b11110000, 0b10100000, 0, 0])`, `flags = 2` (bit 1 set):
byte 0 -> row0 nibble `1111` -> `"11110000"`, row1 nibble `0000` -> `"00000000"`; byte 1 -> row2
nibble `1010` -> `"10100000"`, row3 nibble `0000` -> `"00000000"`; bytes 2-3 (`0x00`) -> rows 4-7
all `"00000000"`.

**Two-frame stream** (Part 2/3) — one raw frame with an all-`0xFF` payload followed by one RLE
frame `payload=bytes([64,0])`:
```
hex = "0008" + "00" + "ff"*8 + "0002" + "01" + "40" + "00"
```
`part2` returns `[(0, b"\xff"*8), (1, b"\x40\x00")]`; `part3` returns the raw glyph (all `1`s)
followed by the all-off glyph, separated by one blank line in the stdout rendering.

## Edge cases hidden tests are known to target
- Both RLE and COMPACT bits set (`flags = 0b11`) → `ValueError` from Part 1, regardless of
  payload content.
- Raw payload with length `!= 8` → `ValueError`.
- RLE payload with odd length, a `count == 0`, a `value` other than 0/1, or a total pixel count
  `!= 64` (both under and over) → `ValueError` for each case independently.
- COMPACT payload with length `!= 4` → `ValueError`.
- Empty byte stream (`data = b""`) → Part 2 returns `[]`, Part 3 returns `[]` (zero frames is not
  an error — it's simply an empty file).
- Stream that ends exactly after a complete final frame (no partial header) → parses cleanly,
  no error.
- Stream that ends with a partial header (1 or 2 leftover bytes, not 3) → `EOFError`.
- Stream that ends with a `LEN` field promising more payload bytes than remain → `EOFError`.
- A frame with `LEN == 0` (a payload-less frame) — flags must still make sense: `flags=0`
  (raw) with `LEN=0` is itself invalid at the Part 1 level (raw needs exactly 8 bytes), so this
  can only legitimately appear paired with... nothing valid for 8x8 glyphs; hidden tests probe
  that `part2` still frames it correctly (parses `LEN=0` as a zero-length payload) even though
  `part1(b"", 0)` must then raise `ValueError` — i.e. Part 2's framing must never itself validate
  glyph semantics, only byte counts.
- Multiple frames using different flag values back to back in the same stream.

## Clarifications (this repo's additions — the source does not specify these)
- **Non-streaming Part 2 signature.** The source insists `iter_frames` be a generator so a
  100MB file is never fully materialized in memory. This repo's harness needs pure functions
  that return plain, comparable data (`CONVENTIONS.md`), so `part2` here takes the **entire**
  byte stream as a `bytes` argument and returns a **list**, not a generator over a file-like
  object. This is a deliberate simplification for testability — if you are drilling this
  problem to prepare for the *actual* interview (should you get it), remember the real ask is a
  generator over a stream, and you should practice that version too, not just this one.
- **stdin/stdout hex encoding.** Entirely this repo's invention (see Input/Output above); the
  source is graded by direct function calls in a cloned repo, not stdin/stdout.
- **Part 2's `LEN=0` framing behavior** (yields a frame with an empty payload rather than
  treating zero-length as an error) is inferred from "the format" section not saying anything
  special about `LEN=0`, plus the general principle stated in the source that Part 2 must not
  know about glyph semantics.

## Variants seen in the wild
- 090 号 popular 帖（同一个 divyavenn 仓库，`090__20251203__bit_font_renderer__popular_7100088.py`）
  只有标题列表，没有正文，但它的三段式命名（"Draw One Character / Draw a Word / Compressed Fonts
  (RLE)"）明显是**另一套**规则——那是逐字符 ASCII 渲染 + RLE 压缩，不是这里的二进制帧格式。
- 032 号文件（同一个仓库）是纯 `*`/`&` 符号替换 + 按宽度换行，跟这里的二进制帧协议完全不是
  一回事。
- 这三份文件（004/032/090）全部声称来自同一个 1point3acres 题目标签 "Bitfont"，但规则互不兼容——
  `catalog/discovery/2026-09/C_batchB.md` 的结论是"需要作为家族而非单题看待"。

## 这个家族的其他版本
- **cd08_bitmap_ascii_render**：ASCII 位图字符集渲染（`font: dict[str,str]` + 逐字形拼接），
  这是三者里**唯一**被 PracHub 完整题面核实过的版本（置信度 high）。
- **本题（cd09）**：自定义二进制帧格式（`FRAME`/`FLAGS`/RLE/COMPACT 三种编码），置信度
  low-medium，**唯一**来源怀疑是二次创作，无法在原始 1point3acres 页面核实。
- **cd10_bitfont_render_compress_invert**：四段式（画字符→画单词→RLE 压缩→翻转），仅有标题级
  证据，规则全部本仓库自拟。
这三道题**规则互不兼容，不能互相替代**。面试当场拿到的可能是这三者之一、三者的某种混合、
或者一个本仓库完全没见过的第四个版本——把三道都做一遍是目前能做到的最大覆盖，但不保证覆盖到
真题。

## Sources
- GitHub `divyavenn/coding_problems`：
  `stripe/coding/004__20260423__bitfont_repository_implement_decoders_and_compose_them__oj_c3826719.py`
  （本轮通过 `raw.githubusercontent.com` 直接读取全文，2026-09-03）
- 该文件自称来源：`https://www.1point3acres.com/interview/problems/c3826719-e927-4380-9e5e-e54bd82496c4`
  （本轮与上一轮均因 Cloudflare 拦截无法访问，**未核实**）
- `catalog/discovery/2026-09/C_batchB.md` `## C27`（对这份来源"low-medium，疑似二次创作"的
  判定原文）

## What this tests
- **S02** — parsing a structured binary wire format (fixed-size header fields, a
  length-prefixed variable-size payload).
- **S09** — byte-exact output (bit-grid rendering, hex re-encoding of payload bytes).
- **S18** — validation/error paths across three independent failure families (raw length,
  RLE arithmetic, COMPACT length, mutually-exclusive flags, truncated stream).
- **S19** — Part 1 / Part 2 / Part 3 must stay strictly decoupled; Part 3 is graded partly on
  *not* needing to touch Part 1/2.
- **A candidate new skill, not covered by S01–S24 or A01–A16** — see `REPORT.md`'s "建议新增
  技能 S25" section: big-endian multi-byte length fields, MSB-first bit extraction within a
  byte, nibble-level bit extraction, and RLE run-length decoding, all as one combined "binary
  frame decoding" skill family.
