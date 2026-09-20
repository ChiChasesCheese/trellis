---
id: python-dataclass-default-factory
node: python.dataclasses-enums
type: qa
step: 2
tags: [grown]
---
## Q
为什么 `@dataclass` 里字段默认值不能直接写 `items: list = []`，而要写 `field(default_factory=list)`？

## A
类体里的默认值只求值**一次**，在类定义时；如果默认值是可变对象（列表、字典），所有没有显式传参的实例会**共享同一个**列表对象——一个实例 `append` 会影响所有实例。`field(default_factory=list)` 让 dataclass 在**每次构造实例**时才调用一次 `list()`，每个实例拿到自己独立的新列表。
```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list[str] = field(default_factory=list)
```
