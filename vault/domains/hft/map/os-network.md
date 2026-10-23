%% trellis:begin %%
# 操作系统与网络

让操作系统别打扰交易线程（绑核、隔离、中断、缺页、抖动），以及从网卡、交换机到跨城线路的网络延迟。

## Topics
- [[domains/hft/map/os-network.cpu-isolation|绑核与 CPU 隔离]]
- [[domains/hft/map/os-network.interrupts|中断与 IRQ 亲和性]]
- [[domains/hft/map/os-network.syscalls|系统调用与上下文切换的成本]]
- [[domains/hft/map/os-network.page-faults|缺页、mlock 与预触内存]]
- [[domains/hft/map/os-network.jitter|抖动（jitter）的来源]]
- [[domains/hft/map/os-network.kernel-stack|内核网络栈的代价]]
- [[domains/hft/map/os-network.kernel-bypass|内核旁路（kernel bypass）]]
- [[domains/hft/map/os-network.tcp-udp|TCP 与 UDP 组播在交易中的分工]]
- [[domains/hft/map/os-network.nic-switch|网卡与交换机]]
- [[domains/hft/map/os-network.wan|跨城线路：光纤、微波与光速]]
- [[domains/hft/map/os-network.time-sync|时间同步：PTP、GPS 与 NTP]]
%% trellis:end %%

## Notes
