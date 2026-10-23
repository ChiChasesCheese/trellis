---
id: hl-os-spsc-cached-index
node: foundations.os-processes-threads-ipc
type: qa
step: 28
---
## Q
SPSC 环形缓冲里「缓存对方序号」优化是什么？它解决什么问题？

## A
生产者每次 `offer` 都读 `head` 判断是否满，这是对「消费者正在写的缓存行」的读，触发缓存行在两个核间传递（乒乓）。

优化：生产者**本地缓存**上次看到的 `head`（`cachedHead`），只有「按缓存值看起来满了」才真正重读（`getAcquire`）；消费者对 `tail` 同样（`cachedTail`）。多数时候一次共享内存读都不需要。
