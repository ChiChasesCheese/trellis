%% trellis:begin %%
# 内核旁路（kernel bypass）
*操作系统与网络*

应用直接读写网卡的收发队列：Solarflare / AMD OpenOnload 与 ef_vi、DPDK、RDMA；延迟降到 1 微秒左右，代价是复杂度。

**Requires:** [[domains/hft/map/os-network.kernel-stack|内核网络栈的代价]]

## Readings
- [[dpdk-overview|DPDK 概览]]
- [[wiki-rdma|RDMA]]

## Cards (4)
1. [[hft-os-network-kernel-bypass-mechanism]]
2. [[hft-os-network-kernel-bypass-options]]
3. [[hft-os-network-kernel-bypass-latency-numbers]]
4. [[hft-os-network-kernel-bypass-costs]]
%% trellis:end %%

## Notes
