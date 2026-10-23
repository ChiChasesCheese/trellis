---
id: hl-cq-q31-false-sharing
node: cpp-questions.g-concurrency
type: qa
step: 18
---
## Q
面试题：什么是伪共享（false sharing）？怎么检测和避免？
What is false sharing? How would you detect and avoid it?

## A
- 两个线程各自写**不同的变量**，但这两个变量在**同一条缓存行**（通常 64 字节）上；缓存一致性协议让这条线在核之间来回搬运，性能暴跌，线程实际上被串行化了，哪怕它们没有共享数据。
- 解决：让各线程的热变量**各占一条缓存行**——`alignas(64)` 或填充。
- 补充：**真共享**（true sharing）是多个线程确实在写同一个变量，只能靠减少共享或批处理解决。
