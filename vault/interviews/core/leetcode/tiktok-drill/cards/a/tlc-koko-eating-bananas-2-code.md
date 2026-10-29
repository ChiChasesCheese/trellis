---
id: tlc-koko-eating-bananas-2-code
node: a.koko-eating-bananas
type: qa
step: 2
---
## Q
**LC 875 爱吃香蕉的珂珂**｜写出 Python 实现

`piles` 是各堆香蕉数（`1 <= piles.length <= 10^4`，`1 <= piles[i] <= 10^9`），`h`（`piles.length <= h <= 10^9`）小时内要吃完；每小时只能选一堆，吃 `k` 根或吃完这堆。返回最小的整数速度 `k`。

## A
**思路。** 速度 `k` 的可行性单调，在 `[1, max(piles)]` 上二分找第一个可行的 `k`。可行 = 每堆需要 `ceil(p / k)` 小时，总和不超过 `h`。

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    lo, hi = 1, max(piles)                  # 答案在 [1, max(piles)]
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum((p + mid - 1) // mid for p in piles)   # 向上取整
        if hours <= h:
            hi = mid                        # mid 够快，答案在 [lo, mid]
        else:
            lo = mid + 1                    # mid 太慢，答案在 (mid, hi]
    return lo
```

运行：`([3,6,7,11], 8)` → `4`，`([30,11,23,4,20], 5)` → `30`，`([30,11,23,4,20], 6)` → `23`，`([1], 1)` → `1`，`([10**9], 1)` → `1000000000`；`10^4` 堆、每堆随机到 `10^9` 的输入约 `10 ms`。

**复杂度。** 时间 `O(n log M)`：二分约 `log2(10^9) ≈ 30` 轮，每轮 `O(n)`；空间 `O(1)`。

**写法要点。** `(p + mid - 1) // mid` 是整数向上取整，不经过浮点，`10^9` 量级也不会丢精度（`math.ceil(p / mid)` 在更大的数上会）；`sum` 配生成器表达式不建临时列表；`lo < hi` 的区间收缩模板找“第一个满足条件的值”，循环结束时 `lo == hi`。Python 3.10 起可以用 `bisect_left(range(1, max(piles) + 1), True, key=…)` 把整个二分压成一行，面试里先写显式循环。
