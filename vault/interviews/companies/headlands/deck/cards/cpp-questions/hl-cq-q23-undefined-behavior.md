---
id: hl-cq-q23-undefined-behavior
node: cpp-questions.f-ub-debug
type: qa
step: 1
---
## Q
面试题：什么是未定义行为（UB）？C++ 为什么要有它？举例。
What is undefined behavior? Why does C++ have it? Give examples.

## A
- **UB**：标准对这个程序**不作任何规定**，编译器可以假设它永远不会发生并据此优化；结果可能是“正常”、崩溃，或莫名其妙的错误结果，而且 `-O0` 和 `-O2` 可以不同。
- **为什么保留**：为了不为“检查”付费（边界、溢出、空指针的检查，不要求就不花钱）。
- **常见 UB**：有符号整数溢出；数组 / 容器越界；解引用空指针或悬空指针；读未初始化变量；移位量 ≥ 位宽或为负；数据竞争；严格别名违规；非 `void` 函数没有 `return` 就结束；修改 `const` 对象；违反 ODR。
