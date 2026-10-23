---
id: hl-javaq-e-q18-follow-ups
node: java-questions.e-jit-gc
type: qa
step: 4
---
## Q
追问：什么是代码缓存（code cache），满了会怎样？能不能强制编译或关掉 JIT？
What is the code cache and what happens when it's full? Can you force compilation or disable it?

## A
- **代码缓存**：存放编译后机器码的区域；满了 JIT **停止编译**，性能下降；用 `-XX:ReservedCodeCacheSize` 调大。
- **关掉 / 限制 JIT**：`-Xint` 纯解释；`-XX:TieredStopAtLevel=1` 只用 C1。这些仅用于诊断，**生产别这么做**。
- `-Xint` 还会改变可见性相关的行为（并发里的 bug 表现不同）。
