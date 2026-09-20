---
id: structure-api-leaking-internals
node: structure.api
type: qa
step: 4
---
## Q
```python
class Cart:
    def __init__(self):
        self._items = []
    def items(self):
        return self._items
```
`items()` 这样直接返回内部列表会有什么故障模式？方法应该怎么改？

## A
两个故障模式：**绕过不变式**——调用方可以直接 `cart.items().append(x)`，跳过 `Cart` 本该做的校验（比如库存上限）；**生命周期耦合**——调用方持有并遍历这个列表时，如果 `Cart` 内部同时在修改它，行为会变得难以预测。

应该返回一份**快照**（`list(self._items)` 或 `tuple(self._items)`），或者一个只读视图（字典可以用 `types.MappingProxyType`）。封装不是把字段命名成 `_items` 就够了——真正的封装是"外部永远拿不到指向可变内部状态的引用"。
