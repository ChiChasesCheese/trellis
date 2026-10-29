---
id: tlc-construct-binary-tree-from-preorder-and-inorder-traversal-0-whole
node: a.construct-binary-tree-from-preorder-and-inorder-traversal
type: qa
---
## Q
**LC 105 从前序与中序遍历序列构造二叉树**｜Medium · LC TikTok 热度 62/100 · CodeTop 国内累计 62 次 · 最近 2026-06-29（CodeTop）

给两个整数数组 `preorder`（二叉树的前序遍历）和 `inorder`（同一棵树的中序遍历），构造这棵二叉树并返回根节点。`1 <= preorder.length <= 3000`，`inorder.length == preorder.length`，`-3000 <= preorder[i], inorder[i] <= 3000`，两个数组都**无重复元素**，且输入保证合法。例：`preorder = [3,9,20,15,7]`，`inorder = [9,3,15,20,7]` → `[3,9,20,null,null,15,7]`；`preorder = [-1]`，`inorder = [-1]` → `[-1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前序的第一个值是根；这个值在中序里把序列切成「左子树 | 根 | 右子树」两段；用哈希表 `值 → 中序下标` 在 `O(1)` 内定位根，用一个前序迭代器按「根、左、右」的顺序逐个消费，先建左子树再建右子树，整棵树 `O(n)` 还原。

**识别。** 「给两种遍历序列，还原树」是分治（divide and conquer）题：前序告诉你谁是根，中序告诉你左右子树各占哪一段。「无重复元素」是在暗示可以用值当键做哈希查找（有重复值时根的位置不唯一，题目就不成立）。`n = 3000` 时每层线性找根的 `O(n^2)` 能过，但哈希把它降到 `O(n)`，面试官期待后者。

**推导。** 暴力：每层递归取前序首元素当根，用 `inorder.index(root)` 线性找位置，再把两个数组切片复制给左右子树，时间和空间都是 `O(n^2)`。浪费有两处：根的位置每次重新找、数组每次重新复制。修正：先扫一遍中序建字典，之后找根 `O(1)`；递归参数改成中序区间 `[lo, hi)`，不复制数组。再看前序：根后面紧跟着整个左子树，再是整个右子树，所以不用算左子树有多大，只要保证「先建左、后建右」，前序迭代器逐个吐出的值恰好依次是各子树的根。

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    index = {v: i for i, v in enumerate(inorder)}   # 值 -> 中序下标
    pre = iter(preorder)                            # 前序序列只会被顺序消费一次

    def build(lo: int, hi: int) -> TreeNode | None:  # 还原中序区间 inorder[lo:hi]
        if lo == hi:
            return None
        val = next(pre)                              # 前序的下一个值就是这段的根
        mid = index[val]
        node = TreeNode(val)
        node.left = build(lo, mid)                   # 必须先建左再建右，顺序和前序一致
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder))
```

运行：示例 1 → `[3, 9, 20, None, None, 15, 7]`，示例 2 → `[-1]`；`preorder = [1,2]`、`inorder = [2,1]`（左链）→ `[1, 2]`；`inorder = [1,2]`（右链）→ `[1, None, 2]`。链状树深度 3000 时，默认递归上限（1000）会抛 `RecursionError`，`sys.setrecursionlimit(10000)` 后正常。

**复杂度。** 时间 `O(n)`：建字典一遍，每个节点创建一次、查字典一次；空间 `O(n)`：字典加递归栈（最坏链状 `O(n)` 深）。

**易错点。**
- 先建右子树会出错：右子树的根在前序里排在整个左子树之后。示例 1 先建右子树，迭代器被提前消费，最终抛 `StopIteration`。
- 用 `inorder.index(val)` 加切片，退化成 `O(n^2)`；先建字典。
- 链状树深度可达 3000，超过 Python 默认递归上限 1000：面试里说明这一点，并给出显式栈的迭代版本（见追问）。

**追问。**
- LC 106 由中序和后序构造：后序的最后一个是根，从后往前消费，所以要**先建右子树再建左子树**。
- 避免递归：用栈单趟扫描，前序的新值若前一个节点还没走到中序的“最左”就挂左边，否则弹栈找到挂右孩子的祖先；时间 `O(n)`，没有递归深度问题。
- 只给前序和后序（LC 889）不能唯一确定树；有重复值时中序也不能唯一定位根。

**同模式。** LC 106 中序加后序构造、LC 889 前序加后序构造、LC 1008 前序遍历构造二叉搜索树、LC 297 二叉树的序列化与反序列化。
