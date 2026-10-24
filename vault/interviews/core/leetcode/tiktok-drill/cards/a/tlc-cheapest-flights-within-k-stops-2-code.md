---
id: tlc-cheapest-flights-within-k-stops-2-code
node: a.cheapest-flights-within-k-stops
type: qa
step: 2
---
## Q
**LC 787 K 站中转内最便宜的航班**｜写出 Python 实现

`n` 个城市（`2 <= n <= 100`），航班列表 `flights`（`[from, to, price]`，价格 `1` 到 `10^4`，无重复、无自环，至多 `n * (n - 1) / 2` 条），出发地 `src`、目的地 `dst`（`src != dst`）和 `k`（`0 <= k < n`）。返回最多中转 `k` 次的最低价格，没有这样的路线返回 `-1`。

## A
**思路。** 距离数组 `dist`，起点为 `0`，其余为无穷。循环 `k + 1` 轮，每轮复制一份 `nxt`，遍历所有航班，用旧 `dist` 更新 `nxt`；轮末 `dist = nxt`。最后读 `dist[dst]`。

```python
from math import inf

def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    dist: list[float] = [inf] * n
    dist[src] = 0
    for _ in range(k + 1):                  # 最多 k 个中转 = 最多 k + 1 条边：松弛 k + 1 轮
        nxt = dist[:]                       # 每轮只用上一轮的结果，否则一轮里会连走多条边
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == inf else int(dist[dst])
```

运行：示例 1（`k = 1`）→ `700`，示例 2（`k = 1`）→ `200`，示例 3（`k = 0`）→ `500`，`n = 3`、`flights = [[0,1,5]]`、`src = 0`、`dst = 2`、`k = 2` → `-1`。

**复杂度。** 时间 `O(k * E)`：`k + 1` 轮，每轮扫描全部航班；空间 `O(n)`：`dist` 与 `nxt` 两个数组。

**写法要点。**
- `from math import inf`，用 `inf` 表示不可达；`dist[u] + w` 在 `dist[u]` 是 `inf` 时仍是 `inf`，比较自然为假，不需要额外判断。
- `dist[:]` 复制整个数组，`O(n)`；复制比“在原数组上就地松弛再用一个旧值数组”更直接。
- `for u, v, w in flights` 把航班三元组直接解包。
- 类型标注 `list[float]`，因为 `inf` 是浮点数；返回时对有限值转成 `int`。
- 不需要邻接表：Bellman-Ford 遍历边列表即可。
