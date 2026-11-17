---
id: api-hard-to-misuse-keyword-only
node: api.hard-to-misuse
type: qa
step: 3
---
## Q
`Transaction(merchant, card, amount, day)` 前三个字段都是字符串或 `int`，调用方把 `card` 和 `merchant` 填反了，类型检查器也看不出。接口怎样才能让这种错写不出来？

## A
**同类型相邻的参数，强制写名字**

- **位置参数靠记忆**：参数顺序是实现细节，调用方一眼看不出填反；两个都是 `str` 时没有任何工具能拦；
- **仅关键字（keyword-only）**：函数用 `*` 隔开，`def f(a, *, b)`；dataclass 用 `@dataclass(kw_only=True)`（Python 3.10 起）；
- **调用处自己说明含义**：`Transaction(merchant="m", card="visa", amount=5)`，评审时一眼能看出对错；
- **加字段不破坏旧调用**：因为都是按名字传，在中间插入新字段也不会让位置错位；
- **内部构造也一样**：不同记录的字段顺序不一致时，建键按名字取，不要按位置取。

```python
from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class Transaction:
    merchant: str
    card: str
    amount: int

try: Transaction("m", "visa", 5)
except TypeError as e: print(e)
t = Transaction(merchant="m", card="visa", amount=5)
print(t)
```

**知识点：**难以用错的接口（Hard to Misuse）
