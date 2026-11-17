---
id: data-value-entity-identity-vs-equality
node: data.value-entity
type: qa
step: 1
---
## Q
两个 `Money(5, "USD")` 应该相等，两个同名的 `User("ann")` 却不一定是同一个用户。判等到底该看内容还是看身份？Python 里两种类各怎么写？

## A
**值对象按内容判等，实体按 id 判等**

- **值对象（value object）**：没有“这一个”的概念，内容相同就是同一个值，如金额、坐标、日期范围；不可变，可以随便共享；
- **实体（entity）**：有生命周期的“这一个”，内容会变但还是它，如账户、订单；用 id 判等；
- **值对象**：`@dataclass(frozen=True)` 自动生成按字段比较的 `__eq__` 和 `__hash__`；
- **实体**：`@dataclass(eq=False)` 保留身份比较，或手写 `__eq__` 与 `__hash__` 只看 `id`；
- **判断办法**：问“把两个对象互相替换，业务会不会变？”换成同值的 `Money` 不会，换成另一个账户一定会。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    cents: int
    cur: str

class Account:
    def __init__(self, id: int, balance: int): self.id, self.balance = id, balance
    def __eq__(self, o): return isinstance(o, Account) and self.id == o.id
    def __hash__(self): return hash(self.id)

print(Money(500, "USD") == Money(500, "USD"))          # True
a, b = Account(1, 100), Account(1, 250)
print(a == b, len({a, b}))                             # True 1：余额不同，仍是同一个账户
```

**知识点：**值对象与实体（Value vs Entity）
