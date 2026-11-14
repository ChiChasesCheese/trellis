---
slug: distance-between-bus-stops
---
## Q
**LC 1184 公交站间的距离**｜Easy

环形线路 `n` 站，`distance[i]` 是站 `i` 到 `i+1` 的距离，可顺可逆，求 `start` 到 `destination` 的最短距离。

## A
**一句话。** 环上只有两条路，一条是 `[min, max)` 段之和，另一条是总长减去它，取小。

```python
def distance_between_bus_stops(distance, start, dest):
    a, b = sorted((start, dest))
    one = sum(distance[a:b])           # 顺时针 a -> b
    return min(one, sum(distance) - one)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（切片另占 `O(n)`）。

**易错点。**
- 没把 `start > destination` 的情况换过来：`distance[5:2]` 是空列表，得 `0`。
- 切片写成 `[a:b+1]`：多算了从 `b` 出发的那段。

**追问。**
- 多次查询？：前缀和 `pre`，一段是 `pre[b] - pre[a]`，另一段 `total - 它`。
- 单向环（只能顺时针）？：`start ≤ destination` 时是 `pre[d] - pre[s]`，否则 `total - (pre[s] - pre[d])`。

**同模式。** LC 134 加油站、LC 918 环形子数组的最大和、LC 2134 最少交换次数来组合所有的 1 II
