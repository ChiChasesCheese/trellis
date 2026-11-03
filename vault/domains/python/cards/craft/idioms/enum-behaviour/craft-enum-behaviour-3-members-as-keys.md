---
id: craft-enum-behaviour-3-members-as-keys
node: craft.idioms.enum-behaviour
type: qa
step: 3
---
## Q
**Enum 的行为 · 枚举成员作字典键，比字符串常量好在哪**｜写法

状态机的转移表用 `(状态, 事件)` 当键。键写成字符串 `("idle", "pay")` 最省事。同一份表用枚举成员当键，为什么在出错的时候好得多？

## A
**要点。** 字符串键的拼写错误是「合法的值」：`("idle", "payy")` 只是查不到，被当成一个非法转移悄悄处理。枚举成员是对象，拼错名字在读代码的那一刻就是 `AttributeError`，而且 IDE 可以补全、重命名。只有在系统边界上（解析请求、读配置）才用字符串转回成员，转换失败也立刻报错。

```python
from enum import Enum

class State(Enum):
    IDLE = "idle"
    COIN = "coin"

class Event(Enum):
    PAY = "pay"
    REFUND = "refund"

TRANSITIONS = {(State.IDLE, Event.PAY): State.COIN, (State.COIN, Event.REFUND): State.IDLE}
STR_TRANSITIONS = {("idle", "pay"): "coin", ("coin", "refund"): "idle"}

print(STR_TRANSITIONS.get(("idle", "payy")))        # 字符串拼错：静默的 None
try:
    TRANSITIONS[(State.IDLE, Event.PAYY)]           # 枚举拼错：立刻报错
except AttributeError as e:
    print(type(e).__name__, e)
print(State("coin"), State["COIN"])                 # 边界处：按值或按名字转回成员
try:
    State("coinn")
except ValueError as e:
    print(type(e).__name__, e)
```

实际输出（Python 3.14；报错文字在 3.11 里略有不同）：

```
None
AttributeError type object 'Event' has no attribute 'PAYY'
State.COIN State.COIN
ValueError 'coinn' is not a valid State
```

**为什么。** 枚举成员是单例且可哈希，作字典键与元组一起用没有任何额外代价；比较用 `is` 或 `==` 都是常数时间的身份判断。

**易错。** `State("coin")` 按值查找，`State["COIN"]` 按名字查找，两者不同。对外部输入用前者并捕获 `ValueError`，不要让「未知状态」变成一个 `KeyError` 漏出去。
