---
id: hl-javaq-f-q25-say60
node: java-questions.f-concurrency
type: qa
step: 30
---
## Q
用英文 60 秒回答：What is the Java Memory Model? What does "happens-before" mean, and why do we need it?

## A
结构：为什么需要（编译器与 CPU 重排、缓存）→ happens-before 的含义与规则 → 没有边就是数据竞争 → 自己测过的 volatile 与普通标志位实验。

> "The memory model defines when one thread's writes are guaranteed to be visible to another, because compilers and CPUs reorder instructions and cache values. The central concept is happens-before: if A happens-before B, A's effects are visible to B and can't be reordered past it. The rules are program order within a thread, unlock-before-later-lock on the same monitor, a volatile write before later reads of it, `Thread.start` and `join`, and transitivity. Without such an edge you have a data race and no guarantees. I can show it: a plain boolean flag read in a spin loop never became visible to the reader thread once the JIT compiled the loop, while the volatile one did - and with the JIT disabled the plain one even 'worked', which is exactly why such bugs are hard to find."
