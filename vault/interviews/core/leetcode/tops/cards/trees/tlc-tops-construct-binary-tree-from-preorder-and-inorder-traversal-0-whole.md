---
id: tlc-tops-construct-binary-tree-from-preorder-and-inorder-traversal-0-whole
node: trees.construct-binary-tree-from-preorder-and-inorder-traversal
type: qa
---
## Q
**LC 105 从前序与中序遍历序列构造二叉树**｜Medium · 全公司热度第 258 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给定两个整数数组 `preorder` 和 `inorder`，其中 `preorder` 是二叉树的先序遍历，`inorder` 是同一棵树的中序遍历，请构造二叉树并返回其根节点。`1 <= preorder.length <= 3000`，`inorder.length == preorder.length`，`-3000 <= preorder[i], inorder[i] <= 3000`，两个数组都**无重复**元素，`inorder` 的元素都出现在 `preorder` 中，且两者都保证是同一棵二叉树的遍历序列。例：`preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]` → `[3,9,20,null,null,15,7]`；`preorder = [-1], inorder = [-1]` → `[-1]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 分治建树 + 哈希表：先序给出根，中序切分左右子树。

**一句话。** 先序的第一个元素是根；它在中序里的位置把中序切成「左子树 | 根 | 右子树」，先序紧接着的是左子树的先序，再是右子树的先序。

**识别。** 给两种遍历序列还原树：先序/后序告诉你「谁是根」，中序告诉你「左右各有多少个」，二者缺一不可。「无重复元素」是能用哈希表定位根的前提。`n <= 3000`，要避免每次在中序里线性查找（`O(n^2)`）。

**推导。** 取先序第一个值 `v` 作根，在中序里 `index(v)` 找到分界，左边 `k` 个是左子树，右边是右子树；再对两半递归。每次线性找 `v` 总共 `O(n^2)`；建 `值 -> 中序下标` 的哈希表后查找 `O(1)`。先序数组不再切片：先序的访问顺序恰好是「根、整个左子树、整个右子树」，所以只要按这个顺序递归，用一个迭代器逐个取下一个值即可，中序只需要用区间 `[lo, hi)` 表示当前子树的范围。

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    pos = {v: i for i, v in enumerate(inorder)}    # 值 -> 中序下标，O(1) 定位分界
    pre = iter(preorder)                           # 先序按「根、左、右」被依次消费

    def build(lo: int, hi: int) -> TreeNode | None:  # 当前子树对应 inorder[lo:hi]
        if lo >= hi:
            return None                            # 区间为空：没有这棵子树，也不消费先序
        val = next(pre)                            # 先序的下一个值就是这棵子树的根
        mid = pos[val]
        node = TreeNode(val)
        node.left = build(lo, mid)                 # 必须先建左再建右：先序里左子树排在前面
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder))
```

运行：`[3,9,20,15,7]` 与 `[9,3,15,20,7]` → `[3,9,20,null,null,15,7]`；`[-1]` 与 `[-1]` → `[-1]`；`[1,2,3]` 与 `[3,2,1]` → `[1,2,null,3]`；`[1,2,3]` 与 `[1,2,3]` → `[1,null,2,null,3]`。

**复杂度。** 时间 `O(n)`：建表 `O(n)`，每个节点建一次；空间 `O(n)`：哈希表加递归栈（最坏 `O(n)`）。

**拓展优化。**
- 同一个骨架解 LC 106（中序 + 后序）：后序的最后一个是根，从后往前消费，所以要**先建右子树再建左子树**。
- 递归深度：见易错点；极端链状输入要把 `build` 改成显式栈。

**易错点。**
- 先建右子树再建左子树：迭代器按先序消费，顺序反了就把左子树的值分给了右边。示例 1 中根 `3` 之后的 `9` 被当成右子树的根，迭代器很快用尽，抛 `StopIteration`。
- 每次用 `inorder.index(val)` 查找、再用切片 `inorder[:k]` 递归：每层复制和查找 `O(n)`，总 `O(n^2)`。
- 先序是 `[1,2,3,...,3000]`、中序是 `[1,2,3,...,3000]` 的单链：递归深度 `3000`，超过 CPython 默认上限约 `1000`，会抛 `RecursionError`；`sys.setrecursionlimit` 调高即可。

**同模式。** LC 106 从中序与后序遍历序列构造二叉树、LC 889 根据前序和后序遍历构造二叉树、LC 108 将有序数组转换为二叉搜索树、LC 297 二叉树的序列化与反序列化。
