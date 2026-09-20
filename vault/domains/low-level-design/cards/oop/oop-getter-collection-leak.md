---
id: oop-getter-collection-leak
node: oop.pillars
type: qa
step: 2
---
## Q
```python
class Floor:
    def __init__(self, spots: list[Spot]) -> None:
        self._spots = spots

    @property
    def spots(self) -> list[Spot]:
        return self._spots
```
解释封装为什么仍然被破坏了，并按优先级给出三种修法。

## A
下划线前缀只是约定，Python 没有真正的 private——但即使当作它是私有的，`spots` 这个 property 返回的仍然是内部那个 list 对象本身，调用方拿到手可以 `append`/`clear`，绕开 `Floor` 想强制的每一条规则。构造函数同样有泄漏：直接存下调用方传进来的 list，调用方之后照样能继续改它。

1. **根本不要暴露** —— 改成暴露操作：`floor.find_free_spot(size)`。
2. 返回**不可变视图**（`tuple(self._spots)`），并在构造函数里做防御性拷贝：`self._spots = list(spots)`。
3. 只有当调用方确实需要任意遍历时，才暴露一个只读的迭代器。

property 返回可变的内部结构（list、dict、自定义的可变对象）是 code review 中最常见的封装泄漏。
