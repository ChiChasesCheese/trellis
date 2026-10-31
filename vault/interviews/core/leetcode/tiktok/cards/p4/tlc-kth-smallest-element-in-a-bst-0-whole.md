---
id: tlc-kth-smallest-element-in-a-bst-0-whole
node: p4.kth-smallest-element-in-a-bst
type: qa
---
## Q
**LC 230 二叉搜索树中第 K 小的元素**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 23 次 · 最近 2024-04-10（国内 CodeTop）

给二叉搜索树的根节点 `root` 和整数 `k`，返回树中第 `k` 小的元素（`k` 从 `1` 开始）。节点数 `n`，`1 <= k <= n <= 10^4`，`0 <= Node.val <= 10^4`。例：`root = [3,1,4,null,2]`、`k = 1` → `1`；`root = [5,3,6,2,4,null,null,1]`、`k = 3` → `3`。进阶：树经常被修改（插入 / 删除）且要频繁查第 `k` 小，怎么优化？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 二叉搜索树（BST）的中序遍历是升序，所以做递归中序遍历（左、根、右），用计数器数到第 `k` 个节点立刻返回；不用遍历整棵树。`O(h + k)`。

**识别。** 「BST + 第 k 小 / 有序」直接对应中序遍历：左子树的所有值 < 根 < 右子树的所有值，中序「左、根、右」正好按升序吐出节点。`n` 到 `10^4`，退化成链时深度 `10^4`，超过 CPython 默认递归上限约 `1000`，见易错点和追问。

**推导。** 暴力：遍历整棵树收集全部值，排序后取第 `k - 1` 位，`O(n log n)` → 浪费：BST 已经按结构排好序，排序是白做；而且 `k` 小的时候没必要读完整棵树 → 先中序收集到列表再取下标，`O(n)` → 再改成边走边数，数到第 `k` 个就一路返回，`O(h + k)` → 进阶：频繁修改又频繁查询时，每个节点多存一个「子树大小」，查询时按大小逐层向下，`O(h)`。

```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    def dfs(node: TreeNode | None) -> int | None:
        nonlocal k
        if node is None:
            return None
        if (found := dfs(node.left)) is not None:   # 左子树里已经数到第 k 个：一路返回，不再往下走
            return found
        k -= 1                                      # 递归返回的顺序就是升序：数当前节点
        if k == 0:
            return node.val
        return dfs(node.right)

    result = dfs(root)
    if result is None:
        raise ValueError("k 超过节点数")
    return result
```

运行：`[3,1,4,null,2]`、`k=1` → `1`；`[5,3,6,2,4,null,null,1]`、`k=3` → `3`；`10^4` 个节点的右链（值 `0` 到 `9999`），调高递归上限后 `k=10000` → `9999`（链上的最大值），`k=1` → `0`；`10^4` 个节点的左链（值递减），`k=1` 在默认递归上限下抛 `RecursionError`。

**复杂度。** 时间 `O(h + k)`：先下到最左要 `h` 步，之后每弹出一个节点摊销 `O(1)`；空间 `O(h)`，递归栈里最多一条路径。

**易错点。**
- 在进入节点时就计数、再去左子树：数成了「先序」位置，`[5,3,6,2,4,null,null,1]`、`k=3` 得到 `2`，正确是 `3`；计数必须放在 `dfs(node.left)` 返回之后。
- 左子树的返回值没有往上传：`dfs(node.left)` 找到答案后调用者不接，就会继续往右数，`k` 变成负数，最后返回 `None` 或错值；找到就立刻 `return`。
- 递归深度：链状 BST 有 `10^4` 层，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见追问）。

**追问。**
- 树很深、递归会超限：迭代中序，一路向左把节点压栈，弹出的顺序就是升序，减到 `0` 就返回；`O(h + k)` 时间，栈里最多一条路径。

```python
def kth_smallest_iter(root: TreeNode | None, k: int) -> int:
    stack: list[TreeNode] = []
    node = root
    while stack or node:
        while node:                    # 一路向左，沿途入栈
            stack.append(node)
            node = node.left
        node = stack.pop()             # 弹出的顺序就是升序
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    raise ValueError("k 超过节点数")
```

- 频繁修改 + 频繁查询：每个节点维护子树大小 `size`，查询时左子树大小 `>= k` 去左边，`== k - 1` 就是当前，否则 `k -= 左 + 1` 去右边，`O(h)`；插入 / 删除沿路径更新 `size`。
- 第 `k` 大：镜像遍历（右、根、左），或者用 `n - k + 1`。
- 多次查询、树不变：中序一次存数组，之后每次 `O(1)`；或者用 BST 迭代器（LC 173）按需产出。

**同模式。** LC 98 验证二叉搜索树、LC 173 二叉搜索树迭代器、LC 94 二叉树的中序遍历、LC 538 把二叉搜索树转换为累加树。
