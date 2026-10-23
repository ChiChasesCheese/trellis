---
id: hl-j10-pinning-experiment
node: java21.j10-virtual-threads
type: qa
step: 18
---
## Q
调度器限制为 2 个载体，8 个虚拟线程各持有自己的锁睡 200 ms，`ReentrantLock` 与 `synchronized` 两版耗时分别约多少？为什么相差 4 倍？

## A
设置：`-Djdk.virtualThreadScheduler.parallelism=2 -Djdk.virtualThreadScheduler.maxPoolSize=2`；锁彼此独立、无竞争，差别只来自是否 pin。

- `ReentrantLock` 内 sleep：约 **312 ms**。睡着时被卸载，2 个载体轮流服务 8 个虚拟线程，总耗时约等于一次 sleep。
- `synchronized` 内 sleep：约 **1324 ms**。睡着的线程抱着载体不放，2 个载体一次只能睡 2 个，8 个要 4 批，约 4 × 330 ≈ 1300 ms。
