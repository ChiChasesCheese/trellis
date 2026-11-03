---
id: craft-lazy-expiry-settle-on-access-4-across-problems
node: craft.patterns.lazy-expiry-settle-on-access
type: qa
step: 4
---
## Q
**惰性过期 · 库存、四子棋、拍卖里同一种「访问时结清」**｜模式

库存预留到点要释放，四子棋一方超时要判负，拍卖到点要结束且只结束一次。这三个需求里没有一个用了定时器。它们是怎么做到「到点的事恰好发生一次」的？

## A
**要点。** 同一个骨架：状态里存「截止时间」，任何访问的第一步调用一个结清函数，把世界推进到当前时间应有的样子。恰好一次由锁保证：「第一个看到它的人」在锁里完成状态翻转，之后的人看到的已经是翻转后的状态。

```python
# inventory-management：恰好到点也算过期
while self._expiry and self._expiry[0][0] <= now:
    at, rid = heapq.heappop(self._expiry)
    ...

# connect-four：没有后台线程，任何访问都先看一眼回合是否超时
if (self._move_seconds is not None and not self._finished(m)
        and self._clock() - m.turn_started >= self._move_seconds):
    m.forfeited, m.forfeit_winner = Reason.TIMEOUT, m.players[1 - mover]

# online-auction._tick：结束是被「第一个看它的人」触发的
if self._status is AuctionStatus.SCHEDULED and now >= self.starts_at:
    self._status = AuctionStatus.ACTIVE
```

不变：截止时间存在状态里，结清函数幂等（已结清再调用什么都不做）。变化：结清的对象不同（预留、回合、拍卖状态），以及是否产生事件。

**见于。** inventory-management、ttl-cache、connect-four、kv-store、library、online-auction、idempotent-transfer。

**信号。** 需求里出现「超时」「过期」「到点自动」；而你想起一个 timer 或后台线程。先问：没有人访问的时候，这件事有没有人关心？
