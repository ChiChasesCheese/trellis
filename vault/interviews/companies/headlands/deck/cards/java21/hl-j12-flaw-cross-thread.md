---
id: hl-j12-flaw-cross-thread
node: java21.j12-scoped-values
type: qa
step: 3
---
## Q
`ThreadLocal` 的第二个结构性毛病：不跨线程。`InheritableThreadLocal` 为什么也不够好？

## A
新线程读 `ThreadLocal` 得到 `null`，上下文传不过去。

`InheritableThreadLocal` 在建线程时把整张表**复制**给孩子：线程多时复制成本和内存很大；线程池里的线程也不是你的任务创建的，继承不到。

虚拟线程把线程数从几百变成几百万，每个线程一张 `ThreadLocalMap`，`InheritableThreadLocal` 每次 fork 复制一遍，这个毛病被放大。
