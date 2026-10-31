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
- LC 543 二叉树的直径（高频）
- LC 508 出现次数最多的子树元素和（高频）
- LC 2673 使二叉树所有路径值相等的最小代价（高频）
- 二叉树最大路径和（并输出路径）（高频）

**最近公共祖先 / 距离**
- LC 236 二叉树的最近公共祖先
- LC 863 二叉树中所有距离为 K 的结点（DFS 建父指针，再 BFS）
- LC 2385 感染二叉树需要的总时间（高频）

**前序下传信息 + 哈希**
- LC 437 路径总和 III
- N 叉树路径和（前缀和加哈希）（高频）

**构造与序列化**
- LC 105 从前序与中序遍历序列构造二叉树
- LC 297 二叉树的序列化与反序列化
- LC 428 序列化和反序列化 N 叉树
- LC 889 从前序与后序遍历序列构造二叉树（高频）
- LC 2196 根据描述创建二叉树（高频）

**树 + 双向链表**
- LC 426 将二叉搜索树转化为排序的双向链表（中序 DFS，接前驱指针）
- LC 430 扁平化多级双向链表（高频）
- 展平多级链表（值为空的嵌套节点要排除）（高频）

**BST 相关（中序性质）**
- LC 450 删除二叉搜索树中的节点
- LC 98 验证二叉搜索树（高频）
- LC 230 二叉搜索树中第 K 小的元素（高频）
- LC 99 恢复二叉搜索树（高频）

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

**例题：** LC 543 二叉树的直径

给一棵二叉树的根节点，返回该树的**直径**：树中任意两个节点之间最长路径的长度，路径可能经过也可能不经过根节点，长度用路径上的**边数**表示。树中节点数在 `[1, 10^4]`，`-100 <= Node.val <= 100`。

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

**例题：** LC 508 出现次数最多的子树元素和

给二叉树的根结点 `root`，返回出现次数最多的**子树元素和**；如果有多个和出现次数并列最多，全部返回（顺序不限）。一个结点的子树元素和，是以它为根的子树上所有结点（含它自己）的值之和。节点数在 `[1, 10^4]`，`-10^5 <= Node.val <= 10^5`。

```python
from collections import Counter
def find_frequent_tree_sum(root: TreeNode | None) -> list[int]:
    freq: Counter[int] = Counter()
    def subtree_sum(node: TreeNode | None) -> int:
        if node is None:
            return 0
        s = node.val + subtree_sum(node.left) + subtree_sum(node.right)
        freq[s] += 1
        return s
    subtree_sum(root)
    top = max(freq.values(), default=0)
    return [s for s, c in freq.items() if c == top]
```

**例题：** LC 2673 使二叉树所有路径值相等的最小代价

给整数 `n`，表示一棵满二叉树的节点数，节点编号 `1` 到 `n`，根是 `1`，每个非叶子节点 `i` 的左孩子是 `2 * i`、右孩子是 `2 * i + 1`。数组 `cost`（下标从 `0` 开始，长度 `n`）中 `cost[i]` 是节点 `i + 1` 的值。每次操作可以把任意一个节点的值加 `1`，次数不限。要让根到每个叶子的路径值（路径上所有节点值之和）都相等，求最少的操作次数。`3 <= n <= 10^5`，`n + 1` 是 `2` 的幂，`1 <= cost[i] <= 10^4`。

```python
def min_increments(n: int, cost: list[int]) -> int:
    c = [0] + cost
    ans = 0
    for i in range(n // 2, 0, -1):
        left, right = c[2 * i], c[2 * i + 1]
        ans += abs(left - right)
        c[i] += max(left, right)
    return ans
```

**例题：** 二叉树最大路径和（并输出路径）

二叉树的每个节点有整数值（可以为负）。路径是树中一条相连的节点序列，每个节点至多出现一次，不要求经过根或叶子；路径和是路径上节点值之和。求路径和的最大值，**并返回取得最大和的那条路径**（节点序列）。节点数 `1 <= n <= 3 * 10^4`，`-1000 <= val <= 1000`，树可能退化成一条链。

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
def max_path_sum(root: TreeNode) -> tuple[int, list[TreeNode]]:
    gain: dict[TreeNode, int] = {}
    down: dict[TreeNode, TreeNode | None] = {}
    best, peak = root.val, root
    def dfs(node: TreeNode | None) -> int:
        nonlocal best, peak
        if node is None:
            return 0
        left, right = max(dfs(node.left), 0), max(dfs(node.right), 0)
        down[node] = node.left if left and left >= right else node.right if right else None
        gain[node] = node.val + max(left, right)
        if node.val + left + right > best:
            best, peak = node.val + left + right, node
        return gain[node]
    dfs(root)
    def arm(child: TreeNode | None) -> list[TreeNode]:
        chain = []
        while child:
            chain.append(child)
            child = down[child]
        return chain
    left_arm = arm(peak.left) if peak.left and gain[peak.left] > 0 else []
    right_arm = arm(peak.right) if peak.right and gain[peak.right] > 0 else []
    return best, left_arm[::-1] + [peak] + right_arm
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

**例题：** N 叉树路径和（前缀和加哈希）

给一棵 N 叉树（每个节点有整数值 `val` 和孩子列表 `children`）和整数 `target`，统计所有**自上而下**的路径条数，使路径上的节点值之和等于 `target`：路径不必从根开始，也不必在叶子结束，但只能从节点往它的孩子方向走。面试官不接受对每个节点都向下暴力搜索的 `O(n · h)`，要求 `O(n)`。节点数 `0 <= n <= 10^5`，`-10^9 <= val, target <= 10^9`（值可以为负），树可能很深（退化成链）。

```python
from collections import Counter
def path_sum(root: Node | None, target: int) -> int:
    """统计自上而下的路径条数（起点终点任意，只能往孩子方向走），路径和等于 target。"""
    seen = Counter({0: 1})
    def dfs(node: Node | None, prefix: int) -> int:
        if node is None:
            return 0
        cur = prefix + node.val
        ans = seen[cur - target]
        seen[cur] += 1
        for child in node.children:
            ans += dfs(child, cur)
        seen[cur] -= 1
        return ans
    return dfs(root, 0)
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

**例题：** LC 430 扁平化多级双向链表

给一个双向链表，每个节点有 `val`、`prev`、`next`，还有一个 `child` 指针；`child` 可以指向另一条独立的双向链表，子链表的节点同样可以有自己的 `child`，层层嵌套。把整个结构扁平化成单层双向链表：带子链表的节点 `curr` 的子链表必须出现在 `curr` 之后、`curr.next` 之前；所有 `child` 置为 `null`；返回扁平链表的头。节点数不超过 `1000`，`1 <= Node.val <= 10^5`，输入可能是空链表。

```python
def flatten(head: 'Node | None') -> 'Node | None':
    def dfs(node: Node) -> Node:
        tail = node
        while node:
            nxt = node.next
            tail = node
            if node.child:
                child_tail = dfs(node.child)
                node.next = node.child
                node.child.prev = node
                child_tail.next = nxt
                if nxt:
                    nxt.prev = child_tail
                node.child = None
                tail = child_tail
            node = nxt
        return tail
    if head:
        dfs(head)
    return head
```

**例题：** 展平多级链表（值为空的嵌套节点要排除）

多级双向链表的每个节点有 `val`、`prev`、`next`、`child`；`child` 指向一条可继续嵌套的子链表，子链表放在该节点之后、它原来的后继之前。把它展平成单层双向链表，变化是：作为「嵌套入口」的节点自己的 `val` 为 `None`（空），它不能出现在结果里，但它的 `child` 仍要展开。所有保留节点的 `child` 置空，`prev`/`next` 重新连好，返回新链表的头；没有任何有值节点时返回 `None`。节点数不超过 `1000`。

```python
def flatten_skip_empty(head: 'Node | None') -> 'Node | None':
    order: list[Node] = []
    def collect(node: Node | None) -> None:
        while node:
            order.append(node)
            collect(node.child)
            node = node.next
    collect(head)
    new_head: Node | None = None
    tail: Node | None = None
    for node in order:
        node.child = None
        if node.val is None:
            continue
        node.prev, node.next = tail, None
        if tail:
            tail.next = node
        else:
            new_head = node
        tail = node
    return new_head
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
