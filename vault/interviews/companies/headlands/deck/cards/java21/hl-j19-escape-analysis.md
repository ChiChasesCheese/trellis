---
id: hl-j19-escape-analysis
node: java21.j19-runtime-zgc-jit
type: qa
step: 24
---
## Q
什么是逃逸分析（escape analysis）和标量替换（scalar replacement）？它们对低延迟有什么意义？

## A
JIT 分析「`new` 出来的对象是否会被存到堆里、传给别的线程、从方法返回」。**不逃出方法**就根本不必在堆上分配：把字段拆成几个**局部变量**（寄存器），连对象头都不要，这就是标量替换。

意义：分配得少 → GC 触发得少 → 暂停得少。所以「写出让 JIT 看穿的代码」（小方法、不把临时对象存进字段、`record` + 局部使用）是 Java 低延迟的第一原则。

逃逸分析**依赖内联**：对象一传进没被内联的方法，对 JIT 来说就逃逸了。
