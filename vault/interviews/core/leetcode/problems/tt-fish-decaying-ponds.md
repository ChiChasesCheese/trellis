---
slug: tt-fish-decaying-ponds
---
## Q
**鱼塘捕鱼（产量递减）**｜Hard

`n` 个鱼塘，第 `i` 塘首捞 `fish[i]` 条，之后每捞一次下次少 `decay[i]` 条（不低于 `0`）。共 `t` 个时间单位（`t` 可达 `10^9`），每次选一塘捕一次，求最多捞多少条。

## A
**一句话。** 每塘收获不增，答案是所有机会里最大的 `t` 个之和；二分阈值 `x`，严格大于 `x` 的等差数列全拿，余下名额各拿 `x`。

```python
def count_at_least(ponds, x, cap):
    # 单次产量 >= x 的机会数，数到 cap 为止
    total = 0
    for f, d in ponds:                # 按首捞量降序
        if f < x:
            break
        if d == 0:
            return cap                # 永远产 f：机会无限
        total += (f - x) // d + 1
        if total >= cap:
            return cap
    return total

def max_fish(fish, decay, t):
    ponds = sorted([(f, d) for f, d in zip(fish, decay)
                    if f > 0], reverse=True)
    if not ponds:
        return 0
    if count_at_least(ponds, 1, t) < t:
        x = 0                         # 全部正产量都不足 t 次
    else:
        lo, hi = 1, ponds[0][0]       # 最大的 x 使机会数 >= t
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if count_at_least(ponds, mid, t) >= t:
                lo = mid
            else:
                hi = mid - 1
        x = lo
    taken = total = 0
    for f, d in ponds:
        if f <= x:
            break
        k = (f - x - 1) // d + 1      # >= x+1 的项数
        taken += k
        total += k * f - d * k * (k - 1) // 2
    return total + (t - taken) * x    # 余下名额每次恰拿 x
```

**复杂度。** 时间 `O(n log n + n log max(fish))`，空间 `O(n)`。

**易错点。**
- 阈值处并列：`[3,3]`、`[1,1]`、`t = 3` 应得 `8`；拿所有 `>= x` 的会多拿，只拿严格大于又不补 `(t - taken) * x` 则得 `6`。
- 一塘榨干再换下一塘：`[10,6]`、`[4,1]`、`t = 3` 得 `18`，应为 `22`。
- 不在 `0` 处截断：序列 `5, 0, -5` 会出现负产量。
- `decay = 0` 当普通塘：`(f - x) // d` 除零，该塘机会无限要单独记满。

**追问。**
- 每塘最多捕 `c[i]` 次？：计数里每塘取 `min(c[i], (f - x) // d + 1)`。
- `t` 很小？：堆模拟更直观，`O(t log n)`。

**同模式。** LC 1648 销售价值减少的颜色球、LC 378 有序矩阵中第 K 小的元素、LC 719 找出第 K 小的数对距离、LC 875 爱吃香蕉的珂珂
