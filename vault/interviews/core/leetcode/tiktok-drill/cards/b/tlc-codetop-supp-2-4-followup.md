---
id: tlc-codetop-supp-2-4-followup
node: b.codetop-supp-2
type: qa
step: 4
---
## Q
**补充题 2 圆环回原点问题**｜追问

面试官接着问：（1）`k` 到 `10^9`，`O(nk)` 不行怎么办？（2）有没有 `O(k)` 的闭式？（3）允许原地不动呢？

## A
1. **`k` 很大。** 转移是线性的：新向量 = 转移矩阵 × 旧向量。矩阵快速幂 `O(n^3 log k)`；因为转移是循环结构，也可以把 `(x + x^{-1})^k` 看成模 `x^n - 1` 的多项式，用循环卷积做快速幂，`O(n^2 log k)`。
2. **闭式。** 走 `k` 步，其中 `j` 步顺时针、`k - j` 步逆时针，净位移 `2j - k`，回到原点当且仅当 `(2j - k) % n == 0`。把满足条件的 `j` 的组合数 `C(k, j)` 加起来：

```python
from math import comb

MOD = 10**9 + 7


def ring_ways_comb(n: int, k: int) -> int:
    return sum(comb(k, j) for j in range(k + 1) if (2 * j - k) % n == 0) % MOD
```

`(5, 5)` → `2`，`(1000, 1000)` → `159835831`，与 DP 结果一致；`k` 大时需要预处理阶乘和逆元，把 `comb` 换成 `O(1)` 的模运算。
3. **允许不动。** 每步三种选择，转移多一项：`ways[i - 1] + ways[i] + ways[(i + 1) % n]`。

**Python 提醒**：`math.comb(k, j)` 返回精确的大整数，`k` 到千级没问题；求和后再取一次模即可。`k` 很大时再逐个调用会很慢，要改用阶乘表。
