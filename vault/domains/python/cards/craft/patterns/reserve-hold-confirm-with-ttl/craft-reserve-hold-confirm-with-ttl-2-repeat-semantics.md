---
id: craft-reserve-hold-confirm-with-ttl-2-repeat-semantics
node: craft.patterns.reserve-hold-confirm-with-ttl
type: qa
step: 2
---
## Q
**预留—确认—过期 · 重复确认、取消已过期的预留，应该无操作还是报错**｜模式

预留有 ACTIVE、CONFIRMED、CANCELLED、EXPIRED 四个状态。确认、取消各有四种当前状态可能。重复确认、取消已过期的预留、取消已发货的预留，应该怎么处理，依据是什么？

## A
**要点。** 判据：这次调用想要的结果，是否已经成立。已经成立（重复确认、取消已取消或已过期的）就无操作，重试因此是安全的；与已经发生的事实冲突（取消已发货的、确认已过期的）才抛错，让调用方知道意图没达成。

```python
class Status(Enum):
    ACTIVE = auto(); CONFIRMED = auto(); CANCELLED = auto(); EXPIRED = auto()

class ReservationExpired(Exception): ...
class InvalidState(Exception): ...

def confirm(status: Status) -> str:
    match status:
        case Status.ACTIVE:
            return "确认成功 -> CONFIRMED"
        case Status.CONFIRMED:
            return "无操作（重复确认）"                # 重试是安全的
        case Status.EXPIRED:
            raise ReservationExpired("已过期")
        case Status.CANCELLED:
            raise InvalidState("已取消")

def cancel(status: Status) -> str:
    match status:
        case Status.ACTIVE:
            return "取消成功 -> CANCELLED"
        case Status.CONFIRMED:
            raise InvalidState("已发货，不能取消")      # 与已发生的事实冲突
        case Status.CANCELLED | Status.EXPIRED:
            return "无操作"                            # 结果已经是调用方想要的

for op in (confirm, cancel):
    for st in Status:
        try:
            out = op(st)
        except Exception as e:
            out = f"抛 {type(e).__name__}"
        print(f"{op.__name__:7s} {st.name:10s} -> {out}")
```

八种组合的实际输出：

```
confirm ACTIVE     -> 确认成功 -> CONFIRMED
confirm CONFIRMED  -> 无操作（重复确认）
confirm CANCELLED  -> 抛 InvalidState
confirm EXPIRED    -> 抛 ReservationExpired
cancel  ACTIVE     -> 取消成功 -> CANCELLED
cancel  CONFIRMED  -> 抛 InvalidState
cancel  CANCELLED  -> 无操作
cancel  EXPIRED    -> 无操作
```

**为什么。** 取消已过期的预留无操作：用户点取消时，系统可能刚好把它过期了，让他看到一个错误毫无意义，库存早已放回。

**易错。** 需要提前把这张表说清楚，因为调用方会重试，重试遇到的正是这些状态。
