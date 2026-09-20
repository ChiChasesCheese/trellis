---
id: python-context-contextmanager-decorator
node: python.context-iterators
type: qa
step: 2
tags: [grown]
---
## Q
`@contextlib.contextmanager` 怎么把一个生成器函数变成上下文管理器？`yield` 前后的代码各对应 `__enter__`/`__exit__` 的哪部分？

## A
装饰后的函数被调用时不会立即执行——`with` 触发 `__enter__` 时才真正启动这个生成器，跑到 `yield` 表达式为止，`yield` 出的值绑定给 `as` 变量；`with` 块结束时触发 `__exit__`，让生成器从 `yield` 处**恢复执行**，跑完 `yield` 之后的代码。所以 `yield` **之前**的代码相当于 `__enter__`，`yield` **之后**的代码相当于 `__exit__`。
```python
from contextlib import contextmanager

@contextmanager
def transaction(conn):
    conn.begin()
    yield conn
    conn.commit()
```
