---
slug: minimum-time-to-complete-trips
---
## Q
**LC 2187 完成旅途的最少时间**｜Medium

第 `i` 辆车跑一趟要 `time[i]`，可连续跑多趟，车之间互不影响。求所有车总共至少完成 `totalTrips` 趟所需的最少时间。

## A
**一句话。** 对时间二分：时间 `t` 内总趟数是 `Σ t // time[i]`，它随 `t` 单调不减，找最小的 `t` 使总趟数 `≥ totalTrips`。

```python
def minimum_time(time, totalTrips):
    lo, hi = 1, min(time) * totalTrips   # 最快的车独自跑也够
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(mid // t for t in time) >= totalTrips:
            hi = mid                     # 够了，答案 <= mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log(min(time)·totalTrips))`，空间 `O(1)`。

**易错点。**
- 上界取得太小：如 `max(time)` 时趟数不够，`min(time) * totalTrips` 才一定够。
- 判断用 `>` 而不是 `>=`：总趟数刚好等于 `totalTrips` 就够了。
- 总趟数用浮点除法：要整除，一趟没跑完不算。

**追问。**
- 这类题怎么识别？：「最小化满足条件的值」且条件对该值单调，就是对答案二分。
- 为什么不能直接公式算？：要对每辆车取整，和不是光滑函数，二分更稳。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力、LC 410 分割数组的最大值、LC 1482 制作 m 束花所需的最少天数
