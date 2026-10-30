---
id: tlc-flatten-binary-tree-to-linked-list-2-code
node: b.flatten-binary-tree-to-linked-list
type: qa
step: 2
---
## Q
**LC 114 二叉树展开为链表**｜写出 Python 实现

二叉树节点数在 `[0, 2000]`，值在 `[-100, 100]`。原地展开成单链表：`right` 指向下一个节点，`left` 全为 `null`，顺序与先序相同。要求 `O(n)` 时间，函数无返回值。

## A
**思路。** 递归：`dfs(node)` 把 `node` 的子树展开成链并返回链尾。先分别展开左、右子树；有左子树时，把原右子树接在左链的尾后面，再把左链搬到 `node.right`，`node.left` 置空；返回整条链的尾（右链有尾用右链的，否则左链的，否则自己）。

```python
def flatten(root: TreeNode | None) -> None:
    def dfs(node: TreeNode | None) -> TreeNode | None:   # 把 node 子树展开成链，返回链的尾节点
        if node is None:
            return None
        left_tail = dfs(node.left)                       # 左子树展开后的尾
        right_tail = dfs(node.right)                     # 右子树展开后的尾
        if left_tail:                                    # 有左子树才需要拼接
            left_tail.right = node.right                 # 原右子树接在左链后面
            node.right = node.left                       # 左链搬到右边
            node.left = None
        return right_tail or left_tail or node           # 整条链的尾：优先右链，其次左链，最后是自己

    dfs(root)
```

运行：`[1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`，`[]` → `[]`，`[0]` → `[0]`；深度 2000 的左链在默认递归上限下抛 `RecursionError`，调高上限后展开，沿 `right` 数到 `2000` 个节点且每个 `left` 都是 `None`。

**复杂度。** 时间 `O(n)`：每个节点只被 `dfs` 访问一次，拼接是常数次指针操作；空间 `O(h)`：递归栈，`h` 是树高，链状树时 `O(n)`（深度 2000 会触到默认递归上限）。

**写法要点。** 嵌套函数 `dfs` 返回链尾，调用方直接用 `left_tail.right = node.right`，不用再沿右链找末端；`return right_tail or left_tail or node` 用 `or` 的短路取第一个非空的尾；拼接的顺序不能换（先接右、再搬左）；不返回任何值，修改的是传入的树。要 `O(1)` 额外空间属于进阶，需要改写成沿 `right` 走的迭代版。
