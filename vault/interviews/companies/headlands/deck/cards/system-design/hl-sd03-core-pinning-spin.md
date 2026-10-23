---
id: hl-sd03-core-pinning-spin
node: system-design.sd03-low-latency-trading
type: qa
step: 12
---
## Q
热线程的核心绑定和 OS 配置怎么做？举一台 16 核主机的分配。忙等的代价是什么？

## A
- 每个热线程独占一个物理核（避开 SMT 兄弟线程），用 `isolcpus` / `nohz_full` 隔离，`taskset` 或库绑定；关闭 `irqbalance`，中断引到别的核；NUMA：网卡所在 NUMA 节点上的核 + 本地内存；`performance` 调频策略；大页（hugepages）；关闭 swap。
- 16 核示例：核 0 Feed Handler；核 1–8 分片线程；核 9 Order Gateway；核 10 Journaler；核 11 监控；核 12–15 操作系统与其他。

**忙等（busy-spin）**：热线程永不阻塞（不 park、不 `wait`、不 `Thread.sleep`），在空环上自旋，`Thread.onSpinWait()`（x86 上是 `PAUSE` 指令，降低功耗和对兄弟线程的影响）。代价：每个热线程烧满一个核，这是低延迟的固定成本，必须在预算里说出来。
