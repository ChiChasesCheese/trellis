# pc11 Character Frequencies — report

## Summary
两道 fastprep.io 结构化来源的暖场 Easy 题（跨字符串计数 / 跨嵌套列表计数）合并成一道 3-part：Part 1 扁平列表原题 → Part 2 任意深度嵌套、必须迭代展开 **(reconstructed 合并)** → Part 3 top-k 打平全带上 **(reconstructed)**。

## Sources & confidence
MED（fastprep.io 两个页面，Easy/Phone Screen，2026-06 报告）；Part 3 未见一手报道，按计数排序类暖场题最常见追问方向重建。

## Approach by part
1. 用字典累加每个字符出现次数（含空格、标点，区分大小写），按 `(-count, char)` 排序。
2. 展开用显式栈（`list` 当栈、`iter()` 当"当前遍历到哪"），不递归；栈深度等于嵌套深度，不受 Python 调用栈限制。展开后复用 Part 1 的计数/排序逻辑。
3. 在 Part 2 排序结果上找第 `k` 名的次数作为阈值，向后扫描把所有次数等于阈值的都纳入（可能超过 k 个）。
4. line-driven 的嵌套输入没有用 `ast.literal_eval`/`json.loads`——这两个库自己是递归实现，几千层嵌套会先于我们的代码报 `RecursionError`/`SyntaxError`，等于让 IO 层面白测了"迭代展开"这个考点；改成手写的显式栈扫描器解析一行类 JSON 语法。

## Pitfalls hidden tests target
- 统计对象是所有字符，不只是字母（空格、标点也要算）
- 排序 tie-break：次数相同按字符升序
- Part 1 收到嵌套结构必须报错（不能悄悄兼容）
- Part 2 顶层非 list / 叶子既非 str 也非 list 的类型校验
- 2 万层嵌套不能递归展开（直接用 Python 循环构造对象验证，绕开任何序列化格式自身的递归限制）
- Top-k 的两种打平场景：打平发生在第 1 名之后、打平发生在中间名次之后
- `k = 0`、`k` 超过不同字符总数
- Unicode 多字节字符按单个 code point 统计

## Complexity & measured cost
Part 1/2 均 O(总字符数) 时间、O(不同字符数) 额外空间；Part 3 额外 O(不同字符数 log) 排序后线性扫描找打平截断点。IO 层 perf 测试用 5000 个叶子、400 层嵌套（json.dumps 序列化本身受 Python 默认递归限制，故没有用来测极端深度）验证 2 秒内完成；真正的"任意深度不递归"结论直接对纯函数 API 用循环构造的 20000 层嵌套对象验证，绕开序列化器。编排者用 `collections.Counter` + 显式排序作为独立基准，在 200/150 组随机小输入上分别交叉验证 Part 1 和 Part 3，0 不一致。

## Test inventory
23 tests — part1 7（含 2 样例、1 fmt、1 io）· part2 8（含 1 样例、1 perf、1 io）· part3 6（含 1 样例含 4 断言、1 io）；edge 12 · fmt 1 · perf 1 · io 3。

## Skills exercised
S06 计数哈希 + 确定性排序 tie-break（与滑窗/事件流题同一类考法）· 迭代展开任意深度结构，避免递归深度限制 · 输入格式设计要意识到"解析器本身的递归限制"这个隐藏坑
