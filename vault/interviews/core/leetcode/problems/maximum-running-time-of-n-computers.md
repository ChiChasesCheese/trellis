---
slug: maximum-running-time-of-n-computers
---
## Q
**LC 2141 同时运行 N 台电脑的最长时间**｜Hard

`n` 台电脑，电池 `batteries[i]` 能供电若干分钟；任意整数时刻可随意换电池（换下的还能接到别的电脑上）。求所有电脑同时运行的最长分钟数。

## A
**一句话。** 二分答案 `t`：每块电池最多贡献 `t` 分钟（同一时刻只能接一台），能撑 `t` 分钟当且仅当 `sum(min(b, t)) >= n·t`。

```python
def max_run_time(n, batteries):
    lo, hi = 0, sum(batteries) // n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        # 超过 mid 的电量用不上：一块电池同一时刻只供一台
        if sum(min(b, mid) for b in batteries) >= n * mid:
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**复杂度。** 时间 `O(m log S)`（`m` 块电池，`S` 为总电量），空间 `O(1)`。

**易错点。**
- 只看总电量 `sum >= n·t`：一块大电池不能同时给两台电脑用，要先截到 `t`。
- `mid` 向下取整配 `lo = mid`：死循环。

**追问。**
- 为什么截断后够就一定可行？：把截断后的电量按时间轴依次铺满 `n` 条长 `t` 的轨道，每块不超过 `t` 不会在同一时刻出现两次。
- 不二分？：排序后大电池若超过「剩余总量 / 剩余台数」就单独占一台，去掉后重算，最后答案为剩余总量整除剩余台数。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 2861 最大合金数、LC 2187 完成旅途的最少时间
