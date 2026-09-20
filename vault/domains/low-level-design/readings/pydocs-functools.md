---
nodes: [python.first-class-functions, patterns.strategy]
url: https://docs.python.org/3/library/functools.html
---
# functools — Higher-order functions and operations on callable objects

值得读：`partial`、`wraps`、`singledispatch` 这些高阶函数工具，直接对应
`python-functions-first-class`、`python-functions-command-partial` 两张卡；同时也是 `patterns-strategy-callable`
卡"策略用函数形式实现"的技术底座——把一个可插拔算法定成参数，在 Python 里往往就是传一个 `Callable`，`functools` 提供的正是围绕这个
思路的标准工具箱，读它能补上闭包、装饰器与 `partial` 三种"打包一个策略"的写法该怎么选。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/functools.html)

## Archived copy
![[pydocs-functools-clip]]
%% trellis:end %%
