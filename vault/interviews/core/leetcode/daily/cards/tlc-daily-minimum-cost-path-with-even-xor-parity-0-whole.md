---
id: tlc-daily-minimum-cost-path-with-even-xor-parity-0-whole
node: math-bit-sim.minimum-cost-path-with-even-xor-parity
type: qa
---
## Q
**LC 4100 平衡异或路径的最小开销**｜Hard

给你一棵含有 `n` 个节点的树，节点编号 `0` 到 `n - 1`，用二维数组 `edges` 表示，`edges[i] = [u_i, v_i, c_i]` 表示节点 `u_i` 与 `v_i` 之间有一条开销为 `c_i` 的边；再给你长度为 `n` 的数组 `values`，`values[i]` 是节点 `i` 的值。如果两个**不同**节点之间的路径上所有节点（含两端点）的值的按位异或，在二进制中含有**偶数**个置位，则称该路径为平衡异或路径。路径的开销是它所有边开销之和。返回一条平衡异或路径的最小开销，不存在则返回 `-1`。`2 <= n <= 10^5`，`edges.length == n - 1`，`0 <= u_i, v_i <= n - 1`，`1 <= c_i <= 10^9`，`1 <= values[i] <= 10^9`，`edges` 表示一棵合法的树。例：`edges = [[0,1,4],[0,2,6],[0,3,3],[3,4,5]]`，`values = [3,1,7,1,3]` → `7`（路径 `1-0-3`，异或 `1^3^1 = 3`，开销 `4 + 3`）；`edges = [[0,1,5],[1,2,10]]`，`values = [1,7,3]` → `5`；`edges = [[0,1,5],[0,2,7],[0,3,9]]`，`values = [1,3,5,9]` → `-1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 奇偶性压缩（`popcount(a ^ b)` 的奇偶 = 两者奇偶之和）+ 局部最优：最优路径至多两条边。

**核心题。**

- LC 136 只出现一次的数字（NeetCode 150、Hot 100、Top Interview 150）：同一个异或性质：异或只依赖每个数自己的位奇偶

**一句话。** 把每个节点缩成一位 `par[i] = popcount(values[i]) mod 2`，路径合法当且仅当路径上 `par = 1` 的节点个数为偶数；边开销为正，所以最优路径只会是「两端 `par` 相同的单条边」或「`1 - 0 - 1` 的两条边」，枚举这两类取最小。

**识别。** 题面是树上的路径最值，`n = 10^5` 容易往树形 DP 或换根上想；但「异或的置位个数奇偶」只依赖每个点自己的奇偶，条件是纯奇偶计数，应当先化简再看路径结构。

**推导。** `popcount(a ^ b) ≡ popcount(a) + popcount(b) (mod 2)`，所以整条路径的异或的奇偶 = 各点 `par` 之和的奇偶，路径合法 ⇔ 其中 `par = 1` 的点数为偶数。取任意一条合法路径：若某条边的两端 `par` 相同，这条边本身就是合法路径，开销不超过原路径（开销为正）；若没有这样的边，`par` 沿路径交替，点数 `>= 4` 时必含连续的 `1,0,1`（合法、更便宜），点数为 `3` 时只有 `1,0,1` 合法（`0,1,0` 只有一个 `1`）。所以最优路径只有「同奇偶单边」和「`1,0,1` 两条边」两种。

```python
import heapq
from math import inf


def min_cost_balanced_path(edges: list[list[int]], values: list[int]) -> int:
    n = len(values)
    par = [v.bit_count() & 1 for v in values]     # 每个点的置位数奇偶
    odd_edges: list[list[int]] = [[] for _ in range(n)]   # odd_edges[b]：b 到 par=1 的邻居的边开销
    ans = inf
    for u, v, c in edges:
        if par[u] == par[v]:
            ans = min(ans, c)                     # 两点同奇偶：单边合法
        if par[v] == 1:
            odd_edges[u].append(c)
        if par[u] == 1:
            odd_edges[v].append(c)
    for b in range(n):
        if par[b] == 0 and len(odd_edges[b]) >= 2:    # 1-0-1：中点 par=0，两端 par=1
            ans = min(ans, sum(heapq.nsmallest(2, odd_edges[b])))
    return -1 if ans == inf else ans
```

运行：示例 1 → `7`（`par = [0,1,1,1,0]`，中点 `0` 的奇邻边开销 `4, 6, 3`，取 `3 + 4`）；示例 2 → `5`（`par = [1,1,1]`，边 `0-1` 同奇偶）；示例 3 → `-1`；`edges = [[0,1,1],[0,2,1]]`，`values = [1,3,3]` → `-1`。

**复杂度。** 时间 `O(n)`（`nsmallest` 对度数求和线性），空间 `O(n)`。

**易错点。**
- 只考虑单边：示例 1 没有任何两端同奇偶的边，得到 `-1`，正确是 `7`。
- 两条边时不检查中点的 `par` 是 `0`，把 `0,1,0` 也算合法：`edges = [[0,1,1],[0,2,1]]`，`values = [1,3,3]`（`par = [1,0,0]`，路径 `1-0-2` 只含一个 `1`）得到 `2`，正确是 `-1`。
- 用 `values[i] & 1` 代替置位数的奇偶：`edges = [[0,1,5]]`，`values = [1,2]` 里 `1 & 1 = 1`、`2 & 1 = 0`，判成不同奇偶得到 `-1`，正确是 `5`（`1 ^ 2 = 3`，有两个置位）。

**同模式。** LC 2246 相邻字符不同的最长路径、LC 124 二叉树中的最大路径和、LC 543 二叉树的直径、LC 687 最长同值路径。
