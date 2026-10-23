---
id: hl-cq-q23-impl-unspecified-undefined
node: cpp-questions.f-ub-debug
type: qa
step: 3
---
## Q
C++ 里“实现定义”（implementation-defined）、“未指定”（unspecified）和“未定义”（undefined）行为有什么区别？无符号溢出算 UB 吗？实际怎么避免有符号溢出？

## A
- **实现定义**：编译器必须写文档说明，例如 `sizeof(int)`。
- **未指定**：几种合法结果之一都行，例如函数实参的求值顺序。
- **未定义**：没有任何约束。
- **无符号溢出不是 UB**：按 2^N 取模回绕。
- **避免有符号溢出**：用更宽的类型，或在需要回绕时用无符号；运算前先检查；或用溢出内建函数。
