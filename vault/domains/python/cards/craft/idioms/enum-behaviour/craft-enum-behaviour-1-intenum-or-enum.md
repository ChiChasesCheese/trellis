---
id: craft-enum-behaviour-1-intenum-or-enum
node: craft.idioms.enum-behaviour
type: qa
step: 1
---
## Q
**Enum 的行为 · 什么时候该用 IntEnum**｜写法

通知系统里每个渠道有「至少多重要我才收」的门槛：短信只收紧急的，邮件什么都收。优先级如果用 `"low"/"high"` 字符串或散落的整数常量，比较就要自己写一张映射。`IntEnum` 解决了什么，又带来什么隐患？

## A
**要点。** 枚举（enum）是一组有名字的常量，成员之间默认只能比较身份。`IntEnum` 的成员同时是 `int`：可以直接用 `>=` 比大小，可以排序，也可以当数组下标。当「等级」本身是个有序的刻度（优先级、严重度、舱位）时用它；成员之间没有大小关系时用普通 `Enum`。

```python
import json
from enum import Enum, IntEnum

class Priority(IntEnum):
    MARKETING = 10
    TRANSACTIONAL = 20
    URGENT = 30

class Color(Enum):                 # 对照：普通 Enum
    RED = 10

min_priority = {"sms": Priority.URGENT}
def wanted(channel: str, p: Priority) -> bool:
    return p >= min_priority.get(channel, Priority.MARKETING)    # 比大小，一行

print(wanted("sms", Priority.TRANSACTIONAL), wanted("email", Priority.TRANSACTIONAL))
print(Priority.MARKETING == 10, Color.RED == 10)
print(Priority.URGENT + 1)
print(json.dumps({"p": Priority.URGENT}))
```

实际输出：

```
False True
True False
31
{"p": 30}
```

**代价。** 这个便利同时是漏洞：`Priority.MARKETING == 10` 为真，所以任何整数都能在不报错的情况下被当成优先级，`URGENT + 1` 也能算出一个不存在的等级 31。序列化出去的只有数字 30，名字丢了，日志里要靠人记。

**易错。** 不需要比较的状态（`IDLE`、`DISPENSING`）不要用 `IntEnum`：否则 `State.IDLE == 0` 之类的比较悄悄成立，类型检查器也拦不住。
