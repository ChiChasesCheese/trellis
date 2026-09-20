---
id: python-context-exit-suppress
node: python.context-iterators
type: qa
step: 6
tags: [grown]
---
## Q
`__exit__(self, exc_type, exc, tb)` 返回 `True` 和返回 `False`/`None` 在异常处理上分别意味着什么？

## A
返回真值（`True`）告诉解释器“这个异常我已经处理了”，`with` 语句**吞掉**异常，正常往下执行；返回假值（`False`/`None`，缺省）表示“没处理”，异常照常向外传播。
```python
class SuppressKeyError:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb):
        return exc_type is KeyError  # 只吞掉 KeyError

with SuppressKeyError():
    {}["missing"]  # 异常被吞掉，之后代码继续
```
