---
nodes:
- functions.functools
- functions.decorators
title: functools 模块：高阶函数工具箱
corpus: python-docs
section: 44-functools
url: https://docs.python.org/3/library/functools.html
tags:
- canonical
---

# functools 模块：高阶函数工具箱

functools 是写装饰器和函数式代码离不开的工具箱：lru_cache/cache 提供开箱即用的记忆化缓存，但要求所有参数都可哈希，且默认不会自动过期，长期运行的服务如果缓存键空间无限增长（比如以请求 ID 为键）会造成事实上的内存泄漏，这是使用它最容易忽略的陷阱；partial() 可以固定一个函数的部分参数生成新函数，比写 lambda 包装更清晰也更快；singledispatch 让你根据第一个参数的运行时类型自动分派到不同实现，是给函数重载最 Pythonic 的方式；wraps（update_wrapper 的装饰器形式）在写装饰器时用来把原函数的 __name__、__doc__ 等元数据复制到包装函数上，否则被装饰的函数在调试器、文档生成工具里会显示成包装器的名字而不是原名字。total_ordering 则只需定义一个比较方法就能自动补全其余几个。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/functools.html)

## Archived copy
![[pydocs-functools-module-clip]]
%% trellis:end %%
