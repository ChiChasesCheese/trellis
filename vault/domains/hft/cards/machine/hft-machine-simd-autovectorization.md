---
id: hft-machine-simd-autovectorization
node: machine.simd
type: qa
step: 3
---
## Q
编译器的自动向量化（auto-vectorization）需要循环满足哪些条件？Java 和 C++ 在使用 SIMD 上有什么不同？

## A
自动向量化是编译器（或 JIT）自己把普通标量循环改写成 SIMD 指令。它通常要求：
- 循环次数在进入循环时就能确定（简单的 `for (i = 0; i < n; i++)`）；
- 访问的是**连续**的数组，下标是 `i` 这种简单形式；
- 迭代之间**没有依赖**（`a[i]` 的结果不依赖 `a[i-1]`），也没有提前跳出（`break`）；
- 编译器能确定两个数组不会互相重叠（别名，aliasing）。

任何一条被破坏，编译器就会保守地放弃，退回标量代码。

对比：
- **Java**：HotSpot 的 C2 编译器能自动向量化一部分简单循环（叫 SuperWord），但不保证；想显式控制可用 `jdk.incubator.vector` 的 Vector API（仍是孵化模块）。
- **C++**：除自动向量化外，还可以直接写 intrinsics（如 `_mm256_add_epi32`）或手写汇编，控制力最强，但可移植性差。

实践：先写简单、连续、无依赖的循环，再用编译器报告或性能测量确认它真的被向量化了，不要想当然。
