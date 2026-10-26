# hc21 · 解法与原理

「打印 42 的平方根」看起来是送分题，其实是在考你是否真的理解数值算法：起点怎么选、什么时候停、边界怎么处理，以及整数版为什么不能偷懒用浮点数。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll use Newton's method: start from a guess x and repeat x = (x + a / x) / 2. Before I start: can I assume a is non-negative? What should I do for a negative input — throw, or return NaN? And how many digits do you want printed?"

面试官通常会说：负数你自己定，说明白就行，打印 15 位有效数字。你可以答：负数抛异常（调用者传错了参数，静默返回 NaN 容易被忽略），NaN 也一样。

## Part 1 · 牛顿迭代

**思路**：解方程 x² = a。在当前猜测 x 处，用切线代替曲线，切线与横轴的交点就是下一个猜测，即 `x' = (x + a / x) / 2`。先处理边界（负数、NaN、0、无穷），再写循环。

- **起点**：取 `max(a, 1)`。它不小于 √a（a ≥ 1 时 a ≥ √a，a < 1 时 1 > √a）。
- **停止条件**：从起点之后，由均值不等式，每个迭代值都不小于 √a，并且单调下降。所以「下一个值不再比当前小」就说明已经到了 `double` 能表示的极限，直接返回当前值。这比「相对误差小于 1e-15」稳：后者在相邻两个 `double` 的间距大于容差时可能永远达不到。
- **a = 0**：除以 0 会出问题，直接返回 0。无穷大也直接返回（否则 `inf / inf` 得到 NaN，循环不会停）。

**原理：为什么每步精度翻倍**

设当前值 x = √a(1 + ε)，代入公式得 x' = √a(1 + ε²/(2(1 + ε)))。新误差约等于旧误差平方的一半。所以只要 ε 已经比较小，每走一步，正确的位数大约翻一倍。sqrt(42) 从起点 42 开始，相对误差依次是 5.48、2.32、0.81、0.18、1.4e-2、9.5e-5、4.5e-9，再下一步就到了 `double` 的极限，一共 8 次迭代。前几步相对误差下降慢，是因为起点离答案还很远，误差平方的关系还没生效。

Java 打印 `String.format("%.14f", x)`（小数点后 14 位，加上整数位共 15 位有效数字），C++ 打印 `printf("%.15g", x)`，得到 `6.48074069840786`。

**Java**

```java
public static double newtonSqrt(double a) {
    if (!(a >= 0)) throw new IllegalArgumentException("a must be >= 0: " + a);  // 负数和 NaN
    if (a == 0 || Double.isInfinite(a)) return a;
    double x = Math.max(a, 1.0);
    while (true) {
        double next = (x + a / x) / 2;
        if (next >= x) return x;
        x = next;
    }
}
```

**C++**

```cpp
inline double newton_sqrt(double a) {
    if (!(a >= 0)) throw std::invalid_argument("a must be >= 0");
    if (a == 0 || std::isinf(a)) return a;
    double x = std::max(a, 1.0);
    while (true) {
        const double next = (x + a / x) / 2;
        if (next >= x) return x;
        x = next;
    }
}
```

写 `!(a >= 0)` 而不是 `a < 0`，是因为 NaN 和任何数比较都为假，`a < 0` 会放过 NaN。

复杂度：每步 O(1)。a 很大或很小时（如 1e300），起点离答案很远，前面每步只能把值减半，所以迭代次数在这些情形下是几百次（1e300 约 500 次），之后才进入翻倍精度的阶段。

## Part 2 · 整数平方根

**思路**：在 `[1, n]` 里二分，找最大的 `r` 使得 `r * r <= n`。

**原理：两个防溢出的细节**

1. 判断条件不写 `mid * mid <= n`，写 `mid <= n / mid`。mid ≥ 1 时，`mid <= floor(n / mid)` 与 `mid * mid <= n` 等价，但不会溢出。n = `Long.MAX_VALUE` 时，答案 3037000499 的平方 9223372030926249001 虽然放得下，但如果 mid 取到更大的值，`mid * mid` 就溢出了。
2. 取中点用 `lo + (hi - lo + 1) / 2`。向上取整，是因为找的是「最大的满足条件的数」，条件为真时 `lo = mid`，如果向下取整，`lo` 可能不动，循环不会结束。同时不写 `(lo + hi) / 2`，因为 lo + hi 可能超过 `Long.MAX_VALUE`。

不变量：`lo * lo <= n`，答案在 `[lo, hi]` 里。n < 2 的时候直接返回 n（避免 n = 0 时除以 0）。

**Java**

```java
public static long isqrt(long n) {
    if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
    if (n < 2) return n;
    long lo = 1, hi = n;
    while (lo < hi) {
        long mid = lo + (hi - lo + 1) / 2;
        if (mid <= n / mid) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
```

**C++**

```cpp
inline long long isqrt(long long n) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    if (n < 2) return n;
    long long lo = 1, hi = n;
    while (lo < hi) {
        const long long mid = lo + (hi - lo + 1) / 2;
        if (mid <= n / mid) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
```

复杂度：时间 O(log n)，n 接近 2^63 时大约 63 次循环；空间 O(1)。C++ 里有符号溢出是未定义行为（UB），所以防溢出不是可选的。

## Part 3 · 口头追问和回答

**1. 牛顿迭代为什么收敛得这么快？**

见 Part 1 的原理：新误差约等于旧误差平方的一半，所以进入收敛区间之后，正确的位数每步大约翻倍。sqrt(42) 的相对误差是 1.4e-2、9.5e-5、4.5e-9，每一步的指数大约翻倍。这叫二次收敛（quadratic convergence）。

**2. 二分法和牛顿法比，各需要多少步？**

二分法每步只确定 1 个二进制位，`double` 有 53 位有效数字，对 [0, 42] 上的 sqrt(42) 实测，二分到相邻两个 `double` 重合需要 55 步。牛顿法同样的精度只需要 8 步。二分的好处是简单、不会跑偏，不需要除法，也适合整数版。

**3. 为什么 `(long) Math.sqrt(n)` 对大的 n 不可靠？**

`double` 只有 53 位有效数字，n 超过 2^53 时，n 转成 `double` 就要舍入，相邻两个 `double` 的间距超过 1。结果是：n 比一个完全平方数 k² 小 1，转成 `double` 后可能舍入成 k²，开方得到整数 k，而正确答案是 k-1。实测最小的反例是 k = 67108865（即 2^26 + 1），n = k² − 1 = 4503599761588224。Part 2 的 `9223372030926249000` 也是一例：`Math.sqrt` 返回 3037000499.0，正确答案是 3037000498。

**4. 整数版也能用牛顿法吗？**

可以：`x = (x + n / x) / 2`，当 `x` 不再下降时停止，用整数除法。要注意两点：起点不能取 n，因为 n = `Long.MAX_VALUE` 时 `x + n / x = n + 1` 溢出；起点取 2^32 就够，它大于任何 `long` 的平方根，并且 `x + n / x` 不会超过 `Long.MAX_VALUE`。n = 0 要单独处理，不然会除以 0。在 0 到 4999 以及 `Long.MAX_VALUE`、3037000499² 等点上验证过，结果都和精确值一致。

**5. 硬件是怎么算平方根的？**

现代 CPU 有专门的平方根指令（x86 上 `double` 是 `sqrtsd`），`std::sqrt` 和 `Math.sqrt` 通常直接编译成它。IEEE 754 标准要求平方根的结果是「正确舍入」的，也就是和精确值之间最多差半个最低位，所以这条指令的结果是确定的，和软件实现的牛顿迭代相比，不会有最后一位的差别。

**6. 快速平方根倒数是什么？**

用于 1/√x 的一个老技巧：把 `float` 的位模式当整数，`i = 0x5f3759df - (i >> 1)` 得到一个粗略的估计，再做一步牛顿迭代 `y = y * (1.5 - 0.5 * x * y * y)`。在 10 万个随机 `float` 上测得，估计值的最大相对误差约 3.4%，一步牛顿之后约 0.18%。它是在除法和平方根指令很慢的年代用的；现在有硬件指令，一般不再需要。

## 常见错误

1. 迭代停止条件写成 `x * x == a`：浮点数几乎永远不会严格相等，死循环。
2. 没处理 a = 0：`a / x` 除以 0，得到 NaN 或无穷。
3. 整数版判断写成 `mid * mid <= n`：n 很大时乘积溢出，Java 回绕成负数，C++ 是 UB。
4. 用 `(lo + hi) / 2` 取中点，并配合 `lo = mid`：lo + hi 溢出；向下取整时 `lo` 不前进，死循环。
5. 整数版直接 `(long) Math.sqrt(n)`：n 大于 2^53 时会出错。
