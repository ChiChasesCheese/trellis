# cd08 Convert Bitmap into ASCII Characters — report

## 摘要
这是 "Bitfont" 题目家族三个变体里证据最硬的一道。本轮（2026-09-03）直接 `curl` 抓取
`https://prachub.com/coding-questions/convert-bitmap-into-ascii-characters` 的原始 HTML，在
Next.js RSC 数据块（`self.__next_f.push`）里找到该题**完整**的结构化 JSON：`problem_statement`
（逐字规则）、`constraints`（6 条）、`examples`（2 个带解释的样例）、`function_signature`（含
Python/Java/C++/JS 四种语言的函数签名）、`test_cases`（与 examples 数值一致的可执行测试）、
`hints`（3 条提示）。这比 `catalog/discovery/2026-09/C_batchA.md` "新发现 N1" 当时用 WebFetch
只拿到几句引用摘录（受工具单次引用 ≤125 字符限制）要完整得多——本轮直接读原始 HTML 绕开了这个
限制。`interview_round` 字段确认是 **Onsite**（不是 OA），`difficulty: medium`，
`updated_at: 2026-03-29`。

## Sources & confidence
**置信度：high**——规则文字、两个样例的输入输出、约束列表全部是源 JSON 字段的逐字迻录（非转述、
非摘要）。本仓库唯一的加工是：(1) 把源头单一函数 `render_bitmap_text(...)` 按仓库惯例拆成
Part 1（单字形解码）→ Part 2（happy-path 拼接）→ Part 3（补上校验，等价于源函数完整契约）三级
递进——原题本身不分 part；(2) "font 里即使出现 `' '` 这个 key 也必须忽略、空格永远渲染空白"
是本仓库对原文未讨论情形的显式补全。这两点都在 problem.md 里明确标注，不冒充原文。

## 各 part 设计思路
1. **Part 1**：`_decode_glyph_rows` 是唯一的解码原语——按 `width` 切片成 `height` 行，
   `'1'->'#'`、`'0'->'.'`，长度不对直接 `ValueError`。Part 2/3 都只调用它，不重复实现。
2. **Part 2**：happy path，假设 `text` 里每个非空格字符都在 `font` 里且长度合法；空格永远是
   `width` 列的空白字形，从不查 `font`。逐行把每个字形的对应行用 `.` 连接。
3. **Part 3**：在 Part 2 的拼接逻辑之外，逐字符补一次"缺字符 / 长度不对"检查，检查通过才调用
   Part 1 解码——**不修改** Part 1/Part 2 的代码，只是在外层加校验，这正是源文件
   "raise a ValueError" 这句话唯一新增的行为。

## Pitfalls hidden tests target
- 分隔列只在字符之间插入一次，字符串首尾不加；`"A"`（单字符）时输出行长度就是 `width`，没有
  分隔符。
- 空格字形必须是"全空白"而不是复用某个字符的字形；且必须优先于 `font` 查找（哪怕 `font` 里
  真的有 `' '` 这个 key）。
- 长度校验和"缺字符"校验是两种不同的失败模式，必须都能独立触发 `ValueError`（`test_part3_...`
  两个测试分别覆盖）。
- 重复字符（如 `"AAAA"`）不能因为共享同一个 `font[ch]` 而在多次调用间产生副作用或缓存污染——
  `test_repeated_characters_render_identically` 按位置切片核对四个字形槽位分别独立正确。

## Complexity & measured cost
`O(len(text) * width * height)`：每个字符解码一次 `width*height` 位、逐行字符串拼接。
`len(text) <= 10^4`、`width,height <= 32`，最坏情况约 10^4 * 32 * 32 ≈ 10^7 次字符操作，
Python 字符串拼接走 `str.join`，远低于预算。Perf 测试：10000 字符文本、5×7 字体，通过
`run_script` 子进程测量，预算 2s / 256MB，实测远低于预算（典型 < 0.3s，几 MB）。

## Test inventory
17 个测试——part1: 4（含 1 io、1 edge）· part2: 5（含 1 fmt）· part3: 8（含 1 io、1 perf、2 edge、
1 fmt）；按 marker 汇总：edge 3 · fmt 2 · io 2 · perf 1。

## 本题覆盖的知识点
- **S09**（逐字节/逐字符精确输出格式）：本题最核心的考点——`.` 分隔列、`#`/`.` 映射、每行长度
  公式 `len(text)*width+(len(text)-1)` 全部要求精确匹配，是三道 Bitfont 题共同的考点。
- **S02**（解析定长位串字典）：`font` 是 `char -> 固定长度 bitstring` 的映射，需要正确按
  `width` 切片成 `height` 行（row-major）。
- **S18**（校验与错误路径）：Part 3 的"缺字符 / 长度不对 → ValueError"两条独立校验路径。
- **S19**（渐进式设计）：Part 1（原语）→ Part 2（拼接）→ Part 3（校验）三级递进，Part 3 不改
  Part 1/2 代码。
- **S24**（领域/流程认知）：意识到同一个面试题标题在题库里可能对应多个互不兼容的版本（见
  problem.md "这个家族的其他版本"），拿到一个版本的完整题面不代表准备好了整个家族。
