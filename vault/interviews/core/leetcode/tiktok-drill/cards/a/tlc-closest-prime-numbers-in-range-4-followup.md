---
id: tlc-closest-prime-numbers-in-range-4-followup
node: a.closest-prime-numbers-in-range
type: qa
step: 4
---
## Q
**LC 2523 范围内最接近的两个质数**｜追问

面试官接着问：（1）`right` 大到 `10^12`，但 `right - left <= 10^6`，怎么办？（2）同一上界下有大量查询怎么办？（3）扫描能不能提前结束？

## A
1. **分段筛（segmented sieve）。** 只开 `right - left + 1` 长度的数组，用 `2..√right` 之内的数当筛子，划掉它们落在区间里的倍数。起点取 `max(p*p, 大于等于 lo 的第一个 p 的倍数)`：

```python
from math import isqrt


def primes_in_range(left: int, right: int) -> list[int]:
    lo = max(left, 2)
    seg = bytearray([1]) * max(right - lo + 1, 0)     # seg[i] 对应数字 lo + i
    for p in range(2, isqrt(right) + 1):              # 拿合数当筛子也无妨，只是多划几次
        start = max(p * p, (lo + p - 1) // p * p)
        seg[start - lo :: p] = bytes(len(range(start - lo, len(seg), p)))
    return [lo + i for i, ok in enumerate(seg) if ok]
```

2. **多次查询。** 先把 `10^6` 以内的质数表建一次，每次查询用 `bisect_left(primes, left)` 和 `bisect_right(primes, right)` 切出窗口，再对窗口扫相邻对：每次 `O(log P + 窗口长度)`。
3. **提前返回。** 质数对的差只有 `(2, 3)` 为 1，其余至少是 2；从小到大扫描时第一次遇到差 `<= 2` 的一对就是答案。

**Python 提醒**：对 `bytearray` 做步长不为 1 的切片赋值时，右边长度必须与切片长度严格相等，否则抛 `ValueError: attempt to assign bytes of size 2 to extended slice of size 3`；用 `bytes(len(range(start, stop, step)))` 精确构造全零字节串。
