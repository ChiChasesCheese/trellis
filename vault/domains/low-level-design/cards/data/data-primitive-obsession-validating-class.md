---
id: data-primitive-obsession-validating-class
node: data.primitive-obsession
type: qa
step: 3
---
## Q
放款服务里“金额”只认正整数，布尔、浮点、`0`、负数都是非法。校验写在每个用金额的函数开头，有什么问题？把金额做成一个小类以后，规则放在哪里？

## A
**规则放进类型的构造函数，拿到这个类型就等于校验过**

- **散落的校验**：十个函数各检查一遍，总有一个漏掉或者检查得不一样；
- **构造即校验**：`Amount.__post_init__` 检查一次，之后任何拿到 `Amount` 的函数都不用再检查；
- **校验写在一处**：`type(x) is int` 排除 `True`（`bool` 是 `int` 的子类），再检查 `> 0`；
- **冻结**：`frozen=True`，构造之后不会被改成非法值；运算通过方法（`plus`）返回新值；
- **边界处转换一次**：外面来的原始值在适配层转成 `Amount`，错了就是 400，内部不再见原始 `int`。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Amount:
    cents: int
    def __post_init__(self):
        if type(self.cents) is not int or self.cents <= 0:
            raise ValueError("invalid_amount")
    def plus(self, other: "Amount") -> "Amount":
        return Amount(self.cents + other.cents)

print(Amount(500).plus(Amount(250)))
for bad in (True, 2.5, 0, -3):
    try: Amount(bad)
    except ValueError as e: print(bad, e)
```

**知识点：**用小类型代替裸值（Primitive Obsession）
