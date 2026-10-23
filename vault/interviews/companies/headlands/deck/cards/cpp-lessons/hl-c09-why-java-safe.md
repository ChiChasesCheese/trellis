---
id: hl-c09-why-java-safe
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 16
---
## Q
面试问：Java 为什么没有这些问题？代价是什么？
Interview question: Why does Java not have undefined behaviour, and what does it cost?

## A
- Java 在**运行期做检查**：边界、空引用、类型；**GC 保证内存安全**（没有 use-after-free、double free）；数据竞争只有弱语义。
- 代价：检查带来运行时开销，GC 带来**不可预测的暂停**，还有对象头和指针间接。
- C++ 反之：不检查换速度，由程序员负责。
