---
id: tlc-minimum-distance-between-bst-nodes-0-whole
node: a.minimum-distance-between-bst-nodes
type: qa
---
## Q
**LC 783 二叉搜索树节点最小距离**｜Easy · CodeTop 国内累计 2 次 · 最近 2026-05-26（CodeTop）

给二叉搜索树（BST）的根节点 `root`，返回树中任意两个不同节点值之差的最小值（差取绝对值，是正数）。节点数在 `[2, 100]`，`0 <= Node.val <= 10^5`。例：`root = [4,2,6,1,3]` → `1`，`root = [1,0,48,null,null,12,49]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** BST 的中序遍历（inorder traversal）是升序序列，最小差一定出现在序列中**相邻**的两个值之间；中序遍历时记住上一个值，边走边更新答案。`O(n)`。

**识别。** 「BST + 任意两节点的最小差」：BST 的核心性质是中序有序，「任意两数最小差」在有序序列里只需看相邻对。树不保证平衡，但 `n <= 100`，递归深度不是问题。

**推导。** 暴力：取出所有值两两比较，`O(n^2)` → 改进：取出后排序再比相邻，`O(n log n)`，但没用上 BST 的结构 → BST 的中序遍历本身就按升序产出值，省掉排序 → 不存数组，只记前一个值 `prev`，`O(n)` 时间、`O(h)` 空间（`h` 为树高）。

```python
from math import inf


def min_diff_in_bst(root: TreeNode | None) -> int:
    best = inf
    prev: int | None = None              # 中序遍历中上一个节点的值

    def inorder(node: TreeNode | None) -> None:
        nonlocal best, prev
        if node is None:
            return
        inorder(node.left)
        if prev is not None:             # 中序是升序：只需和前一个值比
            best = min(best, node.val - prev)
        prev = node.val
        inorder(node.right)

    inorder(root)
    return best
```

运行：`[4,2,6,1,3]` → `1`，`[1,0,48,null,null,12,49]` → `1`，`[5,1,null,null,4]` → `1`，`[0,null,100000]` → `100000`。

**复杂度。** 时间 `O(n)`，每个节点访问一次；空间 `O(h)`，递归栈深度等于树高，最坏退化成链时 `O(n)`。

**易错点。**
- 只比较父子节点：最小差可能出现在隔代节点之间。`[5,1,null,null,4]`（`4` 是 `1` 的右孩子）中父子差是 `4` 和 `3`，会错成 `3`；正确是 `5 - 4 = 1`。
- 把 `prev` 初始化成 `0`：第一个节点也会和 `0` 比。`[1,null,10]` 会错成 `1`，正确是 `9`。用 `None` 表示「还没有前一个」。

**追问。**
- 不用递归：用栈模拟中序，一路压左孩子、弹出访问、转向右孩子。
- 如果不是 BST：只能取出所有值排序后比相邻，`O(n log n)`。
- `O(1)` 额外空间：Morris 中序遍历，借用空的右指针临时连回后继，遍历完恢复。

**同模式。** LC 530 二叉搜索树的最小绝对差（同一题）、LC 98 验证二叉搜索树、LC 230 二叉搜索树中第 K 小的元素、LC 501 二叉搜索树中的众数。
