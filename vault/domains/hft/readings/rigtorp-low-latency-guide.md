---
nodes: [os-network.cpu-isolation, os-network.interrupts, os-network.jitter, machine.power-smt, os-network.page-faults]
url: https://rigtorp.se/low-latency-guide/
---
# Low latency tuning guide

一份面向交易系统的 Linux 调优清单：关超线程、隔离核、nohz_full、中断亲和、大页、关透明大页。

**读的时候提取：**
- 每一项调优消除的是哪一种抖动。
- 如何验证一个核真的被隔离了。

%% trellis:begin %%
## Source
[Open the original ↗](https://rigtorp.se/low-latency-guide/)

## Archived copy
![[rigtorp-low-latency-guide-clip]]
%% trellis:end %%
