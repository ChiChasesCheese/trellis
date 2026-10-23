---
id: hl-c09-why-ub-exists
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 2
---
## Q
面试问：C++ 为什么保留 UB，而不是直接定义成崩溃或回绕？
Interview question: Why does C++ keep undefined behaviour instead of defining it?

## A
标准把「程序员保证不会发生」的情况交给编译器当前提，就不必生成检查代码：
- 不做**数组边界检查**（快）。
- 假设**有符号整数不会溢出**（循环可以向量化）。
- 假设**不同类型的指针不指向同一内存**（可以重排读写）。
- 可做优化：向量化、别名分析、删死代码。

一句话：**快是用「出错时不可预测」换来的**。Java 则靠运行期检查和 GC 保证安全，代价是检查开销和不可预测的 GC 暂停。
