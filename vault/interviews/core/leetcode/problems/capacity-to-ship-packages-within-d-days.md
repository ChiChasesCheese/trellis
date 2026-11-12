---
slug: capacity-to-ship-packages-within-d-days
---
## Q
**LC 1011 在 D 天内送达包裹的能力**｜Medium

包裹必须按顺序装船，每天装的总重不超过载重。求能在 `days` 天内送完的最低载重。

## A
**一句话。** 二分答案：载重越大天数越少（单调），在 `[max, sum]` 上二分，用线性贪心判断天数是否够。

```python
def ship_within_days(weights, days):
    def days_needed(cap):
        used, load = 1, 0
        for w in weights:
            if load + w > cap:   # 今天装不下，换一天
                used += 1
                load = 0
            load += w
        return used

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log S)`（`S` 为总重），空间 `O(1)`。

**易错点。**
- 下界写 `1` 而不是 `max(weights)`：装不下的包裹被当成新一天的开头，`[1,2,3,1,1]`、`days=4` 得 `2`，应为 `3`。
- 天数从 `0` 计：少算第一天，`[1..10]`、`days=5` 得 `11`，应为 `15`。
- 当成可调换顺序的装箱：每天只能装连续一段，贪心必须按顺序。

**追问。**
- 怎么收窄二分范围？：下界可取 `max(max(weights), ceil(sum/days))`。
- 换成「分成 `m` 段使最大段和最小」呢？：就是 LC 410，代码不用改。

**同模式。** LC 410 分割数组的最大值、LC 875 爱吃香蕉的珂珂、LC 1482 制作 m 束花所需的最少天数、LC 2187 完成旅途的最少时间
