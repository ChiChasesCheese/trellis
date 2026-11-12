---
slug: minimum-cost-path-with-even-xor-parity
---
## Q
**LC 4100 平衡异或路径的最小开销**｜Hard

带边权的树，节点有值 `values`。若路径（含两端）上所有节点值的异或含偶数个置位，则路径平衡。求平衡路径（两端不同）的最小开销，无则 `-1`。

## A
**一句话。** 每点缩成置位奇偶 `par`，边权为正，最优路径只会是「两端同奇偶的单边」或「`1-0-1` 两条边」。

```python
def min_cost_balanced_path(edges, values):
    n = len(values)
    par = [v.bit_count() & 1 for v in values]
    odd = [[] for _ in range(n)]   # odd[b]：b 到 par=1 邻居的边权
    ans = inf
    for u, v, c in edges:
        if par[u] == par[v]:
            ans = min(ans, c)      # 单边合法
        if par[v] == 1:
            odd[u].append(c)
        if par[u] == 1:
            odd[v].append(c)
    for b in range(n):
        if par[b] == 0 and len(odd[b]) >= 2:   # 1-0-1
            ans = min(ans, sum(nsmallest(2, odd[b])))
    return -1 if ans == inf else ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只考虑单边：示例 1 没有同奇偶的边，得 `-1`，应为 `7`。
- 两条边不要求中点 `par = 0`：`par=[1,0,0]` 的 `1-0-2` 只含一个 `1`，不合法。
- 用 `values[i] & 1` 当奇偶：`1` 与 `2` 的异或 `3` 有两个置位，合法，按末位会判成不合法。

**追问。**
- 为什么更长的路径不用考虑？：长路径可以拆成更短的合法子路径，且边权为正，开销只会更大。

**同模式。** LC 124 二叉树中的最大路径和、LC 543 二叉树的直径、LC 2246 相邻字符不同的最长路径
