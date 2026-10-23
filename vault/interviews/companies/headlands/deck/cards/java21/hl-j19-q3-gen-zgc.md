---
id: hl-j19-q3-gen-zgc
node: java21.j19-runtime-zgc-jit
type: qa
step: 36
---
## Q
面试问：分代 ZGC 比普通 ZGC 好在哪？
What does Generational ZGC buy you over single-generation ZGC?

## A
- 依据**分代假说**：大部分对象死得早；
- 非分代 ZGC 每轮标记整堆；分代 ZGC **常回收年轻代（便宜）、很少回收老年代**；
- 好处：更少的 GC CPU、更少的堆余量、更少的 allocation stall；
- 版本：JDK 21 用 `-XX:+UseZGC -XX:+ZGenerational` 开启，**23 起默认分代，24 起移除旧模式**。

英文骨架：「Most objects die young, so we collect the young generation often and cheaply, the old one rarely.」
