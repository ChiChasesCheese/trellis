---
slug: maximum-white-tiles-covered-by-a-carpet
---
## Q
**LC 2271 毯子覆盖的最多白色砖块数**｜Medium

不相交区间 `[l, r]` 都是白砖，长 `carpetLen` 的毯子放在任意位置，最多盖住多少白砖。坐标到 `10^9`。

## A
**一句话。** 最优位置一定让毯子一端贴着某段端点；按段滑窗，枚举毯子右端对齐每段右端，整段滑出的减掉，左端那段露出的一截再扣。

```python
def maximum_white_tiles(tiles, carpet_len):
    tiles.sort()
    ans = cover = i = 0
    for l, r in tiles:            # 毯子右端对齐 r
        cover += r - l + 1
        while tiles[i][1] < r - carpet_len + 1:
            cover -= tiles[i][1] - tiles[i][0] + 1
            i += 1                # 整段滑出毯子
        out = max(0, r - carpet_len + 1 - tiles[i][0])
        ans = max(ans, cover - out)   # 扣掉左边露出的
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（不计排序）。

**易错点。**
- 枚举数轴上每个起点：坐标到 `10^9`，只能枚举段端点。
- 露出部分写成 `tiles[i][0] - (r - len + 1)`：符号反了，用 `max(0, 毯子左端 - 段左端)`。

**追问。**
- 为什么只对齐右端就够？：每格权重相同，对称地，左端对齐段左端的最优值等于某个右端对齐的值。
- 每格权重不同（LC 3413）？：要镜像坐标再做一遍左端对齐。

**同模式。** LC 3 无重复字符的最长子串、LC 3413 收集连续 K 个袋子可以获得的最多硬币数量
