---
id: hft-os-network-interrupts-irq-affinity
node: os-network.interrupts
type: qa
step: 2
---
## Q
什么是 IRQ 亲和性（IRQ affinity）？为什么低延迟服务器要关掉 `irqbalance`？

## A
IRQ 亲和性规定某个设备的中断可以由哪些核来处理。在 Linux 里，每个中断号对应 `/proc/irq/<N>/smp_affinity`，往里写一个核的位掩码就能设置，例如写 `3` 表示只允许 0 号和 1 号核处理。

`irqbalance` 是一个常驻的后台程序，它会定期把各设备的中断**重新分配**到不同的核上，目的是均衡各核的负载。对通用服务器这很合理，但对交易服务器是灾难：
- 它不知道哪个核是交易线程专用的；
- 它可能在你运行的过程中，把网卡的中断挪到交易核上，让交易线程开始每个包被打断一次。

做法：
1. 关掉 `irqbalance`（`systemctl disable --now irqbalance`）；
2. 手动把所有设备的中断（网卡、磁盘、定时器等）绑到留给操作系统的核（如 0、1 号）；
3. 用 `cat /proc/interrupts` 检查交易核对应的中断计数：理想情况是几乎不增长。

这样交易核上看不到任何设备中断，线程的执行就连续了。
