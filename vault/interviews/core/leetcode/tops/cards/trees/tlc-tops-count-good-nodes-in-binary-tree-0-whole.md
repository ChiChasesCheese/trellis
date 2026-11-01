---
id: tlc-tops-count-good-nodes-in-binary-tree-0-whole
node: trees.count-good-nodes-in-binary-tree
type: qa
---
## Q
**LC 1448 统计二叉树中好节点的数目**｜Medium · 全公司热度第 724 名 · NeetCode 150、LeetCode 75

给你一棵根为 `root` 的二叉树，返回二叉树中**好节点**的数目。好节点 `X` 的定义：从根到 `X` 所经过的节点中，没有任何节点的值大于 `X` 的值（根节点永远是好节点）。节点数在 `[1, 10^5]`，节点值在 `[-10^4, 10^4]`。例：`root = [3,1,4,3,null,1,5]` → `4`；`root = [3,3,null,4,2]` → `3`；`root = [1]` → `1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 带参数的前序 DFS：自顶向下把「路径上的最大值」传给孩子。

**一句话。** 沿根到当前节点的路径带着当前最大值 `mx`；`node.val >= mx` 就是好节点，计 `1`，再用 `max(mx, node.val)` 更新后传给左右子树，累加两侧的计数。

**识别。** 判断某节点的性质依赖「祖先路径上的信息」（最大值、和、深度），用自顶向下传参的 DFS；对比 LC 104/543 那种自底向上返回的写法。`n <= 10^5`，`O(n)` 一次遍历。

**推导。** 对每个节点向上回溯到根找最大值，最坏 `O(n·h)`。路径最大值可以在向下走的过程中顺手维护：孩子的路径比父亲的路径只多一个节点，`mx` 随之只增不减，传一个整数即可，无需回溯。

```python
def good_nodes(root: TreeNode) -> int:
    def dfs(node: TreeNode | None, mx: int) -> int:   # mx：根到 node 父亲这条路径上的最大值
        if node is None:
            return 0
        good = 1 if node.val >= mx else 0          # 没有祖先比它大（相等也算好节点）
        mx = max(mx, node.val)                     # 往下传的是包含自己的最大值
        return good + dfs(node.left, mx) + dfs(node.right, mx)

    return dfs(root, root.val)                     # 根自己与自己比：永远是好节点
```

运行：`[3,1,4,3,null,1,5]` → `4`；`[3,3,null,4,2]` → `3`；`[1]` → `1`；`[2,1,null,0,null,-1]`（单调递减的链）→ `1`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，递归栈。

**拓展优化。**
- 深链输入改成显式栈，栈里放 `(节点, 路径最大值)`：
```python
def good_nodes_iter(root: TreeNode) -> int:
    count = 0
    stack = [(root, root.val)]
    while stack:
        node, mx = stack.pop()
        if node.val >= mx:
            count += 1
        mx = max(mx, node.val)
        for child in (node.left, node.right):
            if child:
                stack.append((child, mx))
    return count
```

**易错点。**
- 用 `>` 代替 `>=`：值与路径最大值相等的节点被漏掉。`[3,3,null,4,2]` 得 `2`，正确是 `3`（第二个 `3` 与根相等，也是好节点）。
- 初值取 `0` 而不是 `root.val`：节点值可以为负，`[-1]` 得 `0`，正确是 `1`（根永远是好节点）。
- 链状树深度 `10^5` 远超 CPython 默认递归上限约 `1000`，会抛 `RecursionError`；需调高上限或用上面的迭代版。

**同模式。** LC 98 验证二叉搜索树（带上下界传参）、LC 112 路径总和、LC 1026 节点与其祖先之间的最大差值、LC 437 路径总和 III。
