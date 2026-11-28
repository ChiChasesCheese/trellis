---
id: hi-c-lld-amazon-locker-b03-py-transition-table
node: lld.problem-breakdowns.amazon-locker.beyond
type: qa
step: 4
---
## Q
**快递柜 · Python：格口状态用转换表约束**｜拓展 · 加分

扩展里格口有可用、预约中、已占用、停用四种状态，怎样让"不允许的跳转"一定报错，而不是靠到处写 `if`？

## A
**模式。** 转换表状态机：把"从哪个状态能去哪个状态"写成一张数据表。

```python
from enum import Enum, auto


class S(Enum):
    AVAILABLE = auto()
    RESERVED = auto()
    OCCUPIED = auto()
    OUT_OF_SERVICE = auto()


ALLOWED: dict[S, set[S]] = {
    S.AVAILABLE: {S.RESERVED, S.OCCUPIED, S.OUT_OF_SERVICE},
    S.RESERVED: {S.OCCUPIED, S.AVAILABLE},    # 确认存件 / 取消或超时
    S.OCCUPIED: {S.AVAILABLE},                # 包裹被取走
    S.OUT_OF_SERVICE: {S.AVAILABLE},          # 修好后
}


class Compartment:
    def __init__(self) -> None:
        self.status = S.AVAILABLE

    def to(self, new: S) -> None:             # 所有状态变化只走这一个入口
        if new not in ALLOWED[self.status]:
            raise ValueError(f"{self.status.name} -> {new.name}")
        self.status = new


c = Compartment()
c.to(S.RESERVED)
c.to(S.OCCUPIED)
try:
    c.to(S.RESERVED)          # 已占用的格口不能被再次预约
except ValueError:
    pass
```
- **好处：** 规则是一眼能审查的数据；新增状态只改表，不改散落各处的 `if`。
- **和布尔标志的区别：** 布尔表达不出"预约中"，两个布尔又有非法组合；枚举加转换表让非法跳转直接抛错。
- **代价：** 多一层间接；状态只有两三种时，布尔更直接。
- **常见补充：** 转换表里的动作（开门、记日志）可以放在表的值里做成"转换 + 回调"，但回调越多越难读。
