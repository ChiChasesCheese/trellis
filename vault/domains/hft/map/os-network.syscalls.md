%% trellis:begin %%
# 系统调用与上下文切换的成本
*操作系统与网络*

一次系统调用从用户态进内核态再返回，一次上下文切换还要换掉缓存和 TLB 的热数据；为什么热路径上一个都不要。

**Unlocks:** [[domains/hft/map/os-network.kernel-stack|内核网络栈的代价]]

## Cards (4)
1. [[hft-os-network-syscalls-what-and-why-costly]]
2. [[hft-os-network-syscalls-cpu-budget-math]]
3. [[hft-os-network-syscalls-context-switch-contrast]]
4. [[hft-os-network-syscalls-hidden-in-hot-path]]
%% trellis:end %%

## Notes
