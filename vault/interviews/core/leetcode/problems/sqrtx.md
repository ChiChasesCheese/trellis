---
slug: sqrtx
---
## Q
**LC 69 x 的平方根**｜Easy

求非负整数 `x` 的平方根，向下取整，不能用 `pow` 或 `**0.5`。

## A
**一句话。** 对答案二分：找最大的整数 `m` 使 `m*m <= x`。

```python
def my_sqrt(x):
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2   # 向上取整，否则会死循环
        if mid * mid <= x:
            lo = mid               # mid 可行
        else:
            hi = mid - 1
    return lo
```

**复杂度。** 时间 `O(log x)`，空间 `O(1)`。

**易错点。**
- `mid` 向下取整：`x=1` 时 `mid=0`，`lo=mid` 区间不缩，死循环。
- 条件写成 `mid*mid < x`：`x=4` 得 `1`，应为 `2`。
- 其他语言 `mid*mid` 溢出 32 位：改写成 `mid <= x // mid` 或用 64 位。

**追问。**
- 牛顿迭代怎么写？：`r = x` 起，`r = (r + x // r) // 2` 直到 `r*r <= x`，约 19 轮收敛。
- 判断完全平方数（LC 367）？：同样二分，最后检查 `lo*lo == x`。

**同模式。** LC 367 有效的完全平方数、LC 50 Pow(x, n)、LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力
