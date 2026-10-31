---
id: tlc-binary-tree-maximum-path-sum-0-whole
node: p2.binary-tree-maximum-path-sum
type: qa
---
## Q
**LC 124 二叉树中的最大路径和**｜Hard · LC TikTok 近 6 个月热度 53/100（全时段 62） · 近一年被问：美国 5 次、国内 0 次 · CodeTop 国内累计 79 次 · 最近 2026-10-13（国内 CodeTop）

二叉树中的**路径**是一条节点序列，相邻节点之间有边，同一个节点在序列中至多出现一次；路径至少包含一个节点，不一定经过根节点。**路径和**是路径中各节点值的总和。给根节点 `root`，返回其最大路径和。树中节点数目范围 `[1, 3 * 10^4]`，`-1000 <= Node.val <= 1000`。例：`root = [1,2,3]` → `6`（`2 -> 1 -> 3`）；`root = [-10,9,20,null,null,15,7]` → `42`（`15 -> 20 -> 7`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 后序遍历（先孩子、后父亲）：对每个节点算「向下延伸的最大单链和」`gain`，负的一侧舍弃；以该节点为最高点的路径和是 `val + 左增益 + 右增益`，全局取最大；向父亲返回时只能选一侧：`val + max(左, 右)`。`O(n)`。

**识别。** 「树上任意两点之间的路径」→ 每条路径都有唯一的最高点（拐点）；枚举拐点 + 左右各取一条向下的单链，是树形 DP（DP on trees）的标准套路。节点值可以是负数，负的子树不要。`n = 3×10^4`，`O(n)` 的一遍后序遍历就够，递归写法最直观；一条链的深度也是 `3×10^4`，要留意递归上限。

**推导。** 暴力：枚举所有点对，求路径和，`O(n^2)` 个点对（还要算路径）→ 浪费：路径可以按最高点归类，每个节点只需要知道左右两边「向下最好能走多远」 → 子树只需向父亲汇报一个数（单链的最大和），父亲再把左右两个汇报合并成「穿过自己的路径」的候选答案。

**简单解法。** 枚举最高点：对每个结点现算左右两条向下单链（`down`，负的舍弃），不复用结果。

```python
def max_path_sum(root: TreeNode | None) -> int:
    def down(node: TreeNode | None) -> int:        # 从 node 往下走的最大单链和，现算、不缓存
        if node is None:
            return 0
        return node.val + max(down(node.left), down(node.right), 0)

    def dfs(node: TreeNode | None) -> int:         # 每个结点都当一次最高点
        if node is None:
            return -(10 ** 9)
        through = node.val + max(down(node.left), 0) + max(down(node.right), 0)
        return max(through, dfs(node.left), dfs(node.right))

    return dfs(root)
```

时间 `O(n·h)`、最坏单链 `O(n^2)`，空间 `O(h)`；`down` 被反复重算，链状的 `3 * 10^4` 结点会超时，后序一遍把单链和顺手返回就是最优解。

最优解：

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

运行：`[1,2,3]` → `6`，`[-10,9,20,null,null,15,7]` → `42`，`[-3]` → `-3`，`[2,-1]` → `2`，`[-2,-1]` → `-1`；3×10^4 个节点的链（每个值为 `1`）在默认递归上限下抛 `RecursionError`，把上限调到 100000 后 → `30000`。

**复杂度。** 时间 `O(n)`：每个节点访问一次、常数次操作；空间 `O(h)`：递归栈，`h` 是树高，链状树时 `O(n)`。

**拓展优化。**
- 返回最大路径本身：多记每个结点向下最好的一侧和取得最大值的最高点，最后从最高点向两侧走一遍；时间仍是 `O(n)`。

```python
def max_path_nodes(root: TreeNode) -> list[TreeNode]:
    best, top = root.val, root
    gain: dict[TreeNode, int] = {}                 # 从结点向下的最大单链和
    nxt: dict[TreeNode, TreeNode | None] = {}      # 这条最好的单链下一步走哪个孩子

    def dfs(node: TreeNode | None) -> int:
        nonlocal best, top
        if node is None:
            return 0
        left, right = max(dfs(node.left), 0), max(dfs(node.right), 0)
        if node.val + left + right > best:
            best, top = node.val + left + right, node
        nxt[node] = node.left if left >= right and left > 0 else node.right if right > 0 else None   # 单链往增益更大的正一侧走
        gain[node] = node.val + max(left, right)
        return gain[node]

    dfs(root)
    # 以最高点 top 为中心，左右各沿 nxt 走下去（只有增益为正的一侧才走）
    left_chain: list[TreeNode] = []
    cur = top.left if gain.get(top.left, 0) > 0 else None
    while cur:                                     # 从最高点往左下走，得到由近到远的链
        left_chain.append(cur)
        cur = nxt[cur]
    right_chain: list[TreeNode] = []
    cur = top.right if gain.get(top.right, 0) > 0 else None
    while cur:
        right_chain.append(cur)
        cur = nxt[cur]
    return left_chain[::-1] + [top] + right_chain  # 左链倒过来接最高点，再接右链
```

**易错点。**
- 负增益必须舍弃：`max(gain, 0)`。漏掉时 `[2,-1]` 得 `1`（把 `-1` 也加进来），正确是 `2`。
- 返回给父亲的只能是**一侧**：把 `val + left + right` 作为返回值，`[1,2,3,null,null,4,5]` 会得到 `15`（拼出一条分叉的非法「路径」），正确是 `12`（`4 → 3 → 5`）。
- 初值不能是 `0`：所有节点为负时答案是负数（`[-3]` → `-3`），`best` 要用 `root.val` 或 `-inf` 初始化。
- 递归深度：链状树深度为 `n = 3×10^4`，CPython 默认递归上限约 1000，会抛 `RecursionError`；要么 `sys.setrecursionlimit(100000)`，要么改成显式栈（见追问）。

**追问。**
- 路径必须从根出发（LC 112 / 437 一类）：只有单链，去掉「左右合并」那一步。
- 树很深怎么办：用显式栈，先序（根、右、左）收集节点，倒着处理就是孩子先于父亲，用字典 `gain` 记每个节点的单链和，不受递归上限影响，时间 `O(n)`、空间 `O(n)`：
```python
def max_path_sum_stack(root: TreeNode | None) -> int:
    order: list[TreeNode] = []
    stack = [root]
    while stack:                                   # 先序（根右左）收集节点：孩子总排在父亲后面
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    gain: dict[TreeNode, int] = {}                 # gain[node]：从 node 向下走的最大单链和
    best = root.val
    for node in reversed(order):                   # 倒过来 = 孩子先于父亲
        left = max(gain.get(node.left, 0), 0)      # 负收益的子树直接不要；None 不在字典里，取 0
        right = max(gain.get(node.right, 0), 0)
        best = max(best, node.val + left + right)  # 以 node 为最高点的路径
        gain[node] = node.val + max(left, right)   # 往父亲返回时只能选一边
    return best
```

**同模式。** LC 543 二叉树的直径、LC 687 最长同值路径、LC 337 打家劫舍 III、LC 968 监控二叉树。
