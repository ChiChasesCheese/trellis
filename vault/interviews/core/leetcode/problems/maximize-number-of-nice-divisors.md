---
slug: maximize-number-of-nice-divisors
---
## Q
**LC 1808 好因子的最大数目**｜Hard

构造正整数 `n`，质因子（计重数）不超过 `primeFactors` 个（`<= 10^9`）。能被 `n` 的每个质因子整除的因子是好因子，求好因子数目的最大值，对 `10^9+7` 取余。

## A
**一句话。** 若 `n = p1^e1·…·pm^em`，好因子个数是 `e1·e2·…·em`，问题变成「把 `primeFactors` 拆成若干正整数使乘积最大」：尽量拆成 3，余 1 时把一个 `3+1` 换成 `2+2`，用快速幂。

```python
def max_nice_divisors(prime_factors):
    MOD = 10**9 + 7
    n = prime_factors
    if n <= 3:
        return n               # 不拆最好
    q, r = divmod(n, 3)
    if r == 0:
        return pow(3, q, MOD)
    if r == 1:                 # 3 + 1 换成 2 + 2
        return pow(3, q - 1, MOD) * 4 % MOD
    return pow(3, q, MOD) * 2 % MOD
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 余 1 时乘 1：`3·1 < 2·2`，要退一个 3 换成两个 2。
- `n <= 3` 也去拆：`n = 2` 拆成 `1+1` 乘积变小，直接返回 `n`。

**追问。**
- 为什么好因子数是指数之积？：好因子每个质因子的指数取 `1..ei`，各有 `ei` 种选法。
- 为什么拆成 3 最好？：`x > 4` 时拆成 `3` 和 `x-3` 乘积更大，`4 = 2·2`，而 `3^2 > 2^3`，所以 3 优先、2 不超过两个。

**同模式。** LC 50 Pow(x, n)、LC 343 整数拆分
