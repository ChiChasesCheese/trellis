---
slug: reconstruct-itinerary
---
## Q
**LC 332 重新安排行程**｜Hard

用完所有机票 `tickets`（一张一次），从 `JFK` 出发，返回字典序最小的行程。保证有解。

## A
**一句话。** 求欧拉路径（Hierholzer 算法）：DFS 每次走最小的未用边，走进死胡同才入结果，最后反转。

```python
def find_itinerary(tickets):
    g = defaultdict(list)
    for a, b in sorted(tickets, reverse=True):
        g[a].append(b)         # 逆序放，pop() 取到最小
    route = []

    def dfs(u):
        while g[u]:
            dfs(g[u].pop())
        route.append(u)        # 后序：死胡同先入

    dfs("JFK")
    return route[::-1]
```

**复杂度。** 时间 `O(E log E)`，空间 `O(E)`。

**易错点。**
- 普通贪心不回溯：`[["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]` 先走 `KUL` 就卡死。
- 忘了反转：`route` 是后序，直接返回是倒序行程。
- 正序存入再 `pop()`：会先走字典序最大的。

**追问。**
- 为什么后序反转能得到字典序最小？：卡死的点必是终点，先入栈排最后，其余的环按尝试顺序接在前面。
- 怎么判断无解？：欧拉路径要有度数条件且边连通，最后检查 `len(route) == E + 1`。

**同模式。** LC 2097 合法重新排列数对、LC 753 破解保险箱、LC 399 除法求值
