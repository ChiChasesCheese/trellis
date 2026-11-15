---
slug: ugly-number-iii
---
## Q
**LC 1201 丑数 III**｜Medium

正整数是丑数，如果它能被 `a`、`b` 或 `c` 中至少一个整除。返回第 `n` 个丑数（答案在 `[1, 2·10^9]` 内）。

## A
**一句话。** 二分答案：不超过 `x` 的丑数个数由三元容斥算出，找最小的个数不少于 `n` 的 `x`。

```python
def nth_ugly_number(n, a, b, c):
    ab, ac, bc = lcm(a, b), lcm(a, c), lcm(b, c)
    abc = lcm(a, b, c)
    def count(x):                  # 不超过 x 的丑数个数
        return (x // a + x // b + x // c
                - x // ab - x // ac - x // bc + x // abc)
    lo, hi = 1, 2 * 10 ** 9
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(log 2·10^9)`，空间 `O(1)`。

**易错点。**
- 容斥漏掉三者公倍数：加减号是「单个加、两两减、三个加」。
- 三元最小公倍数用 `a * b * c`：必须是真正的 `lcm`，否则减得不对。
- 二分用 `>` 而不是 `>=`：要找最小的满足个数 `≥ n` 的数，结果自然落在某个丑数上。

**追问。**
- 为什么结果一定是丑数？：`count` 在丑数处才加 1，最小的 `count ≥ n` 的 `x` 必须使 `count(x - 1) < n`，即 `x` 本身是丑数。
- 和 LC 264 丑数 II 的区别？：那里用质因数 `2, 3, 5` 生成序列，这里除数任意，所以二分加容斥。

**同模式。** LC 878 第 N 个神奇数字、LC 264 丑数 II、LC 793 阶乘函数后 K 个零、LC 313 超级丑数
