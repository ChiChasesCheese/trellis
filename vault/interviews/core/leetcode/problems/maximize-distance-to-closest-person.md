---
slug: maximize-distance-to-closest-person
---
## Q
**LC 849 到最近的人的最大距离**｜Medium

`seats[i]` 为 `1` 表示有人、`0` 表示空位（至少一人一空位）。选一个空位坐下，使它到最近的人的距离最大，返回该距离。

## A
**一句话。** 看连续空位段：两端段的距离是段长，中间段是下标差的一半，取最大。

```python
def max_dist_to_closest(seats):
    prev, best = -1, 0       # prev：上一个有人的下标
    for i, s in enumerate(seats):
        if s:
            d = i if prev < 0 else (i - prev) // 2  # 端段/中间段
            best = max(best, d)
            prev = i
    return max(best, len(seats) - 1 - prev)   # 右端段
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 两端段也除以 2：`[1,0,0,0]` 坐最右端距离是 `3`，写成 `3 // 2` 得 `1`。
- 中间段用空位数的一半：`[1,0,0,0,1]` 下标差 `4`，答案 `2`，用 `3 // 2` 得 `1`。
- `prev` 初值设成 `0`：`[0,0,1]` 开头段被当成中间段，得 `1`，应为 `2`。

**追问。**
- 想知道坐哪个座位？：同时记录最大距离对应的位置，中间段取 `prev + 距离`，端段取端点。

**同模式。** LC 1162 地图分析、LC 605 种花问题、LC 821 字符的最短距离
