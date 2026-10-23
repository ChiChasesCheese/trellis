---
id: hl-j16-hb-def
node: java21.j16-concurrency-primitives
type: qa
step: 6
---
## Q
什么是 Java 内存模型（JMM）和先行发生（happens-before，HB）？数据竞争（data race）又是什么？

## A
**JMM** 是一套规则，说明什么情况下线程 B 一定看到线程 A 的写入。核心概念是 **happens-before**：X HB Y ⇒ X 的结果对 Y **可见**，且 X 不会被重排到 Y 之后。

**数据竞争**：两个线程访问同一变量、至少一个是写、且它们之间**没有 HB 关系**。有数据竞争的程序 JMM 几乎不保证什么（只保证「不凭空造值」）。

目标：**每一对「写—读」之间都能找到一条 HB 链**。
