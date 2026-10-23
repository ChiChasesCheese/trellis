---
id: hl-j10-vthread-properties
node: java21.j10-virtual-threads
type: qa
step: 9
---
## Q
虚拟线程有哪些固定特性：守护、优先级、判断方式、`ThreadLocal`？`main` 结束时没跑完的虚拟线程会怎样？

## A
- 判断：`Thread.currentThread().isVirtual()`。
- **永远是守护线程**（daemon）：`main` 结束时没跑完的虚拟线程不拦 JVM 退出，所以不 `join` 就别指望它跑完。
- 优先级固定 `NORM_PRIORITY`（5），设置无效。
- 可以有 `ThreadLocal`，能用，但别当缓存池。
- `toString` 对比：平台线程 `Thread[#25,p-1,5,main]`（编号、名字、优先级、线程组）；虚拟线程 `VirtualThread[#20,v-1]/runnable@ForkJoinPool-1-worker-1`（编号、名字、状态、所在载体）。
