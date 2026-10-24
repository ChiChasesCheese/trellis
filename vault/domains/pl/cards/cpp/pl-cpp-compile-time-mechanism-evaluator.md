---
id: pl-cpp-compile-time-mechanism-evaluator
node: cpp.compile-time
type: qa
step: 6
---
## Q
编译期求值（constant evaluation）在编译器里是怎么执行的？它对 UB 和步数有什么限制，速度怎样？

## A
**机制**：编译器内置一个**解释器**（抽象机），在编译时一步步执行 `constexpr` 函数。它不会生成机器码再运行，而是直接解释抽象语法树。因为它在解释，所以每一步都能检查操作是否合法。

**能抓出 UB**：常量表达式里**不允许 UB**，求值器遇到就让整个表达式"不是常量"并报错。本机真实报错：

```cpp
constexpr int ov()  { int x = INT_MAX; return x + 1; }          // 有符号溢出
constexpr int oob() { int a[3] = {1,2,3}; int i = 3; return a[i]; }  // 越界
constexpr int np()  { int* p = nullptr; return *p; }             // 空指针
```
- `value 2147483648 is outside the range of representable values of type 'int'`
- `read of dereferenced one-past-the-end pointer is not allowed in a constant expression`
- `read of dereferenced null pointer is not allowed in a constant expression`

这使得编译期求值成为**一个没有 UB 的受控环境**：想验证一段算法没有越界或溢出，就在 `static_assert` 里用测试数据调用它，如果有 UB，编译直接失败。

**步数上限**：为避免死循环卡住编译，求值器有步数上限（Clang 默认约一百万步，可用 `-fconstexpr-steps` 调整）。实测 `loop(10'000'000)` 报错：`constexpr evaluation hit maximum step limit; possible infinite loop?`。

**速度**：解释执行比机器码慢几个数量级。同一个朴素递归 `fib(27)`，用 `constexpr` 在编译期求值使编译耗时约 0.3 秒，运行时机器码版本约 0.3 毫秒（一次测量），差三个数量级。所以**不要把重计算放进 `constexpr`**，只放真正需要在编译期得到的结果。

**其他限制**：不能做 I/O，不能访问外部状态（环境变量、文件），不能调用非 `constexpr` 函数；C++20 起可以分配堆内存，但必须在求值结束前释放，结果不能带指向堆的指针出来。

**对比**：Rust 的 `const fn` 同样由一个解释器（MIR 解释器）执行，同样拒绝 UB，同样有步数/时间的限制；这是"编译期执行"这类机制的共同形态，不是 C++ 独有。

**要记住的一点**：把 `constexpr` 当作一个安全沙盒来用：用它做测试和生成表，不用它做重计算。
