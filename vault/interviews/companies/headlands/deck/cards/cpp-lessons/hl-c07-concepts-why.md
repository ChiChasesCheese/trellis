---
id: hl-c07-concepts-why
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 9
---
## Q
面试问：C++20 的 concepts 解决什么问题？和 Java 的 `<T extends Comparable<T>>` 有什么相似与不同？
Interview question: What problem do C++20 concepts solve?

## A
- **问题**：模板对 `T` 的要求只写在文档里，传错类型就是几百行模板内部报错。
- **concept** 是命名的**编译期谓词**，写在模板头上，相当于 Java 的 `<T extends Comparable<T>>`，但还能表达「这段代码能编译」。
- 好处：①要求写进接口；②**错误信息直接指出被违反的约束**（如 `'std::string' does not satisfy 'Numeric'`）；③基于约束的重载选择。
- 它同时取代了 SFINAE 式写法。
