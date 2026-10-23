---
id: hl-hc03-closed-form-trap
node: problems.hc03-recursive-sum
type: qa
step: 11
---
## Q
`n * (n + 1) / 2` 对大 n 为什么是错的？怎样写才正确，`sumTo(long n)` 怎么实现？

## A
高斯公式 `1+…+n = n(n+1)/2`，区间 `[a,b]` 的和 `= (a+b) × (b−a+1) / 2`，O(1)、不爆栈。但**先乘后除时乘积先溢出**，即使最终答案装得下。

例：n = 4 294 967 295 时 `n×(n+1) = 2⁶⁴ − 2³²` 在 `long` 里回绕成 −2³²，除 2 得 **−2 147 483 648**——无异常，答案却是负数（`naiveClosedForm` 就是这个静默错误）。

**正确顺序**：`n` 与 `n+1`（区间则是 `a+b` 与 `b−a+1`，差是奇数 `2a−1`）奇偶**相反**，必有一个偶数；**先把偶数那个除以 2**（整除无余数）再相乘，乘积只有一半大。
```java
static long sumTo(long n) {
    if (n < 0) throw new IllegalArgumentException("n < 0");
    long b = Math.addExact(n, 1);
    return (n % 2 == 0) ? Math.multiplyExact(n / 2, b)
                        : Math.multiplyExact(n, b / 2);
}
```
检查：`sumTo(4_294_967_295L)` = 9 223 372 034 707 292 160 装得下；`sumTo(4_294_967_296L)` 的 `multiplyExact` 超过 2⁶³−1，抛异常。

被除的是偶数，对负数也是精确除法，没有向零取整问题——这是「先除偶数」比「先乘再除」更好的另一个理由。C++ 里可用 `__int128`（乘积 < 2¹²⁷），或同样先除偶数并用 `__builtin_mul_overflow`。
