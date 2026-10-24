---
id: pl-cpp-philosophy-found-zero-overhead
node: cpp.philosophy
type: qa
step: 2
---
## Q
C++ 的“零开销原则”（zero-overhead principle）具体是哪两句话？怎样用实测检验一个抽象是否真的零开销？

## A
Stroustrup 的表述有两半：
1. **不用的不付费**：程序没用到某个语言特性，就不该为它承担任何运行时成本。没有虚函数的类没有虚表指针；没写 `try` 的路径上没有额外指令。
2. **用到的手写也不会更快**：用了某个高层抽象，生成的代码不该比你亲手写的低层版本更慢。

注意“零开销”指**运行时**，不是编译时间，也不是学习成本；这两项恰恰是 C++ 付出的代价。

**检验方法**：比较抽象版本与手写版本的体积、汇编和耗时。本机（Apple Silicon，`-O2`）实测：

```cpp
std::unique_ptr<int> p;   // sizeof == 8，与裸指针 int* 相同
std::array<int, 4> a;     // sizeof == 16，与 int[4] 相同
std::accumulate(v.begin(), v.end(), int64_t{0});  // 对比手写下标循环
```

一亿个 `int` 求和，`std::accumulate` 约 4.6 ms，手写下标循环约 4.4 ms，量级相同（一次测量）。`std::accumulate` 是模板，调用时被内联展开成同样的循环，编译器还会自动向量化。

**例外要知道**：零开销只对“被编译器看穿的抽象”成立。`std::function`、虚函数、`shared_ptr` 的原子引用计数都是有成本的抽象；它们遵守的是第一句话（你不用就不付费），而不是第二句。

**要记住的一点**：判断一个 C++ 抽象的成本，不要看名字，看它是被编译期展开（模板、`constexpr`、内联），还是引入了运行时机制（虚表、堆分配、原子操作）。
