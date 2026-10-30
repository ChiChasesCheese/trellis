---
id: tlc-delete-node-in-a-bst-0-whole
node: p4.delete-node-in-a-bst
type: qa
---
## Q
**LC 450 删除二叉搜索树中的节点**｜Medium · LC 字节 热度 50/100 · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 5 次 · 最近 2026-03-11（国内 CodeTop）

给二叉搜索树（BST）的根节点 `root` 和一个值 `key`，删除 BST 中值为 `key` 的节点，并保证删除后仍是 BST。返回（可能更新后的）根节点。节点数在 `[0, 10^4]`，`-10^5 <= Node.val <= 10^5`，节点值唯一，`-10^5 <= key <= 10^5`。进阶：时间复杂度 `O(h)`，`h` 为树高。例：`root = [5,3,6,2,4,null,7], key = 3` → `[5,4,6,2,null,null,7]`（`[5,2,6,null,4,null,7]` 也正确）；`key = 0`（不存在）→ 原树不变；`root = [], key = 0` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归：`key` 比根小就去左子树删、比根大就去右子树删，每层用返回值把删完的子树接回来；命中后分情况——没有左孩子就返回右子树，没有右孩子就返回左子树，两个孩子就用**中序后继**（右子树里最小的节点）的值覆盖自己，再到右子树里删掉那个后继。`O(h)`。

**识别。** 「BST 的增删查」的核心是利用有序性每步丢掉一半（平衡时 `O(log n)`）；删除难在「删掉节点后留下的空位怎么补」。能顶替它的节点必须大于左子树所有节点、小于右子树所有节点：只有左子树最大（前驱）和右子树最小（后继）。「返回删除后的子树根」是递归的天然形状：每层让父节点用返回值重新接上，根被删时也不用特判。

**推导。** 暴力：中序遍历取出所有值，去掉 `key`，重新建树，`O(n)` → 观察：只有目标节点附近需要调整，沿一条路径往下 `O(h)` 即可找到 → 分情况：叶子直接删；一个孩子，孩子顶替；两个孩子，左右子树都要保留，选后继 `succ` 顶替（`succ` 在右子树的最左端），复制它的值到目标位置，再在右子树里删除原来的 `succ`；`succ` 没有左孩子，会落到「没有左孩子」的分支，一步结束。

```python
def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    if root is None:
        return None                            # 树里没有 key
    if key < root.val:
        root.left = delete_node(root.left, key)      # 目标在左子树：删完用返回值接回来
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right                  # 没有左孩子（含叶子）：右子树顶替自己
        if root.right is None:
            return root.left                   # 只有左孩子：左子树顶替自己
        succ = root.right                      # 两个孩子：用中序后继（右子树最小值）顶替
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)   # 再到右子树里删掉那个后继
    return root
```

运行：`[5,3,6,2,4,null,7]` 删 `3` → `[5,4,6,2,null,null,7]`，删 `0` → 不变，删 `5`（根，有两个孩子）→ `[6,3,7,2,4]`；`[]` 删 `0` → `[]`；`[1]` 删 `1` → `[]`；值为 `1` 到 `10^4` 的右斜链依次删 `5000` 和 `10000`，调高递归上限后 → 剩 `9998` 个节点；默认上限下删 `10000` 抛 `RecursionError`。

**复杂度。** 时间 `O(h)`（找目标 + 找后继，各一条路径）；空间 `O(h)`（递归栈）。

**易错点。**
- 目标有两个孩子时，直接返回右孩子，丢掉了左子树。`[5,3,6,2,4,null,7]` 删 `3`，中序遍历变成 `[4,5,6,7]`（正确 `[2,4,5,6,7]`）。
- 忘了用返回值接回子树：只写 `delete_node(root.left, key)` 而不赋给 `root.left`，被删的节点还挂在父节点上，`[5,3,6,2,4,null,7]` 删 `3` 之后输出的树不变。
- 递归深度：树退化成链时有 `10^4` 层，CPython 默认递归上限约 `1000`，删链尾会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成迭代（见追问）。

**追问。**
- 树很深、递归会超限：迭代版先沿路径找到目标和它的父节点，两个孩子时找后继并转成删除后继，最后让孩子顶替；`O(h)` 时间、`O(1)` 空间。

```python
def delete_node_iter(root: TreeNode | None, key: int) -> TreeNode | None:
    parent, node = None, root
    while node and node.val != key:            # 先找到 key 所在的节点和它的父节点
        parent = node
        node = node.left if key < node.val else node.right
    if node is None:
        return root                            # 树里没有 key
    if node.left and node.right:               # 两个孩子：用中序后继（右子树最小值）顶替
        succ_parent, succ = node, node.right
        while succ.left:
            succ_parent, succ = succ, succ.left
        node.val = succ.val
        parent, node = succ_parent, succ       # 问题转成删除后继，它至多有一个右孩子
    child = node.left or node.right            # 至多一个孩子：让孩子顶替自己的位置
    if parent is None:
        return child                           # 删的是根
    if parent.left is node:
        parent.left = child
    else:
        parent.right = child
    return root
```

- 用前驱（左子树最大）替换也正确，只是结果的形状不同。
- 要求不复制值、只改指针（节点携带大对象）：把 `succ` 节点本身接到目标的位置，并处理好 `succ_parent` 对 `succ.right` 的接管。

**同模式。** LC 700 二叉搜索树中的搜索、LC 701 二叉搜索树中的插入操作、LC 669 修剪二叉搜索树、LC 98 验证二叉搜索树。
