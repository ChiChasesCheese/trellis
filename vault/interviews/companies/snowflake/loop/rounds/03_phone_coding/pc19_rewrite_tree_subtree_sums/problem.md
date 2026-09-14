# pc19 · Rewrite Tree With Subtree Sums — 完全二叉树数组反向扫描 → 一般二叉树迭代后序

> TrueInterview 87 题清单第 12 题，2026-06 报告。Part 1 的题干与 worked example 是一手预览原文；
> Part 2 **(reconstructed)**。

## 背景

TrueInterview（`kevin-2023-code/Tech-Interview-Questions`，见 `../../../catalog/raw/github_repos.md`
§2 第 12 行、§3）列出 Snowflake 一轮 Algorithm 题 "Rewrite Tree With Subtree Sums"：两棵**同形**完全
二叉树用层序数组表示，把 `root2` 的每个位置改写成 `root1` 对应子树的和；预览给出的例子
`[5,2,3,1,4,6,7] → [28,7,16,1,4,6,7]` 就是本题 Part 1 的第一个 worked example。

## 输入

Part 1：两个层序数组 `root1`、`root2`，代表**完全二叉树**（下标 `i` 的孩子是 `2i+1`、`2i+2`），
长度相同（"同形"）。
Part 2：一个可能有空洞、深度不受限（最深 1e5）的一般二叉树，用节点对象表示。

## API 契约（英文签名）

```python
def rewrite_subtree_sums(root1: list[int], root2: list[int]) -> list[int]
def rewrite_subtree_sums_tree(root1: "TreeNode | None") -> "TreeNode | None"
```
`TreeNode(val, left=None, right=None)`。Part 1 中 `len(root1) != len(root2)` → `ValueError`
（不是"同形"）。

## 规则

### Part 1 — 完全二叉树数组，反向扫描，O(1) 额外空间（不含输出数组）（一手原题）

"把 `root1` 每个节点的子树和写进 `root2` 对应位置"：**`root2` 原来的值完全不重要**（整道题就是要
覆盖它们），所以结果只是 `root1` 的函数；`root2` 只用来检查"同形"这个契约（长度必须相等）。完全二叉树
的数组表示有一个好性质：任意节点的孩子下标永远比它自己大，所以从下标 `n-1` 倒着扫到 `0`，扫到 `i`
时它的孩子（如果存在）已经算完子树和了——不需要递归，一次反向遍历就够。

### Part 2 — 一般二叉树、节点对象、必须迭代（不能递归） **(reconstructed)**

完全二叉树的数组表示在深度 1e5 时完全不可行（需要 `2^100000` 个格子），所以"深度 1e5"这个追问逼着你
换表示：用真正的节点对象 `TreeNode(val, left, right)`，允许任意空洞（`left`/`right` 可以是
`None`）。`rewrite_subtree_sums_tree(root1)` 返回一棵**新树**（不修改 `root1`），形状与 `root1`
完全相同，每个节点的值是 `root1` 里对应节点的子树和。**必须迭代**：先用显式栈做一次后序遍历（孩子先于
父节点处理）算出每个节点的子树和，再用同样的后序顺序（孩子已经在结果字典里）建出新树；两遍都不递归，
一条深度 1e5 的"退化成链表"的树也不会撞到 Python 的递归深度上限。

## Worked examples（全部由 `solution.py` 实际运行得出）

- `rewrite_subtree_sums([5, 2, 3, 1, 4, 6, 7], [0]*7)` = `[28, 7, 16, 1, 4, 6, 7]`
- `rewrite_subtree_sums([9], [0])` = `[9]`
- `rewrite_subtree_sums([], [])` = `[]`
- `rewrite_subtree_sums([-1, -2, 3], [0, 0, 0])` = `[0, -2, 3]`
- 节点树版本的同一棵树（前序带 `#` 序列化）：
  `5 2 1 # # 4 # # 3 6 # # 7 # #` → `28 7 1 # # 4 # # 16 6 # # 7 # #`
  （和 Part 1 的例子是同一棵树，验证两个 Part 的答案完全一致）

## `main()` 命令流

```
PART 1                               PART 2
5 2 3 1 4 6 7 | 0 0 0 0 0 0 0        5 2 1 # # 4 # # 3 6 # # 7 # #
→ 28 7 16 1 4 6 7                    → 28 7 1 # # 4 # # 16 6 # # 7 # #
```
Part 1 每行：`root1 的值 | root2 的值`（空格分隔）。Part 2 每行：LeetCode 风格的前序 token 流，
`#` 表示该位置没有孩子（不是"没有更多输入"），输出同样格式。

## 边界清单

- 空树 / 只有一个节点
- `root2` 的值应被完全忽略（覆盖前后的值不影响结果）
- 负数值（子树和可以是负数或零）
- Part 1：`root1`、`root2` 长度不同 → `ValueError`
- Part 2：只有左孩子的链、只有右孩子的链、左右孩子都缺的混合空洞形状
- Part 2：深度 1e5 的退化树（纯左链）不能触发 `RecursionError`，也要在时间预算内跑完

## 追问

1. **Part 1 为什么不用递归？** 完全二叉树数组本身已经保证"孩子下标 > 父节点下标"，用这个单调性反向
   扫描一遍就够，比写递归更省一次函数调用栈，也顺便回答了"如果这棵树深度很大怎么办"。
2. **Part 2 为什么不能直接沿用 Part 1 的数组表示，只是允许 `None` 占位？** 数组表示的下标运算
   `2i+1`/`2i+2` 隐含"这是一棵接近满的树"；一条深度 1e5 的纯链表形状的二叉树用这种数组要开
   `2^100000` 个格子，物理上不可行——这才是"换成节点对象"的根本原因，不只是为了绕开递归深度。
3. **一次遍历能不能同时算子树和、又建出新树？** 可以：本 solution 就是对同一份后序节点顺序跑两遍
   （第一遍只读值算和，第二遍只用第一遍算好的和建新节点），也可以把两件事合并到同一次后序遍历里；
   拆成两遍是为了让每一遍的职责更单一，容易验证。

## 来源与置信度

- **MED（聚合站，题面付费，仅预览可见）**：`kevin-2023-code/Tech-Interview-Questions`
  `companies/snowflake.md`，2026-06 报告，"Rewrite Tree With Subtree Sums"，Algorithm；题干与
  `[5,2,3,1,4,6,7] → [28,7,16,1,4,6,7]` 例子均为原文。见 `../../../catalog/raw/github_repos.md`
  §2 第 12 行、§3。
- Part 2（一般树 / 节点对象 / 深度 1e5 / 必须迭代）为重建。

## 考什么

S01 完全二叉树的数组编码与下标单调性 · S03 递归改迭代（显式栈，postorder）· 识别"数组表示在深度很大
时物理上不可行"、必须换成节点表示，而不是死磕原有表示法打补丁。
