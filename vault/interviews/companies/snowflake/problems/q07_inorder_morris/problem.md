# q07 · Inorder Traversal — recursive → iterative → Morris (constant space)

**Type:** LC 原题 + 现场追问 · **Stage:** Phone Screen (2019) / OA 题库复用 (2023) ·
**Last asked:** 2023 (Canada 题库索引 #20) · **Frequency:** 2 独立来源 · **Confidence:** medium-high

## 背景

LeetCode 94「Binary Tree Inorder Traversal」是 Snowflake 电面的经典开场题，考察点不在"能不能写出
中序遍历"，而在**现场追问能不能把空间复杂度压到 O(1)**（Morris 遍历）。同一道题也在 2023 年的 OA
题库池里原题复用。三个 part 对应候选人在面试现场被要求依次展示的三种实现，且都必须产出完全相同的
遍历结果——差异只在于额外空间/调用栈开销。

> "He told me I would get a bonus point if I could do it in constant space"
>
> — 2019 Snowflake phone screen, https://leetcode.com/discuss/interview-question/424385/snowflake-phone-screen-patching-array/
>   (Q2 = LeetCode "Binary Tree Inorder Traversal" with this live follow-up)

## 输入格式

`main()` 的 stdin 格式：第一行 `PART n`（n ∈ {1,2,3}）；第二行是一棵树的 LeetCode 风格
level-order CSV 列表（字符串 `"null"` 或空字符串表示缺失的子节点），例如 `1,null,2,3`；第二行为空
或缺失表示空树。输出：一行逗号连接的中序遍历值（空树输出空行）。

`build_tree(values: list[str]) -> TreeNode | None` 是 `main()` 内部用来把 CSV 解析成树的辅助函数
（标准 LeetCode level-order BFS build：用一个"待分配子节点"的队列，按 (left, right) 顺序消费值，
`null`/空字符串的位置不产生新的队列项）。

## 规则 Part 1..3

### Part 1 — 递归中序遍历

`part1(root: TreeNode | None) -> list[int]` — 标准递归中序遍历（left, node, right）。调用栈深度
O(h)（h = 树高），这是三个实现里唯一会在极端深树上炸调用栈的版本。

### Part 2 — 迭代中序遍历（显式栈）

`part2(root: TreeNode | None) -> list[int]` — 用显式栈（Python list，分配在堆上，不是调用栈）做
迭代中序遍历，不允许递归。对所有树，输出必须和 part1 完全一致。

### Part 3 — Morris 中序遍历（O(1) 额外空间）

`part3(root: TreeNode | None) -> list[int]` — 经典 Morris 遍历：用"前驱指针临时穿线（threading）"
技巧，不用栈、不用递归，额外空间 O(1)。关键点：**遍历结束后必须把树恢复成原来的形状**（不能留下
悬空的穿线指针）。对所有树，输出必须和 part1/part2 完全一致。

算法：对每个 `node`，如果有左子树，找到它的中序前驱（左子树中最右的节点）。第一次到达 `node`
时，把 `predecessor.right` 临时指向 `node`（穿线），然后向左子树走；第二次通过穿线回到 `node`
时（此时 `predecessor.right is node`），说明左子树已经访问完，先把穿线拆掉（`predecessor.right =
None`，恢复原状），再输出 `node.val`，然后向右走。如果 `node` 没有左子树，直接输出并向右走。

## 3+ Worked Examples

```
build_tree(["1","null","2","3"])          # root=1, right child=2, 2 的 left child=3
  -> inorder [1, 3, 2]                     # part1 == part2 == part3

build_tree([])            -> inorder []
build_tree(["1"])         -> inorder [1]

build_tree(["5","3","8","1","4","7","9"])
  # 标准 level-order BFS build: root=5; left=3,right=8; 3 的 children=1,4; 8 的 children=7,9
  -> inorder [1, 3, 4, 5, 7, 8, 9]
```

## 隐藏测试边界清单

- 空树（`root is None`）：三个 part 都返回 `[]`
- 单节点树
- 只有左子树的链（left-only chain）、只有右子树的链（right-only chain）
- **关键差异化测试（题面明确要求，不能省略）**：构造一棵纯右链的深树（2000 个节点，只有
  `.right`，深度超过 Python 默认递归上限）。在 `sys.setrecursionlimit(300)` 的临时约束下（用
  try/finally 保存并恢复原始 limit，绝不能让改动泄漏到其它测试）：
  1. 断言 `part1(deep_root)` 在此限制下抛出 `RecursionError`（证明朴素递归版本用 O(n) 调用栈）；
  2. 断言 `part3(deep_root)`（Morris）在同样受限的 recursion limit 下成功返回正确的 2000 个元素
     `[0, 1, ..., 1999]`（证明 Morris 的 O(1) 调用栈/空间，它从不递归）；
  3. 断言 `part2(deep_root)`（显式栈迭代）在同样受限下也成功（它的"栈"是堆上的 Python list，不
     是调用栈）。
- Morris 遍历后重新对同一棵树对象跑 `part1`，结果必须和第一次一致（证明穿线被正确拆除，没有
  留下悬空指针污染树结构）
- 一棵 ~1e5 节点的、构造时本身不递归（迭代构造）的近似平衡树，做 part3 的性能测试
- `main()`/io：stdin 格式——第一行 `PART n`，第二行 CSV level-order 树值（第二行为空表示空树）；
  输出一行逗号连接的中序值（空树输出空行）；用 `run_script` 测试

## 变体

- 前序 / 后序遍历的 Morris 变体（Morris 后序需要"逆转右链"技巧，比中序难得多，是常见的追问延伸）。
- 要求同时返回节点引用（而不仅仅是值），用于后续"找中序后继"之类的追问。
- LC 2023 Canada 题库复用版本可能只考 part1（最基础），part2/part3 是面试官现场追问，不一定每次
  都问到——但本题按照"三个 part 全都要能独立通过"的完整口径出题，覆盖所有已知追问路径。

## 来源与置信度

- https://leetcode.com/discuss/interview-question/424385/snowflake-phone-screen-patching-array/
  — 2019 phone screen 逐字引用："He told me I would get a bonus point if I could do it in
  constant space"；Q2 = LeetCode "Binary Tree Inorder Traversal"。
- https://leetcode.com/problems/binary-tree-inorder-traversal/ — LC 94 原题；2023 Canada 题库
  索引 #20 复用同一题，MEDIUM-HIGH confidence。

## 考什么

skills: **S08** LC 原题 + 复杂度再压一档（Morris、Floyd、O(m·n)）· S04 树的递归/迭代/O(1) 空间
三种遍历范式互换 · S09 精确格式化输出（stdin/stdout 单行 CSV 协议）。
