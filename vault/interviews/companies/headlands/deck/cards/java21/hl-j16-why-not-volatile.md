---
id: hl-j16-why-not-volatile
node: java21.j16-concurrency-primitives
type: qa
step: 16
---
## Q
既然有 `volatile`，为什么发布数据还要用 release/acquire？它们在 x86 上的差别是什么？

## A
`volatile` 多禁止了「写之后的读」被重排到写之前（**StoreLoad**），正是写缓冲造成的那种重排。禁止它 CPU 必须**排空写缓冲**，x86 上要一条 `lock`/`mfence` 类全栅栏，约十几到几十个周期。

release/acquire **不禁止 StoreLoad**，所以 x86 上 release 写和 acquire 读**就是普通 `mov`**（x86 本就不重排 Load-Load / Store-Store / Load-Store），只约束编译器，没有 CPU 栅栏开销。

注意别说太绝对：AArch64 上 HotSpot 把 volatile 和 acquire/release 都编成 `ldar`/`stlr`，差别没 x86 明显。
