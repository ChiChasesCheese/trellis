---
nodes:
- types.protocols-generics
- functions.decorators
title: PEP 612：参数规范变量 ParamSpec
corpus: peps
section: 16-pep-0612
url: https://peps.python.org/pep-0612/
tags:
- canonical
---

# PEP 612：参数规范变量 ParamSpec

精确回答“装饰器签名保真为什么需要专门语法”。用 Callable[..., R] 标注一个转发 *args/**kwargs 的装饰器时，被装饰函数的具体参数类型全部丢失，PEP 里给出的例子会在类型检查通过的情况下运行时报错——这正是“类型系统跟不上一个非常常见的装饰器写法”的具体证据。ParamSpec 把参数列表本身当作一个可以被引用、转发的类型变量：Callable[P, R] 配合 *args: P.args, **kwargs: P.kwargs，让装饰器返回值的参数签名和被装饰函数保持一致；Concatenate 则处理装饰器额外插入或移除首个参数（例如注入 Request 对象）的情况。理解这篇能解释为什么写“万能转发装饰器”时类型检查总是形同虚设，以及标准库/第三方装饰器要写对类型签名该用什么工具。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0612/)

## Archived copy
![[peps-pep612-paramspec-clip]]
%% trellis:end %%
