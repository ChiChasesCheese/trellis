---
slug: furthest-building-you-can-reach
---
## Q
**LC 1642 可以到达的最远建筑**｜Medium

向后爬建筑，遇到上坡必须用一架梯子或等高的砖块，给定砖数和梯子数，求最远能到达的下标。

## A
**一句话。** 梯子留给最大的几次攀爬：小根堆存用梯子的攀爬高度，超过梯子数就把最小的一次改用砖。

```python
def furthest_building(heights, bricks, ladders):
    h = []    # 小根堆：当前用梯子的攀爬高度
    for i in range(len(heights) - 1):
        climb = heights[i + 1] - heights[i]
        if climb <= 0:
            continue
        heappush(h, climb)          # 先假设用梯子
        if len(h) > ladders:        # 梯子不够，最小的改用砖
            bricks -= heappop(h)
            if bricks < 0:
                return i
    return len(heights) - 1
```

**复杂度。** 时间 `O(n log ladders)`，空间 `O(ladders)`。

**易错点。**
- 先用砖、砖不够再用梯子：梯子浪费在小攀爬上，`[1,5,1,2,3,4,10000]`、`4` 砖、`1` 梯得 `3`，应为 `5`。
- `return i + 1`：循环里的 `i` 是出发点，到不了 `i+1`，最远是 `i`。
- 梯子数为 `0`：堆会被立刻弹出，逻辑照常成立，不必特判。

**追问。**
- 要输出每次攀爬用砖还是梯子？：堆里最终剩下的用梯子，其余用砖，入堆时带上下标。
- 建筑在线到来呢？：堆天然支持，每栋 `O(log ladders)`。

**同模式。** LC 253 会议室 II、LC 502 IPO、LC 871 最低加油次数、LC 1167 连接棒材的最低费用
