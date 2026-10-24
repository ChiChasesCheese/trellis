---
id: pl-abstraction-equality-hashing-foundation-python-eq-hash
node: abstraction.equality-hashing
type: qa
step: 3
---
## Q
Python 的 `==` 与 `is`、`__eq__` 与 `__hash__` 是什么关系？为什么只定义 `__eq__` 会让对象不能放进集合？

## A
`is` 比较同一性（同一个对象），`==` 调用 `__eq__` 比较值，默认的 `__eq__` 退化成 `is`。`hash(x)` 调用 `__hash__`。字典的键、集合的元素要求可哈希。

Python 的规则是：**一个类只要定义了 `__eq__` 而没有定义 `__hash__`，它的 `__hash__` 会被自动设为 `None`**，实例变成不可哈希。因为解释器无法保证你新的相等定义与旧的哈希（基于 `id`）一致，宁可禁止：

```python
class P:
    def __init__(self, x): self.x = x
    def __eq__(self, o): return self.x == o.x
P.__hash__        # None
{P(1)}            # TypeError: unhashable type: 'P'
```

要放进集合就必须同时定义 `__hash__`，并保证相等的对象哈希相同；通常哈希只基于**不变**的字段。内置容器的规则一致：`list`、`dict`、`set` 是可变的，所以不可哈希，`tuple`、`frozenset`、`str` 可哈希（`tuple` 里含 `list` 时哈希仍失败）。

`dataclass` 的默认行为：`@dataclass` 生成 `__eq__`，同时把 `__hash__` 设为 `None`；`@dataclass(frozen=True)` 才同时生成基于字段的 `__hash__`，因为冻结保证了字段不变。

此外 Python 的比较有一个速记：容器的 `in` 和 `==` 会先用 `is` 做快速判断，再调用 `__eq__`，这对 `NaN` 有意外的后果（见浮点一张）。
