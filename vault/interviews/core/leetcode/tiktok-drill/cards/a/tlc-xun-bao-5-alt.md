---
id: tlc-xun-bao-5-alt
node: a.xun-bao
type: qa
step: 5
---
## Q
**LCP 13 寻宝**｜另一种解法

不做压缩，直接在完整状态上搜索怎么写？它适合什么规模，和「BFS + 状态压缩 DP」怎么选？

## A
**思路。** 状态 `(行, 列, 已触发集合, 手里是否有石头)`。走一步花 `1`；在石堆拿起、在未触发的机关放下都免费；到达 `T` 且机关全部触发即结束。花费只有 `0` 和 `1`，用 Dijkstra 扩展。

```python
import heapq
from math import inf


def minimal_steps_state_search(maze: list[str]) -> int:
    cells = {(r, c): ch for r, row in enumerate(maze) for c, ch in enumerate(row)}
    start = next(p for p, ch in cells.items() if ch == "S")
    target = next(p for p, ch in cells.items() if ch == "T")
    mech = {p: i for i, p in enumerate(p for p, ch in cells.items() if ch == "M")}
    full = (1 << len(mech)) - 1
    begin = (*start, 0, 0)
    dist = {begin: 0}
    heap = [(0, begin)]
    while heap:
        d, state = heapq.heappop(heap)
        if d > dist[state]:
            continue
        r, c, mask, carry = state
        if (r, c) == target and mask == full:
            return d
        moves = []
        if cells[r, c] == "O" and not carry:
            moves.append(((r, c, mask, 1), 0))
        if (r, c) in mech and carry and not mask >> mech[r, c] & 1:
            moves.append(((r, c, mask | 1 << mech[r, c], 0), 0))
        for p in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if cells.get(p, "#") != "#":
                moves.append(((*p, mask, carry), 1))
        for nxt, w in moves:
            if d + w < dist.get(nxt, inf):
                dist[nxt] = d + w
                heapq.heappush(heap, (d + w, nxt))
    return -1
```

运行：`["S#O","M..","M.T"]` → `16`，`["S#O","M.#","M.T"]` → `-1`。

**取舍。** 状态完整，Dijkstra 必然正确，不依赖「搬石头可压缩成往返」。状态数约 `行 * 列 * 2^k * 2`：小迷宫只有几千个；`100 × 100`、`16` 个机关约 `1.3 * 10^9`，不可行。压缩解法的状态是 `2^k * k`，与迷宫大小无关，是正式答案；本写法用于小数据对照。
