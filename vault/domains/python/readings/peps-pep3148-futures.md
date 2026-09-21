---
nodes:
- concurrency.executors
title: PEP 3148：concurrent.futures 的执行器设计
corpus: peps
section: 11-pep-3148
url: https://peps.python.org/pep-3148/
tags:
- canonical
---

# PEP 3148：concurrent.futures 的执行器设计

这是 ThreadPoolExecutor/ProcessPoolExecutor 统一接口的原始设计文档。动机很朴素：在此之前用线程或进程实现并行，每次都要手写启动、work/result 队列、等待完成或失败超时这套模板代码，各模块各写一套还没法设一个全局并发上限。Rationale 说明设计深受 Java java.util.concurrent 影响：Future 类本身不绑定具体求值方式（可以是线程、进程甚至 RPC），Executor 是具体实现（对应 Java 的 ExecutorService）。文档也交代了被否决的替代方案——像 weakref 那样返回透明代理对象，或者引入新语法标记异步调用；都因为增加复杂度或改变语言语义被放弃，最终选择“显式 Future，调用方必须知道自己在消费 Future”这条路线。理解这段取舍，能解释 submit()/map()/as_completed() 为什么是现在这个样子。
