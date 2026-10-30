---
id: tlc-binary-tree-maximum-path-sum-0-whole
node: p2.binary-tree-maximum-path-sum
type: qa
---
## Q
**LC 124 二叉树中的最大路径和**｜Hard · LC TikTok 热度 62/100（近 6 个月） · 近一年被问：美国 5 次、国内 0 次 · CodeTop 国内累计 79 次 · 最近 2026-10-13（CodeTop）

二叉树中的**路径**是一条节点序列，相邻节点之间有边，同一个节点在序列中至多出现一次；路径至少包含一个节点，不一定经过根节点。**路径和**是路径中各节点值的总和。给根节点 `root`，返回其最大路径和。树中节点数目范围 `[1, 3 * 10^4]`，`-1000 <= Node.val <= 1000`。例：`root = [1,2,3]` → `6`（`2 -> 1 -> 3`）；`root = [-10,9,20,null,null,15,7]` → `42`（`15 -> 20 -> 7`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 后序遍历（先孩子、后父亲）：对每个节点算「向下延伸的最大单链和」`gain`，负的一侧舍弃；以该节点为最高点的路径和是 `val + 左增益 + 右增益`，全局取最大；向父亲返回时只能选一侧：`val + max(左, 右)`。`O(n)`。

**识别。** 「树上任意两点之间的路径」→ 每条路径都有唯一的最高点（拐点）；枚举拐点 + 左右各取一条向下的单链，是树形 DP（DP on trees）的标准套路。节点值可以是负数，负的子树不要。`n = 3×10^4`，一条链的深度也是 `3×10^4`，递归需要注意栈。

**推导。** 暴力：枚举所有点对，求路径和，`O(n^2)` 个点对（还要算路径）→ 浪费：路径可以按最高点归类，每个节点只需要知道左右两边「向下最好能走多远」 → 子树只需向父亲汇报一个数（单链的最大和），父亲再把左右两个汇报合并成「穿过自己的路径」的候选答案。下面用显式栈做后序，避免深树递归。

```python
def max_path_sum(root: TreeNode | None) -> int:
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

运行：`[1,2,3]` → `6`，`[-10,9,20,null,null,15,7]` → `42`，`[-3]` → `-3`，`[2,-1]` → `2`，`[-2,-1]` → `-1`；3×10^4 个节点的链（每个值为 `1`）→ `30000`。

**复杂度。** 时间 `O(n)`：每个节点常数次操作；空间 `O(n)`：`order` 与 `gain`。

**易错点。**
- 负增益必须舍弃：`max(gain, 0)`。漏掉时 `[2,-1]` 得 `1`（把 `-1` 也加进来），正确是 `2`。
- 返回给父亲的只能是**一侧**：把 `val + left + right` 作为返回值，`[1,2,3,null,null,4,5]` 会得到 `15`（拼出一条分叉的非法「路径」），正确是 `12`（`4 → 3 → 5`）。
- 初值不能是 `0`：所有节点为负时答案是负数（`[-3]` → `-3`），`best` 要用 `root.val` 或 `-inf` 初始化。

**追问。**
- 返回路径本身：在每个节点记录「最好的一侧是左还是右」，最后沿最高点向两边回溯。
- 路径必须从根出发（LC 112 / 437 一类）：只有单链，去掉「左右合并」那一步。
- 递归写法：更短，面试里常写；3×10^4 深的链需要 `sys.setrecursionlimit`。

**同模式。** LC 543 二叉树的直径、LC 687 最长同值路径、LC 337 打家劫舍 III、LC 968 监控二叉树。
