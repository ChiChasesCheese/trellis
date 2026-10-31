---
id: tlc-patterns-tree-dfs-1-signals
node: patterns.tree-dfs
type: qa
step: 1
---
## Q
**二叉树 DFS（Tree DFS）｜信号**

什么样的题面该想到二叉树的 DFS？「后序返回子树信息」「前序带参数下传」「全局最优」三种写法各由什么信号触发？

## A
树的递归基础模型：**一个节点的答案由它的子树答案和自己的值组合而成**。

**后序（先递归孩子，再处理自己）——要从子树拿信息：**
- 高度、节点数、是否平衡、直径、子树和：返回高度，顺手更新答案（例：LC 543 二叉树的直径）。
- 最近公共祖先：在左右子树里各找一次，看目标出现在哪里（例：LC 236 二叉树的最近公共祖先）。
- 返回一个数组而不是一个数：好叶子节点对返回「每个叶子到我的距离」的计数（例：LC 1530 好叶子节点对的数量）。

**前序（先处理自己，再把信息传给孩子）——需要从根到当前的信息：**
- 路径和、当前深度、连续长度：把当前长度向下传（例：LC 298 二叉树最长连续序列）。
- 路径可以从任意节点开始向下：向下传前缀和，用哈希统计（例：LC 437 路径总和 III）。

**全局最优（跨节点路径）**：路径可能「拐弯」经过某个节点的两侧，但向上返回时只能延伸一侧 → 用 `nonlocal best` 记录全局，返回单侧收益（例：LC 124 二叉树中的最大路径和）。

**构造类**：给遍历序列还原树，用前序确定根、中序确定左右范围（例：LC 105 从前序与中序遍历序列构造二叉树；高频：LC 889 根据前序和后序遍历构造二叉树）。

**近似信号：**
- 按**层**处理、右视图 → BFS（例：LC 199 二叉树的右视图）。
- BST 的有序性相关（验证、第 k 小）→ 中序 / 上下界（例：LC 98 验证二叉搜索树）。
- 节点数 `10^5` 且树可能退化成链 → 递归深度爆栈（CPython 默认约 1000），改迭代或调高 `sys.setrecursionlimit`（例：LC 94 二叉树的中序遍历，进阶要求迭代）。
- 要找任意两点的路径 → LCA，或把树当图用 BFS（例：LC 1740 找到二叉树中的距离；高频：LC 863 二叉树中所有距离为 K 的结点）。

**例题：** LC 543 二叉树的直径

返回二叉树中任意两个节点之间最长路径的长度（边数），路径可以不经过根，节点数 `[1, 10^4]`。

```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
    best = 0
    def height(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        lh, rh = height(node.left), height(node.right)
        best = max(best, lh + rh)
        return 1 + max(lh, rh)
    height(root)
    return best
```

**例题：** LC 236 二叉树的最近公共祖先

在二叉树里找两个指定节点的最近公共祖先（节点可以是自己的祖先），节点数 `[2, 10^5]`，值互不相同，`p != q` 且都在树中。

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

**例题：** LC 1530 好叶子节点对的数量

两个叶子节点之间的最短路径长度 `<= distance` 就是好叶子节点对，返回对数，节点数 `[1, 2^10]`，`1 <= distance <= 10`。

```python
from itertools import accumulate
def count_pairs(root: TreeNode | None, distance: int) -> int:
    ans = 0
    def dfs(node: TreeNode | None) -> list[int]:
        nonlocal ans
        if node is None:
            return [0] * (distance + 1)
        if not node.left and not node.right:
            return [1] + [0] * distance
        left = [0] + dfs(node.left)[:distance]
        right = [0] + dfs(node.right)[:distance]
        right_prefix = list(accumulate(right))
        ans += sum(left[i] * right_prefix[distance - i] for i in range(distance + 1))
        return [a + b for a, b in zip(left, right)]
    dfs(root)
    return ans
```

**例题：** LC 298 二叉树最长连续序列

计算从父节点到子节点、依次递增 1 的最长路径的长度，节点数 `[1, 3 * 10^4]`。

```python
def longest_consecutive(root: TreeNode | None) -> int:
    best = 0
    def dfs(node: TreeNode, length: int) -> None:
        nonlocal best
        best = max(best, length)
        for child in (node.left, node.right):
            if child:
                dfs(child, length + 1 if child.val == node.val + 1 else 1)
    if root:
        dfs(root, 1)
    return best
```

**例题：** LC 437 路径总和 III

求二叉树里节点值之和等于 `targetSum` 的向下路径的数目，路径不必从根开始、不必在叶子结束，节点数 `[0, 1000]`，值可为负。

```python
from collections import Counter
def path_sum(root: TreeNode | None, target_sum: int) -> int:
    prefix: Counter[int] = Counter({0: 1})
    def dfs(node: TreeNode | None, total: int) -> int:
        if node is None:
            return 0
        total += node.val
        count = prefix[total - target_sum]
        prefix[total] += 1
        count += dfs(node.left, total) + dfs(node.right, total)
        prefix[total] -= 1
        return count
    return dfs(root, 0)
```

**例题：** LC 124 二叉树中的最大路径和

路径是节点序列（相邻节点有边、每个节点至多出现一次，至少一个节点，不必过根），求最大路径和，节点数 `[1, 3 * 10^4]`，值 `-1000..1000`。

```python
def max_path_sum(root: TreeNode | None) -> int:
    best = root.val
    def gain(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)
    gain(root)
    return best
```

**例题：** LC 105 从前序与中序遍历序列构造二叉树

给定无重复元素的先序遍历 `preorder` 和中序遍历 `inorder`，构造并返回这棵二叉树，`1 <= preorder.length <= 3000`。

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

**例题：** LC 199 二叉树的右视图

站在二叉树右侧，从上到下返回能看到的节点值，节点数 `[0, 100]`。

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    level = [root] if root else []
    while level:
        ans.append(level[-1].val)
        level = [kid for node in level for kid in (node.left, node.right) if kid]
    return ans
```

**例题：** LC 98 验证二叉搜索树

判断二叉树是否是有效的二叉搜索树（左子树严格小、右子树严格大），节点数 `[1, 10^4]`，值在 32 位整数范围内。

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

**例题：** LC 94 二叉树的中序遍历

返回二叉树的中序遍历，节点数 `[0, 100]`；进阶要求用迭代完成。

```python
def inorder_traversal(root: TreeNode | None) -> list[int]:
    result: list[int] = []
    def dfs(node: TreeNode | None) -> None:
        if node is None:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    dfs(root)
    return result
```

**例题：** LC 1740 找到二叉树中的距离

返回二叉树中值为 `p` 与值为 `q` 的结点之间的距离（路径上的边数），节点数 `[1, 10^4]`，值唯一。

```python
def find_distance(root: TreeNode | None, p: int, q: int) -> int:
    def lca(node: TreeNode | None) -> TreeNode | None:
        if node is None or node.val in (p, q):
            return node
        left, right = lca(node.left), lca(node.right)
        return node if left and right else left or right
    def down(node: TreeNode, target: int) -> int:
        if node.val == target:
            return 0
        for child in (node.left, node.right):
            if child and (d := down(child, target)) >= 0:
                return d + 1
        return -1
    top = lca(root)
    return down(top, p) + down(top, q)
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

**例题：** LC 863 二叉树中所有距离为 K 的结点

给一棵二叉树的根结点 `root`、树中的一个目标结点 `target` 和一个整数 `k`，返回到 `target` 距离恰为 `k` 的所有结点的值（距离 = 两结点间路径的边数，可以向上走也可以向下走），答案顺序任意。约束：结点数在 `[1, 500]`，`0 <= Node.val <= 500`，所有 `Node.val` 互不相同，`target` 是树上的结点，`0 <= k <= 1000`。

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
