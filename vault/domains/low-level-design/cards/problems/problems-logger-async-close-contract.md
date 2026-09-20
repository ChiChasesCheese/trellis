---
id: problems-logger-async-close-contract
node: problems.components.logger
type: cloze
step: 7
tags: [grown]
---
日志框架的异步 handler（一条有界队列加一个工作线程）关闭时必须做完三步：先{{c1::拒收新记录}}，再{{c2::把哨兵放进队尾、让工作线程把队列排空（drain）}}，最后{{c3::join 工作线程、再关闭被包住的内层 handler}}。少任何一步丢掉的都是{{c4::崩溃前最后那几条——最值钱的那几条}}。另外，"检查是否已关闭"和"入队"必须在同一把锁里完成，否则一条记录可能在哨兵之后才进队列，从此{{c5::永远没人消费}}。
