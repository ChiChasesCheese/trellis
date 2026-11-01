---
id: tlc-tops-flatten-binary-tree-to-linked-list-0-whole
node: trees.flatten-binary-tree-to-linked-list
type: qa
---
## Q
**LC 114 二叉树展开为链表**｜Medium · 全公司热度第 545 名 · Hot 100、Top Interview 150

给你二叉树的根节点 `root`，将它展开为一个单链表：展开后的链表仍使用 `TreeNode`，其 `right` 指针指向链表中的下一个节点，`left` 指针始终为 `null`；链表的顺序与二叉树的**先序遍历**相同。节点数在 `[0, 2000]`，`-100 <= Node.val <= 100`。例：`root = [1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`；`root = []` → `[]`；`root = [0]` → `[0]`。进阶：你可以使用原地算法（`O(1)` 额外空间）展开这棵树吗？

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二叉树 DFS：逆先序（右、左、根）+ 前驱指针，原地改指针。

**一句话。** 先序是「根、左、右」，倒过来「右、左、根」访问，每访问一个节点，就把它的 `right` 接到刚访问过的节点（也就是先序里它的后继），`left` 置空。

**识别。** 「按先序展开成链表、原地」：先序的后继是「自己的左子树的第一个，否则右子树的第一个」。倒着访问，后继总是上一个访问的节点，一个变量 `prev` 就够。`n <= 2000`。

**推导。** 想要的链表就是先序遍历的节点顺序。若倒序处理，先把右子树、左子树都处理成「以各自先序开头为头」的链，当前节点的后继就是上一个处理的节点：`node.right = prev`。倒序保证改指针时，所依赖的子树还没有被破坏。

**简单解法。** 先序遍历把节点收集进列表，再按顺序把每个节点的 `left` 置空、`right` 指向下一个，需要 `O(n)` 额外空间。

```python
def flatten(root: TreeNode | None) -> None:
    nodes: list[TreeNode] = []

    def preorder(node: TreeNode | None) -> None:
        if node is None:
            return
        nodes.append(node)                         # 根、左、右
        preorder(node.left)
        preorder(node.right)

    preorder(root)
    for a, b in zip(nodes, nodes[1:]):
        a.left = None                              # 左指针置空
        a.right = b                                # 右指针指向先序里的下一个
    if nodes:
        nodes[-1].left = None
```

最优解（栈深度 `O(h)`，无需列表）：

```python
def flatten(root: TreeNode | None) -> None:
    prev: TreeNode | None = None                   # 上一个访问的节点，也就是当前节点在先序里的后继

    def dfs(node: TreeNode | None) -> None:
        nonlocal prev
        if node is None:
            return
        dfs(node.right)                            # 逆先序：右、左、根
        dfs(node.left)
        node.left = None
        node.right = prev                          # 后继接在右边；此时左右子树都已处理完，改指针安全
        prev = node

    dfs(root)
```

运行：`[1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`；`[]` → `[]`；`[0]` → `[0]`；`[1,null,2]` → `[1,null,2]`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，递归栈。

**拓展优化。**
- 进阶 `O(1)` 额外空间：对每个有左子树的节点，找到左子树最右的节点（它是先序里左子树的最后一个），把右子树接到它后面，再把左子树整体挪到右边。
```python
def flatten_o1(root: TreeNode | None) -> None:
    node = root
    while node:
        if node.left:
            pred = node.left
            while pred.right:                      # 左子树最右节点 = 左子树先序的最后一个
                pred = pred.right
            pred.right = node.right                # 原右子树接在它后面
            node.right = node.left                 # 左子树挪到右边
            node.left = None
        node = node.right
```

**易错点。**
- 正序处理（根、左、右）时先改 `node.right = node.left`：原右子树被丢掉。`[1,2,5,3,4,null,6]` 整条链走到 `3` 就断了，先序只剩 `1,2,3`，丢掉 `4,5,6`。要么先保存右子树，要么用逆序。
- 忘了把 `left` 置空：链表里每个节点仍带着左子树，输出里出现重复结构。
- 链状树深度 `2000` 会触到 CPython 默认递归上限约 `1000`；需调高上限或使用上面的 `O(1)` 版。

**同模式。** LC 116 填充每个节点的下一个右侧节点指针、LC 430 扁平化多级双向链表、LC 897 递增顺序搜索树、LC 426 将二叉搜索树转化为排序的双向链表。
