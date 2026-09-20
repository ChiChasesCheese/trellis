---
id: python-typing-generic-repository
node: python.typing
type: qa
step: 2
tags: [grown]
---
## Q
写一个可以装任意元素类型的 `Stack`，怎么用 `TypeVar`/泛型让类型检查器知道 `pop()` 返回的类型和 `push()` 传入的类型一致？

## A
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()
```
`Stack[int]()` 会让类型检查器把 `T` 绑定成 `int`，之后 `push("x")` 或者把 `pop()` 的结果当字符串用都会被标红——不用为每种元素类型重复写一个 `IntStack`/`StrStack`。
