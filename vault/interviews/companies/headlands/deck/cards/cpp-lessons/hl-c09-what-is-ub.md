---
id: hl-c09-what-is-ub
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 1
---
## Q
面试问：什么是未定义行为（undefined behaviour，UB）？它和 Java 的行为有何不同？
Interview question: What is undefined behaviour in C++?

## A
- **Java**：每个程序行为都有定义。整数溢出回绕，数组越界抛 `ArrayIndexOutOfBoundsException`，空引用抛 `NullPointerException`，数据竞争也只会读到「某个写过的值」。
- **C++**：标准把一类错误标成 UB——程序一旦执行到，**标准对整个程序不再有任何要求**：可能碰巧正常、崩溃、结果错，或编译器因为「UB 不会发生」的假设把你的检查整个删掉。
- 最危险的特点：UB 的表现取决于优化级别、编译器版本、周围代码，**测试通过不代表没有**。
