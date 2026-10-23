%% trellis:begin %%
# 内核网络栈的代价
*操作系统与网络*

一个包从网卡到应用要经过中断、协议栈、socket 缓冲、系统调用和内存拷贝，总共几微秒。

**Requires:** [[domains/hft/map/os-network.syscalls|系统调用与上下文切换的成本]]

**Unlocks:** [[domains/hft/map/os-network.kernel-bypass|内核旁路（kernel bypass）]], [[domains/hft/map/os-network.tcp-udp|TCP 与 UDP 组播在交易中的分工]]

## Readings
- [[dpdk-overview|DPDK 概览]]

## Cards (4)
1. [[hft-os-network-kernel-stack-packet-path]]
2. [[hft-os-network-kernel-stack-cost-breakdown]]
3. [[hft-os-network-kernel-stack-busy-poll-tuning]]
4. [[hft-os-network-kernel-stack-burst-overload]]
%% trellis:end %%

## Notes
