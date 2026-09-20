---
id: problems-logger-drop-must-be-counted
node: problems.components.logger
type: qa
step: 8
tags: [grown]
---
## Q
日志框架的异步 handler 用一条**有界**队列把写盘挪出业务线程。队列满了该阻塞还是该丢弃？不管选哪个，有一件事是必须做的，是什么？

## A
两个选项都合理，代价不同：阻塞（`queue.put`）保证一条不丢，代价是业务线程被日志拖慢——在日志量暴涨的事故现场，日志系统反而成了系统的瓶颈；丢弃（`put_nowait` 配 `except queue.Full`）保护业务线程，代价是日志出现空洞。按场景选即可，但**丢弃必须计数并暴露成一个可读的属性**（如 `dropped_count`）。没有计数器的丢弃是最坏的做法：排查问题的人会以为那段时间什么都没发生，而事实是记录被悄悄扔了。队列无界不是第三个选项——那只是把丢日志换成了把内存吃光。
