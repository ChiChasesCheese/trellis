---
id: cc-python-classes-dataclass-ordering
node: python.classes
type: qa
---
## Q
You want a record that sorts by `(day, seq)`, prints readably, and cannot be mutated by accident. Write the decorator line and say what each argument buys.

## A
```python
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True, slots=True)
class Email:
    day: int
    seq: int
    text: str = field(compare=False)
```

- `order=True` generates `<`, `<=`, `>`, `>=` comparing **all** fields in declaration order — so declaration order *is* the sort order.
- `field(compare=False)` keeps a payload out of the comparison; declare it last.
- `frozen=True` gives immutability and a usable `__hash__`; `slots=True` (3.10+) removes the per-instance `__dict__`.
- If ordering is the *only* reason for the class, a plain tuple sorts faster and costs less memory ([[cc-performance-memory-sort-key-cost]]).

## Q zh
你要一个按 `(day, seq)` 排序、打印可读、且不会被误改的记录类型。写出装饰器那一行，并说明每个参数买到了什么。

## A zh
```python
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True, slots=True)
class Email:
    day: int
    seq: int
    text: str = field(compare=False)
```

- `order=True` 生成 `<`、`<=`、`>`、`>=`，按声明顺序比较**所有**字段 —— 所以声明顺序*就是*排序顺序。
- `field(compare=False)` 把载荷排除在比较之外；把它声明在最后。
- `frozen=True` 带来不可变性和可用的 `__hash__`；`slots=True`（3.10+）去掉每个实例的 `__dict__`。
- 如果建类的*唯一*理由是排序，普通 tuple 排得更快、内存更省（[[cc-performance-memory-sort-key-cost]]）。
