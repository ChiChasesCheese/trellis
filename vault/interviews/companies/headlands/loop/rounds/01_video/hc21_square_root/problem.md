# hc21 · 平方根

面试之前就有人被要求「写一个 C++ 程序，打印 42 的平方根」，面试官喜欢追问你是怎么做的。标准库一行 `std::sqrt(42)` 就能完成，所以真正的问题是：不用库函数，你能不能自己写出来，并说清楚它为什么对。先写牛顿迭代求 `double` 的平方根，再写不用浮点数的整数平方根（`long` 范围内不溢出），最后口头回答收敛速度、`(long) Math.sqrt(n)` 为什么不可靠、硬件怎么算平方根。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Write a C++ program that prints the square root of 42. Don't call `sqrt`."
> 接着会问："How did you pick the starting value?" "When do you stop?" "What about 0 and negative numbers?" "Now do it for a `long`, without floating point." "Why is `(long) Math.sqrt(n)` wrong?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：精度要到几位？负数怎么处理？输入是 `double` 还是整数？ |
| 3–15 分钟 | **Part 1**：牛顿迭代，打印 sqrt(42) |
| 15–30 分钟 | **Part 2**：整数平方根 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 牛顿迭代（约 13 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static double newtonSqrt(double a)` |
| C++ | `double newton_sqrt(double a)` |

- 迭代公式 `x' = (x + a / x) / 2`。
- 起点、停止条件自己定，并且要能说出理由。负数和 NaN 抛异常（Java `IllegalArgumentException`，C++ `std::invalid_argument`）；`a = 0` 直接返回 0。
- 结果和 `Math.sqrt` / `std::sqrt` 的相对误差不超过 1e-12。
- 打印 sqrt(42) 到 15 位有效数字，得到 `6.48074069840786`（Java `String.format("%.14f", x)`，C++ `printf("%.15g", x)`）。
- 例子：`newtonSqrt(144) ≈ 12`，`newtonSqrt(0.25) ≈ 0.5`，`newtonSqrt(1e300)` 和 `newtonSqrt(1e-300)` 也要对，不能死循环。

## Part 2 · 整数平方根（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static long isqrt(long n)` |
| C++ | `long long isqrt(long long n)` |

- 返回 `floor(sqrt(n))`，n ≥ 0；不用浮点数，任何中间值都不能溢出。n < 0 抛异常。
- 例子：`isqrt(0)=0`，`isqrt(15)=3`，`isqrt(16)=4`，`isqrt(10^12)=1000000`，`isqrt(10^12-1)=999999`。
- `isqrt(Long.MAX_VALUE) = 3037000499`。3037000499 的平方是 9223372030926249001，已经很贴近 `Long.MAX_VALUE`，所以 `mid * mid` 这种写法在这里会溢出。
- `isqrt(9223372030926249000) = 3037000498`：比完全平方数少 1，用浮点数的写法会在这里出错。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 牛顿迭代为什么收敛得这么快？每一步精度发生了什么变化？
2. 二分法和牛顿法比，各需要多少步？
3. 为什么 `(long) Math.sqrt(n)` 对大的 n 不可靠？
4. 整数版也能用牛顿法吗？要注意什么？
5. 硬件是怎么算平方根的？
6. 「快速平方根倒数」是什么？

## 边界

- `a = 0`，`a < 0`，NaN，很大和很小的 `a`
- `n = 0`、`n = 1`，完全平方数和它前面的一个数
- `Long.MAX_VALUE`，以及 3037000499 的平方

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc21_square_root       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc21_square_root --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc21_square_root       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc21_square_root --tag part1
```
