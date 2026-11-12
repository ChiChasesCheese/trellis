---
slug: swim-in-rising-water
---
## Q
**LC 778 水位上升的泳池中游泳**｜Hard

`n×n` 网格高度互不相同，时间 `t` 时水位为 `t`，相邻两格都被淹没才能游过去。求从左上到右下的最少时间。

## A
**一句话。** 求路径上最大高度的最小值（瓶颈路径）：小根堆做 Dijkstra，邻格入堆的键是 `max(当前键, 邻格高度)`。

```python
def swim_in_water(grid):
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]   # (所需最低水位, 行, 列)
    seen = {(0, 0)}
    while heap:
        t, x, y = heappop(heap)
        if x == y == n - 1:
            return t
        for nx, ny in [(x+1, y), (x-1, y),
                       (x, y+1), (x, y-1)]:
            if 0 <= nx < n and 0 <= ny < n \
                    and (nx, ny) not in seen:
                seen.add((nx, ny))
                h = max(t, grid[nx][ny])
                heappush(heap, (h, nx, ny))
    return -1
```

**复杂度。** 时间 `O(n² log n)`，空间 `O(n²)`。

**易错点。**
- 把 `max` 写成 `+`：当成最短路径和，示例 1 得 `4`，应为 `3`。
- 只允许向右向下：最优路线可能要向左走一段，示例 2 得 `20`，应为 `16`。
- 起点高度没计入（初始键写 `0`）：`[[3,0],[1,2]]` 得 `2`，应为 `3`。

**追问。**
- 不用堆怎么做？：二分水位加 BFS 判断连通，或并查集按高度逐格点亮。
- 换成最小体力消耗路径（LC 1631）？：边权改为相邻高度差，键仍是路径最大边权。

**同模式。** LC 1631 最小体力消耗路径、LC 1102 得分最高的路径、LC 743 网络延迟时间、LC 1514 概率最大的路径
