---
id: data-defensive-copy-freeze
node: data.defensive-copy
type: qa
step: 3
---
## Q
一个 `Order` 被多处读取，每次 `get_order()` 都深拷贝一份很慢。除了拷贝，还有什么办法让调用方改不动它？这个办法什么时候会失效？

## A
**对象本身不可变，就不需要拷贝**

- **冻结**：`@dataclass(frozen=True)` 的实例不能重新赋值字段，可以放心地多处共享，读取是 O(1)；
- **字段也得不可变**：`items: tuple[...]` 而不是 `list`；冻结只管字段赋值，字段里的列表照样能被 `append`（浅冻结）；
- **失效的情形**：冻结 dataclass 里存了 `list` 或 `dict`，以为安全，其实还是后门；
- **代价转移**：不可变对象的“修改”是造新对象（`dataclasses.replace`），写入变贵、读取变便宜，适合读多写少；
- **出口仍要新建容器**：返回一个列表时，哪怕元素是冻结的，也要 `list(...)` 一个新的，不然调用方能改你的列表本身。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Order:
    id: int
    items: tuple[str, ...]          # 元组：字段不可变
    tags: list[str]                 # 冻结不管里面的 list

o = Order(1, ("a",), ["x"])
try: o.id = 2
except Exception as e: print(type(e).__name__)      # FrozenInstanceError
o.tags.append("leak")                               # 没拦住
print(o.tags)
```

**知识点：**防御性拷贝（Defensive Copying）
