---
id: craft-functional-core-imperative-shell-5-reducer-at-scale
node: craft.architecture.functional-core-imperative-shell
type: qa
step: 5
---
## Q
**函数式核心 + 命令式外壳 · 从额度重放到事件流的 reducer**｜架构

额度系统把发放和扣费事件按时间排序，重放一遍算出剩余额度；流处理系统里的消费者收到事件，也要更新状态，而且消息队列会重复投递。这两件事里「纯函数 + 外壳」怎么对应？到了多机，外壳多了哪些职责？

## A
**要点。** 一台机器：核心是 `_replay(grants, charges, until)`，输入全部事件，输出分配和剩余额度，外壳只存事件、调用它。多机：核心变成 `reduce(state, event) -> state`，外壳换成消费者进程，负责从日志取事件、持久化状态、提交偏移（offset）。变的是外壳的职责，核心还是纯函数；Redux、Elm 也是这个形状。

```python
@dataclass(frozen=True)
class State:
    balance: int = 0
    seen: frozenset[str] = frozenset()      # 已处理的事件 id

def reduce(s: State, event_id: str, delta: int) -> State:
    """纯函数：旧状态 + 事件 -> 新状态，不读时钟，不碰外部。"""
    if event_id in s.seen:
        return s                        # 重复投递：返回原状态
    return State(s.balance + delta, s.seen | {event_id})

stream = [("g1", 100), ("c1", -30), ("c1", -30), ("c2", -20)]   # c1 被投递了两次
s = State()
for eid, d in stream:
    s = reduce(s, eid, d)
print(s.balance)
```

事件流 `[g1 +100, c1 -30, c1 -30, c2 -20]`，`c1` 被投递两次，逐条 `reduce` 后的 `balance`，实际输出：

```
50
```

100 − 30 − 20 = 50：重复的 `c1` 没有被扣两次。

**为什么。** 核心是纯的，所以同一串事件重放多少次、在哪台机器重放，结果都一样；「重放到某个时间点」（`until`）就是只喂前缀。

**代价。** 多机时外壳要保证「状态落盘」和「偏移提交」这两步不分家，否则崩溃后重放会漏或重；纯核心不会替你解决这个问题，它只保证重放可重复。
