---
id: pl-trends-others-intro-cpp
node: trends.other-languages
type: qa
step: 2
---
## Q
C++ 的核心思想是什么：零开销原则（zero-overhead principle）、RAII 和模板？它们怎样影响了 Rust 和其他语言？

## A
**背景**：C++ 在 1980 年代作为“带类的 C”出现，目标是在保留 C 的性能和硬件控制能力的同时提供抽象。

**零开销原则**（Bjarne Stroustrup 的表述）：你不使用的特性，不应该为它付出代价；你使用的特性，手写也不会更好。抽象应该在编译期消失，运行时只剩机器码。

**RAII**（Resource Acquisition Is Initialization，资源获取即初始化）：把资源（内存、文件、锁）的生命周期绑定到一个对象的生命周期。对象创建时获取，离开作用域时**析构函数自动运行**释放，包括异常发生时。

```cpp
Guard a("A");
{ Guard b("B"); ... }       // b's destructor runs at the closing brace
```

真实输出顺序：`acquire A`、`acquire B`、`release B`、`end of main`、`release A`：释放发生在作用域结束的确定位置，与垃圾回收的“某个以后的时刻”不同。

**模板**（templates）：在编译期根据类型参数生成专门的代码，`maxof<int>` 与 `maxof<double>` 是两份独立的机器码，没有运行时的类型判断。代价是编译慢、错误信息长。

**流向**：
- **Rust** 把 RAII 变成默认和强制：`Drop` trait 在值离开作用域时运行，所有权系统保证只释放一次，并在此之上加了借用检查。泛型也采用单态化（和模板同样生成专用代码），但加了 trait 约束让错误清晰。
- **Go** 在一定程度上是对 C++ 复杂度和编译时间的反应。
- **Java/C#** 的泛型选择了不同路径（擦除、运行时具体化），避免模板的代码膨胀。

**要记住的一点**：C++ 证明了“强抽象加高性能”可以同时成立，代价是语言复杂度；Rust 是在不放弃这个目标的前提下，试图把这种复杂度变成编译期检查。
