# cd09 · Bitfont 二进制帧解码：重建题，练 S25"字节序 + MSB-first 取位 + nibble + RLE"的通用套路

> [!tldr]
> - 这题考的是：一个自定义二进制帧格式（`LEN_HI/LEN_LO/FLAGS/PAYLOAD`），PAYLOAD 按 FLAGS 分三种
>   编码（raw / RLE / COMPACT）解出一个 8x8 位图——本题是**重建题**，唯一来源是 GitHub 上一份对
>   1point3acres 帖子的转录，原帖因 Cloudflare 无法核实，**置信度 low-medium**
> - 三步套路：先写"只管 payload、不管帧"的 `part1`（三种编码各一个私有函数）→ 再写"只管字节数、
>   不管 payload 语义"的 `part2`（纯游标扫描）→ `part3` 是两者的直接组合，不能反过来改前两者
> - 最值得带走的一个模式：**字节序拼接 / MSB-first 取位 / nibble 切片 / RLE 游程解码**，这四个
>   操作是"自定义二进制协议解析"这一类题目的通用词汇表——不止这一道题会用到

## 1. 题目在说什么（人话版）
面试官说："我们看一个叫 Bitfont 的、自己编的小二进制格式，不需要任何字体专业知识，这只是个载体，
真正考的是写两个小解码器再把它们组合起来。" 文件是一串 **FRAME**，每帧代表一个字形：3 字节头部
（16-bit 大端长度 + 1 字节 FLAGS）+ 变长 PAYLOAD。PAYLOAD 编码一个 8x8 单色位图，具体怎么编码
看 FLAGS 的低两位：`raw`（8 字节，每字节一行，MSB 是最左边像素）、`RLE`（`(count, value)` 字节对
的序列，游程之和必须正好是 64）、`COMPACT`（4 字节，每字节的高/低 nibble 分别是相邻两行，右边 4
列固定补 0）。

**先说清楚这道题的位置**：它属于同一个"Bitfont"题名下三个互不兼容版本之一。`cd08` 是唯一被
PracHub 完整原文核实过的版本（ASCII 字符串位串渲染，置信度 high）；本题（cd09）来自一份"内容详实
到像面试官逐字讲稿"的 GitHub 转录文件，但唯一的上游 1point3acres 页面两轮排查都被 Cloudflare
拦截，**无法确认这是不是二次创作**；`cd10` 是仅有标题级证据、规则全部自拟的重建题。三者字体数据
结构、编码规则完全不兼容，本题练的是"二进制帧解析"这一类通用技能，而不是"背下这份规格就等于准备好
了 Stripe 的 Bitfont 真题"。

## 2. 读题：把文字变成模型
- **实体**：`FRAME`（头部三字段 + payload）、`glyph`（8x8 的 0/1 网格）。
- **输入长什么样**：一段字节流（本仓库用 hex 字符串编码进 stdin），可能包含 0 到多个 FRAME，
  背靠背排列，没有结束哨兵——EOF 就是结束。
- **输出要什么**：Part 1 输出一个 8x8 网格；Part 2 输出 `(flags, payload)` 元组列表；Part 3 输出
  多个网格，中间用一行空行分隔。
- **状态**：Part 2 内部有一个"读到第几个字节了"的游标，但这是**函数内部的局部状态**，不是跨调用
  要记住的东西——每次调用 `part2(data)` 都从 `pos=0` 重新开始。
- **一句话建模**：**定长头部 + 变长 payload 的二进制帧协议解析**，payload 内部是三条互相独立的
  "按位/按半字节/按游程"解码规则。

> [!note] 为什么 Part 1/Part 2 要严格分开
> 题面原文明确说"Part 2 不应该理解 payload 语义"、"Part 3 不应该需要改 Part 1/2 的代码"——这不是
> 客套话，是评分点。`part2` 只关心"这一帧有几个字节"，完全不管这些字节按 raw/RLE/COMPACT 解读出来
> 是什么；`part1` 只关心"给我 payload 和 flags，我解出网格"，完全不知道这个 payload 是从哪个偏移
> 量的字节流里切出来的。这样 `LEN=0`（空 payload）这种在语义上没意义的帧，`part2` 依然能正确地
> 把它当成一个合法帧解析出来，报错留给 `part1` 在真正尝试解码的时候去报。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 `PART n` + hex 字符串，转成 `bytes`，分发调用。
2. **Part 1 最小可用**：先写 `_decode_raw`（最简单：`(byte >> (7-col)) & 1`），立刻用一个手算过的
   样例（比如 `0b11000000` 应该是 `"11......"`）验证位方向对不对——**方向反了不会报错，只会全错**，
   这是这类题目最值钱的一次自测。再补 `_decode_rle`、`_decode_compact`，`part1` 本身只做 flags
   分发 + 互斥检查。
3. **Part 2 叠加**：纯字节游标扫描，一次处理一帧的三字节头部 + 变长 payload，判断流是否截断
   （`EOFError`）——**这一步完全不调用 `part1`**，只是切片。
4. **Part 3 叠加**：`[part1(payload, flags) for flags, payload in part2(data)]`，一行代码，不
   引入新逻辑。
5. **收尾**：字节序、MSB-first、nibble 高低顺序这三处都各手算一遍 worked example 核对方向。

## 4. 代码怎么组织
```
_decode_raw(payload) -> grid          # 8 字节，每字节一行，MSB-first
_decode_rle(payload) -> grid          # (count,value) 对，游程之和校验 == 64
_decode_compact(payload) -> grid      # 4 字节，每字节两行（高/低 nibble），右 4 列补 0
part1(payload, flags) -> grid         # 只做 flags 位判断 + 分发，不做实际解码
part2(data) -> list[(flags, payload)] # 纯字节游标，不解释 payload 内容
part3(data) -> list[grid]             # part1、part2 的直接组合
main(stdin, stdout)                   # I/O 分发
```
拆分原则：**每种编码一个私有函数，`part1` 只做分发**；`part2` 全程不导入/不调用 `part1` 的任何
东西。这样"Part 3 不该改 Part 1/2"这条要求在结构上就自动满足，不需要额外小心。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
FLAG_RLE, FLAG_COMPACT = 0b01, 0b10

def _decode_raw(payload):
    if len(payload) != 8:
        raise ValueError(f"raw payload must be 8 bytes, got {len(payload)}")
    return [[(byte >> (7 - col)) & 1 for col in range(8)] for byte in payload]   # MSB-first

def _decode_rle(payload):
    if len(payload) % 2 != 0:
        raise ValueError("RLE payload must have even length")
    pixels = []
    for i in range(0, len(payload), 2):
        count, value = payload[i], payload[i + 1]
        if value not in (0, 1) or count == 0:
            raise ValueError("bad RLE pair")
        pixels.extend([value] * count)                    # 游程展开
    if len(pixels) != 64:
        raise ValueError(f"RLE pixel total must be 64, got {len(pixels)}")
    return [pixels[r * 8 : (r + 1) * 8] for r in range(8)]

def part2(data):
    frames, pos, n = [], 0, len(data)
    while pos < n:
        if n - pos < 3:
            raise EOFError("stream ended in frame header")
        length = (data[pos] << 8) | data[pos + 1]          # 大端序拼 16-bit 长度
        flags = data[pos + 2]
        pos += 3
        if n - pos < length:
            raise EOFError("stream ended mid-payload")
        frames.append((flags, data[pos : pos + length]))
        pos += length
    return frames

def part3(data):
    return [part1(payload, flags) for flags, payload in part2(data)]   # 只是组合
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：题面说'assume big-endian throughout'，所以 16-bit 长度是
  `LEN_HI << 8 | LEN_LO`；如果面试官给的是小端序，这一行要反过来写，我先手算一个样例锁死方向。」
- 写 `_decode_raw` 时：「MSB-first 意味着 `byte` 的第 7 位是最左边的像素，我用 `>> (7-col)` 而
  不是 `>> col`，写完我会用一个手算过的字节验证一下方向。」
- 写 `part2` 时：「这个函数完全不认识 `part1`，也不知道 payload 里装的是什么——它只回答'这一帧有
  几个字节'，这样即使 payload 语义以后再加一种编码，`part2` 一行都不用改。」
- 交付时：「三个 part 都过了；RLE 和 COMPACT 同时置位这种互斥标志的情况我在 `part1` 最前面先检查，
  确保报的是'互斥标志'错误，不会被后面的长度检查抢先报出一个不相关的错误信息。」

## 7. 二进制帧解码的通用套路（S25，不止这道题会用到）
这道题最值得抽出来的不是"这个格式的规则"，而是解这一**类**题共同要用到的四个原语：

- **字节序拼接**：多字节整数 = 从若干个 8-bit 字节按声明的字节序组装。大端序就是"第一个字节是
  高位"：`(b0 << 8) | b1` 拼两字节，三字节同理 `(b0<<16)|(b1<<8)|b2`。判断方向的方法：题面会
  直接写"big-endian"/"little-endian"，找不到就用 worked example 反推——手算一个已知长度的样例，
  看拼出来的数对不对。
- **MSB-first 取位**：先想清楚"第 0 列对应哪一端"。本题是"最高位是最左边的像素"，所以取第 `col`
  列（从 0 开始，最左边是第 0 列）要用 `(byte >> (7 - col)) & 1`——列号越大，右移位数越少。写一个
  独立的小函数（这题就是 `_decode_raw` 内的这行表达式），所有依赖"按位取值"的地方都调用它，不要在
  多个函数里各写一遍位移表达式，写反了会全错但不会报错，是最难自己发现的一类 bug。
- **nibble 切片**：本质是"把字节按更细粒度切开，每组独立解释"。`(byte >> 4, byte & 0xF)` 拿到高、
  低两个 4-bit 半字节，取半字节内的位复用同一个"按 MSB-first 取 N 位"的逻辑（这题是 `range(4)`
  版本的 `_decode_raw`），不要为 nibble 重新发明一套位移公式。
- **RLE 游程解码**：`(count, value)` 对逐个展开，**边解码边累加总长度**，最后校验总数是否等于
  声明的大小（本题是 64）——这条校验本身就是发现"少算/多算一个游程"的免费探测器，写完代码之后手算
  一个样例走一遍，比只看代码更容易发现方向问题。

**通用建议**：拿到任何"自定义二进制协议"题，先不要想框架逻辑（怎么切帧、怎么拼装），先把上面这
四类原语各写成一个独立的小函数，每写一个就用题面给的 worked example 手算验证一遍方向——方向错了
的位运算代码"看起来能跑"（不会崩溃，只是全错），比空指针异常更难发现，越早用样例锁死方向，后面
叠加框架逻辑时越不用回头怀疑底层原语。

## 8. 同族题 / 延伸
- **cd08_bitmap_ascii_render**：同一题名下唯一被 PracHub 完整原文核实的版本（置信度 high），
  字体是已经解码好的 ASCII 位串（`dict[str,str]`），不涉及任何字节级位运算——如果面试拿到的是这个
  版本，本文讲的 S25 全套技能都用不上，直接看 `cd08` 那篇的 S09 格式化套路即可。
- **cd10_bitfont_render_compress_invert**：同一题名下另一个重建题（置信度低，仅标题级证据），
  字体是 `dict[str, list[int]]`（每行一个整数），渲染规则跟本题的 MSB-first 取位方向一致（题面
  故意保持一致，便于识别），但**没有帧格式、没有 COMPACT**，RLE 压缩是人类可读的文本 token
  （`"count:bit"`），不是本题这种二进制字节对——两者的 RLE **看起来像同一个概念，实现完全不同**，
  不要把 cd09 的 `_decode_rle` 直接搬过去用。
- S25（二进制帧解码）是 2026-09-03 才加进 `skills_matrix.md` 的新技能编号，证据强度弱于 S01–S24
  （详见 `skills_matrix.md` 里"S25 的收录理由与它的不确定性"一节）——技能本身是真的，但"Stripe 考
  这个"这件事没有被证实，练它是为了覆盖一类通用能力，不是因为确定会考到这份具体规格。
- 练习命令：`python3 loop/mock.py start cd09 -m 60`
