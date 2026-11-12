---
slug: minimum-number-of-refueling-stops
---
## Q
**LC 871 最低加油次数**｜Hard

汽车要行驶 `target` 英里，初始有 `startFuel` 升油，油箱无限，沿途加油站 `stations[i] = [位置, 油量]`。求最少加油次数，到不了返回 `-1`。

## A
**一句话。** 贪心加最大堆：路过的站只入堆不加油，到不了下一站时再回头补堆里油最多的。

```python
def min_refuel_stops(target, start, stations):
    heap = []                     # 路过的站的油量（取负数）
    fuel = start                  # 当前能到的最远位置
    stops = 0
    for pos, gas in [*stations, [target, 0]]:  # 终点=油0的站
        while fuel < pos:         # 到不了：补油最多的站
            if not heap:
                return -1
            fuel -= heappop(heap)
            stops += 1
        heappush(heap, -gas)
    return stops
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 用 `if` 代替 `while`：补一次可能还不够，`(14, 4, [[4,5]])` 应为 `-1`，却返回 `1`。
- 漏掉终点这个虚拟站：`(100, 10, [[10,60],[20,30],[30,30],[60,40]])` 会返回 `1`，应为 `2`。
- 把 `fuel` 当剩余油量：它是最远可达位置，直接与站的绝对位置比较。

**追问。**
- 为什么回头加最大的是对的？：路过的每个站都可以事后再选，只在不得不加时选最大的，次数最少。
- 也能用 DP 吗？：`dp[i]` 为加 `i` 次油能到的最远处，`O(n^2)`。

**同模式。** LC 253 会议室 II、LC 1642 可以到达的最远建筑、LC 502 IPO、LC 630 课程表 III
