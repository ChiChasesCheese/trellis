%% trellis:begin %%
# 绑核与 CPU 隔离
*操作系统与网络*

线程亲和性（affinity）、isolcpus、nohz_full、rcu_nocbs；让交易线程独占一个核，调度器和内核任务不来打扰。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.threading|线程模型：一核一线程与 SPSC 队列]]

**Unlocks:** [[domains/hft/map/os-network.interrupts|中断与 IRQ 亲和性]], [[domains/hft/map/os-network.jitter|抖动（jitter）的来源]], [[domains/hft/map/java.tuning|低延迟 JVM 调优]]

## Readings
- [[java-thread-affinity|Java Thread Affinity]]
- [[kernel-per-cpu-kthreads|减少每 CPU 内核线程带来的 OS 抖动]]
- [[rigtorp-low-latency-guide|Low latency tuning guide]]

## Drills
- [[os-network-p999-every-4s|练习：p99.9 每隔 4 秒跳一次，按可能性列出原因]]

## Cards (4)
1. [[hft-os-network-cpu-isolation-affinity-why]]
2. [[hft-os-network-cpu-isolation-boot-params]]
3. [[hft-os-network-cpu-isolation-affinity-vs-isolation]]
4. [[hft-os-network-cpu-isolation-core-budget]]
%% trellis:end %%

## Notes
