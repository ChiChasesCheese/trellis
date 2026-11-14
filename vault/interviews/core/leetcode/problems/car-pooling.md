---
slug: car-pooling
---
## Q
**LC 1094 拼车**｜Medium

车有 `capacity` 个座位，只向东开。`trips[i] = [人数, from, to]`，在 `from` 上车、`to` 下车，问全程是否从不超载。坐标 `≤ 1000`。

## A
**一句话。** 差分数组：上车点 `+人数`、下车点 `-人数`，前缀和就是每个位置车上的人数。

```python
def car_pooling(trips, capacity):
    diff = [0] * 1001
    for k, s, t in trips:
        diff[s] += k
        diff[t] -= k            # 到 t 已经下车
    cur = 0
    for d in diff:
        cur += d                # 前缀和 = 此刻车上人数
        if cur > capacity:
            return False
    return True
```

**复杂度。** 时间 `O(n + U)`，空间 `O(U)`，`U = 1001`。

**易错点。**
- 在 `t + 1` 处减：乘客在 `to` 已经下车，`[[2,1,5],[3,5,7]]`、容量 3 会误判超载。
- 逐公里累加每趟行程：单趟 `O(to - from)`，坐标大时超时。

**追问。**
- 坐标到 `10^9`？：把 `(from, +k)`、`(to, -k)` 排序扫描（同点先下后上），`O(n log n)`。
- 返回最大载客量？：同一个前缀和取最大值。

**同模式。** LC 253 会议室 II、LC 1109 航班预订统计、LC 2848 与车相交的点
