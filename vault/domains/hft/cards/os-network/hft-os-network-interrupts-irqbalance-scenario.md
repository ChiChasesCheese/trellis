---
id: hft-os-network-interrupts-irqbalance-scenario
node: os-network.interrupts
type: qa
step: 4
---
## Q
一个交易系统的延迟在 p50 上很漂亮，但 p99.9 每隔一段时间出现几十微秒的尖刺，怎么判断是不是中断造成的？

## A
p50 是中位数，p99.9 是千分之一的最慢情况。中位数好、极端值差，说明大部分时候没问题，偶尔被外部事件打断，中断是头号嫌疑。

排查步骤：
1. 在交易核上观察 `/proc/interrupts`：隔一秒读两次，看这个核那一列的计数有没有增长。如果有增长，增长的是哪类中断（网卡、定时器 `LOC`、重新调度 `RES` 等）。
2. 看 `systemctl status irqbalance`：如果它在运行，说明中断可能被重新分配过。
3. 用 `perf` 或 `trace-cmd` 抓 `irq:irq_handler_entry` 事件，看有哪些中断在交易核上触发，各占多久。

典型根因：
- `irqbalance` 把网卡队列的中断挪到了交易核；
- 另一个设备（比如磁盘控制器、管理网卡）的中断没有绑核；
- 定时器中断没通过 `nohz_full` 去除。

修复：绑好中断亲和性、关掉 `irqbalance`、必要时加 `nohz_full`。验证标准：交易核的中断计数在运行期间基本不再增长。
