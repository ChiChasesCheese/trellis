# hc03 · 解法与原理

递归求和本身不难，难在每一句追问都在看你懂不懂计算机的某一层：整数怎么表示、函数调用怎么占用栈、编译器能帮你做什么。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll write `sum(n) = n + sum(n - 1)` with `sum(0) = 0`. Before I start: can n be negative? What type should the result be? And what should happen if the sum doesn't fit — throw, or return something special?"

面试官通常会说：负数抛异常，先用 `int`，溢出要报错。问出这三点，说明你在写代码之前就想到了边界。

## Part 1 · 递归 + 溢出检查

**思路**：先判断 `n < 0`，再写递归出口 `n == 0`，最后把加法换成「会检查溢出的加法」。

**原理：为什么要检查溢出**

`int` 是 32 位补码，最大值 2147483647。1+…+65535 = 2147450880 还放得下，再加 65536 就超了。

- **Java**：超出时加法会**回绕**成一个负数，不报错。`Math.addExact` 会在溢出时抛 `ArithmeticException`。
- **C++**：有符号整数溢出是**未定义行为**（undefined behavior，UB）。编译器可以假设它永远不会发生，所以「先加完，再判断结果是不是变成了负数」这种写法，判断本身可能被优化掉。正确做法是用 `__builtin_add_overflow`（clang / gcc 都支持）：它一边加一边告诉你有没有溢出。

**Java**

```java
public static int sumRecursive(int n) {
    if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
    if (n == 0) return 0;
    return Math.addExact(n, sumRecursive(n - 1));
}
```

**C++**

```cpp
inline int sum_recursive(int n) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    if (n == 0) return 0;
    int sum;
    if (__builtin_add_overflow(n, sum_recursive(n - 1), &sum)) throw std::overflow_error("sum does not fit int");
    return sum;
}
```

复杂度：时间 O(n)，栈空间 O(n)，因为每一层递归都占一个栈帧。

## Part 2 · 循环版和公式版

**循环版的思路**：递归在每一层栈帧里「记着」还没加上的 n，循环用一个变量 `sum` 记住同样的信息。栈空间从 O(n) 变成 O(1)。

**公式版的思路**：1+…+n = n(n+1)/2，O(1)。

**原理：公式为什么要先除 2 再乘**

n 和 n+1 里恰好有一个是偶数，所以 n(n+1) 一定能被 2 整除。但如果先算 n × (n+1)，中间结果是答案的 2 倍：n = 4294967295 时，答案 9223372034707292160 还放得进 `long`，乘积却已经放不下了。先把偶数的那个除以 2 再乘，中间结果就不会比答案大，只剩最后这一次乘法可能溢出，用 `Math.multiplyExact` / `__builtin_mul_overflow` 检查即可。

还有一个小坑：n = `Long.MAX_VALUE` 是奇数，(n+1)/2 不能直接写成 `(n + 1) / 2`，因为 n + 1 本身就溢出了。改写成 `n / 2 + 1`，对奇数 n 两者相等。

**Java**

```java
public static long sumIterative(long n) {
    if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
    long sum = 0;
    for (long i = 1; i <= n; i++) sum = Math.addExact(sum, i);
    return sum;
}

public static long sumFormula(long n) {
    if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
    return n % 2 == 0 ? Math.multiplyExact(n / 2, n + 1) : Math.multiplyExact(n, n / 2 + 1);
}
```

**C++**

```cpp
inline long long sum_iterative(long long n) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    long long sum = 0;
    for (long long i = 1; i <= n; ++i)
        if (__builtin_add_overflow(sum, i, &sum)) throw std::overflow_error("sum does not fit long long");
    return sum;
}

inline long long sum_formula(long long n) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    const long long a = n % 2 == 0 ? n / 2 : n;
    const long long b = n % 2 == 0 ? n + 1 : n / 2 + 1;
    long long product;
    if (__builtin_mul_overflow(a, b, &product)) throw std::overflow_error("sum does not fit long long");
    return product;
}
```

## Part 3 · 口头追问和回答

**1. n = 一百万时递归版会怎样？**

会栈溢出。每次函数调用都要在线程栈上压一个栈帧（参数、局部变量、返回地址），栈的大小是固定的。Java 抛 `StackOverflowError`；C++ 是进程直接收到 `SIGSEGV` 崩溃，`try/catch` 接不住。在 C++ 里，一个 512 KiB 的线程栈能走多深，取决于每个帧有多大，在这台 Mac 上实测：`-O0` 约 7700 层，`-O2` 约 3 万层，开 ASan 时约 1.5 万层。所以「能递归多深」没有固定答案。

**2. 尾递归能解决吗？**

尾递归是指递归调用是函数的最后一个动作，例如 `sum(n, acc) = sum(n - 1, acc + n)`。理论上编译器可以把它变成循环（尾调用优化，tail call optimization，TCO）。

- **Java 永远不做**：JVM 的栈帧对异常堆栈、调试器是可见的，`javac` 和 JIT 都不消除尾调用。
- **C++ 可能做，但标准不保证**：在这台 Mac 上用 clang 跑一亿层，`-O0` 时尾递归和普通递归都会崩，`-O2` 时两种都能跑完（clang 连 `n + f(n-1)` 都改成了循环）。换个编译选项就会崩的代码不能依赖。clang 的 `[[clang::musttail]]` 可以强制尾调用，但只有 clang 支持。

结论：**要稳定的栈深就写循环**。

**3. 为什么 C++ 里不能「先加，再看结果是不是变成了负数」？**

因为有符号溢出是 UB。编译器看到 `if (a + b < a)` 时，可以推理「a + b 不会溢出，所以这个条件当 b ≥ 0 时永远为假」，然后直接删掉这个判断。无符号整数的溢出是有定义的回绕，有符号的不是。

**4. 公式版为什么要先除 2 再乘？**

见 Part 2 的原理：先乘，中间结果是答案的 2 倍，会比答案先溢出。

**5. 一亿个数怎么并行求和？**

切成「核数」那么多块，每个线程算一块的部分和，最后把部分和加起来。

- **Java**：可以用 `ForkJoinPool` 或者 `LongStream.parallel().sum()`。
- **C++**：可以用几个 `std::thread`，或者 `std::async`。线程数取核数（`hardware_concurrency()`），不要一块一个线程。

还要说到两点：

- 求和是**内存带宽受限**的，核数翻倍，速度不会跟着翻倍；数据太少时，开线程的成本比计算本身还高。
- 整数加法满足结合律，所以怎么切块结果都一样；`double` 不满足，并行的结果会和顺序求和有微小差别。

## 常见错误

1. 忘记 `n < 0` 的检查：递归永远到不了出口，一直到栈溢出。
2. 用普通的 `+`：Java 静默回绕成负数，C++ 是 UB。
3. 公式写成 `n * (n + 1) / 2`：n 大的时候中间结果先溢出。
4. 说「编译器会把尾递归优化掉，所以没事」：Java 不做，C++ 不保证。
