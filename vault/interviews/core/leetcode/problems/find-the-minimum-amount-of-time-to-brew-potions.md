---
slug: find-the-minimum-amount-of-time-to-brew-potions
---
## Q
**LC 3494 酿造药水需要的最少总时间**｜Medium

`n` 个巫师按顺序处理 `m` 瓶药水，巫师 `i` 处理药水 `j` 用时 `skill[i]·mana[j]`；药水做完一道必须立刻交给下一位巫师。求全部做完的最短时间（`n, m <= 5000`）。

## A
**一句话。** 药水一旦开始就不能停，它到达巫师 `i` 的时刻是 `t + mana·pre[i]`（`pre` 为技能前缀和），必须不早于巫师 `i` 做完上一瓶的时刻 `f[i]`；所以开始时刻 `t = max(f[i] - mana·pre[i])`，再更新 `f`。

```python
def min_time(skill, mana):
    n = len(skill)
    pre = list(accumulate(skill, initial=0))
    f = [0] * n                # f[i]：巫师 i 做完上一瓶的时刻
    for m in mana:
        # 开始时刻 t：到达每位巫师时他都已空闲
        t = max(f[i] - m * pre[i] for i in range(n))
        f = [t + m * pre[i + 1] for i in range(n)]
    return f[-1]
```

**复杂度。** 时间 `O(nm)`，空间 `O(n)`。

**易错点。**
- 每位巫师各自取 `max(自己空闲, 上一位做完)`：药水不能在两位巫师之间等待，开始时刻要整体决定。
- 前缀和下标错位：到达巫师 `i` 前经过的是 `skill[0..i-1]`，用 `pre[i]`；做完是 `pre[i+1]`。

**追问。**
- 不存 `f` 数组？：`f[i] = t' + m'·pre[i+1]`（`t'`、`m'` 属于上一瓶），所以 `t - t' = max(m'·pre[i+1] - m·pre[i])`，只依赖相邻两瓶的 `mana`；对点 `(pre[i], pre[i+1])` 取凸包后还能二分加速。
- 为什么取最大值就够？：每个约束都是 `t >= f[i] - m·pre[i]`，最小的可行 `t` 就是它们的最大值。

**同模式。** LC 134 加油站、LC 1840 最高建筑高度
