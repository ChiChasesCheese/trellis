---
id: tlc-tt-path-sum-n-ary-prefix-sum-0-whole
node: p3.tt-path-sum-n-ary-prefix-sum
type: qa
---
## Q
**N 叉树路径和（前缀和加哈希）**｜Medium · 近一年被问：美国 3 次、国内 3 次 · 最近 2026-05-30（美国面试记录）

给一棵 N 叉树（每个节点有整数值 `val` 和孩子列表 `children`）和整数 `target`，统计所有**自上而下**的路径条数，使路径上的节点值之和等于 `target`：路径不必从根开始，也不必在叶子结束，但只能从节点往它的孩子方向走。面试官不接受对每个节点都向下暴力搜索的 `O(n · h)`，要求 `O(n)`。节点数 `0 <= n <= 10^5`，`-10^9 <= val, target <= 10^9`（值可以为负），树可能很深（退化成链）。例：`10 -> [5 -> [3 -> [3, -2], 2 -> [1]], -3 -> [11]]`，`target = 8` → `3`（路径 `5 -> 3`、`5 -> 2 -> 1`、`-3 -> 11`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前缀和加哈希计数：DFS 时维护「根到当前节点」的前缀和 `cur`，用 `Counter` 记录这条根路径上每个前缀和出现的次数；以当前节点结尾、和为 `target` 的路径条数，就是 `Counter` 里前缀和 `cur - target` 出现的次数；进入孩子前登记 `cur`，离开节点时撤销（回溯）。递归 DFS，`O(n)` 时间。

**识别。** 「路径不必从根开始」的子路径和，是「子数组和」在树上的版本：数组上用前缀和加哈希（LC 560），树上就把「根到当前节点」看成一个数组，沿着这条链做同样的事。因为值可以为负，滑动窗口不适用，必须用前缀和计数。树可能退化成 `10^5` 层的链，递归深度要留意（见易错点）。

**推导。** 暴力：对每个节点向下 DFS，累加路径和，`O(n · h)`，链状树是 `O(n^2)`。浪费：从不同起点出发的向下搜索重复走了同一段路径。洞察：路径 `a -> ... -> b` 的和等于 `prefix[b] - prefix[a的父亲]`，所以以 `b` 结尾的合法路径数，就是根到 `b` 这条链上、满足 `prefix[a的父亲] = prefix[b] - target` 的祖先个数。一个哈希表记录当前链上各前缀和的出现次数，`O(1)` 查询；回溯时把当前节点的前缀和减一，保证哈希表里始终只有当前链上的前缀和。

```python
from collections import Counter


def path_sum(root: Node | None, target: int) -> int:
    """统计自上而下的路径条数（起点终点任意，只能往孩子方向走），路径和等于 target。"""
    seen = Counter({0: 1})                        # 前缀和 -> 当前根到当前节点这条链上出现的次数；空前缀 0 出现 1 次

    def dfs(node: Node | None, prefix: int) -> int:   # prefix：根到 node 的父亲的前缀和
        if node is None:
            return 0
        cur = prefix + node.val                   # 根到 node 的前缀和
        ans = seen[cur - target]                  # 以 node 结尾、和为 target 的路径数（先查询）
        seen[cur] += 1                            # 进入：再登记 cur，供子孙节点配对
        for child in node.children:
            ans += dfs(child, cur)
        seen[cur] -= 1                            # 离开：撤销（回溯），兄弟分支看不到它
        return ans

    return dfs(root, 0)
```

运行：开头的树 `target = 8` → `3`；`Node(0, [Node(0), Node(0)])`、`target = 0` → `5`（三个单点路径加两条根到孩子的路径）；`None` → `0`；`Node(5)`、`target = 5` → `1`，`target = 6` → `0`，`target = 0` → `0`；`10^5` 层的全 `1` 链、`target = 3` 在默认递归上限下抛 `RecursionError`，调高上限后 → `99998`。

**复杂度。** 时间 `O(n)`（每个节点进入、离开各一次，哈希表操作 `O(1)`），空间 `O(h)`（递归栈与哈希表，最坏链状树 `O(n)`）。

**易错点。**
- 忘记初始的 `seen[0] = 1`：从根开始的路径（前缀和直接等于 `target`）漏掉，`Node(5)`、`target = 5` 得到 `0`，正确是 `1`。
- 先登记 `seen[cur] += 1` 再查询：`target = 0` 时会把「空路径」数进去，`Node(5)`、`target = 0` 得到 `1`，正确是 `0`；顺序是先查询、后登记。
- 不回溯：兄弟分支的前缀和留在哈希表里。树 `Node(3, [Node(-4, [Node(-1, [Node(4)]), Node(0)])])`、`target = 3`，正确是 `2`（`3` 单点、`-1 -> 4`），不撤销得到 `3`。
- 递归深度：链状树深度 `10^5`，CPython 默认递归上限约 1000，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见追问）。

**追问。**
- 二叉树版本（LC 437）：同一个算法，把 `children` 换成 `left`、`right`。
- 只统计向上的路径（从节点走向祖先）：同样的前缀和，换成“自底向上”的方向定义，或者对每个节点向上累加，面试里说明区别即可。
- 返回所有路径本身：哈希表里存前缀和对应的祖先下标列表，找到后截取当前链上的片段。
- 不想递归（树很深）：显式栈，栈里放 `(节点, 父亲的前缀和)`，节点为 `None` 的项是「退出标记」，弹出时撤销登记，模拟递归返回时的回溯：
```python
from collections import Counter


def path_sum_stack(root: Node | None, target: int) -> int:
    """统计自上而下的路径条数（起点终点任意，只能往孩子方向走），路径和等于 target。"""
    if root is None:
        return 0
    seen = Counter({0: 1})                        # 前缀和 -> 当前根到当前节点这条链上出现的次数；空前缀 0 出现 1 次
    ans = 0
    stack: list[tuple[Node | None, int]] = [(root, 0)]    # (节点, 父亲的前缀和)；node 为 None 表示「退出」标记
    while stack:
        node, prefix = stack.pop()
        if node is None:
            seen[prefix] -= 1                     # 离开某个节点：撤销它的前缀和（回溯）
            continue
        cur = prefix + node.val                   # 根到 node 的前缀和
        ans += seen[cur - target]                 # 以 node 结尾、和为 target 的路径数
        seen[cur] += 1
        stack.append((None, cur))                 # 先压退出标记，它会在所有孩子处理完之后弹出
        stack.extend((child, cur) for child in node.children)
    return ans
```

**同模式。** LC 437 路径总和 III、LC 560 和为 K 的子数组、LC 1248 统计优美子数组、LC 974 和可被 K 整除的子数组。
