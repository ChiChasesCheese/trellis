---
id: pl-cpp-compile-time-found-constexpr
node: cpp.compile-time
type: qa
step: 3
---
## Q
`constexpr` 函数和 `constexpr` 变量是什么？同一个函数怎样既能在编译期、又能在运行期使用？

## A
**`constexpr` 变量**：声明时必须用**常量表达式**初始化，值在编译期确定，可以用作数组大小、模板实参，并且被放进只读数据段。

**`constexpr` 函数**：一个"**可以**在编译期求值"的函数。如果所有实参在编译期已知，并且结果被用在需要常量的地方，编译器就在编译期执行它；否则它是一个普通运行时函数。**同一份源码两种用法**，不用写两个版本。

```cpp
constexpr int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
static_assert(fib(10) == 55);       // 编译期求值，错了就编译失败
fib(argc + 9);                       // 实参运行时才知道：普通函数，实测得 55
```

**能做什么（越来越多）**：
- C++11：单个 `return` 表达式；
- C++14：局部变量、循环、分支；
- C++20：编译期动态分配（仅限在求值结束前释放的临时分配）、`std::string`、`std::vector`、虚函数；
- C++23：更多标准库函数标成 `constexpr`。

**一个实用例子**：在编译期生成查找表：

```cpp
constexpr auto primes() {
  std::array<int, 20> a{}; int n = 0;
  for (int i = 2; n < 20; ++i) { bool p = true;
    for (int j = 2; j * j <= i; ++j) if (i % j == 0) p = false;
    if (p) a[n++] = i; }
  return a;
}
constexpr auto P = primes();   // P[19] == 71，数据已在可执行文件里
```

运行时 `P[19]` 只是一次内存读取，没有任何计算。

**限制**：不能做 I/O、不能调用没有标成 `constexpr` 的函数、不能依赖运行时才有的信息（随机数、当前时间、命令行参数）。

**要记住的一点**：`constexpr` 函数是"能在编译期用的普通函数"，函数名带 `constexpr` 不保证编译期执行；是否在编译期，取决于**调用的上下文**。
