---
id: hl-javaq-e-q20-say60
node: java-questions.e-jit-gc
type: qa
step: 29
---
## Q
用英文 60 秒回答：What is escape analysis? What optimisations come from it, and when does it fail?

## A
结构：证明对象不逃出方法 → 标量替换与锁消除 → 实测 48 ms 对 386 ms 与 4.8 GB → 依赖内联、存进字段或容器就失败 → 当作额外收益并用计数器验证。

> "Escape analysis is a C2 optimisation that proves an object never leaves the compiled method - it's not stored in a field, returned, or passed to a call that wasn't inlined. If so, the JVM can do scalar replacement: the object's fields live in registers and the allocation disappears; it can also elide locks on such objects. I measured it on a small immutable `Point` record in an arithmetic loop: with it on, steady state allocated zero bytes and ran in about 48 ms; with `-XX:-DoEscapeAnalysis` it allocated 4.8 GB and took about 386 ms. It depends on inlining, so it fails when the method is too big or the object is stored somewhere. I treat it as a bonus rather than a guarantee, and verify with allocation counters."
