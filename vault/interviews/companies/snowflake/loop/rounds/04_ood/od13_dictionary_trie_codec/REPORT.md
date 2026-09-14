# od13 Dictionary Trie Codec — report

## Summary
自定义 trie 编码：Part 1 序列化/反序列化正确性（迭代构建、迭代序列化、迭代解析，全部按字典
序返回单词）→ Part 2 压缩率下界（用编码自身的 flag 字符数当节点数，证明
`len(data) <= sum(len(w)) + 2N`，reconstructed）→ Part 3 非法输入分类拒绝 + 不重建整棵树的
`starts_with` 流式前缀查询（reconstructed）。唯一来源是 TrueInterview 同步清单的标题级预览，
编码格式本身完全自选。

## Sources & confidence
MED：kevin-2023-code/Tech-Interview-Questions（TrueInterview 同步）第 63 题 "Serialize and
Deserialize Dictionary Trie"，Algo，2025-12 报告，正文付费，只见"trie + serialize/deserialize
+ 字典序返回"这句预览摘要。

## Approach by part
1. 编码语法 `node ::= flag (letter node)* '#'`，`flag` 取 `'0'/'1'`；字符集设计成"控制字符
   （0/1/#）与数据字符（小写字母）互不相交"，天然无需转义。构建用普通嵌套 dict（非递归的逐词
   遍历）；序列化用显式栈保存 `[node, sorted_letters, next_idx]` 三元组做迭代先序遍历；反序列
   化用一个"当前打开节点前缀"的显式栈做迭代递归下降。
2. 压缩率证明：每个节点贡献 2 个非字母字符，每条边贡献 1 个字母字符，`len(data) = 3N-1`
   （`N`=节点数），而单词总长度 ≥ 边数 `N-1`（每条边至少被一个单词走过），代入得
   `len(data) <= sum(len(w)) + 2N`；`N` 可以直接数编码里的 `0`/`1` 字符个数得到，不需要重建
   树，测试因此可以完全黑盒地校验这条不等式。
3. `starts_with` 只扫描字符串：匹配到当前前缀字符就深入该子节点（消费其 flag，继续扫下一个前
   缀字符），不匹配就用一个只占 O(1) 额外空间的"深度计数器"跳过整棵子树——因为本编码里字母不
   改变嵌套深度，`flag` 开一层、`#` 关一层，恰好是括号匹配。`deserialize` 的非法输入分类（坏
   flag、悬空边、未闭合节点、多余尾部数据）逐条在解析主循环里检测并抛 `ValueError`。

## Pitfalls hidden tests target
- 空单词表、空字符串作为单词（根节点自身是单词）两种退化情形
- 单词包含非小写字母字符必须在 `serialize` 阶段就拒绝，而不是留到序列化后产生歧义编码
- 压缩率不等式在"高度共享前缀"和"完全不共享前缀"两种极端下都必须成立
- 反序列化的每一类非法输入都要单独覆盖（坏 flag / 悬空边 / 未闭合 / 尾部多余数据）
- `starts_with` 必须正确跳过"字母序更靠前但不是目标"的兄弟子树，才能找到后面的目标分支
  （用故意反字母序排列的单词验证）
- 深度 10**4 的单链输入，`sys.setrecursionlimit()` 调低后 serialize/deserialize 依然不报
  `RecursionError`，证明是显式栈迭代而非 Python 递归

## Complexity & measured cost
`serialize`/`deserialize` 均为 O(总编码长度)，迭代实现，栈深度 = trie 最大深度（等于最长单词
长度），不占用 Python 调用栈。`starts_with` 是 O(前缀路径长度 + 沿途需要跳过的兄弟子树总大
小)，不建立任何 trie 对象。10**4 深度单链的往返测试 <0.01s；3000 个随机单词的 SERIALIZE 端到
端脚本远低于 2s 预算。

## Test inventory
33 tests — part1 8 · part2 4（含 1 边界、2 perf）· part3 9（含 1 参数化恶意输入用例展开为多条、
1 命令流、1 随机交叉验证）· fmt/io 若干；edge 17 · perf 2 · io 2 · fmt 1（跨 part 统计，含参数
化用例按 10 条恶意输入展开计入 part3 edge）。

## Skills exercised
S09 类设计先定契约（先划分字符集再证明无歧义）· 自定义序列化格式设计（与 od14 长度前缀编码、
od15 JSON 解析同族）· 树的迭代遍历/构造应对深链输入 · 不重建整个数据结构就能回答局部查询的
流式/惰性解析模式。
