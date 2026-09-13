# cd10 · Bitfont 渲染/压缩/翻转：证据最弱的重建题，练"渐进设计里怎么强制复用而不是重新实现"

> [!tldr]
> - 这题考的是：四段式（画单字符 → 画一个词 → RLE 文本压缩/解压 → 翻转）——本题是 Bitfont 家族
>   三个变体里**证据最弱的一个**（只有两个来源的标题/小标题，规则、数据结构、样例全部本仓库自拟，
>   **置信度低**）
> - 三步套路：`part1` 只做一件事（单字符渲染原语）→ `part2`/`part4` 靠"调用 `part1`"而不是重新
>   推导像素来完成 → `part3` 是独立的一对纯函数（压缩/解压），跟渲染逻辑完全不接触
> - 最值得带走的一个模式：当后面的 part 本质是"对同一份数据做个变换、再用同一个渲染器画出来"时，
>   变换和渲染要分开写，渲染只写一份——这是这道题唯一有具体来源依据的设计要求

## 1. 题目在说什么（人话版）
一个内部小工具给硬件终端渲染 8x8 位图字体（没有图形库）。这道题按四步搭建它：画一个字符、画一整个
词、用游程编码压缩字体（省空间）、给字形做"反色"（翻转每个像素，复用同一个渲染函数而不是再写一个）。

**先说清楚这道题的证据强度**：两个来源都只到标题级——一份 GitHub 文件只有 6 个小标题（"Draw One
Character / Draw a Word / Compressed Fonts (RLE) / Bonus: Multiple Font Types"等），没有任何
规则文本；PracHub 词条整页被登录墙锁住，只能读到标题和一句 `meta_description`。**下面的字体数据
结构、渲染符号、RLE 编码格式、invert 的精确语义、函数签名、约束数字、worked examples——全部是
本仓库自己编的**，不是任何来源的原文。它属于同一"Bitfont"题名下三个互不兼容版本之一：`cd08` 是
唯一被 PracHub 完整原文核实的版本（置信度 high）；`cd09` 是自定义二进制帧格式的重建题（置信度
low-medium）；本题置信度最低。练这道题的价值不在于"背下这份规格"，而在于练熟"四段递进 + 强制
复用"这套方法论——如果真题真的落在这个方向，这套方法论是通用的。

## 2. 读题：把文字变成模型
- **实体**：`font: dict[str, list[int]]`（字符 → 8 个整数，一行一个字节）、单个字形的渲染结果
  （8 行字符串）、RLE 压缩后的 token 字符串。
- **输入长什么样**：每行是 `0..255` 的整数，bit 7（MSB）是最左边像素——这个位方向故意跟 `cd09`
  的 raw 编码保持一致，但**数据结构不同**（这里是 `list[int]`，`cd09` 是帧里的字节流），不要
  混用两边的解码函数。
- **输出要什么**：Part 1/2/4 是 8 行字符串；Part 3 是一个 `"|"`/`";"`/`":"` 三级分隔符的 token
  字符串，或者反向解压出的整数列表。
- **状态**：**没有**，四个 part 全是纯函数——这一点跟 `cd08` 一样，是这整个 Bitfont 家族的共同
  特征。
- **一句话建模**：**一个渲染原语 + 两种复用它的变换（横向拼接、位翻转） + 一对跟渲染完全无关的
  独立编解码函数**。

> [!note] 为什么 Part 4 不能重新实现渲染
> 唯一相对具体的线索是 PracHub 的 `meta_description`："modular code reuse for transformations
> such as inversion"——这句话直接点名"翻转"应该复用已有的渲染代码，而不是重新写一遍
> `'#'`/`'.'` 映射逻辑。做法是：先把每行整数异或 `0xFF` 得到翻转后的行数据，包成一个**临时的
> 单条目 font 字典**，再调用 `part1` 去渲染它——这样 `part1` 的渲染规则只存在一份，`part4` 一行
> 都不需要知道 `'#'`/`'.'` 是怎么映射的。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 `PART n` + JSON，分发到四个 part。
2. **Part 1 最小可用**：`_render_row(byte)` 是唯一的位到字符映射，`part1` 只是对 `font[ch]` 的
   8 个字节逐个调用它。缺字符直接让字典查找的 `KeyError` 自然抛出，不额外包装。
3. **Part 2 叠加**：对 `word` 里每个字符调用 `part1`（空格特判为全零字形，不查字典），按行用
   `sep` 个 `.` 连接——**不重新推导像素**，必须复用 `part1` 的返回值。
4. **Part 3 独立实现**：`compress`/`decompress` 是一对纯函数，跟 `font`/`part1` 完全无关，逐行
   独立做游程编码；先写 `compress`，再写 `decompress`，用同一个样例做一次 round-trip 自测
   （`decompress(compress(rows)) == rows`）。
5. **Part 4 叠加**：`[byte ^ 0xFF for byte in font[ch]]` 得到翻转行，包成临时字典调用 `part1`——
   **不修改**调用方传入的原始 `font[ch]` 列表。
6. **收尾**：`sep=0`（无分隔符）、全 0/全 1 字形、随机字形的 round-trip 都过一遍。

## 4. 代码怎么组织
```
_render_row(byte) -> str                              # 唯一的位到字符映射，MSB-first
part1(font, ch) -> list[str]                           # 渲染原语，KeyError 自然抛出
part2(font, word, sep=1) -> list[str]                   # 逐字符调 part1，按行 join
part3_compress(rows) -> str                             # 独立于 font/渲染的纯编码函数
part3_decompress(s) -> list[int]                        # compress 的精确逆操作
part4(font, ch) -> list[str]                            # 异或翻转 + 临时 font + 调用 part1
main(stdin, stdout)                                     # I/O 分发
```
拆分原则：**渲染逻辑只在 `_render_row`/`part1` 里出现一次**；Part 3 是完全独立的一对函数，不接触
`font`/渲染；Part 4 通过"构造临时数据 + 调用已有原语"完成，而不是新增一条渲染路径。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def _render_row(byte):
    return "".join("#" if (byte >> (7 - col)) & 1 else "." for col in range(8))

def part1(font, ch):
    return [_render_row(byte) for byte in font[ch]]     # font[ch] 缺失时 KeyError 自然抛出

def part2(font, word, sep=1):
    blank = [_render_row(0)] * 8
    glyphs = [blank if ch == " " else part1(font, ch) for ch in word]   # 复用 part1，不重推像素
    sep_str = "." * sep
    return [sep_str.join(g[row] for g in glyphs) for row in range(8)]

def part3_compress(rows):
    row_tokens = []
    for byte in rows:
        bits = [(byte >> (7 - c)) & 1 for c in range(8)]
        tokens, i = [], 0
        while i < 8:
            j = i
            while j < 8 and bits[j] == bits[i]:
                j += 1
            tokens.append(f"{j-i}:{bits[i]}")            # 游程 token
            i = j
        row_tokens.append(";".join(tokens))
    return "|".join(row_tokens)

def part4(font, ch):
    inverted = [byte ^ 0xFF for byte in font[ch]]        # 不改原 font[ch]，新建一份
    return part1({ch: inverted}, ch)                      # 复用 part1 渲染，不重写渲染逻辑
```

## 6. 面试里怎么说（边写边讲）
- 写 Part 2 时：「我调用 `part1` 拿到每个字符已经渲染好的字符串，再按行拼接——这样渲染规则只有
  一份，以后如果 `'#'`/`'.'` 的映射要改，我只用改 `_render_row` 一个地方。」
- 写 Part 4 时：「我先把这行数据异或 `0xFF` 算出翻转后的字节，包成一个临时的单条目字典传给
  `part1`，而不是自己再写一遍 `'#'`/`'.'` 的判断——面试官如果问'为什么不直接在 `part1` 的返回值
  上做字符串替换'，我会说异或位再渲染更贴近'这是同一份数据的另一种解释'这个语义，而不是'渲染完
  之后再做字符串层面的整容'。」
- 写 Part 4 的边界时：「我确认了一下 `font[ch]` 这个列表在函数结束前后没有变化——我是新建了一份
  异或后的列表，没有就地改原数据。」
- 交付时：「Part 3 的 round-trip 我不只测了题面那一个样例，还用随机生成的 8 行字形跑了一遍
  `decompress(compress(x)) == x`，因为这类编解码对最容易在'看起来对一个例子'但漏了某种退化情况
  上翻车。」

## 7. 常见跑偏（方法层面，3 条）
- **Part 4 就地修改 `font[ch]`**：一个"省事"的写法是直接在原列表上异或再传给渲染函数，这样会
  污染调用方的字体数据——凡是"翻转/变换后再渲染"这类需求，先问自己"我是不是在原数据上直接改了"，
  养成"变换永远产出新对象"的习惯。
- **渲染逻辑和压缩逻辑混在一起写**：Part 3 的 `compress`/`decompress` 跟 `font`/渲染完全无关，
  如果写着写着顺手把它们跟 `part1`/`part2` 耦合起来（比如 `compress` 内部调用 `_render_row`），
  会让这两块本来独立的功能变得难以单独测试——保持它们互不知道对方存在。
- **空格/行尾/分隔符散落在多处判断**：`part2` 的分隔符宽度是参数 `sep`，不是写死的 1；渲染类题目
  最容易死在这种"看起来是常量、其实是变量"的细节上——用一个集中的 `_render_row`/拼接表达式管住
  行内容和分隔符，不要在多个 part 里各自重新拼一遍字符串。

## 8. 同族题 / 延伸
- **cd08_bitmap_ascii_render**：同一题名下唯一被 PracHub 完整原文核实的版本（置信度 high），
  字体是 `dict[str,str]` 位串，没有 RLE、没有 invert，是这个标题下"证据最扎实但规则最简单"的
  版本。
- **cd09_bitfont_binary_frames**：同一题名下自定义二进制帧格式的重建题（置信度 low-medium），
  RLE 是二进制 `(count_byte, value_byte)` 对，跟本题人类可读的 `"count:bit"` 文本 token 是**完全
  不同的编码**——两者都叫"RLE"不代表规则一样，练完 `cd09` 不能直接把它的 `_decode_rle` 搬来用在
  这道题上。
- 三道题共享 S09（逐字节精确输出）和 S19（渐进式设计）两个核心考点，但只有本题把"强制代码复用"
  作为唯一相对具体的评分线索（来自 `meta_description`）——如果面试当场真的拿到"渲染+压缩+翻转"
  这个方向的题，多花一点心思在"Part 4 有没有真的调用 Part 1"这件事上，比抠 RLE 编码的具体符号
  更值得。
- Part 3 的 round-trip 测试（`decompress(compress(x)) == x`）是"正确性"的另一个维度——不是只测
  输出格式对不对，而是测"两个函数合起来是不是彼此的精确逆操作"，这类属性测试思路在别的编解码题
  （base64、URL 编码、序列化）里同样适用。
- 练习命令：`python3 loop/mock.py start cd10 -m 60`
