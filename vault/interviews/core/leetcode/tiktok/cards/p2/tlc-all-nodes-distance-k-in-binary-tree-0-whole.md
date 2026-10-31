---
id: tlc-all-nodes-distance-k-in-binary-tree-0-whole
node: p2.all-nodes-distance-k-in-binary-tree
type: qa
---
## Q
**LC 863 二叉树中所有距离为 K 的结点**｜Medium · LC TikTok 近 30 天热度 82/100（全时段 46） · CodeTop 国内累计 10 次 · 最近 2025-09-17（国内 CodeTop）

给一棵二叉树的根结点 `root`、树中的一个目标结点 `target` 和一个整数 `k`，返回到 `target` 距离恰为 `k` 的所有结点的值（距离 = 两结点间路径的边数，可以向上走也可以向下走），答案顺序任意。

约束：结点数在 `[1, 500]`，`0 <= Node.val <= 500`，所有 `Node.val` 互不相同，`target` 是树上的结点，`0 <= k <= 1000`。

例：`root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2` → `[7,4,1]`（`7`、`4` 在 `5` 的下面两层，`1` 要先上到 `3` 再下到 `1`）；`root = [1], target = 1, k = 3` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 树只有向下的指针，所以先遍历一遍给每个结点补上「父指针」，把树变成无向图，再从 `target` 做 `k` 层 BFS（带 `seen`），最后一层的结点值就是答案。`O(n)`。

**识别。** 「距离 `target` 为 `k`」里的距离既包括往下也包括往上（经过祖先再绕到别的子树）——只会向下的树遍历表达不了「向上」，这是要补父指针的信号。「恰好 `k` 步」「到某个源点的距离」是 BFS 的标准问法；`n ≤ 500` 很小，任何 `O(n)` / `O(n log n)` 都够，考点在建模而不在性能。

**推导。** 暴力：对每个结点算它到 `target` 的距离（找两者的最近公共祖先再加深度差），`O(n^2)`。浪费在于每次都重新找路径，而「到同一个 `target` 的距离」本来就是一次单源最短路。关键洞察：把树看成无向图，边权都是 1，那么「距离 `k`」就是 BFS 的第 `k` 层。树里没有现成的向上边，所以先 DFS 记 `parent`，BFS 扩 `k` 层。

**简单解法。** 对每个结点单独算它到 `target` 的距离：记下每个结点从根出发的路径，两路径的公共前缀长度 `c` 对应最近公共祖先，距离 `= len(A) + len(B) - 2c`。

```python
def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    paths: dict[TreeNode, list[TreeNode]] = {}     # 每个结点：从根到它的路径

    def dfs(node: TreeNode | None, path: list[TreeNode]) -> None:
        if node is None:
            return
        path = path + [node]
        paths[node] = path
        dfs(node.left, path)
        dfs(node.right, path)

    dfs(root, [])
    t = paths[target]
    res: list[int] = []
    for node, p in paths.items():
        c = 0
        while c < min(len(p), len(t)) and p[c] is t[c]:   # 公共前缀的长度，最后一个公共结点是最近公共祖先
            c += 1
        if len(p) + len(t) - 2 * c == k:           # 先上到公共祖先再下来：两段深度之和
            res.append(node.val)
    return res
```

时间 `O(n·h)`、空间 `O(n·h)`；`n <= 500` 完全能过，但对每个结点重复比较路径，BFS 一遍单源搜索就够。

最优解：

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

运行：`root=[3,5,1,6,2,0,8,null,null,7,4], target=5, k=2` → `[7, 4, 1]`，`root=[1], target=1, k=3` → `[]`，`同一棵树 target=5, k=0` → `[5]`，`同一棵树 target=7, k=3` → `[6, 3]`。

**复杂度。** 时间 `O(n)`：建父指针遍历每个结点一次，BFS 每个结点至多入队一次；空间 `O(n)`（父指针表、`seen`、栈和队列）。`k` 再大也不增加成本——`frontier` 空了之后每轮是空操作。

**拓展优化。**
- 不建父指针表，空间降到 `O(h)`：一次后序 DFS 返回「到 `target` 的距离」，在每个祖先处按距离 `d` 收下它自己或向另一侧下探。

```python
def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    res: list[int] = []

    def collect(node: TreeNode | None, depth: int) -> None:   # 收集 node 往下恰好 depth 层的结点
        if node is None or depth < 0:
            return
        if depth == 0:
            res.append(node.val)
            return
        collect(node.left, depth - 1)
        collect(node.right, depth - 1)

    def dfs(node: TreeNode | None) -> int:         # node 到 target 的距离；target 不在子树里返回 -1
        if node is None:
            return -1
        if node is target:
            collect(node, k)                       # target 往下的 k 层
            return 0
        left, right = dfs(node.left), dfs(node.right)
        if left == -1 and right == -1:
            return -1
        d = (left if left != -1 else right) + 1    # 当前祖先到 target 的距离
        other = node.right if left != -1 else node.left
        if d == k:
            res.append(node.val)                   # 祖先自己正好在距离 k
        else:
            collect(other, k - d - 1)              # 绕到另一侧子树，再往下 k - d - 1 层
        return d

    dfs(root)
    return res
```

**易错点。**
- BFS 不记 `seen`：从 `5` 往上走到 `3`、再往下走回 `5`，同一结点被反复加入。例树 `k=2` 会返回 `[5, 7, 4, 5, 5, 1]`（正确是 `[7, 4, 1]`，顺序任意）。
- 只向下搜 `target` 的子树：例树 `k=2` 只得 `[7, 4]`，漏掉要先上到 `3` 再下到 `1` 的那一个。
- `k` 大于树能到的最远距离时 `frontier` 为空，返回 `[]`；`k = 0` 返回 `[target.val]`——循环一次都不进，不需要特判。

**追问。**
- 同一棵树上有很多次查询：父指针表只建一次，每次查询只付 BFS 的代价。
- 要求返回每个结点到 `target` 的距离：BFS 时用 `dict[TreeNode, int]` 代替 `seen`，同时记下层号。

**同模式。** LC 133 / 1091 / 752 这类「图上按层 BFS」、LC 236 最近公共祖先（也是「向上」的需求）、LC 1740 二叉树中两结点距离、LC 2385 感染二叉树需要的总时间（从某结点出发，求最远距离——同一建模）。
