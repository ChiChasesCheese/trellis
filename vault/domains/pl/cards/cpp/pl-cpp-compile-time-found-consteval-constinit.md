---
id: pl-cpp-compile-time-found-consteval-constinit
node: cpp.compile-time
type: qa
step: 4
---
## Q
`consteval` 与 `constinit` 各解决什么问题？静态初始化顺序问题（static initialization order fiasco）是什么？

## A
**`consteval`（C++20）**：标记"**立即函数**"，每次调用都**必须**在编译期求值。如果实参不是常量，直接报错：

```cpp
consteval int sq(int x) { return x * x; }
constexpr int a = sq(4);      // OK
int b = sq(argc);             // 错误
```

真实报错：`call to consteval function 'sq' is not a constant expression`，附注 `function parameter 'argc' with unknown value cannot be used in a constant expression`。适用于**绝不允许在运行时执行**的函数：编译期校验格式串（`std::format` 就是这样在编译期检查 `"{}"` 的数量）、生成字符串哈希。

**`constinit`（C++20）**：用于**静态存储期**变量（全局变量、静态局部变量），要求它必须用**常量表达式**初始化，但变量本身仍然**可修改**。

```cpp
constexpr int f() { return 1; }  int g() { return 2; }
constinit int a = f();   // OK
constinit int b = g();   // 错误: variable does not have a constant initializer
```

**它解决的问题：静态初始化顺序灾难**。不同源文件里的全局变量，**初始化顺序未规定**。如果 A.cpp 里的全局变量初始化时用到 B.cpp 里的全局变量，而后者还没初始化，就读到零或垃圾，且换一次链接顺序结果就变。

**原因**：全局变量有两种初始化方式：
1. **静态初始化**（常量初始化）：值在编译期已知，直接写进可执行文件的数据段，程序启动时已经在位，不存在顺序问题；
2. **动态初始化**：要在程序启动时执行代码，不同文件之间顺序不确定。

`constinit` 要求你的全局变量一定走第 1 种，编译器帮你证明"这里没有动态初始化"，因而不会掉进顺序陷阱。需要不可变就用 `constexpr`，需要可变但要安全就用 `constinit`。

**三者分工**：
- `constexpr`：值是编译期常量，不可变；
- `consteval`：函数必须在编译期执行；
- `constinit`：变量必须常量初始化，之后可变。

**要记住的一点**：全局可变状态用 `constinit` 声明，是消除静态初始化顺序问题的最便宜办法。
