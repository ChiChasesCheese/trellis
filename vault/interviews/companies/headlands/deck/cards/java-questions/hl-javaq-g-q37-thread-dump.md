---
id: hl-javaq-g-q37-thread-dump
node: java-questions.g-os
type: qa
step: 12
---
## Q
线程转储里怎么一眼看出锁竞争？死锁怎么发现？

## A
`jcmd <pid> Thread.print` 节选：
```
"waits-for-lock" ... BLOCKED (on object monitor)
	- waiting to lock <0x00000001238020d0> (a java.lang.Object)
"holds-lock" ... TIMED_WAITING (sleeping)
	- locked <0x00000001238020d0> (a java.lang.Object)
```
- 两个线程出现**同一个锁地址**：一个 `locked`、一个 `waiting to lock`，谁持锁、谁在等一目了然；`BLOCKED (on object monitor)` 是在等 `synchronized`。
- **死锁**时 `Thread.print` 末尾会直接报告 deadlock。
