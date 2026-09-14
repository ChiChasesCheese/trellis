# pc28 Preorder Traversal Without Invalid Nodes — report

## Summary
一手预览只给出输入形状（nodes/edges/root/invalid）与"跳过 invalid 节点做前序遍历"，**没有说清
楚 invalid 节点的子树怎么处理**。本 kit 把两种合理读法都实现、都测试（都标
**(reconstructed)**），作为"面试要主动澄清歧义而不是脑补一种"的示范，而不是猜一种就当作唯一
正确答案。

## Sources & confidence
MED（聚合站 TrueInterview 同步清单，题面付费，仅预览输入形状 + 一句描述可见）：见
`../../../catalog/raw/github_repos.md` §2/§3。两种子树处理方式均为重建。

## Approach by part
1. `preorder_skip_invalid_splice`：invalid 节点不输出，但子节点仍入栈（"透明化"）。
2. `preorder_skip_invalid_prune`：invalid 节点不输出，子节点也不入栈（"整棵剪掉"）。
两者都用显式栈（`list` 当栈，子节点反序 push 保证弹出顺序符合 `edges` 给定的从左到右顺序），
避免递归在深度 1e5 的链表形树上撑爆调用栈。

## Pitfalls hidden tests target
- 两种读法在"root 本身 invalid"时结果差异最大（splice 仍遍历 root 的子节点，prune 整棵为空）
- invalid 包含叶子节点时两种读法结果相同（用来确认没有把两个函数写反）
- 子节点顺序必须遵守 `edges` 给出的顺序，不能按编号重排
- 深度 3000/100000 的链表形树必须迭代实现，不能递归（默认递归深度限制会直接报错）
- `invalid` 为全部节点、为空的边界

## Complexity & measured cost
两个函数都是 `O(n)` 时间、`O(n)` 辅助栈空间（最坏情况链表形树，栈深度等于树深度，但用的是
Python list 而非调用栈，不受 `sys.getrecursionlimit()` 限制）。perf：深度 10 万的链表形树端到
端 < 2s。

## Test inventory
17 tests — part1 6（含 1 perf、1 io）· part2 6（含 1 io）；边界与 io 混合计入 edge/fmt/perf/io：
edge 8 · fmt 1 · perf 1 · io 3。

## Skills exercised
S05（树的迭代式前序遍历，显式栈模拟递归）· 对题面歧义的敏感度（两种读法都实现而不是猜一种）·
大深度输入下递归 vs 迭代的正确选择。
