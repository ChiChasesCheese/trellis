---
id: tlc-patterns-tree-dfs-7-problems
node: patterns.tree-dfs
type: qa
step: 7
---
## Q
**二叉树 DFS（Tree DFS）｜本组用到二叉树 DFS 的题**

按变形分类，这个题组里哪些题属于二叉树 DFS？

## A
**后序返回子树信息 + 全局最优**
- LC 124 二叉树中的最大路径和
- LC 1530 好叶子节点对的数量
- LC 298 二叉树最长连续序列

**最近公共祖先 / 距离**
- LC 236 二叉树的最近公共祖先
- LC 863 二叉树中所有距离为 K 的结点（DFS 建父指针，再 BFS）

**前序下传信息 + 哈希**
- LC 437 路径总和 III

**构造与序列化**
- LC 105 从前序与中序遍历序列构造二叉树
- LC 297 二叉树的序列化与反序列化
- LC 428 序列化和反序列化 N 叉树

**树 + 双向链表**
- LC 426 将二叉搜索树转化为排序的双向链表（中序 DFS，接前驱指针）

**BST 相关（中序性质）**
- LC 450 删除二叉搜索树中的节点

提示：先问「这个节点要向父节点报告什么」（高度、单侧收益、距离列表）；再问「是否有跨过当前节点的路径」（需要全局变量）；最后确认空树和退化链的处理。

**例题：** LC 124 二叉树中的最大路径和

二叉树里的路径是相邻节点相连、每个节点至多出现一次的序列，不必经过根。返回最大路径和。结点数 `1..3 * 10^4`，`-1000 <= val <= 1000`。

```python
def max_path_sum(root: TreeNode | None) -> int:
    best = root.val                                # 初值不能是 0：全负树的答案是负数
    def gain(node: TreeNode | None) -> int:        # 从 node 向下走的最大单链和；空节点贡献 0
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)             # 负收益的子树直接不要
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)  # 以 node 为最高点的路径：两侧都可以带
        return node.val + max(left, right)         # 往父亲返回时只能选一边
    gain(root)
    return best
```

**例题：** LC 1530 好叶子节点对的数量

二叉树和整数 `distance`，两个叶子之间的最短路径长度 `<= distance` 就算一对好叶子对，返回好叶子对的数量。结点数 `1..2^10`，`1 <= distance <= 10`。

```python
from itertools import accumulate
def count_pairs(root: TreeNode | None, distance: int) -> int:
    ans = 0
    def dfs(node: TreeNode | None) -> list[int]:    # 返回 cnt：cnt[d] = 子树里距 node 恰好 d 的叶子数（d <= distance）
        nonlocal ans
        if node is None:
            return [0] * (distance + 1)
        if not node.left and not node.right:
            return [1] + [0] * distance             # 叶子自己距自己 0
        left = [0] + dfs(node.left)[:distance]      # 孩子子树的叶子，距 node 都多 1；超过 distance 的丢弃
        right = [0] + dfs(node.right)[:distance]
        right_prefix = list(accumulate(right))      # right_prefix[j]：距离 <= j 的右侧叶子数
        ans += sum(left[i] * right_prefix[distance - i] for i in range(distance + 1))
        return [a + b for a, b in zip(left, right)]
    dfs(root)
    return ans
```

**例题：** LC 298 二叉树最长连续序列

返回二叉树中最长的连续递增路径（每步值加 `1`，只能由父到子）的长度，起点任意。结点数 `1..3 * 10^4`。

```python
def longest_consecutive(root: TreeNode | None) -> int:
    best = 0
    def dfs(node: TreeNode, length: int) -> None:
        nonlocal best
        best = max(best, length)                 # length：以 node 结尾的连续递增路径长度
        for child in (node.left, node.right):
            if child:
                dfs(child, length + 1 if child.val == node.val + 1 else 1)
    if root:
        dfs(root, 1)
    return best
```

**例题：** LC 236 二叉树的最近公共祖先

返回二叉树中两个给定节点 `p`、`q` 的最近公共祖先（节点可以是自己的祖先）。结点数 `2..10^5`，值互不相同，`p`、`q` 都在树中。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:       # 空树、或碰到 p / q：这棵子树的汇报就是它自己
        return root
    left = lowest_common_ancestor(root.left, p, q)   # 左子树里找到了谁
    right = lowest_common_ancestor(root.right, p, q) # 右子树里找到了谁
    if left and right:                               # p、q 分居两侧：当前节点就是最近公共祖先
        return root
    return left or right                             # 只有一边有：把它往上传
```

**例题：** LC 863 二叉树中所有距离为 K 的结点

二叉树的根 `root`、目标节点 `target` 和整数 `k`，返回与 `target` 距离恰为 `k` 的所有节点的值（可向上也可向下走）。结点数 `1..500`，值互不相同，`0 <= k <= 1000`。

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

**例题：** LC 437 路径总和 III

二叉树和整数 `targetSum`，统计节点值之和等于 `targetSum` 的向下路径条数（不必从根开始、不必在叶子结束）。结点数 `0..1000`，`-10^9 <= val <= 10^9`。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> int:
    prefix: Counter[int] = Counter({0: 1})       # 当前根到结点链上：前缀和 -> 出现次数
    def dfs(node: TreeNode | None, total: int) -> int:   # total：根到 node 父亲的和
        if node is None:
            return 0
        total += node.val                        # 根到 node 的和
        count = prefix[total - target_sum]       # 有多少个祖先前缀和恰好差 target_sum
        prefix[total] += 1                       # 进入：把 node 的前缀和加入当前链
        count += dfs(node.left, total) + dfs(node.right, total)
        prefix[total] -= 1                       # 离开：撤销，别的分支看不到这条链
        return count
    return dfs(root, 0)
```

**例题：** LC 105 从前序与中序遍历序列构造二叉树

由前序遍历 `preorder` 和中序遍历 `inorder` 构造二叉树，返回根节点。`1 <= n <= 3000`，元素互不相同。

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    index = {v: i for i, v in enumerate(inorder)}   # 值 -> 中序下标
    pre = iter(preorder)                            # 前序序列只会被顺序消费一次
    def build(lo: int, hi: int) -> TreeNode | None:  # 还原中序区间 inorder[lo:hi]
        if lo == hi:
            return None
        val = next(pre)                              # 前序的下一个值就是这段的根
        mid = index[val]
        node = TreeNode(val)
        node.left = build(lo, mid)                   # 必须先建左再建右，顺序和前序一致
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(inorder))
```

**例题：** LC 297 二叉树的序列化与反序列化

设计二叉树的序列化 `serialize` 与反序列化 `deserialize`，格式自定，只要能还原出原树。结点数 `0..10^4`，`-1000 <= val <= 1000`。

```python
class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        def dfs(node: TreeNode | None) -> None:
            if node is None:
                out.append("#")                    # 空位也要占一格
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)
    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))             # 标记流只被顺序消费一次
        def build() -> TreeNode | None:
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()                    # 先左后右，与序列化的顺序一致
            node.right = build()
            return node
        return build()
```

**例题：** LC 428 序列化和反序列化 N 叉树

设计 N 叉树的序列化 `serialize` 与反序列化 `deserialize`，格式自定，算法必须无状态（不能用成员或全局变量）。结点数 `0..10^4`，树高 `<= 1000`。

```python
class Codec:
    def serialize(self, root: Node | None) -> str:
        out: list[str] = []
        def dfs(node: Node) -> None:
            out.append(f"{node.val} {len(node.children)}")   # 值 + 孩子个数
            for child in node.children:
                dfs(child)
        if root:
            dfs(root)
        return " ".join(out)
    def deserialize(self, data: str) -> Node | None:
        if not data:                              # 空树："".split() 是 []，必须先判空
            return None
        tokens = map(int, data.split())           # 一次性迭代器，递归调用之间共享读到哪了
        def build() -> Node:
            node = Node(next(tokens), [])
            for _ in range(next(tokens)):         # 读到几个孩子，就递归建几棵子树
                node.children.append(build())
            return node
        return build()
```

**例题：** LC 426 将二叉搜索树转化为排序的双向链表

把二叉搜索树原地转成已排序的循环双向链表（`left` 当前驱、`right` 当后继，首尾相连），返回最小节点。结点数 `0..2000`，值互不相同。

```python
def tree_to_doubly_list(root: Node | None) -> Node | None:
    if root is None:
        return None
    first = prev = None
    def inorder(node: Node | None) -> None:    # 中序：左 -> 根 -> 右
        nonlocal first, prev
        if node is None:
            return
        inorder(node.left)
        if prev:
            prev.right, node.left = node, prev # 把上一个节点和当前节点互相连上
        else:
            first = node                       # 中序第一个节点就是最小值
        prev = node
        inorder(node.right)                    # 此时 node.right 还没被改过
    inorder(root)
    first.left, prev.right = prev, first       # 首尾相连成环
    return first
```

**例题：** LC 450 删除二叉搜索树中的节点

二叉搜索树的根 `root` 和 `key`，删除值为 `key` 的节点并保持 BST 性质，返回根节点。结点数 `0..10^4`，值唯一，期望 `O(h)`。

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
