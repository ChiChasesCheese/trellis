---
id: tlc-furthest-building-you-can-reach-0-whole
node: c.furthest-building-you-can-reach
type: qa
---
## Q
**LC 1642 可以到达的最远建筑**｜Medium · LC TikTok 全时段热度 38/100

给定建筑高度数组 `heights`，以及 `bricks` 块砖和 `ladders` 架梯子。你从建筑 `0` 出发，依次向后移动到 `i + 1`：如果 `heights[i] >= heights[i + 1]` 不需要任何东西；否则必须用一架梯子，或者用 `heights[i + 1] - heights[i]` 块砖。以最佳方式使用砖和梯子，返回能到达的最远建筑下标。`1 <= heights.length <= 10^5`，`1 <= heights[i] <= 10^6`，`0 <= bricks <= 10^9`，`0 <= ladders <= heights.length`。例：`heights = [4,2,7,6,9,14,12]`，`bricks = 5`，`ladders = 1` → `4`；`heights = [4,12,2,7,3,18,20,3,19]`，`bricks = 10`，`ladders = 2` → `7`；`heights = [14,3,19,3]`，`bricks = 17`，`ladders = 0` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 梯子要留给最高的几次攀爬：用最小堆保存当前用梯子的攀爬高度，梯子不够时把堆里最小的一次改用砖块，砖块不够就停。

**识别。** 「有限的万能资源（梯子）加有限的可量化资源（砖块），事后可以重新分配」：小根堆维护「当前被梯子覆盖的攀爬」，每多一次攀爬就反悔一次。看到「最小的 k 个 / 最大的 k 个」的动态维护就想到堆。

**推导。** 暴力：每次攀爬枚举「梯子还是砖块」，`2^n`。洞察：在到达终点 `t` 的前提下，所有攀爬的高度已知，最优分配是把最大的 `ladders` 次攀爬交给梯子，其余用砖块，所需砖块是剩余攀爬之和。随着 `t` 向右推进，攀爬集合只增不减，这个「最大 `ladders` 个」用大小为 `ladders` 的最小堆动态维护：新攀爬进堆；堆超过 `ladders`，弹出最小的，这次攀爬用砖块支付。砖块为负时无法到达下一栋。

```python
from heapq import heappop, heappush
from itertools import pairwise


def furthest_building(heights: list[int], bricks: int, ladders: int) -> int:
    ladder_climbs: list[int] = []                # 小根堆：当前用梯子的攀爬高度，最多 ladders 个
    for i, (cur, nxt) in enumerate(pairwise(heights)):
        climb = nxt - cur
        if climb <= 0:                           # 下坡或平地：免费
            continue
        heappush(ladder_climbs, climb)           # 先假设这次用梯子
        if len(ladder_climbs) > ladders:         # 梯子不够：把最小的那次改用砖块
            bricks -= heappop(ladder_climbs)
            if bricks < 0:                       # 砖也不够：到不了 i + 1
                return i
    return len(heights) - 1
```

运行：`([4,2,7,6,9,14,12], 5, 1)` → `4`，`([4,12,2,7,3,18,20,3,19], 10, 2)` → `7`，`([14,3,19,3], 17, 0)` → `3`；`([1,5,1,2,3,4,10000], 4, 1)` → `5`。

**复杂度。** 时间 `O(n log ladders)`，空间 `O(ladders)`。

**拓展优化。**
- 反过来用最大堆存砖块攀爬：每次攀爬先用砖，砖不够时把已用砖里最大的一次换成梯子，把砖还回来；等价但容易写错符号。
- 二分答案：「能否到达 `t`」对 `t` 单调，判定是把前 `t` 个攀爬排序后让最大的 `ladders` 个用梯子，`O(n log² n)`。

```python
def furthest_building_bsearch(heights: list[int], bricks: int, ladders: int) -> int:
    def reachable(t: int) -> bool:               # 能否到达建筑 t
        climbs = sorted((max(0, b - a) for a, b in pairwise(heights[:t + 1])), reverse=True)
        return sum(climbs[ladders:]) <= bricks   # 最大的 ladders 个交给梯子，其余用砖
    lo, hi = 0, len(heights) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if reachable(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**易错点。**
- 用贪心「先用砖块，砖块不够再用梯子」：梯子被浪费在小攀爬上。`[1,5,1,2,3,4,10000]`、`bricks = 4`、`ladders = 1`：先砖会把 4 块砖花在 `1→5` 上，梯子用在 `1→2`，到 `2→3` 就没有资源了，得到 `3`；正确答案 `5`。
- 梯子数为 `0` 时：堆在 `push` 后立刻弹出，逻辑依然成立，不要单独特判漏掉。
- `return i` 与 `return i + 1` 混淆：循环里的 `i` 是出发建筑，到不了 `i + 1`，所以最远是 `i`。

**追问。**
- 要求输出每次攀爬用砖还是梯子：最终留在堆里的 `ladders` 个攀爬用梯子，其余用砖，需要把攀爬下标一起入堆。
- 建筑在线到来、随时回答「现在能到哪」：堆版本天然支持，每来一栋建筑 `O(log ladders)`。

**同模式。** LC 253 会议室 II、LC 502 IPO、LC 871 最低加油次数、LC 1167 连接棒材的最低费用、LC 630 课程表 III。
