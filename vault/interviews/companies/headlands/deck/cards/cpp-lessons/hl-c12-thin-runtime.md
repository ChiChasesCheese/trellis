---
id: hl-c12-thin-runtime
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 2
---
## Q
面试问：Why is C++ faster than other languages? 机制一：运行期系统薄（「不用不付费」）具体指哪些？
Interview question: Why is C++ faster than Java?

## A
- **没有垃圾回收**：没有 GC 线程抢核，没有停顿（safepoint）；不分配就没有分配成本。
- 数组/`vector` 的 `operator[]` **默认不做边界检查**，整数运算直接是机器指令（代价：越界是未定义行为）。
- **没有虚拟机和预热**：编译一次，进程启动即满速；Java 要解释 → C1 → C2 逐步优化，还可能因类型假设失效而**去优化**（deoptimization）。
- 虚函数**只有声明了 `virtual` 才付费**；非虚调用是普通调用，且可内联。
- **零开销抽象**：迭代器、算法、lambda、`unique_ptr` 优化后与手写代码生成相同的机器码。
