---
id: craft-descriptors-where-they-earn-4-shared-function-post-init
node: craft.idioms.descriptors-where-they-earn
type: qa
step: 4
---
## Q
**描述符 · 规则重复三份，共享函数、描述符、基类校验怎么选**｜写法

三个类里各有一条「数量必须是正整数」。可以：写一个共享的校验函数，各类在 `__post_init__` 里调用；写一个描述符；让它们继承一个会自动校验的基类。判断标准是什么？

## A
**要点。** 越简单的机制越优先：共享函数让规则只写一处，调用点显式可见，和冻结加 slots 的数据类完全兼容，读代码的人一眼知道哪些字段被校验。描述符把调用点隐藏起来换来自动化，适合「很多类、很多字段、同一类规则反复出现」。基类校验要靠约定扫描字段，隐式最重。绝大多数情况共享函数就够。

```python
from dataclasses import dataclass

def positive_int(name: str, v: object) -> None:
    if type(v) is not int or v <= 0:
        raise ValueError(f"{name} must be a positive int, got {v!r}")

# 共享函数 + __post_init__：规则写一处，调用点显式
@dataclass(frozen=True, slots=True)
class LineItem:
    qty: int
    cents: int
    def __post_init__(self) -> None:
        positive_int("qty", self.qty)
        positive_int("cents", self.cents)

@dataclass(frozen=True, slots=True)
class Reservation:
    quantity: int
    def __post_init__(self) -> None:
        positive_int("quantity", self.quantity)

for make in (lambda: LineItem(0, 5), lambda: Reservation(-1)):
    try:
        make()
    except ValueError as e:
        print("ValueError:", e)
print(LineItem(2, 500))
```

实际输出：

```
ValueError: qty must be a positive int, got 0
ValueError: quantity must be a positive int, got -1
LineItem(qty=2, cents=500)
```

**为什么。** 规则（`positive_int`）只有一处，两个冻结的 slots 数据类都能用，没有描述符被槽位替换的问题。每个类要显式写一行调用，是故意的：新增字段忘了加校验，在 review 里一眼就能发现。

**信号。** 同一条规则出现在三个以上类、规则种类也不止一两条（正整数、非空、范围、枚举），并且类不是 frozen + slots 数据类，才考虑描述符。否则共享函数。
