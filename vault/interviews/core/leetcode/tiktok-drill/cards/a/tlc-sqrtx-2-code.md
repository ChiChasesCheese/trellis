---
id: tlc-sqrtx-2-code
node: a.sqrtx
type: qa
step: 2
---
## Q
**LC 69 x 的平方根**｜写出 Python 实现

非负整数 `x`，`0 <= x <= 2^31 - 1`。返回 `x` 的算术平方根向下取整后的整数，不能使用 `pow`、`**`、`math.sqrt` 之类的内置开方。要求 `O(log x)`。

## A
**思路。** 在 `[0, x]` 上二分，找最大的 `m` 使 `m * m <= x`。中点向上取整，`mid * mid <= x` 时 `lo = mid`，否则 `hi = mid - 1`，区间收敛到单个答案。

```python
def my_sqrt(x: int) -> int:
    lo, hi = 0, x                                  # 答案 m 满足 m*m <= x，找最大的这样的 m
    while lo < hi:
        mid = (lo + hi + 1) // 2                   # 向上取整，否则 lo = mid 时区间不缩小会死循环
        if mid * mid <= x:
            lo = mid                               # mid 可行：答案至少是 mid
        else:
            hi = mid - 1
    return lo
```

运行：`4` → `2`；`8` → `2`；`0` → `0`；`1` → `1`；`2^31 - 1` → `46340`。

**复杂度。** 时间 `O(log x)`，每轮区间减半；空间 `O(1)`。

**写法要点。** 循环条件 `lo < hi`（不是 `<=`），退出时 `lo == hi` 就是答案；`(lo + hi + 1) // 2` 是向上取整的整数写法；`x = 0` 时 `lo = hi = 0`，循环不进入，直接返回 `0`；Python 的 `mid * mid` 不会溢出，换 C++ / Java 要写成 `mid <= x / mid`；也可以用标准库 `bisect_right(range(x + 1), x, key=lambda m: m * m) - 1`，两行完成同样的事（见追问）。
