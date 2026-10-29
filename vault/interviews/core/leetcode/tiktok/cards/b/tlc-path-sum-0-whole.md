---
id: tlc-path-sum-0-whole
node: b.path-sum
type: qa
---
## Q
**LC 112 路径总和**｜Easy · CodeTop 国内累计 47 次 · 最近 2026-04-14（CodeTop）

给二叉树的根结点 `root` 和整数 `targetSum`，判断树中是否存在**根结点到叶子结点**的路径，使路径上所有结点值之和等于 `targetSum`。叶子结点是没有子结点的结点。

约束：结点数在 `[0, 5000]`，`-1000 <= Node.val <= 1000`，`-1000 <= targetSum <= 1000`。

例：`root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22` → `true`（`5→4→11→2`）；`root = [1,2,3], targetSum = 5` → `false`（两条路径和分别为 `3` 和 `4`）；`root = [], targetSum = 0` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 从根往下 DFS，同时携带「还差多少」`remain = target - 路径和`：走到一个结点就减去它的值；只有在**叶子**结点上并且 `remain == 0` 才算找到。树最深可以到 `5000` 层，所以用显式栈。`O(n)`。

**识别。** 「根到叶子的路径」「路径和等于目标」是树上 DFS 的基础题：把「累计和」变成「剩余量」随着递归向下传递，叶子处判断。关键词：**叶子**（不是任何结点）、**空树返回 false**、值可以为负（不能剪枝）。结点数 `5000` 允许 `O(n)`，但链状树会让递归深度到 `5000`，超过 Python 默认递归上限。

**推导。** 暴力：枚举所有根到叶子的路径，分别求和比较，`O(n·h)`（每条路径单独求和，重叠部分重复）。改进：沿路径向下携带累计量，每个结点只做一次加减，`O(n)`。把「累计和 == target」转写成「剩余量 == 0」，叶子处只需要看 `remain`。实现上，递归写法最短，但退化成链的树（`5000` 层）会 `RecursionError`；所以用显式栈保存 `(结点, 剩余量)`，先压右再压左或反之都可以。判断条件必须同时满足「是叶子」和「剩余量为 0」。

```python
def has_path_sum(root: TreeNode | None, target_sum: int) -> bool:
    if root is None:
        return False                   # 空树没有任何根到叶子的路径
    stack = [(root, target_sum - root.val)]   # (结点, 走到这里后还差多少)
    while stack:                       # 迭代 DFS：树可以退化成 5000 层的链，递归会爆栈
        node, remain = stack.pop()
        if node.left is None and node.right is None and remain == 0:
            return True                # 必须是叶子，并且恰好凑够
        for child in (node.right, node.left):
            if child:
                stack.append((child, remain - child.val))
    return False
```

运行：`root=[5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum=22` → `True`，`root=[1,2,3], targetSum=5` → `False`，`root=[], targetSum=0` → `False`，`root=[1,2], targetSum=1（根不是叶子）` → `False`，`root=[-2,null,-3], targetSum=-5（负数）` → `True`，`5000 个结点的单链，值全为 1，targetSum=5000` → `True`。

**复杂度。** 时间 `O(n)`：每个结点最多入栈、出栈一次；空间 `O(h)`：栈里最多存一条根到叶的链上的待探索结点，平衡树 `O(log n)`，退化成链 `O(n)`。

**易错点。**
- 不检查叶子，任意结点凑够即返回：`root=[1,2]`, `targetSum=1`，根结点值为 `1` 就返回 `true`，但根有孩子，不是叶子，正确答案是 `false`。
- 值可以为负却用 `remain < 0` 剪枝：`root=[-2,null,-3]`, `targetSum=-5`，根处 `remain = -3 < 0` 被剪掉，得 `false`；正确答案是 `true`（`-2 + -3`）。
- 空树返回 `true`：题目示例 3 明确 `[]`, `0` → `false`，因为没有任何根到叶子的路径。
- 递归深度：`5000` 个结点的单链用递归会 `RecursionError`；用显式栈，或明确说明树高假设。

**追问。**
- 返回所有满足条件的路径（LC 113）：DFS 时维护 `path` 列表，到叶子且 `remain == 0` 时拷贝一份加入答案；回溯要在返回时弹出。
- 路径不必从根开始、不必到叶子结束（LC 437）：换成前缀和哈希表，见那一题。
- 改成 N 叉树 / 二叉搜索树：N 叉树把 `(left, right)` 换成 `children`；BST 有序性对此处没有额外帮助，因为路径和不单调。

**同模式。** LC 113 路径总和 II、LC 437 路径总和 III、LC 129 求根到叶子节点数字之和、LC 257 二叉树的所有路径、LC 124 二叉树中的最大路径和。
