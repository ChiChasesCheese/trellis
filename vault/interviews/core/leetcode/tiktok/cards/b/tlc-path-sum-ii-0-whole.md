---
id: tlc-path-sum-ii-0-whole
node: b.path-sum-ii
type: qa
---
## Q
**LC 113 路径总和 II**｜Medium · CodeTop 国内累计 42 次 · 最近 2026-07-24（国内 CodeTop）

给二叉树的根节点 `root` 和整数 `targetSum`，找出所有**从根节点到叶子节点**、路径上节点值之和等于 `targetSum` 的路径（叶子是没有子节点的节点），每条路径以节点值列表的形式返回。树中节点数在 `[0, 5000]`，`-1000 <= Node.val <= 1000`，`-1000 <= targetSum <= 1000`。例：`root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22` → `[[5,4,11,2],[5,8,4,5]]`；`root = [1,2,3], targetSum = 5` → `[]`；`root = [1,2], targetSum = 0` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 深度优先搜索（DFS）从根往下走，沿途维护「还差多少」和一条共享的当前路径；走到叶子且恰好差 0 时，把当前路径拷贝一份放进答案；离开节点时把它从路径里弹出（回溯）。递归实现：进入节点 `append`、离开节点 `pop`，两步在同一个函数里自然成对。`O(n)` 遍历，加上每条命中路径的拷贝。

**识别。** 「根到叶的所有路径 + 满足条件」是 DFS 回溯的标志：要列出路径，就需要一条随进出节点增减的当前路径。「叶子」要求左右孩子都为空，不是「走到空节点」。节点值可以为负，所以不能因为「已超过目标」而剪枝。

**推导。** 暴力：先枚举所有根到叶路径，再对每条求和，`O(n·h)`。浪费：相邻路径共享前缀，前缀和可以一路带着。洞察：DFS 时带着 `rest = targetSum - 路径和`；共享一个 `path` 列表，进入节点 `append`，离开 `pop`；命中叶子时 `path[:]` 拷贝。写成递归 `dfs(node, rest)`：进入节点 `append`，递归左右孩子，离开节点 `pop`，回溯就是函数返回前的最后一行；命中叶子时 `path[:]` 拷贝。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []                          # 当前根到 node 的路径，所有层共享同一个列表

    def dfs(node: TreeNode | None, rest: int) -> None:
        if node is None:
            return
        path.append(node.val)                     # 进入节点
        rest -= node.val
        if node.left is None and node.right is None and rest == 0:
            res.append(path[:])                   # 只有叶子且恰好用完才收：拷贝一份，path 之后还会变
        dfs(node.left, rest)
        dfs(node.right, rest)
        path.pop()                                # 离开节点：回溯

    dfs(root, target_sum)
    return res
```

**运行。** 例 1 → `[[5, 4, 11, 2], [5, 8, 4, 5]]`；例 2 → `[]`；例 3 → `[]`；`None, 0` → `[]`；`[1], 1` → `[[1]]`；`[-2,null,-3], -5` → `[[-2, -3]]`；5000 个节点的左斜链（值全是 `1`）、目标 `5000`，调高递归上限后 → 一条长度 5000 的路径；默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n + k·h)`：遍历 `n` 个节点，每条命中路径拷贝 `O(h)`（`k` 条，`h` 为树高），最坏 `O(n·h)`；空间 `O(h)`（递归栈和 `path`，不含输出）。

**易错点。**
- 只判断 `rest == 0` 而不判叶子：`[1,2]`、目标 `1` 会在节点 `1` 处收下 `[1]`，正确答案是 `[]`。
- 收集时忘了拷贝：`res.append(path)` 之后 `path` 被回溯清空，答案变成一堆空列表。
- 离开节点时忘了 `path.pop()`：兄弟子树接着用被污染的路径，`[1,2,3]`、目标 `4` 会收下 `[1, 2, 3]`（和是 `6`），正确是 `[[1, 3]]`。
- 递归深度：链状树有 `5000` 层，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见追问）。
- 因为 `rest < 0` 就剪枝：节点值有负数，`[-2,null,-3]`、目标 `-5` 在根处就被剪掉，漏掉 `[-2, -3]`。

**追问。**
- 只问是否存在这样的路径（LC 112）：递归 `rest = target - root.val`，叶子处判断 `root.val == target`，左右用 `or` 短路，不需要 `path`。
- 路径不必从根开始、不必到叶子结束（LC 437）：用前缀和哈希表计数，沿 DFS 维护 `{前缀和: 出现次数}`，`O(n)`。
- 树很深、递归会超限：显式栈，栈里存 `(节点, 进入前还差多少)`；弹出节点时 `append` 并更新 `rest`，随后先压一个 `None` 退出标记，再压右、左孩子，孩子都处理完后弹到 `None`，把 `path` 的最后一个值 `pop`，回溯成对出现。

```python
def path_sum_iter(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    path: list[int] = []                          # 当前根到栈顶节点的路径，共享同一个列表
    stack: list[tuple[TreeNode | None, int]] = [(root, target_sum)]   # (节点, 进入前还差多少)；节点为 None 是"退出"标记
    while stack:
        node, rest = stack.pop()
        if node is None:                          # 子树处理完毕：回溯，把这个节点移出路径
            path.pop()
            continue
        path.append(node.val)
        rest -= node.val
        if node.left is None and node.right is None and rest == 0:
            res.append(path[:])                   # 只有叶子且恰好用完才收：拷贝一份，path 之后还会变
        stack.append((None, 0))                   # 先压退出标记，它会在两个孩子都处理完后才被弹出
        if node.right:
            stack.append((node.right, rest))
        if node.left:
            stack.append((node.left, rest))       # 后压的先弹：左子树先走，结果与递归写法同序
    return res
```

**同模式。** LC 112 路径总和、LC 257 二叉树的所有路径、LC 437 路径总和 III、LC 129 求根到叶子节点数字之和、LC 124 二叉树中的最大路径和。
