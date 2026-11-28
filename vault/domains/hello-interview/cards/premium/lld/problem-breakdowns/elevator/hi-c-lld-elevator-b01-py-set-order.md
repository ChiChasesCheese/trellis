---
id: hi-c-lld-elevator-b01-py-set-order
node: lld.problem-breakdowns.elevator.beyond
type: qa
step: 1
---
## Q
**电梯系统 · Python：集合的迭代顺序为什么每次运行不同**｜拓展 · 加分

`next(iter(requests))` 在不同次运行里取到不同的请求。底层是什么原因？怎么写才确定？

## A
**模式。** 确定性选择：从无序容器取元素，一律带排序键。

```python
from dataclasses import dataclass
from enum import Enum, auto


class Kind(Enum):
    UP = auto()
    DOWN = auto()
    DEST = auto()


@dataclass(frozen=True)
class Req:                      # frozen 且 eq=True，Python 据此自动生成 __hash__
    floor: int
    kind: Kind


reqs = {Req(3, Kind.UP), Req(3, Kind.DOWN), Req(3, Kind.DEST)}
first = next(iter(reqs))        # 随进程变化：枚举的哈希来自成员名这个字符串
stable = min(reqs, key=lambda r: (r.floor, r.kind.value))   # 排序键写全：先楼层，再类型
assert stable.kind is Kind.UP   # 每次运行都一样
```
- **底层：** 字符串的哈希值在每个进程启动时用随机盐计算（防哈希碰撞攻击），枚举成员按名字哈希，包含它的元组和数据类的哈希也随之改变；集合按哈希值排布，迭代顺序因此跟着变。设置环境变量 `PYTHONHASHSEED` 可固定它，用来复现问题，但不能当作设计依据。
- **对比：** 字典保证插入顺序，集合不保证；需要确定顺序就用 `min/max/sorted` 加完整的排序键。
- **何时不用：** 顺序无关的聚合（求和、是否存在）不需要。
