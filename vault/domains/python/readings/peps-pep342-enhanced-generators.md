---
nodes:
- iteration.yield-from
title: PEP 342：用增强生成器实现协程
corpus: peps
section: 08-pep-0342
url: https://peps.python.org/pep-0342/
tags:
- canonical
---

# PEP 342：用增强生成器实现协程

这是 send()/throw()/close() 方法的源头，把 yield 从语句变成表达式的那次改动。动机很直接：生成器只能向直接调用者产出值，没法接收值或异常，也不能在 try/finally 里安全 yield（无法保证清理代码执行）。这次改动把 yield 变成可以接住 send() 传入值的表达式，让生成器能实现真正的协作式调度——一个 trampoline 函数可以在多个生成器间来回 send，从而实现非阻塞 I/O 而不必写线程或回调地狱。同时新增 close() 在垃圾回收时自动调用，使 yield 出现在 try/finally 块中变得安全。理解这篇是理解“为什么生成器只能消费一次”“生成器为什么能当协程用”这两个常见问题的必要背景，也是 PEP 380/492 的直接前身。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0342/)

## Archived copy
![[peps-pep342-enhanced-generators-clip]]
%% trellis:end %%
