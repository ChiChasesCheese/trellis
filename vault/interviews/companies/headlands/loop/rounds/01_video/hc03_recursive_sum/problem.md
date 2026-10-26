# hc03 · 递归求和 1..n

面试官让你写一个递归函数，算 1 到 n 的和。代码一分钟就能写完，分数在后面的追问里：结果放不下怎么办、n 很大时递归会怎样、能不能不用递归、公式会不会溢出。你要做的是先写出正确的递归，然后跟着追问一步步改。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Write a function that returns the sum of 1 to n, recursively. Don't use the formula."
> 接着会问："What if n is large?" "What about overflow?" "Can you do it without recursion?" "Now use the formula."

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：n 能不能是负数？结果用什么类型？溢出时怎么办？ |
| 3–15 分钟 | **Part 1**：递归版，带溢出检查 |
| 15–30 分钟 | **Part 2**：循环版和公式版 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 递归 + 溢出检查（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static int sumRecursive(int n)` |
| C++ | `int sum_recursive(int n)` |

- `sum(n) = n + sum(n - 1)`，`sum(0) = 0`。
- `n < 0`：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- 结果放不进 `int`：Java 抛 `ArithmeticException`，C++ 抛 `std::overflow_error`。不能返回一个回绕后的负数。
- 例子：`sum(10) = 55`，`sum(65535) = 2147450880`（还放得下），`sum(65536)` 溢出。
- 65536 层递归在默认线程栈上会先栈溢出，所以测试把这两个用例放在一个大栈线程里跑。

## Part 2 · 不用递归（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static long sumIterative(long n)` · `static long sumFormula(long n)` |
| C++ | `long long sum_iterative(long long n)` · `long long sum_formula(long long n)` |

- 结果改用 64 位，负数和溢出的规则同 Part 1。
- `sumIterative(1_000_000) = 500000500000`：一百万层递归会爆栈，循环没有问题。
- `sumFormula` 是 O(1) 的 n(n+1)/2。`sumFormula(4294967295) = 9223372034707292160` 还放得下，但朴素的 `n * (n + 1)` 在这里已经溢出了；`sumFormula(4294967296)` 和 `sumFormula(Long.MAX_VALUE)` 必须报溢出。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. n = 一百万时递归版会怎样？为什么？
2. 尾递归能解决吗？Java 会做尾调用优化吗？C++ 呢？
3. 为什么 C++ 里不能「先加，再看结果是不是变成了负数」？
4. 公式版为什么要先除 2 再乘？
5. 如果给你一亿个数让你求和，怎么并行？

## 边界

- `n = 0`、`n = 1`、`n < 0`
- `int` 的临界点：65535 / 65536
- `long` 的临界点：4294967295 / 4294967296，以及 `Long.MAX_VALUE`

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc03_recursive_sum       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc03_recursive_sum --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc03_recursive_sum       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc03_recursive_sum --tag part1
```
