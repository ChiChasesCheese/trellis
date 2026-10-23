---
id: hl-cq-q20-templates-vs-generics
node: cpp-questions.e-templates
type: qa
step: 1
---
## Q
面试题：C++ 模板和 Java 泛型有什么不同？什么是 concepts 和 SFINAE？
How do C++ templates differ from Java generics? What are concepts and SFINAE?

## A
- **Java 泛型**靠**类型擦除**：编译成同一份字节码，容器里装引用，原始类型要装箱。
- **C++ 模板**是**编译期代码生成**：每个具体类型各自实例化一份，没有装箱、没有擦除，可对 `T` 做任何能编译通过的操作（“编译期鸭子类型”）。
- 代价：代码膨胀、编译变慢、错误信息难读（模板体只在实例化时才检查）。
- **concepts**（C++20）给模板参数写约束；C++11 的老办法是 **SFINAE** 和 `enable_if`。
- 模板还能接收非类型参数，如 `std::array<int, 16>`，Java 做不到。
