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
- LC 102 二叉树的层序遍历（高频）
- LC 116 填充每个节点的下一个右侧节点指针（高频）

**树转图 + BFS**
- LC 863 二叉树中所有距离为 K 的结点
- LC 2385 感染二叉树需要的总时间（高频）

**序列化与反序列化**
- LC 297 二叉树的序列化与反序列化
- LC 428 序列化和反序列化 N 叉树

**BST 性质**
- LC 450 删除二叉搜索树中的节点
- LC 426 将二叉搜索树转化为排序的双向链表（中序）
- LC 98 验证二叉搜索树（高频）
- LC 230 二叉搜索树中第 K 小的元素（高频）
- LC 99 恢复二叉搜索树（高频）

**与树 DFS 相邻**
- LC 105 从前序与中序遍历序列构造二叉树
- LC 236 二叉树的最近公共祖先
- LC 889 从前序与后序遍历序列构造二叉树（高频）
- LC 2196 根据描述创建二叉树（高频）

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

**例题：** LC 102 二叉树的层序遍历

给二叉树的根节点 `root`，返回其节点值的**层序遍历**：逐层地，从左到右访问所有节点，每层一个列表。树中节点数在 `[0, 2000]` 内，`-1000 <= Node.val <= 1000`。

```python
from collections import deque
def level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    queue = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)
    return res
```

**例题：** LC 116 填充每个节点的下一个右侧节点指针

给一棵完美二叉树（所有叶子在同一层，每个非叶子节点都有两个孩子），节点有 `val`、`left`、`right`、`next` 四个字段。填充每个节点的 `next` 指针，让它指向同一层中右边紧邻的节点；某层最右边的节点，`next` 为 `None`。初始时所有 `next` 都是 `None`。树中节点数在 `[0, 2^12 - 1]` 范围内，`-1000 <= node.val <= 1000`。进阶：只用常量额外空间；递归实现也算符合，递归栈不计入额外空间。

```python
def connect(root: 'Node | None') -> 'Node | None':
    leftmost = root
    while leftmost and leftmost.left:
        node = leftmost
        while node:
            node.left.next = node.right
            if node.next:
                node.right.next = node.next.left
            node = node.next
        leftmost = leftmost.left
    return root
```

**例题：** LC 2385 感染二叉树需要的总时间

给二叉树的根节点 `root`，树中节点的值**互不相同**，再给整数 `start`。第 `0` 分钟，值为 `start` 的节点开始被感染。之后每分钟，满足下面两个条件的节点会被感染：此前没有被感染；与一个已被感染的节点**相邻**（父子相邻）。返回感染整棵树需要的分钟数。节点数在 `[1, 10^5]`，`1 <= Node.val <= 10^5`，值互不相同，树中一定存在值为 `start` 的节点。

```python
from collections import defaultdict, deque
def amount_of_time(root: TreeNode, start: int) -> int:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    def link(node: TreeNode) -> None:
        for child in (node.left, node.right):
            if child:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                link(child)
    link(root)
    queue = deque([start])
    seen = {start}
    minutes = -1
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            u = queue.popleft()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
    return minutes
```

**例题：** LC 98 验证二叉搜索树

给二叉树的根结点 `root`，判断它是否是有效的二叉搜索树（BST）。有效的定义：结点的左子树只含**严格小于**当前结点的值；右子树只含**严格大于**当前结点的值；所有左、右子树自身也必须是 BST。树中结点数在 `[1, 10^4]`，`-2^31 <= Node.val <= 2^31 - 1`。

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    prev: int | None = None
    def inorder(node: TreeNode | None) -> bool:
        nonlocal prev
        if node is None:
            return True
        if not inorder(node.left):
            return False
        if prev is not None and node.val <= prev:
            return False
        prev = node.val
        return inorder(node.right)
    return inorder(root)
```

**例题：** LC 230 二叉搜索树中第 K 小的元素

给二叉搜索树的根节点 `root` 和整数 `k`，返回树中第 `k` 小的元素（`k` 从 `1` 开始）。节点数 `n`，`1 <= k <= n <= 10^4`，`0 <= Node.val <= 10^4`。

```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    def dfs(node: TreeNode | None) -> int | None:
        nonlocal k
        if node is None:
            return None
        if (found := dfs(node.left)) is not None:
            return found
        k -= 1
        if k == 0:
            return node.val
        return dfs(node.right)
    result = dfs(root)
    if result is None:
        raise ValueError("k 超过节点数")
    return result
```

**例题：** LC 99 恢复二叉搜索树

给二叉搜索树的根结点 `root`，其中**恰好两个**结点的值被错误地交换了。请在**不改变树结构**的情况下恢复这棵树（原地交换两个结点的值即可）。结点数在 `[2, 1000]`，`-2^31 <= Node.val <= 2^31 - 1`。

```python
def recover_tree(root: TreeNode | None) -> None:
    prev: TreeNode | None = None
    first = second = None
    def inorder(node: TreeNode | None) -> None:
        nonlocal prev, first, second
        if node is None:
            return
        inorder(node.left)
        if prev and prev.val > node.val:
            if first is None:
                first = prev
            second = node
        prev = node
        inorder(node.right)
    inorder(root)
    if first and second:
        first.val, second.val = second.val, first.val
```

**例题：** LC 889 从前序与后序遍历序列构造二叉树

给两个整数数组 `preorder` 和 `postorder`，`preorder` 是一棵**无重复值**二叉树的前序遍历，`postorder` 是同一棵树的后序遍历，重构并返回这棵二叉树；如果有多个答案，返回任意一个。`1 <= preorder.length <= 30`，`1 <= preorder[i] <= preorder.length`，`preorder` 中所有值不同，`postorder.length == preorder.length`，`1 <= postorder[i] <= postorder.length`，`postorder` 中所有值不同，保证两者是同一棵二叉树的前序和后序。

```python
def construct_from_pre_post(preorder: list[int], postorder: list[int]) -> TreeNode | None:
    post_idx = {v: i for i, v in enumerate(postorder)}
    def build(pre_lo: int, post_lo: int, size: int) -> TreeNode | None:
        if size == 0:
            return None
        root = TreeNode(preorder[pre_lo])
        if size == 1:
            return root
        left_root = preorder[pre_lo + 1]
        left_size = post_idx[left_root] - post_lo + 1
        root.left = build(pre_lo + 1, post_lo, left_size)
        root.right = build(pre_lo + 1 + left_size, post_lo + left_size, size - 1 - left_size)
        return root
    return build(0, 0, len(preorder))
```

**例题：** LC 2196 根据描述创建二叉树

给二维整数数组 `descriptions`，其中 `descriptions[i] = [parent_i, child_i, isLeft_i]` 表示 `parent_i` 是 `child_i` 的父节点，二叉树中各节点的值互不相同；`isLeft_i == 1` 表示 `child_i` 是 `parent_i` 的左子节点，`isLeft_i == 0` 表示右子节点。按描述构造二叉树并返回根节点，测试保证能构造出有效的二叉树。`1 <= descriptions.length <= 10^4`，`descriptions[i].length == 3`，`1 <= parent_i, child_i <= 10^5`，`0 <= isLeft_i <= 1`。

```python
def create_binary_tree(descriptions: list[list[int]]) -> TreeNode | None:
    nodes: dict[int, TreeNode] = {}
    parents: set[int] = set()
    children: set[int] = set()
    for parent, child, is_left in descriptions:
        for v in (parent, child):
            if v not in nodes:
                nodes[v] = TreeNode(v)
        if is_left:
            nodes[parent].left = nodes[child]
        else:
            nodes[parent].right = nodes[child]
        parents.add(parent)
        children.add(child)
    (root,) = parents - children
    return nodes[root]
```
