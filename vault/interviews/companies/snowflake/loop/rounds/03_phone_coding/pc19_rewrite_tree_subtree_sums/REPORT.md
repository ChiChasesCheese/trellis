# pc19 Rewrite Tree With Subtree Sums — report

## Summary
TrueInterview 87 题清单第 12 题（2026-06）："Rewrite Tree With Subtree Sums"，题干与
`[5,2,3,1,4,6,7]→[28,7,16,1,4,6,7]` 例子为一手预览原文。2-part：Part 1 完全二叉树数组、反向扫描
一遍搞定 · Part 2 一般二叉树、节点对象、必须迭代（深度 1e5）**(reconstructed)**。

## Sources & confidence
MED（TrueInterview 聚合站预览，题面付费）；Part 2 为重建。

## Approach by part
1. `root2` 的原值完全不重要（只做同形校验），从下标 `n-1` 倒着扫到 `0`：完全二叉树数组保证孩子下标
   永远大于父节点下标，扫到 `i` 时孩子已经算好，直接累加。
2. 节点对象表示允许空洞与任意深度；先用显式栈做一次迭代后序遍历得到"孩子先于父节点"的处理顺序，
   算出每个节点的子树和（存进以节点对象为 key 的字典），再按同一顺序建新树（此时孩子的新节点已经在
   字典里）。序列化/反序列化用 LeetCode 风格前序 + `#` token 流（迭代实现），保证一条深度 1e5 的纯链
   也是 O(n) token、O(n) 时间。

## Pitfalls hidden tests target
- `root2` 的值必须被完全忽略
- Part 1 长度不同 → `ValueError`
- Part 2 只有左孩子/只有右孩子的空洞形状
- Part 2 深度 1e5 的退化链不能触发 `RecursionError`（递归版本会在约 1000 层崩溃）
- 负数子树和

## Complexity & measured cost
Part 1：O(n) 时间、O(n) 输出空间、O(1) 额外辅助空间（原地覆盖一份拷贝）。Part 2：两遍 O(n) 迭代
后序遍历，O(n) 额外字典。编排者验证：200 组随机完全二叉树数组（大小 0–40）与递归暴力解 0 不一致；
200 组随机一般二叉树（深度 ≤6，允许空洞）与递归暴力解 0 不一致；深度 100000 的纯左链树端到端验证
无 RecursionError 且子树和按 depth, depth-1, ..., 1 递减。perf：20 万节点的完全二叉树数组端到端 < 2 s。

## Test inventory
18 tests — part1 7（含 1 隐式参数化）· part2 7 · perf 2 · io/fmt 2；edge 9 · fmt 1 · perf 2 · io 2。

## Skills exercised
S01 完全二叉树数组编码与下标单调性 · S03 递归改迭代（显式栈实现 postorder / preorder 构建）·
识别表示方式在极端规模下的物理限制并主动换表示。
