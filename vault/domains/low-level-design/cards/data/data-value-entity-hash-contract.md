---
id: data-value-entity-hash-contract
node: data.value-entity
type: qa
step: 2
---
## Q
给一个可变的类写了 `__eq__` 但没写 `__hash__`，放进 `set` 就报错。写了 `__hash__` 之后，对象放进 `set` 再改字段，又会出什么问题？`__eq__` 和 `__hash__` 怎样配合？

## A
**相等的对象哈希必须相等，哈希依据的字段不能变**

- **只写 `__eq__`**：Python 自动把 `__hash__` 设成 `None`，实例不可哈希，`set` 和 `dict` 的键都用不了；
- **契约**：`a == b` 必须推出 `hash(a) == hash(b)`；`__hash__` 用的字段不能比 `__eq__` 多；
- **哈希字段变了**：对象仍在集合里，却被放在旧哈希对应的桶里，`x in s` 找不到它；集合没报错，只是“丢了”；
- **所以**：值对象冻结，实体只拿不会变的 `id` 做哈希；
- **`@dataclass`（默认 `eq=True`、不冻结）**：生成 `__eq__` 并把 `__hash__` 设为 `None`，要用作键必须 `frozen=True`。

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
try: {Point(1)}
except TypeError as e: print(e)
class Key:
    def __init__(self, k): self.k = k
    def __eq__(self, o): return self.k == o.k
    def __hash__(self): return hash(self.k)

key = Key(1); s = {key}
key.k = 2                                          # 哈希依据的字段变了
print(key in s, len(s))                            # False 1
```

**知识点：**值对象与实体（Value vs Entity）
