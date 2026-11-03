---
id: craft-reserve-hold-confirm-with-ttl-4-across-problems
node: craft.patterns.reserve-hold-confirm-with-ttl
type: qa
step: 4
---
## Q
**预留—确认—过期 · 库存、订座、快递柜、图书馆里的同一个持有**｜模式

库存预留、电影选座、快递柜取件码、图书馆预约取书，场景不同，结构却相同。它们的「占用凭证」和「到期动作」分别是什么？

## A
**要点。** 共同结构：占用带一个 id 和一个到期时间，过期自动放回（惰性），确认是从持有到成交的一次受检转移。变的是凭证的形式和到期放回的是什么。

```python
# inventory-management：预留快照带到期时间，放回的是库存数量
heapq.heappush(self._expiry, (expires_at, entry.id))

# movie-booking：持有收据，放回的是座位
@dataclass(frozen=True, slots=True)
class SeatHold:
    id: str; show_id: str; seat_labels: tuple[str, ...]
    user_id: str; expires_at: datetime

# amazon-locker：取件码带 expires_at，放回的是柜格
grant = AccessGrant(code=code, locker_id=locker.locker_id, ...,
                    issued_at=now, expires_at=now + self._ttl)
heapq.heappush(self._deadlines, (grant.expires_at, code))
```

不变：到期时间存在凭证里，由注入的时钟惰性判断，到期堆负责在没人访问时也能回收。变化：凭证是数量快照、收据、取件码；回收的资源是库存、座位、柜格；确认后的状态是已发货、已出票、已取走。

**见于。** inventory-management、movie-booking、airline（HELD → TICKETED）、amazon-locker、online-shopping、library。

**信号。** 资源有限，占用和使用之间隔着一段人的时间；需求里出现「锁定 15 分钟」「保留到……」「逾期自动释放」。
