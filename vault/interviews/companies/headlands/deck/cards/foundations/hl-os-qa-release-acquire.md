---
id: hl-os-qa-release-acquire
node: foundations.os-processes-threads-ipc
type: qa
step: 39
---
## Q
面试题：为什么用 release / acquire 而不是 `volatile`？

## A
推荐答法：「`volatile` 是顺序一致（sequentially consistent），x86 上写要带 `lock` 前缀或 `mfence`，贵；SPSC 只需要较弱的 release / acquire，x86 上基本是普通 `mov`，ARM 上是 `stlr` / `ldar`，更便宜。」
