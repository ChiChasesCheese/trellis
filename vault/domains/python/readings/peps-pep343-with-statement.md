---
nodes:
- iteration.context-managers
title: PEP 343：with 语句的设计取舍
corpus: peps
section: 09-pep-0343
url: https://peps.python.org/pep-0343/
tags:
- canonical
---

# PEP 343：with 语句的设计取舍

不只是讲 with 的语法，而是记录了它为什么长成现在这样。作者先否决了更早的 PEP 340（用生成器当“匿名代码块模板”，支持 break/continue 穿透），理由是它会把控制流藏进看似普通的语句里，代码变得难以推理；又否决了 PEP 310 的 with VAR = EXPR 写法，改成 with EXPR as VAR，因为前者会让 VAR 实际绑定的是 __enter__() 的返回值而非 EXPR 本身，语义具有欺骗性。文档也解释了 @contextmanager 装饰器为什么必须存在：把生成器包成 __enter__/__exit__ 对象后，用 try/finally 包住 yield 就能保证清理代码在异常时也执行。带走的追问点：__exit__ 返回真值会吞掉异常这一设计，以及为什么 with 不是循环、不支持 break/continue。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0343/)

## Archived copy
![[peps-pep343-with-statement-clip]]
%% trellis:end %%
