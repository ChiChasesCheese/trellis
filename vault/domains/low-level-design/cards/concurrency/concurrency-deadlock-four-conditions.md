---
id: concurrency-deadlock-four-conditions
node: concurrency.hazards
type: cloze
step: 1
---
死锁需要同时满足四个 Coffman 条件：{{c1::互斥（mutual exclusion）}}——资源一次只能被一个线程持有；{{c2::持有并等待（hold and wait）}}——线程已经拿着一把锁，还在等另一把；{{c3::不可抢占（no preemption）}}——锁不能被强制从持有者手里夺走，只能它自己 `release()`；{{c4::循环等待（circular wait）}}——一串线程形成环形等待链。打破其中任何一个都能防止死锁：全局统一的**加锁顺序**打破循环等待，这是面试里最常见也最通用的解法；`Lock.acquire(timeout=...)` 打破持有并等待。
