# cd10 Implement Bitmap Font Render/Compress/Invert — report

## 摘要
本题是**重建题，置信度低**——证据只到标题/小标题级别。两个来源：(1) GitHub
`divyavenn/coding_problems` 里 `090__20251203__bit_font_renderer__popular_7100088.py`，该文件
本身承认只抓到了 1point3acres 某帖的"Public Section Headings"（Part 1: Draw One Character /
Part 2: Draw a Word / Part 3: Compressed Fonts (RLE) / Bonus: Multiple Font Types），没有任何
规则文本；(2) PracHub `implement-bitmap-font-render-compress-invert` 词条，本轮重新 curl 抓取
确认 `is_locked:true`、`content:null`、`schema_data:null`——正文和结构化题面都被登录墙锁死，
只有标题和一句 `meta_description`（"bitmap and matrix manipulation, lossless
compression/decompression techniques, and modular code reuse for transformations such as
inversion"）可读。两个来源对"这题出现在哪个阶段"的标签还互相矛盾（一个说 onsite popular 帖，
PracHub 字段说 `Online Assessment`）。

因此本题的字体数据结构、渲染符号规则、RLE 编码格式、invert 的精确语义、四个 part 的函数签名、
约束数字、worked examples——**全部是本仓库自拟**，只保留了"渲染单字符→渲染单词→RLE 压缩→
翻转"这个四段式主题方向，以及 meta_description 里"用模块化代码复用来实现 invert 这类变换"这
一条相对具体的线索（体现在 Part 4 必须复用 Part 1 而不是重新实现渲染逻辑这条设计要求上）。

## Sources & confidence
**置信度：低**。为了避免和已经用 `dict[str,str]` bitstring 字体、证据扎实的 `cd08` 字面撞车，
本题故意选择了不同的字体数据结构（`dict[str,list[int]]`，每行一个 8-bit 整数）——这是本仓库的
设计选择，不代表真题真的用这种结构，problem.md 已经明确声明。

## 各 part 设计思路
1. **Part 1**：`_render_row` 是唯一的位到字符映射（MSB-first，'#'/'.'）；`part1` 只是对
   `font[ch]` 的 8 个字节逐个调用它。字符缺失直接让字典查找的 `KeyError` 自然抛出，不额外包装。
2. **Part 2**：对 `word` 里每个字符调用 `part1`（空格特判为全零字形，不查字典），逐行用
   `sep` 个 `.` 连接——不重新推导像素，完全复用 Part 1 的渲染结果。
3. **Part 3**：`part3_compress`/`part3_decompress` 是一对纯函数，逐行独立做游程编码
   （`"count:bit"` 用 `;` 连接，8 行用 `|` 连接）；`part3_decompress` 是严格的逆操作，用
   50 组随机 8 字节字形做 round-trip 属性测试而不只测一个固定样例。
4. **Part 4**：`[byte ^ 0xFF for byte in font[ch]]` 得到翻转后的 8 个整数，包成一个临时的
   单条目 font 字典，再调用 `part1` 渲染——不重复实现任何 `'#'`/`'.'` 映射逻辑，且不修改调用者
   传入的原始 `font[ch]` 列表（专门测试覆盖这一点）。

## Pitfalls hidden tests target
- Part 2 的分隔符列数 `sep` 是参数而不是写死的 1——`sep=0` 时字形直接相邻，行长度公式变化。
- 空格永远是全零字形，不能被误当成"font 里缺失的字符"从而报错——这条规则和 `cd08` 保持一致
  （本仓库自己控制的部分尽量跨题族统一）。
- RLE 压缩/解压必须能处理"整行全 0 或全 1"退化成单个 token 的情况（`8:0`/`8:1`），以及能通过
  随机字形的 round-trip 属性测试，而不是只硬编码通过一个样例。
- Part 4 不能就地修改 `font[ch]` 这个列表（一个"省事"的实现可能直接在原列表上做异或再传给
  渲染函数，这样会污染调用者的字体数据）。
- Part 4 必须通过调用 Part 1 来渲染（结构性要求，对应 meta_description 里"modular code reuse
  for transformations such as inversion"这句话）——测试无法直接断言"有没有调用 Part 1"，但
  `test_invert_A` 和 `test_render_A`/`test_render_all_zero_and_all_one_glyph` 共同保证两者的
  渲染规则（'#'/'.' 映射、MSB-first）完全一致，间接锁定这个设计意图。

## Complexity & measured cost
`part1`：`O(1)`（固定 8x8）。`part2`：`O(len(word))`。`part3_compress`/`decompress`：
`O(1)`（固定 8 行 8 位）。Perf 测试：8000 字符长词、27 字符字体表，通过 `run_script` 测量，
预算 2s / 256MB，实测远低于预算。

## Test inventory
20 个测试——part1: 4（含 1 edge）· part2: 6（含 1 edge、1 fmt、1 perf）· part3: 6（含 1 edge、
1 fmt、1 io）· part4: 3（含 2 edge）；按 marker 汇总：edge 6 · fmt 2 · io 2 · perf 1。

## 本题覆盖的知识点
- **S09**（逐字节精确输出）：`'#'`/`'.'` 映射、分隔列宽度、RLE token 的 `:`/`;`/`|` 三级分隔符
  格式，全部要求逐字节匹配——是本题族（cd08/cd09/cd10）共同的核心考点。
- **S02**（解析定长位图数据）：字体是"字符 → 8 个整数行"的定长表示，需要正确做 MSB-first 位
  提取。
- **S19**（渐进式设计 + 强制代码复用）：Part 2 复用 Part 1、Part 4 复用 Part 1 渲染变换后的
  数据，而不是各自重新实现渲染逻辑——这是本题唯一有较具体来源依据（PracHub
  meta_description）的设计原则。
- **S18**（校验/正确性的另一种形式：round-trip 属性）：Part 3 的 `decompress(compress(x)) == x`
  用随机输入验证，而不仅仅是格式匹配一个固定字符串——教会候选人"往返一致性"也是一种需要显式
  测试的正确性维度，不能只测"看起来对"的单个样例。
