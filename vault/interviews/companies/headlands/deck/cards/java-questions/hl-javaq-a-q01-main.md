---
id: hl-javaq-a-q01-main
node: java-questions.a-speed
type: qa
step: 1
---
## Q
面试官问：Java 有垃圾回收（GC）、还跑在虚拟机上，为什么还能很快？C++ 编译器在编译期做的事，JVM 在运行时做什么？
Why can Java be fast even though it is garbage-collected and runs on a VM? What does the JVM do at run time that a C++ compiler does ahead of time?

## A
一句话：Java 源码先编成**字节码**（bytecode），运行时热点方法被 JIT（即时编译器，just-in-time compiler，分 C1 和 C2 两级）编成机器码，并且能用**运行时才知道的信息**优化：真实类型分布、分支概率、已加载的类。

要说的点：
- 稳态下 Java **不是解释执行**：先解释、再 C1、更热再 C2（激进优化）。
- 利用运行时信息做**内联**（inlining）、**逃逸分析**（escape analysis）、**去虚化**（devirtualization）、消除边界检查。
- 代价：**预热**慢、GC、比 C++ 更大的内存占用（对象头 + 指针）。
- 面试官做低延迟，不要说"Java 一样快"，也不要说"Java 慢"。
