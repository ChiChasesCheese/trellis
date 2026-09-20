---
id: python-typing-optional-vs-sentinel
node: python.typing
type: qa
step: 5
tags: [grown]
---
## Q
`update(self, name: str | None = None)` 方法，`None` 到底表示“这个字段不改”还是“把这个字段显式设成 `None`”？为什么这里需要一个哨兵（sentinel）？

## A
当 `None` 本身就是一个合法的业务取值（比如“清空这个字段”）时，用 `None` 同时表达“没传参数”会有歧义——调用方没法区分“不想改”和“想改成空”。解法是引入一个和 `None` 不同的哨兵对象作为默认值，只有默认值原样保留才代表“没传”：
```python
_MISSING = object()

def update(self, name: str | object = _MISSING) -> None:
    if name is not _MISSING:
        self.name = name  # 可以是任何值，包括 None
```
