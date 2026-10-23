%% trellis:begin %%
# 抖动（jitter）的来源
*操作系统与网络*

调度器 tick、SMI（系统管理中断）、透明大页（THP）整理、内核后台线程、频率变化——尾延迟的常见元凶清单。

**Requires:** [[domains/hft/map/os-network.cpu-isolation|绑核与 CPU 隔离]], [[domains/hft/map/os-network.interrupts|中断与 IRQ 亲和性]]

## Readings
- [[kernel-per-cpu-kthreads|减少每 CPU 内核线程带来的 OS 抖动]]
- [[rigtorp-low-latency-guide|Low latency tuning guide]]

## Drills
- [[os-network-p999-every-4s|练习：p99.9 每隔 4 秒跳一次，按可能性列出原因]]

## Cards (4)
1. [[hft-os-network-jitter-what-and-why-tail]]
2. [[hft-os-network-jitter-source-list]]
3. [[hft-os-network-jitter-smi]]
4. [[hft-os-network-jitter-hiccup-meter]]
%% trellis:end %%

## Notes
