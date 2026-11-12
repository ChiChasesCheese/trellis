---
slug: koko-eating-bananas
---
## Q
**LC 875 爱吃香蕉的珂珂**｜Medium

`piles[i]` 是第 `i` 堆香蕉数，每小时选一堆吃 `k` 根（不足就吃完）。求 `h` 小时内吃完的最小整数速度 `k`。

## A
**一句话。** 二分答案：速度越大耗时越少，在 `[1, max(piles)]` 上找第一个耗时 `<= h` 的速度。

```python
def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum((p + mid - 1) // mid for p in piles)
        if hours <= h:
            hi = mid        # 够快，答案在 [lo, mid]
        else:
            lo = mid + 1    # 太慢
    return lo
```

**复杂度。** 时间 `O(n log M)`，空间 `O(1)`。

**易错点。**
- 耗时向下取整：`[3,6,7,11]`、`h=8` 得 `3`，应为 `4`，不足 `k` 根也占一小时，要向上取整。
- 二分边界不成套：`lo <= hi` 配 `hi = mid` 会死循环，配 `hi = mid - 1` 会丢可行解。
- 判定写成 `hours < h`：恰好用满 `h` 小时的速度被排除，答案偏大。

**追问。**
- 每小时能吃多堆、只受总量限制？：退化成 `ceil(sum(piles) / h)`，不需要二分。

**同模式。** LC 1011 在 D 天内送达包裹的能力、LC 410 分割数组的最大值、LC 1482 制作 m 束花所需的最少天数、LC 2187 完成旅途的最少时间
