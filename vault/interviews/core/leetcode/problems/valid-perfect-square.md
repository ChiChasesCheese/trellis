---
slug: valid-perfect-square
---
## Q
**LC 367 有效的完全平方数**｜Easy

给正整数 `num`，不用内置开方函数，判断它是否是某个整数的平方。

## A
**一句话。** 在 `[1, num]` 上二分找平方等于 `num` 的整数。

```python
def is_perfect_square(num):
    lo, hi = 1, num
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 用浮点 `sqrt` 再取整比较：大数时精度不够。
- 把 `mid * mid` 当作可能溢出：Python 整数不会，但 C++/Java 里要用 `mid <= num / mid` 的写法。

**追问。**
- 还有什么方法？：牛顿迭代 `x = (x + num // x) // 2`，收敛更快；或利用「前 `k` 个奇数之和是 `k²`」做减法。
- 上界可以更紧吗？：`hi = num // 2 + 1` 即可（`num > 1`）。

**同模式。** LC 69 x 的平方根、LC 35 搜索插入位置、LC 744 寻找比目标字母大的最小字母、LC 704 二分查找
