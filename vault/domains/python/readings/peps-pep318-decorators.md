---
nodes:
- functions.decorators
title: PEP 318：函数与方法的装饰器语法
corpus: peps
section: 10-pep-0318
url: https://peps.python.org/pep-0318/
tags:
- canonical
---

# PEP 318：函数与方法的装饰器语法

讲清楚装饰器语法要解决什么丑陋现状：在 @ 语法之前，classmethod、staticmethod 这类变换只能写在函数体之后（foo = classmethod(foo)），函数越长这行代码离定义越远，读起来容易漏看，多个变换叠加时还要写 foo = synchronized(lock)(foo); foo = classmethod(foo) 这种重复赋值。@classmethod 语法把“转换意图”挪到声明处，等价于 f = d(f) 在模块导入时立即执行。Motivation 部分同时交代了历史争议：语法讨论从 2002 年持续到 2004 年，核心分歧是“声明意图该放哪里”和“如何不让新手一眼看不懂”，最终选定的 @decorator 写法（“pie syntax”）只是众多提案中的一个。读完能回答“为什么装饰器是这个语法、而不是别的”，以及装饰器在类定义里为什么只加了函数/方法装饰器，类装饰器要等 PEP 3129。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0318/)

## Archived copy
![[peps-pep318-decorators-clip]]
%% trellis:end %%
