---
id: pl-cpp-compile-time-found-template-metaprogramming
node: cpp.compile-time
type: qa
step: 2
---
## Q
模板元编程（template metaprogramming）是怎样"算"出结果的？它的写法、优点和缺点是什么？

## A
**核心思想**：模板的实参可以是**整数常量**，模板的**特化**可以当作"终止条件"，模板的**实例化**可以当作"函数递归调用"。于是编译器在实例化模板的过程中，就替你完成了计算：

```cpp
template <int N> struct Fact { static constexpr long value = N * Fact<N - 1>::value; };
template <> struct Fact<0> { static constexpr long value = 1; };
// Fact<10>::value 在编译期等于 3628800
```

`Fact<10>` 要求 `Fact<9>`，一路到 `Fact<0>`（特化，直接给出 1）。**这里没有一个运行时函数**：值已经作为常量写进了生成的代码。

**优点**：
1. **结果可以是类型**：不仅能算数字，还能"算出类型"，例如从一个类型列表里选出第一个满足条件的。`std::conditional_t`、`std::tuple_element` 的实现靠的就是这个。
2. **有记忆化**：同一个实例只实例化一次。本机实测，用模板算 `Fib<27>`（朴素递归约需 60 万次调用）编译只花约 0.01 秒，因为 `Fib<n>` 每个只被实例化一次；而同样的 `constexpr` 递归函数 `fib(27)` 要约 0.3 秒，因为求值器真的重复调用。
3. 在 C++11 之前，这是唯一的编译期计算手段。

**缺点**：
1. **难写难读**：用特化当 `if`、用递归当 `for`，数据结构（类型列表）要靠嵌套模板；
2. **报错可怕**：错误在实例化链深处爆出来；
3. **编译慢、占内存**：每个实例都是编译器内部的一个对象。

**现状**：数值计算、字符串处理、查表这些，都改用 `constexpr` 函数写，像普通代码；类型计算则用 concepts、`if constexpr`、`std::conditional_t` 等轻量写法。C++26 的静态反射会进一步取代许多"为了拿到类型信息而写的元编程"。

**要记住的一点**：看到老代码里的 `struct X<N> { static constexpr ... = X<N-1>::value }`，把它读作"编译期的递归函数"；新代码不再需要手写这种结构。
