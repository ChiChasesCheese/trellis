---
id: craft-replace-for-state-change-4-when-mutable
node: craft.idioms.replace-for-state-change
type: qa
step: 4
---
## Q
**用 replace 表达状态变化 · 什么时候该用可变对象加 `transition_to`**｜写法

库存预留和司机记录是冻结的、靠 `replace` 换新；机票的 `Booking` 却是可变的 `slots` 数据类，状态变化走 `transition_to`。这是不一致吗？两种做法各适合什么实体？

## A
**要点。** 判据是这个实体**谁在引用它、有多少字段会各自变化**。冻结 + 整体替换适合被多方持有引用、需要保留旧快照的小记录（预留、司机、聊天消息的历史版本、重试的信封）。可变对象适合只有**一个归属者**（一把锁拥有它）、字段多、有受检的生命周期的实体：`Booking` 有状态、已登机的航段、退款额等一串字段，每次变化只动其中一两个，整体替换要重建全部字段，调用方的每个改动点还得各自检查转移是否合法。

```python
class S(Enum):
    HELD = auto(); TICKETED = auto(); CANCELLED = auto()

ALLOWED = {S.HELD: {S.TICKETED, S.CANCELLED}, S.TICKETED: {S.CANCELLED}, S.CANCELLED: set()}

class InvalidTransition(Exception): ...

@dataclass(slots=True)                       # 可变: 一个实体, 一把锁, 多个字段, 生命周期受检
class Booking:
    id: str
    status: S = S.HELD
    refunded: int = 0
    boarded: tuple[str, ...] = ()

    def transition_to(self, target: S) -> None:
        if target not in ALLOWED[self.status]:
            raise InvalidTransition(f"{self.status.name} -> {target.name}")
        self.status = target

b = Booking("b1")
b.transition_to(S.TICKETED)
print(b.status.name)
try:
    b.transition_to(S.HELD)
except InvalidTransition as e:
    print("非法迁移:", e)
# 换成 frozen + replace 也行, 但每次变化重建整个对象, 且转移表的检查要自己写进每个替换点
```

实际输出：

```
TICKETED
非法迁移: TICKETED -> HELD
```

**选择依据。** 可变版把「哪些状态转移是合法的」集中到 `transition_to`：每次状态变化都必须经过它。冻结版每个替换点都得自己检查，容易有人漏。但可变对象不能随意把引用交出去：对外要给快照（见只读视图与快照）。

**代价。** 两种风格在同一系统里并存是合理的，只要每个实体清楚自己属于哪一种，并且在文档里写明谁拥有它、谁能改它。
