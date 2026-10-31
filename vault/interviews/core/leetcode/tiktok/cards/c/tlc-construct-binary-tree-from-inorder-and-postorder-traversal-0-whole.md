---
id: tlc-construct-binary-tree-from-inorder-and-postorder-traversal-0-whole
node: c.construct-binary-tree-from-inorder-and-postorder-traversal
type: qa
---
## Q
**LC 106 从中序与后序遍历序列构造二叉树**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 5 次 · 最近 2023-08-27（国内 CodeTop）

给定同一棵二叉树的中序遍历 `inorder` 和后序遍历 `postorder`，构造并返回这棵二叉树。`1 <= inorder.length <= 3000`，`postorder.length == inorder.length`，`-3000 <= inorder[i], postorder[i] <= 3000`，两个数组都由不同的值组成，`postorder` 中每个值都在 `inorder` 中。例：`inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]` → `[3,9,20,null,null,15,7]`；`inorder = [-1], postorder = [-1]` → `[-1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 后序的最后一个是根，在中序里找到它，左边是左子树、右边是右子树；递归构造，用哈希表直接查根在中序中的位置，并且后序从后往前读时要先建右子树。

**识别。** 「由两种遍历序列还原树」：先序 / 后序提供根，中序提供左右划分；元素互不相同，位置才唯一。

**推导。** 暴力：每层用 `index` 线性查根、切片拷贝数组，`O(n^2)`。洞察：只需要中序区间 `[lo, hi)` 而不用切片；后序从末尾逐个弹出恰好是「根、右子树、左子树」的顺序，所以弹出根后先递归右、再递归左，后序就不用再传区间。

**简单解法。** 切片递归，用 `inorder.index` 线性查根。

```python
def build_tree_slicing(inorder: list[int], postorder: list[int]) -> TreeNode | None:
    if not postorder:
        return None
    root = TreeNode(postorder[-1])               # 后序最后一个是根
    mid = inorder.index(root.val)                # 线性查找根在中序里的位置：左边是左子树，右边是右子树
    root.left = build_tree_slicing(inorder[:mid], postorder[:mid])
    root.right = build_tree_slicing(inorder[mid + 1:], postorder[mid:-1])
    return root
```

每层线性查找加切片拷贝，最坏 `O(n^2)`；`n <= 3000` 完全够用，哈希表和区间下标是进一步优化。

最优解：

```python
def build_tree(inorder: list[int], postorder: list[int]) -> TreeNode | None:
    index = {v: i for i, v in enumerate(inorder)}    # 值 -> 中序下标，免去每次线性查找
    post = list(postorder)                           # 复制一份，因为下面要从末尾逐个取

    def build(lo: int, hi: int) -> TreeNode | None:  # 用中序区间 inorder[lo:hi] 构造子树
        if lo >= hi:
            return None
        root = TreeNode(post.pop())                  # 后序倒着读是「根、右、左」
        mid = index[root.val]
        root.right = build(mid + 1, hi)              # 必须先建右子树，再建左子树
        root.left = build(lo, mid)
        return root

    return build(0, len(inorder))
```

运行：示例一得到根 `3`，左孩子 `9`，右孩子 `20`（其左 `15`、右 `7`）；示例二得到单节点 `-1`；随机树还原后与原树逐节点一致。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（哈希表加递归栈，栈深为树高）。

**拓展优化。**
- 给先序和中序（LC 105）：先序从头读，顺序是「根、左、右」，所以先建左再建右。
- 左链这类退化树深度为 `n`，递归会很深：改成显式栈，一次遍历还原，不需要哈希表：

```python
def build_tree_iterative(inorder: list[int], postorder: list[int]) -> TreeNode | None:
    root = TreeNode(postorder[-1])
    stack = [root]                               # 当前还可能接收左孩子的祖先链
    i = len(inorder) - 1                         # 指向中序里「栈顶节点还没处理完」的位置
    for j in range(len(postorder) - 2, -1, -1):  # 后序倒着读：根、右、左
        node = TreeNode(postorder[j])
        parent = None
        while stack and stack[-1].val == inorder[i]:   # 栈顶在中序里已到头：说明 node 是它们的左子树
            parent = stack.pop()
            i -= 1
        if parent:
            parent.left = node                   # 弹出的最后一个节点收下左孩子
        else:
            stack[-1].right = node               # 没有弹出：node 是栈顶的右孩子
        stack.append(node)
    return root
```

**易错点。**
- 先建左子树再建右子树：后序倒着读是「根、右、左」，先建左会把右子树的根错当成左子树的根，示例一得到错误的树。
- 最坏深度：左链状树深度 `3000`，CPython 默认递归上限约 1000，会抛 `RecursionError`（上面的左链用例实测如此），需要 `sys.setrecursionlimit` 或改成迭代。
- 对 `postorder` 原地 `pop`：修改了调用者的数据，先复制一份。

**追问。**
- 想避开递归深度：上面的迭代版本，栈里保存「还能接右孩子的祖先链」。
- 先序 + 后序能否还原：不唯一（只有一个孩子时无法判断左右）；LC 889 要求结果任选其一。
- 值有重复：中序下标不唯一，需要额外信息（如节点编号）才能还原。

**同模式。** LC 105 从前序与中序遍历序列构造二叉树、LC 889 根据前序和后序遍历构造二叉树、LC 654 最大二叉树、LC 108 将有序数组转换为二叉搜索树、LC 449 序列化和反序列化二叉搜索树。
