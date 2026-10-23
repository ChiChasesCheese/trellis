---
id: hl-javaq-g-q36-vmstat
node: java-questions.g-os
type: qa
step: 8
---
## Q
`vmstat 1` 的 `r`、`b`、`si/so`、`bi/bo`、`in`、`cs`、`us/sy/id/wa/st` 各表示什么？看到 `r=12`、`sy=25%`、`cs=52000` 该怎么判断？

## A
- `r` 可运行队列长度；`b` 阻塞进程数；`si/so` 换页；`bi/bo` 块 I/O；`in` 中断；`cs` 上下文切换；`us/sy/id/wa/st` 用户态 / 系统态 / 空闲 / 等 I/O / 被宿主机抢占。
- 示意输出 `r=12`（远大于核数）→ **CPU 饱和**，可运行队列长。
- `sy=25%` 偏高且 `cs=52000` → 系统态和上下文切换多，怀疑**锁竞争 / 过多线程 / 频繁系统调用**。
- `wa` 高 → 等磁盘；`si/so` 非 0 → 在换页，延迟灾难；`st` 高 → 虚拟机被宿主机抢占。
- 追问："load average 高但 CPU 空闲"：Linux 负载包含不可中断睡眠（D 状态，常是磁盘 / NFS 等待），看 `vmstat` 的 `b` 和 `wa`。
