---
id: mlp-coding-pc06-followups
node: coding.pc06
step: 2
type: qa
---
## Q
**盛水题：追问与变体**｜编程轮

两道盛水题写完后，面试官会怎么追问？

## A
- **容器题为什么双指针不会漏掉最优解：** 固定矮的一侧不动、只动高的一侧，宽度变小、高度仍受矮的限制，面积不会变大；所以每一步移动矮的一侧是唯一可能找到更优解的动作。
- **接雨水为什么不用提前算 `right_max`：** 谁的运行最大值小，这一侧的水就已经被另一侧担保；另一侧路径上必有一根不矮于它的柱子，所以当前柱子头上的水只取决于自己这一侧见过的最高点。
- **两题的双指针不能混着讲：** 形式像，意义不同；容器题移动矮的一侧是因为它限制面积，接雨水移动运行最大值小的一侧是因为这一侧水量已定。证明很容易讲反。
- **二维版（LC 407）：** 边界格子存不住水；用最小堆从边界向内扩张，每次先处理堆里水位最低的格子，邻居积水 `max(0, 当前水位 - 邻居高度)`，邻居以 `max(当前水位, 邻居高度)` 入堆。必须用最小堆：水位由最低的围墙决定，先处理最低的才保证每格第一次被访问时水位就是最终值。

```python
import heapq

def trap_2d(g):
    m, n = len(g), len(g[0])
    if m < 3 or n < 3:
        return 0                                  # 围不住水
    seen = [[False] * n for _ in range(m)]
    heap = []
    for i in range(m):
        for j in range(n):
            if i in (0, m - 1) or j in (0, n - 1):
                seen[i][j] = True
                heapq.heappush(heap, (g[i][j], i, j))   # 边界先入堆
    water = 0
    while heap:
        level, i, j = heapq.heappop(heap)         # 当前最低的围墙
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < m and 0 <= b < n and not seen[a][b]:
                seen[a][b] = True
                water += max(0, level - g[a][b])
                heapq.heappush(heap, (max(level, g[a][b]), a, b))
    return water

print(trap_2d([[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]))   # 4
```

- **会多花一个测试用例的边界：** 少于 2 根线时容器面积为 0；少于 3 根柱子时接雨水为 0；单调递增或递减的柱子积不了水；中间有 0 高度的凹陷；二维网格长或宽小于 3 返回 0；高度不能为负数。

**英文答法。**
- "Moving the **taller** side can only shrink the width and keep the same cap, so it can never help."
- "In 2D the water level is set by the **lowest wall**, so I expand from the border with a **min-heap**."
- "The two-pointer trick is **O(1) space**: no left-max or right-max arrays."
