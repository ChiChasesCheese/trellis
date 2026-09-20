---
id: concurrency-happens-before-edges
node: concurrency.model
type: cloze
---
实际采访中用到的 happens-before 边：释放 mutex → 稍后{{c1::锁定同一 mutex}}；volatile 写 → 稍后{{c2::读相同的 volatile 变量}}；`Thread.start()` 之前的所有东西 → {{c3::启动的线程的第一个动作}}；线程的最后一个动作 → {{c4::`join()` 在等待线程中返回}}。如果两个访问没有被这样的链连接，读取可能看到陈旧或损坏的值。
