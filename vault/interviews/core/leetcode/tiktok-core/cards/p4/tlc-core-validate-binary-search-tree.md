---
id: tlc-core-validate-binary-search-tree
node: p4.validate-binary-search-tree
type: qa
---
## Q
**LC 98 验证二叉搜索树**｜Medium · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 46 次 · 最近 2026-07-03（美国面试记录） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

给二叉树的根结点 `root`，判断它是否是有效的二叉搜索树（BST）。有效的定义：结点的左子树只含**严格小于**当前结点的值；右子树只含**严格大于**当前结点的值；所有左、右子树自身也必须是 BST。树中结点数在 `[1, 10^4]`，`-2^31 <= Node.val <= 2^31 - 1`。例：`root = [2,1,3]` → `true`；`root = [5,1,4,null,null,3,6]` → `false`（根是 `5`，右子结点却是 `4`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** BST 的中序遍历（左、根、右）一定是严格递增序列，所以递归做一次中序遍历，随时和上一个访问的值比较，出现 `<=` 就失败。`O(n)` 时间，`O(h)` 空间，`h` 是树高。

**识别。** 「验证 BST」有两条等价的路：自顶向下给每个结点传一个开区间 `(lo, hi)`，或者利用「中序递增」这条性质。递归最直观；结点数到 `10^4`，退化成链的树深度就是 `10^4`，超过 Python 默认递归上限（约 `1000` 层），见易错点。值域正好是 `int32` 的全部范围，初始「上一个值」不能用 `-2^31` 当哨兵，要用 `None`。

**推导。** 暴力：对每个结点检查「左子树所有值 < 它，右子树所有值 > 它」，每个结点遍历一遍子树，最坏 `O(n^2)`。浪费：每个子树被反复遍历。常见的错误捷径是只比较结点和它的左右孩子，漏掉「整棵子树都要满足」的约束。洞察：BST 的定义等价于中序序列严格递增——左子树都比根小、右子树都比根大，递归展开后恰好是升序。于是一次中序遍历加一个 `prev` 就够了：每个结点只比较一次。

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    prev: int | None = None            # 中序序列里的前一个值

    def inorder(node: TreeNode | None) -> bool:   # 这棵子树的中序是否严格递增
        nonlocal prev
        if node is None:
            return True
        if not inorder(node.left):     # 左子树先走完；已经失败就一路返回
            return False
        if prev is not None and node.val <= prev:   # 中序必须严格递增
            return False
        prev = node.val
        return inorder(node.right)

    return inorder(root)
```

运行：`[2,1,3]` → `True`，`[5,1,4,null,null,3,6]` → `False`，`[1,1]` → `False`，单个结点 `[2147483647]` → `True`，`None` → `True`；`10^4` 个结点的右斜链（值 `0..9999`）→ `True`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个结点访问一次；空间 `O(h)`：递归栈最深是树高，链状树为 `O(n)`。

**易错点。**
- 只比较结点和它的孩子：`[5,4,6,null,null,3,7]` 里每个结点都比自己的左孩子大、比右孩子小，会误判 `True`；正确答案 `False`，因为 `3` 在根 `5` 的右子树里却小于 `5`。
- 用 `<` 而不是 `<=` 判失败：`[1,1]` 里两个 `1` 相等，题目要求严格小于 / 严格大于，应当是 `False`。
- 递归深度：`10^4` 个结点的右斜链，递归深度 `10^4`，超过 CPython 默认递归上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）。
- 用 `-2^31` 当 `prev` 初值：结点值恰好是 `-2^31` 的树 `[-2147483648]` 会被 `val <= prev` 误判成 `False`，正确是 `True`。用 `None`（或 `-inf`）。

**追问。**
- 自顶向下传区间的写法（`lo < val < hi`，往左收紧上界、往右收紧下界），也是递归：
```python
from math import inf


def is_valid_bst_bounds(root: TreeNode | None) -> bool:
    def check(node: TreeNode | None, lo: float, hi: float) -> bool:
        if node is None:
            return True
        return (lo < node.val < hi                       # 落在祖先们划出的开区间里
                and check(node.left, lo, node.val)       # 左子树必须 < 当前值
                and check(node.right, node.val, hi))     # 右子树必须 > 当前值

    return check(root, -inf, inf)
```
- 不想动递归上限：迭代中序，一路向左压栈，弹出时和 `prev` 比较：
```python
def is_valid_bst(root: TreeNode | None) -> bool:
    stack: list[TreeNode] = []
    prev: int | None = None            # 中序序列里的前一个值
    node = root
    while stack or node:
        while node:                    # 一路向左压栈
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and node.val <= prev:   # 中序必须严格递增
            return False
        prev = node.val
        node = node.right
    return True
```
- 允许重复值（比如左子树 `<=` 当前）：只改比较符号，要先问清楚重复值放哪一边。
- 恢复被交换了两个结点的 BST（LC 99）：同样的中序，记录两处逆序。

**同模式。** LC 230 BST 中第 K 小的元素、LC 99 恢复二叉搜索树、LC 501 BST 中的众数、LC 530 BST 的最小绝对差、LC 94 二叉树的中序遍历。
