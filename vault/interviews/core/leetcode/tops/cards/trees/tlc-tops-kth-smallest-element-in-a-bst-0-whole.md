---
id: tlc-tops-kth-smallest-element-in-a-bst-0-whole
node: trees.kth-smallest-element-in-a-bst
type: qa
---
## Q
**LC 230 二叉搜索树中第 K 小的元素**｜Medium · 全公司热度第 235 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给定一个二叉搜索树的根节点 `root`，和一个整数 `k`，请你设计一个算法查找其中第 `k` 小的元素（`k` 从 1 开始计数）。树中的节点数为 `n`，`1 <= k <= n <= 10^4`，`0 <= Node.val <= 10^4`。进阶：如果二叉搜索树经常被修改（插入/删除操作）并且你需要频繁地查找第 `k` 小的值，你将如何优化算法？

例：`root = [3,1,4,null,2]`，`k = 1` → `1`；`root = [5,3,6,2,4,null,null,1]`，`k = 3` → `3`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** BST 的中序遍历（in-order）按升序访问；递归中提前返回（early exit）。

**一句话。** 对 BST 做中序遍历，第 `k` 个被访问的结点就是第 `k` 小，数到 `k` 立刻返回，不再遍历后面。

**识别。** 「BST + 第 k 小/大/有序」就是中序遍历。`n <= 10^4`，线性即可。

**推导。** 把所有值收集起来排序是 `O(n log n)`，没用上 BST。BST 的中序序列天然升序，所以不用排序；而且只需要前 `k` 个，找到就停，时间 `O(h + k)`。实现上让递归函数返回「找到的值或 `None`」，左子树找到就一路原样返回，没找到就在当前结点计数。

```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    def inorder(node: TreeNode | None) -> int | None:
        nonlocal k
        if not node:
            return None
        found = inorder(node.left)      # 左子树里先数；找到了就一路返回
        if found is not None:
            return found
        k -= 1                          # 当前结点是中序里的下一个
        if k == 0:
            return node.val
        return inorder(node.right)

    return inorder(root)
```

**运行。** `[3,1,4,null,2]`、`k = 1` → `1`；`[5,3,6,2,4,null,null,1]`、`k = 3` → `3`；`k = 6` → `6`；`[1]`、`k = 1` → `1`。

**复杂度。** 时间 `O(h + k)`，最坏 `O(n)`；空间 `O(h)`。

**拓展优化。**
- 进阶（频繁修改 + 频繁查询）：在每个结点上维护「以它为根的子树结点数」`size`，查询时看左子树大小 `left`：`k <= left` 去左边，`k == left + 1` 就是当前结点，否则去右边找第 `k - left - 1` 小，单次 `O(h)`；插入/删除时沿路径更新 `size`。再配平衡树（AVL、红黑树）把 `h` 控制在 `log n`。
```python
def kth_by_size(node: TreeNode, k: int, size: dict[TreeNode, int]) -> int:
    left = size.get(node.left, 0)           # 左子树结点数，空树为 0
    if k <= left:
        return kth_by_size(node.left, k, size)
    if k == left + 1:
        return node.val
    return kth_by_size(node.right, k - left - 1, size)
```
- 不用递归：显式栈的中序遍历，一路压左链，弹出第 `k` 个。

**易错点。**
- 用先序遍历：例 2 先序是 `5, 3, 2, 1, 4, 6`，第 3 个是 `2`，正确答案是 `3`。BST 只有中序有序。
- 找到后不返回、继续遍历并覆盖答案：最后得到的是最后访问的值，而不是第 `k` 个。
- 递归深度等于树高：`n = 10^4` 的单链 BST 深度超过 CPython 默认约 1000 的递归上限，抛 `RecursionError`；此时用显式栈的迭代中序。

**同模式。** LC 98 验证二叉搜索树、LC 94 二叉树的中序遍历、LC 530 二叉搜索树的最小绝对差、LC 215 数组中的第 K 个最大元素。
