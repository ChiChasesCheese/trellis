---
id: tlc-patterns-tree-bfs-bst-1-signals
node: patterns.tree-bfs-bst
type: qa
step: 1
---
## Q
**二叉树 BFS 与 BST 性质｜信号**

什么样的题面该想到层序遍历（BFS）？什么样该想到 BST 的中序有序性？序列化题的信号是什么？

## A
**层序遍历（Level-order BFS）的信号：**
- 题面按**层**组织输出：「每一层的节点」「锯齿形层序」LC 103、「每层最大宽度」LC 662（例：LC 103 二叉树的锯齿形层序遍历）。
- 「从右侧看到的节点」「每层最后一个」（例：LC 199 二叉树的右视图）。
- 「到最近叶子的深度」「最小深度」：BFS 遇到第一个叶子就停（例：LC 111 二叉树的最小深度）。
- 把树当**无向图**处理：给节点加父指针，或把边存成邻接表，再从某个点出发做 BFS / DFS：「距离目标节点为 K 的所有节点」LC 863；树形的路网从 `0` 号点出发，数要掉头的边（例：LC 1466 重新规划路线）。

**BST 的信号（二叉搜索树：左 < 根 < 右）：**
- 题面出现「**二叉搜索树**」：**中序遍历是严格递增序列**，是几乎所有 BST 题的钥匙；最小差一定出现在中序相邻的两个节点之间（例：LC 783 二叉搜索树节点最小距离）。
- 验证 BST：每个节点有一个合法的**取值区间**，从上往下收窄，不能只比较父子（例：LC 98 验证二叉搜索树）。
- 第 `k` 小：中序遍历数到第 `k` 个，可以提前停（例：LC 230 二叉搜索树中第K小的元素）。
- 查找 / 插入 / 删除：沿着比较大小的方向走，`O(h)`（LC 450）（例：LC 235 二叉搜索树的最近公共祖先）。
- 转成有序双向链表 LC 426：中序遍历中接指针；同类的串链技巧是靠一个尾指针把节点串起来（例：LC 114 二叉树展开为链表）。

**序列化的信号：**
- 「把树变成字符串再还原」LC 297、428：需要**记录空节点**（或每个节点的孩子数），才能唯一还原结构；对照：只给前序和后序、不记空节点，还原出来的树不唯一（例：LC 889 根据前序和后序遍历构造二叉树）。

**近似信号：**
- 只需要某种遍历序列、不关心层 → DFS 更简单（例：LC 94 二叉树的中序遍历）。
- 路径、子树聚合 → 后序 DFS，不是 BFS（例：LC 543 二叉树的直径）。
- 树的节点数大且可能退化成链 → BFS 用队列没有递归深度问题，是 DFS 的备选（例：LC 107 二叉树的层次遍历 II）。

**例题：** LC 103 二叉树的锯齿形层序遍历

给二叉树的根节点 `root`，返回其节点值的**锯齿形层序遍历**：第一层从左往右，第二层从右往左，之后交替。树中节点数在 `[0, 2000]` 内，`-100 <= Node.val <= 100`。

```python
def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    level = [root]                      # 当前层的节点，始终按从左到右存放
    left_to_right = True
    while level:
        vals = [node.val for node in level]
        res.append(vals if left_to_right else vals[::-1])   # 只在输出时反转
        level = [child for node in level
                 for child in (node.left, node.right) if child]
        left_to_right = not left_to_right
    return res
```

**例题：** LC 199 二叉树的右视图

给二叉树的根节点 `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。节点个数范围 `[0, 100]`，`-100 <= Node.val <= 100`。

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    level = [root] if root else []
    while level:
        ans.append(level[-1].val)                  # 这一层最右的节点
        level = [kid for node in level for kid in (node.left, node.right) if kid]
    return ans
```

**例题：** LC 111 二叉树的最小深度

给二叉树的根 `root`，求它的最小深度：从根节点到**最近的叶子节点**的最短路径上的节点数。叶子节点是没有子节点的节点。树中节点数在 `[0, 10^5]` 内，`-1000 <= Node.val <= 1000`。

```python
from collections import deque
def min_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    queue = deque([(root, 1)])                    # (节点, 它的深度)
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth                          # BFS 按层推进：第一个叶子就是最浅的
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0
```

**例题：** LC 1466 重新规划路线

有 `n` 座城市，编号 `0` 到 `n - 1`，之间共有 `n - 1` 条路线，任意两座城市之间只有唯一一条路线可走（路线网是一棵树）。`connections[i] = [a, b]` 表示一条从城市 `a` 到城市 `b` 的有向路线。城市 `0` 要举办比赛，请重新规划路线方向，使每座城市都能到达城市 `0`，返回需要变更方向的**最少**路线数。数据保证重新规划后每座城市都能到达城市 `0`。`2 <= n <= 5 * 10^4`，`connections.length == n - 1`，`connections[i].length == 2`，`0 <= connections[i][0], connections[i][1] <= n - 1`，`connections[i][0] != connections[i][1]`。

```python
def min_reorder(n: int, connections: list[list[int]]) -> int:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))              # 从 a 走到 b：顺着原方向，即背离城市 0，这条边要反转
        adj[b].append((a, 0))              # 从 b 走到 a：逆着原方向，即朝向城市 0，不用动

    def dfs(u: int, parent: int) -> int:   # 以 u 为根的子树里需要反转的边数
        flips = 0
        for v, cost in adj[u]:
            if v != parent:                # 树没有环：只要不走回父亲，就不会重复访问
                flips += cost + dfs(v, u)  # 进入 v 的这条边的代价 + v 子树里的代价
        return flips

    return dfs(0, -1)
```

**例题：** LC 783 二叉搜索树节点最小距离

给二叉搜索树（BST）的根节点 `root`，返回树中任意两个不同节点值之差的最小值（差取绝对值，是正数）。节点数在 `[2, 100]`，`0 <= Node.val <= 10^5`。

```python
from math import inf
def min_diff_in_bst(root: TreeNode | None) -> int:
    best = inf
    prev: int | None = None              # 中序遍历中上一个节点的值
    def inorder(node: TreeNode | None) -> None:
        nonlocal best, prev
        if node is None:
            return
        inorder(node.left)
        if prev is not None:             # 中序是升序：只需和前一个值比
            best = min(best, node.val - prev)
        prev = node.val
        inorder(node.right)
    inorder(root)
    return best
```

**例题：** LC 98 验证二叉搜索树

给二叉树的根结点 `root`，判断它是否是有效的二叉搜索树（BST）。有效的定义：结点的左子树只含**严格小于**当前结点的值；右子树只含**严格大于**当前结点的值；所有左、右子树自身也必须是 BST。树中结点数在 `[1, 10^4]`，`-2^31 <= Node.val <= 2^31 - 1`。

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    prev: int | None = None            # 中序序列里的前一个值

    def inorder(node: TreeNode | None) -> bool:   # 这棵子树的中序是否严格递增
        nonlocal prev
        if node is None:
            return True
        if not inorder(node.left):     # 左子树先走完；已经失败就一路返回
            return False
        if prev is not None and node.val <= prev:   # 中序必须严格递增
            return False
        prev = node.val
        return inorder(node.right)

    return inorder(root)
```

**例题：** LC 230 二叉搜索树中第K小的元素

给二叉搜索树的根节点 `root` 和整数 `k`，返回树中第 `k` 小的元素（`k` 从 `1` 开始）。节点数 `n`，`1 <= k <= n <= 10^4`，`0 <= Node.val <= 10^4`。

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

**例题：** LC 235 二叉搜索树的最近公共祖先

给一棵二叉搜索树和其中两个不同的结点 `p`、`q`，返回它们的最近公共祖先（一个结点也可以是它自己的祖先）。所有结点的值唯一，`p`、`q` 都在树中。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    lo, hi = min(p.val, q.val), max(p.val, q.val)    # 不假设 p 比 q 小
    node = root
    while node:
        if node.val < lo:              # 两个目标都在右子树
            node = node.right
        elif node.val > hi:            # 两个目标都在左子树
            node = node.left
        else:                          # lo <= node.val <= hi：两路在此分叉（或 node 本身就是其一）
            return node
    return None
```

**例题：** LC 114 二叉树展开为链表

给二叉树的根节点 `root`，原地把它展开成一个单链表：仍用 `TreeNode`，`right` 指向链表的下一个节点，`left` 始终为 `null`，顺序与先序遍历相同。节点数在 `[0, 2000]`，`-100 <= Node.val <= 100`。

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

**例题：** LC 889 根据前序和后序遍历构造二叉树

给两个整数数组 `preorder` 和 `postorder`，`preorder` 是一棵**无重复值**二叉树的前序遍历，`postorder` 是同一棵树的后序遍历，重构并返回这棵二叉树；如果有多个答案，返回任意一个。`1 <= preorder.length <= 30`，`1 <= preorder[i] <= preorder.length`，`preorder` 中所有值不同，`postorder.length == preorder.length`，`1 <= postorder[i] <= postorder.length`，`postorder` 中所有值不同，保证两者是同一棵二叉树的前序和后序。

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

**例题：** LC 94 二叉树的中序遍历

给二叉树的根结点 `root`，返回它的**中序**（左、根、右）遍历结果。树中结点数在 `[0, 100]`，`-100 <= Node.val <= 100`。进阶：递归算法很简单，能用迭代完成吗？

```python
def inorder_traversal(root: TreeNode | None) -> list[int]:
    result: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if node is None:
            return
        dfs(node.left)                 # 先把整个左子树走完
        result.append(node.val)        # 再访问自己：夹在左右之间就是中序
        dfs(node.right)                # 最后走右子树

    dfs(root)
    return result
```

**例题：** LC 543 二叉树的直径

给一棵二叉树的根节点，返回该树的**直径**：树中任意两个节点之间最长路径的长度，路径可能经过也可能不经过根节点，长度用路径上的**边数**表示。树中节点数在 `[1, 10^4]`，`-100 <= Node.val <= 100`。

```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
    best = 0

    def height(node: TreeNode | None) -> int:    # 子树高度（按结点数），空树为 0
        nonlocal best
        if node is None:
            return 0
        lh, rh = height(node.left), height(node.right)
        best = max(best, lh + rh)                # 经过 node 的最长路径的边数 = 左高 + 右高
        return 1 + max(lh, rh)

    height(root)
    return best
```

**例题：** LC 107 二叉树的层次遍历 II

给二叉树的根结点 `root`，返回其结点值**自底向上的层序遍历**：从叶子所在层到根所在层，逐层，每层从左到右。树中结点数在 `[0, 2000]`，`-1000 <= Node.val <= 1000`。

```python
def level_order_bottom(root: TreeNode | None) -> list[list[int]]:
    ans: list[list[int]] = []
    level = [root] if root else []
    while level:
        ans.append([node.val for node in level])              # 这一层的值，从左到右
        level = [child for node in level for child in (node.left, node.right) if child]   # 下一层
    return ans[::-1]                                          # 自顶向下收集，最后整体反转
```
