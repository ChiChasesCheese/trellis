# 09 · 二叉树与最近公共祖先（Trees & LCA）

> 本讲覆盖：LC 236 Lowest Common Ancestor of a Binary Tree · 124 Binary Tree Maximum Path Sum（Hard）· 199 Binary Tree Right Side View · 297 Serialize and Deserialize Binary Tree（Hard）
> 前置：递归（函数调用自己）、第 06 讲的 BFS / `deque`。树的概念从零讲。
> 读完你应该能：(1) 用「相信子树，返回值 + 合并」的套路写任何后序 DFS；(2) 区分「返回给父节点的值」和「更新全局答案的值」；(3) 对每道题说出递归深度风险与迭代替代方案。

## 1. 这个模式是什么，为什么存在

### 1.1 树是什么（从零讲）

- **二叉树（binary tree）**：每个节点最多有两个孩子 `left`、`right`；没有环。最上面的节点叫根（root），没有孩子的叫叶子（leaf）。
- **子树（subtree）**：任意节点连同它下面所有后代构成的树——**子树本身也是一棵二叉树**。这个自相似性就是递归的来源。
- **高度 / 深度**：从根到最远叶子的节点数。平衡的树高 ≈ log n，退化成链（skewed）时高 = n。
- **遍历（traversal）**：前序（根 左 右）、中序（左 根 右）、后序（左 右 根）都是 DFS 的变体；层序（level order）是 BFS。二叉搜索树（BST）的中序遍历是升序。

### 1.2 从最笨的解法开始

LC 236：找二叉树中两个节点 `p`、`q` 的最近公共祖先。最笨的做法：分别找出根到 `p` 的路径和根到 `q` 的路径（两个列表），然后同时从头走，最后一个相同的节点就是答案。O(n) 时间，O(n) 额外空间，并且要遍历树两到三次。

### 1.3 慢在哪里 / 能改进什么

路径列表是**多余的信息**。我们真正需要的只是：「p 和 q 在哪个节点第一次**分到不同子树**」。

> 因果链：对每个节点问两个子树各自的问题——「你那边有 p 或 q 吗？」→ 如果左右两边**都说有**，当前节点就是分叉点，即 LCA → 一次后序 DFS（先问孩子，再合并）就够了，不需要路径。

### 1.4 树递归的统一套路

```text
def solve(node):
    if node is None: return <空树的答案>        # base case
    left  = solve(node.left)                    # 相信子树：它们会返回正确的答案
    right = solve(node.right)
    return combine(node, left, right)           # 只做「合并」这一件事
```

关键一问：**我要向父节点返回什么？** 它和**我要用来更新答案的东西**经常是两回事（见 LC 124：返回「单边最大下行和」，答案却是「左 + 根 + 右」的折线）。
同样模板的 BFS 版本是 `deque` + 「冻结层大小」。

## 2. 模板与逐行讲解

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(values):
    """Level-order list with None holes, like LeetCode: [3,9,20,None,None,15,7]."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    for node in queue:
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root

def find(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)

# Template T1: recursive DFS = "trust the children, combine at the root"
def height(node):
    if node is None:                      # base case: empty tree
        return 0
    left = height(node.left)              # answer for the left subtree
    right = height(node.right)            # answer for the right subtree
    return 1 + max(left, right)           # combine

# Template T2: BFS by levels with a deque
def levels(root):
    out = []
    queue = deque([root] if root else [])
    while queue:
        out.append([n.val for n in queue])
        for _ in range(len(queue)):       # freeze the size: exactly one level per outer loop
            n = queue.popleft()
            if n.left:
                queue.append(n.left)
            if n.right:
                queue.append(n.right)
    return out

# Template T3: DFS that returns one thing UP and updates another thing on the SIDE (diameter)
def diameter(root):
    best = 0
    def depth(node):
        nonlocal best
        if not node:
            return 0
        l, r = depth(node.left), depth(node.right)
        best = max(best, l + r)           # the longest path that bends at this node
        return 1 + max(l, r)              # what the parent may extend: one side only
    depth(root)
    return best

t = build_tree([3, 9, 20, None, None, 15, 7])
assert height(t) == 3
assert levels(t) == [[3], [9, 20], [15, 7]]
assert diameter(build_tree([1, 2, 3, 4, 5])) == 3
```

逐行讲解：

1. `build_tree` / `find`：测试辅助；`build_tree` 按 LeetCode 的层序数组格式（`None` 表示空位）建树，让你能快速复现题目示例。
2. `height`：最小的递归模板。`if node is None: return 0` 是**基准情形**——没有它递归永不停止。
3. `levels`：BFS。`for _ in range(len(queue))` 冻结当前层大小，循环里弹出 `len(queue)` 次，期间新入队的孩子属于下一层；`out.append([...])` 在内层循环之前取整层的值。
4. `diameter`（模板 T3）：`depth(node)` **返回**给父节点的是「从我往下的最大深度」（只能选一边）；**更新**答案用的是 `l + r`（在我这里拐弯的路径）。两件事分开，是 LC 124 / 543 / 687 一整类题的核心。
5. `nonlocal best`：在内层函数里修改外层变量必须声明；也可以把答案放在 `list` 里。

## 3. 完整手算（Worked trace）

LC 236。树如下，`p = 6`，`q = 2`，期望 LCA 是 5：

```text
        3
       / \
      5   1
     / \
    6   2
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#        3
#       / \
#      5   1
#     / \
#    6   2
t = TreeNode(3, TreeNode(5, TreeNode(6), TreeNode(2)), TreeNode(1))
p, q = t.left.left, t.left.right        # p = 6, q = 2

def lca_trace(node, p, q, depth=0):
    pad = "  " * depth
    if node is None:
        print(f"{pad}None -> return None")
        return None
    if node is p or node is q:
        print(f"{pad}node {node.val} is a target -> return it")
        return node
    print(f"{pad}enter {node.val}")
    left = lca_trace(node.left, p, q, depth + 1)
    right = lca_trace(node.right, p, q, depth + 1)
    if left and right:
        print(f"{pad}node {node.val}: left={left.val} right={right.val} -> split point, return {node.val}")
        return node
    res = left or right
    print(f"{pad}node {node.val}: left={left and left.val} right={right and right.val} -> pass up {res and res.val}")
    return res

assert lca_trace(t, p, q).val == 5
```

```text
enter 3
  enter 5
    node 6 is a target -> return it
    node 2 is a target -> return it
  node 5: left=6 right=2 -> split point, return 5
  enter 1
    None -> return None
    None -> return None
  node 1: left=None right=None -> pass up None
node 3: left=5 right=None -> pass up 5
```

读法（缩进表示递归深度）：
- 进入 3 → 进入 5 → 左孩子 6 本身就是目标，直接返回；右孩子 2 也是目标，返回。
- 在节点 5：`left=6` 且 `right=2` 都非空 → 5 就是分叉点，返回 5。
- 回到节点 3：右子树 1 里什么都没找到（返回 `None`），所以 `left or right` = 5，原样向上传。
- 如果 `p` 是 `q` 的祖先（例如 p=5, q=6）：遇到 5 立刻返回 5，不再往下找——这正确，因为 5 本身就是 LCA。

## 4. 题目

### 4.1 LC 236 · Lowest Common Ancestor of a Binary Tree（Medium，频率 75）

```python
# solutions/236_lowest_common_ancestor.py
def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root                                  # found a target (or fell off the tree)
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:                               # p and q are in different subtrees -> root splits them
        return root
    return left or right                             # both targets are on one side (or absent)
```

- **一句话洞见**：后序 DFS——遇到 `p` 或 `q` 就返回自己；左右都返回非空的节点就是分叉点；否则把非空的那一边往上传。
- **复杂度**：时间 O(n)，空间 O(h)（递归栈，h 为树高）。
- **BST 版本（LC 235）**：利用有序性，从根往下：两个值都小于当前就走左，都大于就走右，否则当前就是 LCA，O(h)。

**资深追问**

- **规模 ×1000**：树深可能达到 10⁶，Python 递归会爆栈：改成**带父指针的迭代**——先 DFS/BFS 建 `parent` 字典，再沿 `p` 的祖先链打标记，从 `q` 往上走遇到第一个已标记的节点（或 LC 1650 给了父指针时两个指针交替走）。
- **多次查询**：同一棵树上有 10⁶ 次 LCA 查询 → 预处理：欧拉序 + 稀疏表（O(n log n) 预处理，O(1) 查询）或倍增（binary lifting，O(log n)）。
- **流式 / 分布式**：树被分片存储时，每片返回「是否包含 p / q / 已找到的 LCA」的小结构，由上层合并；LCA 的合并是结合的。
- **内存**：O(h)；退化为链时 O(n)。
- **并发**：树只读时，左右子树可以并行下降（fork-join）。
- **接口 / 边界**：本实现**假设 p 和 q 都在树里**；如果其中一个不在，它会返回另一个，是错的。面试中要问清楚；不保证时，用两个布尔值在 DFS 里记录两者是否都找到。节点值是否唯一？`p == q`？p 是 q 的祖先（允许，节点是自己的祖先）？
- **测试**：p 是 q 的祖先、p 与 q 分别在左右、同一子树深处、p == q、只有两个节点的树；与「路径比较」的暴力对拍。

### 4.2 LC 124 · Binary Tree Maximum Path Sum（Hard，频率 62）

```python
# solutions/124_binary_tree_maximum_path_sum.py
def max_path_sum(root):
    best = float("-inf")

    def gain(node):                                   # best path that starts at node and goes down one side
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)                # a negative branch is better dropped
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)     # path that BENDS at node (may use both sides)
        return node.val + max(left, right)            # what we may hand to the parent: one side only

    gain(root)
    return best
```

- **一句话洞见**：对每个节点，向父节点**返回**「从我往下走的最大单边和」；而**答案**是「在我这里拐弯」的路径 `val + 左 + 右`。负的分支丢掉（`max(…, 0)`）。
- **复杂度**：时间 O(n)，空间 O(h)。
- **易错**：路径至少包含一个节点，所以全为负数时答案是最大的那个负数——`best` 初值用 `-inf`，不是 0。

**资深追问**

- **规模 ×1000**：递归深度；改为迭代后序（用显式栈，或先生成后序序列再自底向上处理）。
- **流式 / 分布式**：每个子树返回 `(单边最大和, 子树内最优)` 这个小元组，父节点合并——天然可以分片计算。
- **内存**：O(h) 栈；`nonlocal best` 只有一个数。
- **并发**：左右子树独立计算，fork-join 并行；合并只涉及两个数。
- **接口**：空树怎么办（返回 `-inf`、`None`，还是抛异常）？要不要返回路径本身（需要额外记录最佳拐点和两条延伸边）？节点值是整数还是浮点？
- **测试**：全负、单节点、链状（skew）、根为负但两边为正、最优路径不经过根；与「枚举所有节点对的路径和」暴力对拍。

### 4.3 LC 199 · Binary Tree Right Side View（Medium，频率 62）

```python
# solutions/199_binary_tree_right_side_view.py
def right_side_view(root):
    if not root:
        return []
    out = []
    queue = deque([root])
    while queue:
        out.append(queue[-1].val)                 # rightmost node of this level
        for _ in range(len(queue)):               # freeze the level size, then drain exactly that many
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return out
```

- **一句话洞见**：层序遍历，每一层只取最后一个节点。
- **DFS 替代**：先右后左遍历，用 `depth == len(res)` 判断「这一层的第一个访问到的节点」，空间 O(h) 而不是 O(宽度)。
- **复杂度**：时间 O(n)，空间 O(宽度)。

**资深追问**

- **规模 ×1000**：宽度最多 n/2（满二叉树最后一层），BFS 队列可能很大；DFS 右优先只需 O(h)——**按树形选择**：矮胖用 DFS，高瘦用 BFS。
- **流式**：节点按层序流入时，每层的最后一个就是答案，边读边输出。
- **内存**：BFS O(宽度) vs DFS O(高度)。
- **并发**：层同步并行（每层的节点并行展开）；或左右子树并行，各自返回按深度的列表，再合并（右边优先）。
- **接口**：左视图、顶视图（需要列号，LC 987）怎么推广？空树返回 `[]`；返回值还是节点？
- **测试**：只有左孩子的深层（左子树更深时左边的节点也可见）、全右链、全左链、空树、单节点。

### 4.4 LC 297 · Serialize and Deserialize Binary Tree（Hard，频率 62）

```python
# solutions/297_serialize_and_deserialize_binary_tree.py
def serialize(root):
    out = []

    def walk(node):
        if not node:
            out.append("#")                   # explicit null marker makes the shape unambiguous
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(out)


def deserialize(data):
    tokens = iter(data.split(","))

    def build():
        tok = next(tokens)                    # consume in the same preorder we wrote
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left = build()
        node.right = build()
        return node

    return build()
```

- **一句话洞见**：前序遍历 + 显式空指针标记（`#`）就能唯一确定一棵树；反序列化按同样的前序顺序消费 token。只有前序**不带空标记**是不唯一的。
- **复杂度**：时间 O(n)，空间 O(n)。

**资深追问**

- **规模 ×1000**：字符串拼接 `",".join` 是线性的；巨大的树用二进制格式（varint + 位图表示空指针）并压缩（zstd）；反序列化改成按流迭代（本实现用 `iter(data.split(","))`，大数据下应改为边读边解析，避免把整个字符串切成列表）。
- **流式**：前序 + 空标记的格式天然可以边读边构造，不需要缓冲整个输入。
- **内存**：递归深度 = 树高；链状树需要迭代实现（显式栈）。
- **并发**：序列化时树被修改会得到不一致的结果 → 先拍快照 / 加读锁；左右子树序列化可并行，再按顺序拼接。
- **接口 / 契约**：核心不变量 `deserialize(serialize(t)) == t`；节点值如果是字符串，分隔符冲突需要转义或长度前缀；**格式版本号**（schema evolution）与向后兼容；非法输入（缺 token、多余 token）要报错而不是返回半棵树。
- **测试**：往返（round trip）测试覆盖：空树、单节点、左链 / 右链、含负数；模糊测试（随机生成树并往返）；格式的固定样例（golden）用来锁定兼容性。

## 5. 常见 bug

1. **忘记基准情形**（`node is None`）：无限递归或 `AttributeError`。
2. **把「返回值」和「答案」混为一谈**（LC 124 / 543）：返回单边、更新双边。
3. **LC 124 的 `best` 初值为 0**：全负数树答案错。
4. **BFS 分层时不冻结层大小**：内层用 `while queue:` 会把刚入队的下一层也一起处理，层就混了；必须用 `for _ in range(len(queue))`（`range` 只在进入循环时求一次值）。
5. **LCA 默认两个节点都在树里**：面试官一追问就露馅。
6. **序列化不带空标记**：`[1,2]` 与 `[1,null,2]` 的前序都是 `1,2`，歧义。
7. **递归过深**：Python 默认 1000；退化成链的树要用迭代。
8. **比较节点用 `==` 值比较**：LCA 用的是**对象身份**（`is`），因为值可能重复。

## 6. 自测题

1. 为什么树递归的时间复杂度是 O(n)，空间是 O(h)？
   <details><summary>答案</summary>每个节点被访问一次，每次做 O(1) 的合并；递归栈同一时刻只存当前根到节点的路径，长度最多 h。</details>
2. LC 236 中，为什么遇到 `p` 就可以直接返回而不再往下找 `q`？
   <details><summary>答案</summary>若 `q` 在 `p` 的子树里，那么 `p` 就是 LCA（节点是自己的祖先），返回 `p` 正确；若 `q` 不在 `p` 下面，`q` 会在别处被找到，两边合并时 `p` 与 `q` 的公共祖先在更上层被识别。</details>
3. LC 124 里 `max(gain(node.left), 0)` 的意义？
   <details><summary>答案</summary>如果某一边的最大下行和是负数，不要它（路径可以选择不向这边延伸），因此下限取 0。</details>
4. 小编程：求二叉树的最大深度（LC 104）和判断是否平衡（LC 110）。
   <details><summary>答案</summary>`depth(node) = 0 if None else 1 + max(depth(l), depth(r))`。平衡：后序里返回高度，发现左右高度差 > 1 就返回 −1 表示不平衡并一路向上传，O(n)。</details>
5. BST 的 LCA 为什么比普通二叉树简单？
   <details><summary>答案</summary>BST 的有序性：若 p、q 都小于当前节点就去左边，都大于就去右边，否则当前节点就是分叉点；O(h) 且无需遍历全树。</details>
6. 资深追问：10⁶ 次 LCA 查询怎么办？
   <details><summary>答案</summary>离线：Tarjan 的并查集算法；在线：欧拉序 + 稀疏表（RMQ）O(1) 查询，或倍增法 O(log n) 查询。预处理 O(n log n) 摊到查询上。</details>
