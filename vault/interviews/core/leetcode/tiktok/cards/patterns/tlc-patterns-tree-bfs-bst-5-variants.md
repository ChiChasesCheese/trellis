---
id: tlc-patterns-tree-bfs-bst-5-variants
node: patterns.tree-bfs-bst
type: qa
step: 5
---
## Q
**二叉树 BFS 与 BST 性质｜变形：最大宽度、删除 BST 节点、第 k 小、距离 K**

这几道题在基本模板上各改了哪一步？

## A
**LC 662 最大宽度**：层内节点按完全二叉树**编号**（左孩子 `2i`，右孩子 `2i+1`），一层的宽度 = 最右编号 − 最左编号 + 1。每层减去最左编号避免数字无限增长（Python 整数不溢出，但数字会变慢）（例：LC 662 二叉树最大宽度；高频：LC 199 二叉树的右视图）。

```python
def width_of_binary_tree(root: TreeNode | None) -> int:
    if not root:
        return 0
    best = 0
    level = [(root, 0)]                    # (节点, 编号)
    while level:
        best = max(best, level[-1][1] - level[0][1] + 1)
        base = level[0][1]
        nxt = []
        for node, idx in level:
            idx -= base
            if node.left:
                nxt.append((node.left, 2 * idx))
            if node.right:
                nxt.append((node.right, 2 * idx + 1))
        level = nxt
    return best
```

`[1,3,2,5,3,null,9]` → `4`；`[1,3,2,5,null,null,9,6,null,7]` → `7`；`[1,3,2,5]` → `2`。

**LC 450 删除 BST 节点**：找到后分三种情况：没有左孩子 → 右孩子顶上；没有右孩子 → 左孩子顶上；两个都有 → 用右子树的最小值（后继）替换当前节点的值，再到右子树里删除后继（例：LC 450 删除二叉搜索树中的节点）。

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

删除 `[5,3,6,2,4,null,7]` 中的 `3` → 层序 `[5,4,6,2,null,null,7]`。

**LC 230 第 k 小**：迭代中序，数到第 `k` 个就返回，提前停止（例：LC 230 二叉搜索树中第K小的元素）。**LC 863 距离 K**：先 DFS 给每个节点记父节点，再从目标做 BFS（邻居 = 左、右、父），第 `k` 层的节点即答案；`[3,5,1,6,2,0,8,null,null,7,4]`，目标 `5`，`k=2` → `[7,4,1]`（顺序不限）（例：LC 863 二叉树中所有距离为 K 的结点）。

**例题：** LC 662 二叉树最大宽度

二叉树（节点数 `1..3000`），每层的宽度是该层最左与最右非空节点之间的长度（两端之间的空位也计入），返回所有层中的最大宽度。

```python
def width_of_binary_tree(root: TreeNode | None) -> int:
    if root is None:
        return 0
    best = 0
    level: list[tuple[TreeNode, int]] = [(root, 0)]      # (节点, 它在满二叉树该层里的编号)
    while level:
        base = level[0][1]                               # 本层最左编号，用来归零
        best = max(best, level[-1][1] - base + 1)
        nxt: list[tuple[TreeNode, int]] = []
        for node, idx in level:
            idx -= base                                  # 归零后编号不会随深度指数膨胀
            if node.left:
                nxt.append((node.left, 2 * idx))
            if node.right:
                nxt.append((node.right, 2 * idx + 1))
        level = nxt
    return best
```

**例题：** LC 450 删除二叉搜索树中的节点

二叉搜索树（节点数 `0..10^4`，节点值唯一）和值 `key`，删除 `key` 对应的节点并保持 BST 性质，返回根节点；要求时间 `O(h)`。

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

**例题：** LC 230 二叉搜索树中第K小的元素

二叉搜索树（节点数 `n`，`1 <= k <= n <= 10^4`），返回第 `k` 小的元素（`k` 从 1 开始）。

```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    def dfs(node: TreeNode | None) -> int | None:
        nonlocal k
        if node is None:
            return None
        if (found := dfs(node.left)) is not None:   # 左子树里已经数到第 k 个：一路返回，不再往下走
            return found
        k -= 1                                      # 递归返回的顺序就是升序：数当前节点
        if k == 0:
            return node.val
        return dfs(node.right)
    result = dfs(root)
    if result is None:
        raise ValueError("k 超过节点数")
    return result
```

**例题：** LC 863 二叉树中所有距离为 K 的结点

二叉树（节点数 `1..500`，节点值互不相同）、树中的目标节点 `target` 和整数 `k`（`0 <= k <= 1000`），返回与 `target` 距离恰为 `k` 的所有节点的值，顺序不限。

```python
def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while stack:                          # 迭代 DFS 给每个结点记父指针（避免递归栈）
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    frontier, seen = [target], {target}   # 从 target 出发的 BFS，一层 = 距离 +1
    for _ in range(k):
        nxt: list[TreeNode] = []
        for node in frontier:
            for nb in (node.left, node.right, parent[node]):
                if nb and nb not in seen:  # seen 防止走回刚来的结点
                    seen.add(nb)
                    nxt.append(nb)
        frontier = nxt
    return [node.val for node in frontier]
```

**例题：** LC 199 二叉树的右视图

二叉树的根节点 `root`，返回站在右侧能看到的节点值（从上到下）；节点数 `0..100`。

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    level = [root] if root else []
    while level:
        ans.append(level[-1].val)
        level = [kid for node in level for kid in (node.left, node.right) if kid]
    return ans
```
