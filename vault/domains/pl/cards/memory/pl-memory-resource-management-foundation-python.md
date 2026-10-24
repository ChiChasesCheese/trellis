---
id: pl-memory-resource-management-foundation-python
node: memory.resource-management
type: qa
step: 3
---
## Q
Python 的 `with` 语句和上下文管理器（context manager）是什么？

## A
`with` 语句要求对象遵守**上下文管理器协议**：有 `__enter__` 方法（进入块时调用，返回值绑定到 `as` 后的名字）和 `__exit__` 方法（离开块时调用，无论正常结束还是抛出异常）。`__exit__` 会收到异常的类型、值、栈；返回真值表示“我处理了，别再传播”，返回假值则让异常继续向上。

```python
with Res("A") as a, Res("B") as b:
    print("body")
    raise ValueError("boom")
```

```console
open A
open B
body
close B exc: ValueError
close A exc: ValueError
```

多个 `with` 项同样后进先出。简单场景可用标准库的 `contextlib.contextmanager` 装饰一个生成器函数：`yield` 之前是进入，之后（放在 `try/finally` 里）是离开。

文件对象自带这个协议：`with open(path) as f:` 块结束时文件一定被关闭。

要记住的一个事实：`with` 让“离开块时一定清理”变成语言保证，而不是依赖对象何时被销毁（那是 CPython 引用计数的实现细节）。
