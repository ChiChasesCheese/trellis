---
id: hl-javaq-g-q34-cost-pinning
node: java-questions.g-os
type: qa
step: 2
---
## Q
为什么"线程数远多于核数反而更慢"、低延迟系统为什么"一线程一核"？线程栈默认多大？绑核有哪几种手段？JVM 的 GC / JIT 线程数怎么影响？

## A
- **间接成本**：被换走线程的 L1/L2 缓存和分支预测状态被冲掉，回来后要重新热身，所以线程多于核数反而慢；低延迟系统因此一线程一核、不让出。
- **线程栈**：默认 `ThreadStackSize` 在 Linux x86_64 是 1024 KB（macOS arm64 是 2048 KB）；栈是虚拟内存预留，按需提交。
- **系统调用**也有成本：用户态 → 内核态（`read / write / futex`），一次约百纳秒到微秒；`synchronized` / `LockSupport.park` 竞争严重时走 `futex`。
- **绑核**：`taskset -c 2,3 java …` 限制整个 JVM；`numactl --cpunodebind` 控制 NUMA；内核参数 `isolcpus` / `nohz_full` 把核从调度器和时钟中断里隔离；Java 里单线程绑核需要库（如 OpenHFT Affinity，经 JNA / JNI）。
- 12 核机器默认：`ParallelGCThreads=10`、`ConcGCThreads=3`、`CICompilerCount=4`；低延迟机器上要给它们留核，否则抢业务线程。
