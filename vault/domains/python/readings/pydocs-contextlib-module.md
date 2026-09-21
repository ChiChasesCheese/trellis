---
nodes:
- iteration.context-managers
title: contextlib 模块：上下文管理器工具箱
corpus: python-docs
section: 46-contextlib
url: https://docs.python.org/3/library/contextlib.html
tags:
- canonical
---

# contextlib 模块：上下文管理器工具箱

contextlib 是写上下文管理器的效率工具箱：@contextmanager 装饰器让你用一个普通生成器函数就能实现上下文管理器协议，规则是把资源获取代码放在 yield 之前，把清理代码放在 yield 之后并用 try/finally 包住，这样即使 with 块内抛了异常，清理代码依然会执行，异常会在 yield 那一行被重新抛出。ExitStack 用来管理运行时才知道有多少个的一组上下文管理器（比如根据配置动态打开若干个文件），可以在循环里动态 enter_context() 累加，退出时保证按后进先出的顺序全部清理。文档还讲了单次使用（用过一次的生成器 CM 不能重新进入）、可重入（可以嵌套多次进入自身）、可复用（可以多次独立使用）这三类上下文管理器的区别，避免误用导致运行时报错。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/contextlib.html)

## Archived copy
![[pydocs-contextlib-module-clip]]
%% trellis:end %%
