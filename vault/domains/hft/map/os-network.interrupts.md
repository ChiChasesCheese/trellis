%% trellis:begin %%
# 中断与 IRQ 亲和性
*操作系统与网络*

网卡和其他设备的中断会打断正在运行的线程；把中断绑到非交易核，关掉 irqbalance。

**Requires:** [[domains/hft/map/os-network.cpu-isolation|绑核与 CPU 隔离]]

**Unlocks:** [[domains/hft/map/os-network.jitter|抖动（jitter）的来源]]

## Readings
- [[kernel-irq-affinity|SMP IRQ affinity]]
- [[rigtorp-low-latency-guide|Low latency tuning guide]]

## Drills
- [[os-network-p999-every-4s|练习：p99.9 每隔 4 秒跳一次，按可能性列出原因]]

## Cards (4)
1. [[hft-os-network-interrupts-what-happens]]
2. [[hft-os-network-interrupts-irq-affinity]]
3. [[hft-os-network-interrupts-interrupt-vs-polling]]
4. [[hft-os-network-interrupts-irqbalance-scenario]]
%% trellis:end %%

## Notes
