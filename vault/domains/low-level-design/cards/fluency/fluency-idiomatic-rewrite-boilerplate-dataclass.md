---
id: fluency-idiomatic-rewrite-boilerplate-dataclass
node: fluency.idiomatic-rewrite
type: qa
step: 3
---
## Q
一个手写的 `Fee` 类有 `__init__`、`__repr__` 和 `__eq__`，放进 `set` 时报 `unhashable type`。改成 `dataclass` 之后，哪些样板消失了，哪些行为跟着变了？什么时候不该改？

## A
**值对象用 `frozen=True` 的 dataclass**

- **手写版的坑**：只写 `__eq__` 不写 `__hash__`，类就变成不可哈希；字段多了，`__repr__` 和 `__eq__` 常漏一个字段；
- **`@dataclass` 生成**：`__init__`、`__repr__`、`__eq__`；`frozen=True` 同时生成 `__hash__` 并禁止赋值，`order=True` 生成比较；
- **校验放进 `__post_init__`**：构造时检查，之后不可变，不合法的对象根本造不出来；
- **可变默认值用 `field(default_factory=list)`**：直接写 `= []` 会被 dataclass 拒绝；
- **冻结是浅层的**：字段是列表，列表照样能改，值对象里用元组；
- **不改的情况**：需要自己控制 `__init__` 的复杂构造、字段之间有大量联动逻辑的类；要解包就用 `NamedTuple`。

```python
from dataclasses import dataclass

class Old:
    def __init__(self, cents): self.cents = cents
    def __eq__(self, o): return self.cents == o.cents
try: hash(Old(1))
except TypeError as e: print(e)                  # unhashable type: 'Old'

@dataclass(frozen=True, order=True)
class Fee:
    cents: int
    def __post_init__(self):
        if self.cents < 0: raise ValueError("cents")
print(Fee(5) == Fee(5), len({Fee(5), Fee(5)}), Fee(1) < Fee(2), Fee(5))
```

<details class="pt"><summary>延伸</summary>

`slots=True`（3.10 起）省内存并拒绝拼错的属性名，创建几十万个小对象时有用；缺点是不能再动态加属性，也不能和多继承里另一个带 `__slots__` 的基类随意组合。

</details>

**知识点：**改写成地道代码（Idiomatic Rewrite）
