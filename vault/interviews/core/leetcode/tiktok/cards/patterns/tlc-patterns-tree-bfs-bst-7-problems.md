---
id: tlc-patterns-tree-bfs-bst-7-problems
node: patterns.tree-bfs-bst
type: qa
step: 7
---
## Q
**二叉树 BFS 与 BST 性质｜本组用到层序遍历或 BST 性质的题**

按变形分类，这个题组里哪些题属于这一类？

## A
**层序遍历**
- LC 199 二叉树的右视图
- LC 103 二叉树的锯齿形层序遍历
- LC 662 二叉树最大宽度

**树转图 + BFS**
- LC 863 二叉树中所有距离为 K 的结点

**序列化与反序列化**
- LC 297 二叉树的序列化与反序列化
- LC 428 序列化和反序列化 N 叉树

**BST 性质**
- LC 450 删除二叉搜索树中的节点
- LC 426 将二叉搜索树转化为排序的双向链表（中序）

**与树 DFS 相邻**
- LC 105 从前序与中序遍历序列构造二叉树
- LC 236 二叉树的最近公共祖先

提示：看到「按层」就写 `for _ in range(len(q))`；看到「二叉搜索树」先想中序有序和取值区间；看到「序列化」先决定空节点怎么标记。

**例题：** LC 199 二叉树的右视图

二叉树根节点 `root`，返回从右侧看到的节点值（自上而下）；节点数 `<= 100`。

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    level = [root] if root else []
    while level:
        ans.append(level[-1].val)
        level = [kid for node in level for kid in (node.left, node.right) if kid]
    return ans
```

**例题：** LC 103 二叉树的锯齿形层序遍历

返回二叉树的锯齿形层序遍历：第一层从左到右，第二层从右到左，交替进行；节点数 `<= 2000`。

```python
def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    level = [root]
    left_to_right = True
    while level:
        vals = [node.val for node in level]
        res.append(vals if left_to_right else vals[::-1])
        level = [child for node in level
                 for child in (node.left, node.right) if child]
        left_to_right = not left_to_right
    return res
```

**例题：** LC 662 二叉树最大宽度

每层宽度是该层最左到最右非空节点之间的长度（两端之间的空位也计入），返回所有层的最大宽度；节点数 `<= 3000`。

```python
def width_of_binary_tree(root: TreeNode | None) -> int:
    if root is None:
        return 0
    best = 0
    level: list[tuple[TreeNode, int]] = [(root, 0)]
    while level:
        base = level[0][1]
        best = max(best, level[-1][1] - base + 1)
        nxt: list[tuple[TreeNode, int]] = []
        for node, idx in level:
            idx -= base
            if node.left:
                nxt.append((node.left, 2 * idx))
            if node.right:
                nxt.append((node.right, 2 * idx + 1))
        level = nxt
    return best
```

**例题：** LC 863 二叉树中所有距离为 K 的结点

二叉树 `root`、目标结点 `target` 和 `k`，返回与 `target` 距离恰为 `k` 的所有结点值（可向上走）；结点数 `<= 500`，值互不相同。

```python
def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    frontier, seen = [target], {target}
    for _ in range(k):
        nxt: list[TreeNode] = []
        for node in frontier:
            for nb in (node.left, node.right, parent[node]):
                if nb and nb not in seen:
                    seen.add(nb)
                    nxt.append(nb)
        frontier = nxt
    return [node.val for node in frontier]
```

**例题：** LC 297 二叉树的序列化与反序列化

设计 `serialize` / `deserialize`，使任意二叉树可转成字符串再还原成同一棵树；节点数 `<= 10^4`，`-1000 <= Node.val <= 1000`。

```python
class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        def dfs(node: TreeNode | None) -> None:
            if node is None:
                out.append("#")
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)
    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))
        def build() -> TreeNode | None:
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()
            node.right = build()
            return node
        return build()
```

**例题：** LC 428 序列化和反序列化 N 叉树

设计 N 叉树的 `serialize` / `deserialize`，格式自定且不得用类成员或全局变量保存状态；节点数 `<= 10^4`，树高 `<= 1000`。

```python
class Codec:
    def serialize(self, root: Node | None) -> str:
        out: list[str] = []
        def dfs(node: Node) -> None:
            out.append(f"{node.val} {len(node.children)}")
            for child in node.children:
                dfs(child)
        if root:
            dfs(root)
        return " ".join(out)
    def deserialize(self, data: str) -> Node | None:
        if not data:
            return None
        tokens = map(int, data.split())
        def build() -> Node:
            node = Node(next(tokens), [])
            for _ in range(next(tokens)):
                node.children.append(build())
            return node
        return build()
```

**例题：** LC 450 删除二叉搜索树中的节点

删除 BST 中值为 `key` 的节点并保持 BST 性质，返回根节点；节点数 `<= 10^4`，值唯一，要求 `O(h)`。

```python
def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)
    return root
```

**例题：** LC 426 将二叉搜索树转化为排序的双向链表

把 BST 原地转成排序的循环双向链表（`left` 当前驱、`right` 当后继），返回最小节点；节点数 `<= 2000`，值互不相同。

```python
def tree_to_doubly_list(root: Node | None) -> Node | None:
    if root is None:
        return None
    first = prev = None
    def inorder(node: Node | None) -> None:
        nonlocal first, prev
        if node is None:
            return
        inorder(node.left)
        if prev:
            prev.right, node.left = node, prev
        else:
            first = node
        prev = node
        inorder(node.right)
    inorder(root)
    first.left, prev.right = prev, first
    return first
```

**例题：** LC 105 从前序与中序遍历序列构造二叉树

给同一棵树的 `preorder` 和 `inorder`（无重复元素），构造并返回这棵树；`1 <= preorder.length <= 3000`。

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    index = {v: i for i, v in enumerate(inorder)}
    pre = iter(preorder)
    def build(lo: int, hi: int) -> TreeNode | None:
        if lo == hi:
            return None
        val = next(pre)
        mid = index[val]
        node = TreeNode(val)
        node.left = build(lo, mid)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(inorder))
```

**例题：** LC 236 二叉树的最近公共祖先

二叉树中两个节点 `p`、`q`，返回它们的最近公共祖先（节点可以是自己的祖先）；节点数 `<= 10^5`，值互不相同。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```
