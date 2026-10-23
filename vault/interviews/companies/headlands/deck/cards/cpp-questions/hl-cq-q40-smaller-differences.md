---
id: hl-cq-q40-smaller-differences
node: cpp-questions.j-cross-language
type: qa
step: 4
---
## Q
除了对象模型和内存，Java 与 C++ 还有哪些较小的差别？`final` 和 `const`、方法默认是否虚、构建模型、`volatile`。

## A
- **`final` vs `const`**：Java 的 `final` 固定的是引用；C++ 的 `const` 约束的是对象。
- **方法**：C++ 默认**非虚**。
- **构建模型**：头文件加链接器，而不是 classpath。
- **`volatile`**：含义不同——在 C++ 里它不是同步。
