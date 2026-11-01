---
id: tlc-tops-minimum-number-of-refueling-stops-0-whole
node: heap-priority-queue.minimum-number-of-refueling-stops
type: qa
---
## Q
**LC 871 最低加油次数**｜Hard · 全公司热度第 214 名

汽车从起点出发驶向目的地，目的地位于出发位置东面 `target` 英里处。沿途有加油站，`stations[i] = [position_i, fuel_i]` 表示第 `i` 个加油站位于出发位置东面 `position_i` 英里处，有 `fuel_i` 升汽油。汽车油箱容量无限，最初有 `startFuel` 升燃料，每行驶 1 英里用掉 1 升汽油。到达加油站时可以停下来，把站里所有汽油转移到车里。返回到达目的地所需的最低加油次数，无法到达则返回 `-1`。到达加油站时剩余燃料为 0 仍可以在那里加油；到达目的地时剩余燃料为 0 也算到达。`1 <= target, startFuel <= 10^9`，`0 <= stations.length <= 500`，`1 <= position_i < position_{i+1} < target`，`1 <= fuel_i < 10^9`。例：`target = 1, startFuel = 1, stations = []` → `0`；`target = 100, startFuel = 1, stations = [[10,100]]` → `-1`；`target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]` → `2`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 贪心 + 最大堆（max-heap）：延迟决策，「事后」补加经过的最大油站。

**一句话。** 一路开，把经过的加油站的油量压进最大堆但先不加；一旦油不够到下一站，就「回头」在已经路过的站里加油量最大的那个，直到够用或没有站可选。

**识别。** 「最少加油次数」「油箱无限」「站的油全部拿走」：每次加油只关心**加多少**，不关心在哪个站加（只要路过了），所以可以延迟到「不得不加」时再决定，并且每次一定选最大的。`stations` 至多 500，但 `target` 达 `10^9`，不能按里程模拟。

**推导。** 暴力：枚举加油站子集，`O(2^n)`；按里程逐英里模拟不可行。设 `fuel` 为当前总油量可以到达的最远位置。到达某站 `p` 要求 `fuel >= p`；不满足时必须在之前路过的站里补加。补哪些？每次补一个都使 `fuel` 增大，要让补的次数最少，每次就选路过的站里油量最大的，这就是最大堆。每个站先压堆（"可选"），在需要时才弹出，目的地当作油量为 0 的最后一站，统一处理。

```python
def min_refuel_stops(target: int, start_fuel: int, stations: list[list[int]]) -> int:
    heap: list[int] = []                       # 已路过但尚未使用的站的油量（取负数实现最大堆）
    fuel = start_fuel                          # 当前所有油能走到的最远位置
    stops = 0
    for pos, gas in [*stations, [target, 0]]:  # 目的地当作油量为 0 的最后一站
        while fuel < pos:                      # 到不了这一站：回头补加路过的站里油最多的
            if not heap:
                return -1                      # 没有可补的站，到不了
            fuel += -heappop(heap)
            stops += 1
        heappush(heap, -gas)                   # 到达这一站，油量放进候选堆，先不用
    return stops
```

运行：`(1, 1, [])` → `0`，`(100, 1, [[10,100]])` → `-1`，`(100, 10, [[10,60],[20,30],[30,30],[60,40]])` → `2`，`(100, 50, [[25,25],[50,50]])` → `1`。

**复杂度。** 时间 `O(n log n)`（每个站最多入堆出堆一次），空间 `O(n)`。

**拓展优化。**
- `n <= 500`，也可以用动态规划：`dp[j]` 表示加油 `j` 次能到达的最远位置，逐站更新（`j` 倒序，避免同一站用两次），最后找最小的 `j` 使 `dp[j] >= target`。这是 1-D DP，`O(n^2)`：

```python
def min_refuel_stops_dp(target: int, start_fuel: int, stations: list[list[int]]) -> int:
    dp = [start_fuel] + [0] * len(stations)    # dp[j]：恰好加 j 次油能到达的最远位置
    for i, (pos, gas) in enumerate(stations):
        for j in range(i, -1, -1):             # 倒序：dp[j] 还是处理前面站时的值
            if dp[j] >= pos:                   # 能开到这一站，才有资格在此加油
                dp[j + 1] = max(dp[j + 1], dp[j] + gas)
    return next((j for j, far in enumerate(dp) if far >= target), -1)
```

- 堆的策略也适用于「最多 k 次」「最少 …」一类变体，核心都是「先欠着，需要时取最优」。

**易错点。**
- 只弹一次：用 `if fuel < pos` 代替 `while`，补一个站还不够时就继续往下走：`(14, 4, [[4,5]])` 补完最远只到 `9`，却返回 `1`（正确 `-1`）。
- 漏掉目的地这个「虚拟站」：循环结束后还要检查能否到 `target`，否则 `(100, 10, [[10,60],[20,30],[30,30],[60,40]])` 会返回 `1`（正确 `2`）。
- 堆里放的是油量，不是站的位置；Python 的 `heapq` 是最小堆，存负数才是最大堆，别忘了弹出时取反。
- `fuel` 是「最远可达位置」，不是「剩余油量」，所以比较用的是站的绝对位置，不用逐站扣油。

**同模式。** LC 253 会议室 II、LC 1642 可以到达的最远建筑、LC 502 IPO、LC 630 课程表 III。
