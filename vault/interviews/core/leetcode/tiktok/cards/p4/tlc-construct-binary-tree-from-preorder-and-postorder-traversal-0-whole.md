---
id: tlc-construct-binary-tree-from-preorder-and-postorder-traversal-0-whole
node: p4.construct-binary-tree-from-preorder-and-postorder-traversal
type: qa
---
## Q
**LC 889 从前序与后序遍历序列构造二叉树**｜Medium · 近一年被问：美国 1 次、国内 0 次 · CodeTop 国内累计 6 次 · 最近 2026-08-24（面试记录）

给两个整数数组 `preorder` 和 `postorder`，`preorder` 是一棵**无重复值**二叉树的前序遍历，`postorder` 是同一棵树的后序遍历，重构并返回这棵二叉树；如果有多个答案，返回任意一个。`1 <= preorder.length <= 30`，`1 <= preorder[i] <= preorder.length`，`preorder` 中所有值不同，`postorder.length == preorder.length`，`1 <= postorder[i] <= postorder.length`，`postorder` 中所有值不同，保证两者是同一棵二叉树的前序和后序。例：`preorder = [1,2,4,5,3,6,7]`，`postorder = [4,5,2,6,7,3,1]` → `[1,2,3,4,5,6,7]`；`[1]`、`[1]` → `[1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前序的第一个元素是根，第二个元素是左子树的根；后序里左子树根恰好是左子树的最后一个元素，所以它在后序中的下标告诉我们左子树有多少个结点，据此把两个数组各切成「左 / 右」两段递归。用哈希表把「值 → 后序下标」预存，每层 `O(1)`，总 `O(n)`。

**识别。** 「由两种遍历序列还原二叉树」是固定题型：前序/后序的首尾给根，**中序**才能切出左右（LC 105 / 106）；这里没有中序，只能借「前序第二个元素 = 左子树根」和「后序里左子树根的位置 = 左子树大小」来切。值互不相同才能用哈希表定位。

**推导。** 暴力：每层在 `postorder` 里用 `list.index` 查位置、切片复制两个数组，`O(n^2)` 时间；`n <= 30` 能过，但面试要说清怎么优化。浪费在重复查找和复制：位置查找换成预建的 `post_idx` 字典，切片换成「起点 + 长度」三个整数，递归只传下标。注意有一个歧义：若一个结点只有一个孩子，前序后序都分不清它是左还是右，所以答案不唯一；约定它是**左孩子**（即 `size > 1` 时恒认为 `preorder[pre_lo+1]` 是左子树根）就得到合法的一棵。

```python
def construct_from_pre_post(preorder: list[int], postorder: list[int]) -> TreeNode | None:
    post_idx = {v: i for i, v in enumerate(postorder)}   # 值 -> 它在后序里的下标，O(1) 查左子树大小

    def build(pre_lo: int, post_lo: int, size: int) -> TreeNode | None:
        if size == 0:
            return None
        root = TreeNode(preorder[pre_lo])
        if size == 1:
            return root
        left_root = preorder[pre_lo + 1]                 # 前序里根后面紧跟的是左子树的根
        left_size = post_idx[left_root] - post_lo + 1    # 后序里左子树根是左子树的最后一个
        root.left = build(pre_lo + 1, post_lo, left_size)
        root.right = build(pre_lo + 1 + left_size, post_lo + left_size, size - 1 - left_size)
        return root

    return build(0, 0, len(preorder))
```

运行：示例 1 → 层序 `[1,2,3,4,5,6,7]`；`[1]`、`[1]` → `[1]`；`[1,2]`、`[2,1]` → `[1,2]`（2 作为左孩子）；`[1,2,3]`、`[3,2,1]` → `[1,2,null,3]`（链）。重建后的树的前序和后序都与输入相同。

**复杂度。** 时间 `O(n)`：每个结点建一次，每次 `O(1)`；空间 `O(n)`：`post_idx` 字典加递归栈（最坏一条链，深度 `n`，这里 `n <= 30`）。

**易错点。**
- `left_size` 要 `+ 1`：`post_idx[left_root] - post_lo` 是左子树根的下标偏移，大小是偏移加一。漏掉 `+ 1` 时示例 1 构出的树前序对、后序变成 `[4,2,6,7,3,5,1]`，与输入不符。
- `size == 1` 必须单独返回，否则 `preorder[pre_lo + 1]` 越界或错读到右兄弟的子树。
- 不要以为答案唯一：`[1,2]` / `[2,1]` 既可以是左孩子也可以是右孩子，任意一个都被接受。

**追问。**
- 为什么两种遍历不能唯一确定树：只有单孩子的结点有歧义，合法的树共 `2^k` 棵（`k` 是单孩子结点数）。
- 能不能 `O(n)` 且不用字典：用一个栈同时扫两个序列，后序指针与栈顶相等时弹栈，是常见的迭代写法。
- 前序 + 中序 / 中序 + 后序（LC 105 / 106）：切分依据换成中序里根的位置，同样用 `值 → 下标` 字典。

**同模式。** LC 105 前序与中序构造二叉树、LC 106 中序与后序构造二叉树、LC 1008 前序遍历构造二叉搜索树、LC 297 二叉树的序列化与反序列化。
