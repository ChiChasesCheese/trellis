---
id: pl-cpp-compile-time-pitfall-not-really-compile-time
node: cpp.compile-time
type: qa
step: 10
---
## Q
`constexpr` 最常见的误用是什么？为什么标了 `constexpr` 的函数仍可能在运行时执行，编译期求值又怎样把构建拖垮？

## A
**误区一：以为 `constexpr` 函数一定在编译期执行**。它只表示"可以"。

```cpp
constexpr int csq(int x) { return x * x; }
int c = csq(argc);          // 实参运行时才知道：在运行时执行，合法
constexpr int a = csq(4);   // 在常量上下文：编译期求值
int d = csq(4);             // 允许编译期，也允许运行时；由优化器决定
```

很多人以为 `int d = csq(4)` 一定在编译期算，其实标准不保证；在 `-O0` 下它可能真的在运行时调用。**要保证**，用 `constexpr` 变量接收，或把函数标 `consteval`（对 `sq(argc)` 这样的调用，编译器直接报错 `call to consteval function`）。

**误区二：把重计算放进 `constexpr`**。求值器是解释器：

```cpp
constexpr int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
constexpr int r = fib(27);
```

实测这一行让编译多花约 0.3 秒（一次测量）；`fib(30)` 就超出步数上限，报 `constexpr evaluation hit maximum step limit`。如果这样的表达式出现在每个源文件都包含的头文件里，**每个翻译单元都要重新求值一遍**，全项目构建时间成倍增加。

**误区三：编译期容器的幻觉**。C++20 允许在 `constexpr` 函数里用 `std::vector`/`std::string`，但分配必须在求值结束前释放，结果必须转成 `std::array` 或常量才能带出来；想把 `std::vector` 本身做成 `constexpr` 全局变量，会报错。

**误区四：`if constexpr` 的条件依赖了非模板参数**。在非模板函数里，被丢弃的分支仍会被完整检查，并不会"不编译"。

**对策**：
1. 用 `consteval` 或 `constexpr` 变量表达"必须在编译期"；
2. 用 `-ftime-trace` 发现耗时的常量求值；
3. 大表放在一个 `.cpp` 里生成，通过函数访问，避免每个文件重复求值；
4. 复杂的预计算，用单独的构建期代码生成程序，而不是塞进 `constexpr`。

**要记住的一点**：`constexpr` 描述的是"**允许**"，不是"**保证**"；要保证，用 `constexpr` 变量或 `consteval`。
