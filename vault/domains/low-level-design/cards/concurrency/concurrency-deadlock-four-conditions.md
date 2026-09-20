---
id: concurrency-deadlock-four-conditions
node: concurrency.hazards
type: cloze
---
死锁需要 **所有四个** Coffman 条件：{{c1::互斥}}（资源不可共享）、{{c2::保持和等待}}（一个线程持有一个锁同时等待另一个）、{{c3::无抢占}}（锁不能被强制夺走）、{{c4::循环等待}}（线程等待的循环链）。打破任何一个都能防止死锁——**全局锁获取顺序**打破{{c5::循环等待}}，这就是为什么锁定顺序是标准的面试解决方案；带超时的 `tryLock` 打破保持-等待。
