---
id: python-protocol-form
node: python.protocols-abc
type: qa
step: 3
tags: [grown]
---
## Q
用 `Protocol` + `runtime_checkable` 写一个“可序列化为 JSON”的接口，并在运行时用 `isinstance` 判断，代码怎么写？

## A
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class JSONSerializable(Protocol):
    def to_json(self) -> dict: ...

def emit(obj: JSONSerializable) -> None:
    if isinstance(obj, JSONSerializable):
        print(obj.to_json())
```
`Protocol` 本身只能用于静态检查；加上 `@runtime_checkable` 才解锁 `isinstance`/`issubclass`——但这只是方法名存在性检查，见下一张卡的限制。
