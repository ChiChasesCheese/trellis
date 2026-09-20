---
id: concurrency-deadlock-detect-vs-prevent
node: concurrency.hazards
type: qa
step: 2
---
## Q
Python 标准库没有内置的死锁检测器（不会自动发现"线程 A 等 B、B 等 A"并帮你恢复），这对 LLD 面试里该选预防还是检测有什么影响？

## A
数据库那样的系统可以在运行时维护一张等待图（wait-for graph）、周期性扫描环、检测到死锁后回滚某个事务来恢复；但 `threading.Lock` 之间没有这种全局视图，也没人替你回滚。所以在机器编码面试的时间尺度里，答案几乎总是**预防**而不是检测和恢复：统一加锁顺序、用 `acquire(timeout=...)` 兜底，把死锁变成设计时就排除掉的情况，而不是运行时要去发现和抢救的情况。

检测和恢复留给真正有事务和回滚机制的系统（数据库、分布式协调服务），不是通用多线程代码的默认答案。
