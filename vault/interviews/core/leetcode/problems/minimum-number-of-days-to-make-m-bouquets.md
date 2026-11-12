---
slug: minimum-number-of-days-to-make-m-bouquets
---
## Q
**LC 1482 制作 m 束花所需的最少天数**｜Medium

`bloomDay[i]` 是第 `i` 朵花盛开的日子。一束花要用相邻的 `k` 朵已开的花，求做出 `m` 束的最少天数，做不到返回 `-1`。

## A
**一句话。** 对天数二分：天数越多开的花越多，可行性单调，判定时扫一遍统计连续开花凑出的束数。

```python
def min_days(bloom_day, m, k):
    if m * k > len(bloom_day):
        return -1

    def can(day):
        bouquets = run = 0         # run：连续已开花数
        for b in bloom_day:
            if b <= day:
                run += 1
                if run == k:       # 凑够一束
                    bouquets += 1
                    run = 0
            else:
                run = 0            # 遇到没开的，连续断开
        return bouquets >= m

    lo, hi = min(bloom_day), max(bloom_day)
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log(max-min))`，空间 `O(1)`。

**易错点。**
- 遇到没开的花忘了清零 `run`：`[7,7,7,7,12,7,7]`、`m=2`、`k=3` 返回 `7`，应为 `12`。
- 凑够一束后不置零：`[1,1,1,1,9]`、`m=2`、`k=2` 只数出 `1` 束，返回 `9`，应为 `1`。
- 不先判 `m*k > n`：二分会返回 `max(bloom_day)` 而不是 `-1`。

**追问。**
- 为什么上界取 `max(bloom_day)`？：那天所有花都开了，若仍不可行就是 `m*k > n`，已提前排除。
- 这类题怎么识别？：「最小化某个值，且值越大越容易可行」就是答案二分。

**同模式。** LC 1011 在 D 天内送达包裹的能力、LC 875 爱吃香蕉的珂珂、LC 410 分割数组的最大值、LC 1283 使结果不超过阈值的最小除数
