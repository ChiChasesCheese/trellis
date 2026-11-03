---
id: craft-enum-behaviour-4-definition-order-and-strenum
node: craft.idioms.enum-behaviour
type: qa
step: 4
---
## Q
**Enum 的行为 · 定义顺序当生命周期，StrEnum 当序列化值**｜写法

外卖配送事件必须按 接单 → 到店 → 取餐 → 送达 的顺序发生。你想直接把 `list(EventType)` 当作合法顺序，而不是另维护一个列表。这依赖枚举的什么保证？另外结束原因要写进 JSON，`StrEnum` 和老写法 `class R(str, Enum)` 有什么区别？

## A
**要点。** 迭代枚举按定义顺序给出成员，与值无关。所以「定义顺序 = 生命周期」是一个真保证，但它也意味着在中间插入一个成员会改变顺序，而没有任何东西报错；顺序一旦有业务含义，就用测试把它钉住。需要序列化为字符串时，Python 3.11 起用 `StrEnum`：它的 `str()` 就是值。

```python
import json
from enum import Enum, IntEnum, StrEnum

class EventType(IntEnum):
    ACCEPT = 1
    ARRIVE = 2
    PICKUP = 3
    DROPOFF = 4

LIFECYCLE = list(EventType)                 # 定义顺序就是生命周期顺序
def in_order(seen: list[EventType]) -> bool:
    return seen == LIFECYCLE[:len(seen)]    # 已发生的必须是前缀

print(in_order([EventType.ACCEPT, EventType.ARRIVE]))
print(in_order([EventType.ACCEPT, EventType.PICKUP]))     # 跳过了到店

class Looser(Enum):                         # 定义顺序和值的顺序不一致
    ACCEPT = 1
    ARRIVE = 2
    DROPOFF = 4
    PICKUP = 3
print([m.name for m in Looser])

class Reason(StrEnum):
    DRAW = "draw"
class Old(str, Enum):
    DRAW = "draw"
print(str(Reason.DRAW), str(Old.DRAW))
print(json.dumps([Reason.DRAW, Old.DRAW]))
```

实际输出：

```
True
False
['ACCEPT', 'ARRIVE', 'DROPOFF', 'PICKUP']
draw Old.DRAW
["draw", "draw"]
```

**为什么。** `Looser` 说明迭代跟随书写顺序而不是数值，所以「按值排序」和「按定义顺序」不是一回事，选一个并说清楚。`StrEnum` 的 `str()` 直接是值，日志、模板里拼接不会出现 `Old.DRAW` 这种带类名的字符串；两者放进 `json.dumps` 都得到 `"draw"`。

**易错。** 往枚举中间插入成员、或者重排定义，会静默改变 `list(...)` 的顺序。如果顺序有业务含义，显式写 `LIFECYCLE = (A, B, C, D)`，不要隐含在书写顺序里。
