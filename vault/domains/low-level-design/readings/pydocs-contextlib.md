---
nodes: [python.context-iterators]
url: https://docs.python.org/3/library/contextlib.html
---
# contextlib — Utilities for with-statement contexts

值得读：`@contextmanager` 把一个生成器函数变成上下文管理器的机制，正是
`python-context-contextmanager-decorator`、`python-context-contextmanager-try-finally` 两张卡的直接依据——`yield`
之前是 `__enter__`，`yield` 之后（包在 `try/finally` 里）是 `__exit__`，读它能补上这个装饰器背后到底做了什么胶水代码，
以及 `ExitStack` 怎么处理"运行时才知道要进入几个上下文"的场景。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/contextlib.html)
%% trellis:end %%
