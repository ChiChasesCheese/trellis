# cd08 · Bitmap → ASCII 渲染：Bitfont 三兄弟里唯一被验证过的一个，练"定长位图解码 + 逐字节精确输出"

> [!tldr]
> - 这题考的是：给一个 `font: dict[str,str]`（字符 → 定长 0/1 位串），把一段文本渲染成 ASCII 网格
>   （`#`/`.`），核心是"按 `width` 切成 `height` 行的 row-major 解码" + "字符之间插一列 `.` 分隔符"
> - 三步套路：先写单字形解码 `part1`（不管文本、不管拼接）→ 再叠加happy-path拼接 `part2` → 补校验
>   `part3`，三层互不重写
> - 最值得带走的一个模式：**只写一个 `_decode_glyph_rows` 解码原语，三个 part 都只在外面加薄层**——
>   这类"渲染题"的 bug 十有八九出在分隔符、空格、行尾这些细节上，原语只写一份，出错也只用改一处

## 1. 题目在说什么（人话版）
Stripe 内部调试工具有时要把结构化数据渲染成纯文本 ASCII 图，方便直接贴进终端或日志——一个常见例子
就是"位图字体渲染器"：给一个字典，把每个字符映射成一串定长的 0/1（按行优先排列的像素），再把一段
文本渲染成一块人眼能直接读的 ASCII 字符画。

小例子（`width=3, height=5`）：`font["A"]` 是长度 15 的位串，`text="A"` 渲染出 5 行、每行 3 个
字符的网格，`'1'→'#'`、`'0'→'.'`。两个字符中间要插一列 `.`，比如 `text="AB"` 输出的每行长度是
`3+1+3=7`。

**先说清楚这道题所在的"位置"**：Stripe 题库里同一个标题下面（"Bitfont"/"bitmap font"）至少有三个
互不兼容的真题版本——本文讲的 cd08 是唯一一个抓到 **完整** PracHub 原文（规则、约束、两个带解释的
样例全部逐字核实，置信度 high）的版本；`cd09_bitfont_binary_frames` 是自定义二进制帧格式的重建题
（置信度 low-medium，唯一来源怀疑是二次创作）；`cd10_bitfont_render_compress_invert` 是四段式
渲染+压缩+翻转的重建题（置信度低，仅标题级证据，规则本仓库自拟）。**三者的字体数据结构、编码规则
完全不同，不能把其中一个的做法套到另一个上**——面试当场拿到哪一个版本，只有到了现场才知道。

## 2. 读题：把文字变成模型
- **实体**：`font`（字符到位串的映射）、`glyph`（单个字符解码出来的 `height` 行网格）、`text`（要
  渲染的字符串）。
- **输入长什么样**：`font: dict[str,str]`，每个 value 长度固定是 `width*height`；`text` 里的每个
  字符（除了空格）理论上都应该能在 `font` 里查到。
- **输出要什么**：`height` 行字符串，每行是把 `text` 里每个字符对应网格的"这一行"用 `.` 连接起来。
- **状态**：**没有**——这是一个纯函数式的问题，同一个字符出现几次，解码结果都应该完全一样，不存在
  "处理过程中要记住什么"。
- **一句话建模**：**定长位图解码（原语） + 横向拼接布局（规则） + 校验（外层）** 三层叠加的问题。

> [!note] 为什么选这个数据结构
> 候选方案是"边解析边拼接，一次过"还是"先把每个字符独立解码成网格，再横向拼"。选后者，因为
> Part 1（单字形解码）和 Part 2（文本布局）在题面里本来就是两件不同的事——解码是"按 `width` 切片 +
> 位映射"，布局是"每行用 `.join` 拼起来"。拆成两层之后，`part2`/`part3` 不用重新推导任何一行像素，
> 只是在调用 `part1`（内部是 `_decode_glyph_rows`）的基础上加拼接规则。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 `PART n` 头 + JSON body，分发到 `part1/2/3`，先让"空实现"跑起来。
2. **Part 1 最小可用**：`_decode_glyph_rows(bitstring, width, height)`——按 `width` 切成 `height`
   行，`'1'→'#'`、`'0'→'.'`。长度校验（`ValueError`）现在就加，因为它是这个原语自己的契约，不是
   Part 3 才需要的东西。立刻用题面样例（单字符 `"A"`）自测。
3. **Part 2 叠加**：写 `_blank_glyph`（空格永远是全空白，不查 `font`），把每个字符的网格用
   `_decode_glyph_rows`/`_blank_glyph` 求出来，再按行用 `.join` 横向拼接。用两个字符的样例
   （`"AB"`）自测分隔符列数对不对。
4. **Part 3 叠加**：在 Part 2 的循环外面加一层"缺字符 / 长度不对 → `ValueError`"的检查，检查通过
   才调用解码——**不改** Part 1/2 的代码，只在外面套一层。
5. **收尾**：单字符（0 个分隔符）、全空/全实字形、`font` 里混进一个无关的 `' '` key 这几个样例都
   过一遍。

## 4. 代码怎么组织
```
_decode_glyph_rows(bitstring, width, height) -> list[str]   # 唯一的解码原语，长度校验在这里
_blank_glyph(width, height) -> list[str]                    # 空格的固定网格，从不查 font
part1(bitstring, width, height) -> list[str]                # 直接调解码原语
part2(font, width, height, text) -> list[str]                # happy path：逐字符取网格 + 按行 join
part3(font, width, height, text) -> list[str]                # part2 的逻辑外面加一层校验再调用
main(stdin, stdout)                                          # 只做 I/O 分发
```
拆分原则：**解码原语（`_decode_glyph_rows`）只出现一次**，`part1` 直接暴露它给外部单独测试，
`part2`/`part3` 都通过它取网格，从不自己重新推导 `'#'`/`'.'` 映射或行切片逻辑。这样即使后面要求
"支持第三种符号"或"支持列优先而不是行优先"，改动也只集中在这一个函数里。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def _decode_glyph_rows(bitstring, width, height):
    if len(bitstring) != width * height:
        raise ValueError(f"invalid bitstring length: expected {width*height}, got {len(bitstring)}")
    rows = []
    for r in range(height):
        row_bits = bitstring[r * width : (r + 1) * width]
        rows.append("".join("#" if bit == "1" else "." for bit in row_bits))
    return rows

def _blank_glyph(width, height):
    return ["." * width] * height

def part2(font, width, height, text):
    glyphs = [
        _blank_glyph(width, height) if ch == " " else _decode_glyph_rows(font[ch], width, height)
        for ch in text
    ]
    # 按行取每个字形对应的那一行，用 '.' 连接——分隔符只在字符之间出现一次
    return [".".join(glyph[row] for glyph in glyphs) for row in range(height)]

def part3(font, width, height, text):
    glyphs = []
    for ch in text:
        if ch == " ":
            glyphs.append(_blank_glyph(width, height)); continue
        if ch not in font:
            raise ValueError(f"character {ch!r} is missing from font")
        glyphs.append(_decode_glyph_rows(font[ch], width, height))   # 校验通过才解码
    return [".".join(glyph[row] for glyph in glyphs) for row in range(height)]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：`font` 里如果碰巧有 `' '` 这个 key，我不打算查它——空格永远是空白字形，
  题面没说这种情况该怎么处理，我按更简单、更不歧义的规则来，等下会专门测一下这一条。」
- 写 Part 1 时：「这是这道题唯一的解码逻辑，我把它单独拆出来，因为 Part 2/3 都要用，而且我想先把
  它的边界条件（长度不对）锁死，不要留到 Part 3 才补。」
- 写 Part 2 时：「分隔符只在字符之间插一次，我用 `.join` 而不是手动拼字符串加 `.`，这样首尾不会
  多出多余的分隔符。」
- 交付时：「三个 part 都过了题面样例；如果时间允许，我会在测试里补一个 `text` 单字符的用例，专门
  确认这时候输出行长度就是 `width`，没有分隔符。」

## 7. 常见跑偏（方法层面，3 条）
- **空格/行尾/换行边界散落在多个地方判断**：`.join` 只在函数里出现一次没问题，但如果每个 part
  都各自写一遍"字符是不是空格"、"这一行要不要加换行"，很容易某个 part 漏改。渲染类题目最容易死在
  这些边界上，做法是把"一个字形怎么变成字符串"这件事集中到一个函数（这题是 `_decode_glyph_rows`
  + `_blank_glyph` 两个），`main()` 里的换行只用一次 `"\n".join(...) + "\n"`，不要在循环体内部
  逐行 `print`——那样容易在最后一行前后多一个或少一个 `\n`。
- **在 Part 2 里顺手加校验**：题面明确说 Part 2 是 happy path、Part 3 才需要校验，如果 Part 2
  提前加了 `if ch not in font` 之类的检查，Part 3 复用 Part 2 时容易在"要不要重复校验一次"上
  纠结，反而让代码变复杂。先老老实实按 part 的契约来。
- **重复字符共享了同一份可变对象**：如果 `_decode_glyph_rows` 内部不小心返回了缓存的 list 而不是
  每次新建一份，`"AAAA"` 这种重复字符的用例会在多次访问同一份数据后暴露出"改一个位置全都变了"的
  bug——这属于"共享可变状态"，不属于这道题的核心逻辑，但是隐藏测试专门覆盖了这一点。

## 8. 同族题 / 延伸
- **cd09_bitfont_binary_frames**：同一题名下的自定义二进制帧格式重建题（`FRAME`/`FLAGS`/RLE/
  COMPACT），置信度 low-medium；核心考点从"字符串位串解码"换成了"字节序 + MSB-first 取位 + RLE
  游程解码"（S25），跟本题的 `_decode_glyph_rows` 完全是两套不同的原语。
- **cd10_bitfont_render_compress_invert**：同一题名下的四段式重建题（画字符→画单词→RLE 文本
  压缩→翻转），置信度低（仅标题级证据）；字体数据结构换成了 `dict[str, list[int]]`（每行一个
  8-bit 整数），跟本题的 `dict[str,str]` 位串也不兼容。
- 三道题共享的唯一确定考点是 **S09（字节/字符级精确输出）**——分隔符、`#`/`.` 映射、行长度公式在
  三道题里都要求精确匹配，三篇文章讲的具体格式细节不同，但"用一个集中的格式化函数管住边界"这条
  方法论是相通的。
- 练习命令：`python3 loop/mock.py start cd08 -m 60`
