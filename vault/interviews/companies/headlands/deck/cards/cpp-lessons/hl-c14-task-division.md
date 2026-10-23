---
id: hl-c14-task-division
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 15
---
## Q
线程池和任务划分有哪几条经验？

## A
- 线程数 ≈ 核数（CPU 密集型），I/O 密集可更多；不要为每个小任务建线程。
- 优先「**分块 + 各自累加 + 最后合并**」，而不是所有线程争一个共享变量。
- 共享可变状态越少越好；能用「每线程私有 + 合并」就不要锁。
