---
id: hl-javaq-d-q12-main
node: java-questions.d-memory
type: qa
step: 6
---
## Q
`System.arraycopy`、手写循环、`Arrays.copyOf`、`clone` 有什么区别？和 C++ 的 `std::copy` 与 `memcpy` 怎么对应？
`System.arraycopy` vs a hand-written loop vs `Arrays.copyOf` vs `clone` — what's the difference? How does that compare to `std::copy` vs `memcpy`?

## A
一句话：`System.arraycopy` 是 JIT 内联的 intrinsic，语义是 **memmove**（重叠安全），带边界和类型检查；`Arrays.copyOf` = 新数组（分配 + 清零 + 拷贝）；手写循环在热路径上常被 C2 识别成同样的拷贝。

C++ 侧：
- `memcpy` 按字节拷贝，**重叠区域是 UB**，对非平凡可拷贝类型（有自定义拷贝构造 / 虚函数）是错的。
- `memmove` 允许重叠。
- `std::copy` 类型感知：平凡类型通常调用 `memmove`，复杂类型逐个调用赋值运算符。

数组的 `clone()` 与 `Arrays.copyOf` 一样，是分配 + 拷贝。
