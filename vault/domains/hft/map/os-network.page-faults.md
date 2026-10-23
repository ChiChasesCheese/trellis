%% trellis:begin %%
# 缺页、mlock 与预触内存
*操作系统与网络*

第一次访问的页会触发缺页中断；启动时预触（pre-fault）所有内存并用 mlock 锁住，避免交易时缺页或被换出。

**Requires:** [[domains/hft/map/machine.tlb-hugepages|虚拟内存、TLB 与大页（huge pages）]]

## Readings
- [[rigtorp-low-latency-guide|Low latency tuning guide]]
- [[rigtorp-virtual-memory|Virtual memory for low latency applications]]

## Drills
- [[os-network-p999-every-4s|练习：p99.9 每隔 4 秒跳一次，按可能性列出原因]]

## Cards (4)
1. [[hft-os-network-page-faults-first-touch]]
2. [[hft-os-network-page-faults-pretouch]]
3. [[hft-os-network-page-faults-mlock-vs-pretouch]]
4. [[hft-os-network-page-faults-surprise-sources]]
%% trellis:end %%

## Notes
