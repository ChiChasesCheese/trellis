---
id: hl-j10-pinning-fix-diagnose
node: java21.j10-virtual-threads
type: qa
step: 20
---
## Q
在 JDK 21 里怎么避免和诊断虚拟线程 pinning？`-Djdk.tracePinnedThreads` 输出里的 `reason:MONITOR` 是什么意思？

## A
**对策**：把「持锁时阻塞」的 `synchronized` 改成 `ReentrantLock`（`lock()/unlock()` 放 `try/finally`）。只能改自己的代码，第三方库里的 `synchronized` 无能为力（老 JDBC 驱动曾是重灾区，升级驱动）。

**诊断**：
- `-Djdk.tracePinnedThreads=full|short` 打印被钉住时的栈；
- JFR 事件 `jdk.VirtualThreadPinned`（超过阈值才记录，默认 **20 ms**）。

输出里 `reason:MONITOR` = 持有 monitor（`synchronized`）；`<== monitors:1` 标出持有它的栈帧所在行。
