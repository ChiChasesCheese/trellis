---
id: oop-self-use-override-trap
node: oop.pillars
type: qa
step: 4
---
## Q
```python
class CountingList(list):
    def __init__(self) -> None:
        super().__init__()
        self.added = 0

    def append(self, item) -> None:
        self.added += 1
        super().append(item)
```
`CountingList().extend([1, 2, 3])` 之后 `added` 仍然是 `0`，不是可能猜的 `3`。为什么？这件事关于继承内置类型说明了什么？

## A
CPython 的 `list.extend` 是 C 层实现，直接操作底层数组，并不会经过 `self.append()` 这条 Python 路径去回调。**self-use（自用）**是"高层方法内部调用同一对象上的其他公开方法"这条约定——Java 的 `AbstractCollection.addAll` 依赖并文档化了这种约定，但 Python 内置的 `list`/`dict`/`set` 完全不承诺这一点：覆盖一个方法未必能拦到通过其他方法发生的操作。

如果确实需要"覆盖一个方法、所有路径都生效"的语义：改为继承 `collections.UserList`（纯 Python 实现，方法之间彼此调用，self-use 有保证），或者用组合——包一个 `list`，自己去转发和记录每个操作。
