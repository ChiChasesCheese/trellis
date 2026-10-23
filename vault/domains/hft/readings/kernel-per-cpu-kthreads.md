---
nodes: [os-network.cpu-isolation, os-network.jitter]
url: https://www.kernel.org/doc/html/latest/admin-guide/kernel-per-CPU-kthreads.html
---
# 减少每 CPU 内核线程带来的 OS 抖动

Linux 内核文档：各种每 CPU 内核线程如何打扰隔离核，以及对应的启动参数。

**读的时候提取：**
- nohz_full、rcu_nocbs、isolcpus 各自移走了什么。
- 哪些干扰无法完全消除。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.kernel.org/doc/html/latest/admin-guide/kernel-per-CPU-kthreads.html)

## Archived copy
![[kernel-per-cpu-kthreads-clip]]
%% trellis:end %%
