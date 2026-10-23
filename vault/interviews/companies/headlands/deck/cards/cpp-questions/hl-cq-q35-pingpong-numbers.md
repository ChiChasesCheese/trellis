---
id: hl-cq-q35-pingpong-numbers
node: cpp-questions.h-os
type: qa
step: 18
---
## Q
两个线程来回传一个令牌，用 `condition_variable` 和对原子变量自旋，往返时间各是多少？差多少倍？为什么？自旋的代价是什么、怎么控制？

## A
- `condition_variable`：往返约 **2424 ns**；原子变量自旋：约 **82 ns**；差约 **30 倍**。
- 原因：`condition_variable` 要经过互斥量、`futex`（Linux）系统调用和调度器唤醒；自旋只是缓存行在两个核之间传递。
- 代价：自旋**占满一个核**（功耗、超线程兄弟、对其他任务的影响）。
- 控制：热线程**绑核**（`taskset` / `pthread_setaffinity_np`，必要时 `isolcpus`）并忙等，冷线程阻塞等待，或先自旋一小会儿再阻塞。
