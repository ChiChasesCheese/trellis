---
id: hl-c06-lambda-what
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 9
---
## Q
面试问：C++ lambda 是什么？和函数指针、`std::function` 有什么区别？
Interview question: What is a lambda, and how does it differ from a function pointer and `std::function`?

## A
- lambda 是**编译器生成的匿名函数对象类**：`[捕获](参数){ 函数体 }`。每个 lambda 有**独一无二的类型**，用 `auto` 或模板参数接收时可以完全**内联**。
- **函数指针**：无状态。
- **`std::function`**：类型擦除，可存任意可调用对象，换来统一类型但多一次间接调用，大捕获还可能堆分配。
- 实践：热路径用模板参数/`auto`；需要**存储回调**才用 `std::function`。
