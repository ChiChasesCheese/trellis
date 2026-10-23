---
id: hl-c14-thread-local
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 5
---
## Q
C++ 的 `thread_local` 是什么？三个线程各自 `++` 它若干次，主线程的值是多少？

## A
- `thread_local int c = 0;`：每个线程独立一份，对应 Java 的 `ThreadLocal<Integer>`。
- 实测：三个线程分别自增 1、2、3 次，各自读到 1、2、3；**主线程自己的副本仍是 0**。
- 好处：不需要锁；经验是共享可变状态越少越好，能用「每线程私有 + 合并」就不要锁。
