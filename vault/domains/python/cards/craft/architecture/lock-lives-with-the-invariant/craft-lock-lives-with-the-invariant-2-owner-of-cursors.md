---
id: craft-lock-lives-with-the-invariant-2-owner-of-cursors
node: craft.architecture.lock-lives-with-the-invariant
type: qa
step: 2
---
## Q
**锁跟着不变量走 · 订阅游标为什么归 Topic 管**｜架构

消息队列（pub-sub）有一条有界日志，日志满了要么丢最老的，要么拒绝新消息（阻塞，BLOCK 反压：慢读者没读完时，生产者不许覆盖）。如果每个订阅者（Subscription）自己持有游标（读到第几条）和自己的锁，BLOCK 能实现吗？

## A
**要点。** 不能。「最老一条能不能丢」取决于所有游标的最小值，这个不变量跨越日志和全部游标，所以游标、日志、锁必须归同一个拥有者（Topic）。游标分散在各个订阅者里，Topic 要判断就得逐个去拿它们的锁，既拿不到一致的快照，又多出锁序问题。

```python
class Topic:
    """日志 + 所有游标都归 Topic，一把锁保护「最慢读者没读到的不许丢」。"""
    def __init__(self, capacity: int) -> None:
        self._lock = threading.Lock()
        self._log: list[str] = []
        self._base = 0                       # 日志第一条的序号
        self._cursor: dict[str, int] = {}    # 订阅者 -> 下一条要读的序号
        self._cap = capacity

    def subscribe(self, name: str) -> None:
        with self._lock:                        # 一把锁：日志 + 全部游标
            self._cursor[name] = self._base + len(self._log)

    def publish(self, msg: str) -> bool:
        with self._lock:
            if len(self._log) == self._cap:
                if self._cursor and min(self._cursor.values()) <= self._base:
                    return False                # 最慢的人还没读到最老一条
                self._log.pop(0); self._base += 1
            self._log.append(msg)
            return True

    def poll(self, name: str) -> str | None:
        with self._lock:
            i = self._cursor[name] - self._base
            if i >= len(self._log):
                return None
            self._cursor[name] += 1
            return self._log[i]

t = Topic(capacity=2)
t.subscribe("fast"); t.subscribe("slow")
print(t.publish("a"), t.publish("b"))
print("满了，两人都没读:", t.publish("c"))
print("fast 读到", t.poll("fast"), t.poll("fast"))
print("slow 还没读，仍然:", t.publish("c"))
print("slow 读到", t.poll("slow"))
print("slow 让出最老一条后:", t.publish("c"))
```

容量 2，订阅者 fast 和 slow，实际输出：

```
True True
满了，两人都没读: False
fast 读到 a b
slow 还没读，仍然: False
slow 读到 a
slow 让出最老一条后: True
```

**为什么。** fast 读完了也不行，因为最老一条 slow 还没读；等 slow 读走 a，最小游标前进，才能腾出位置。

**代价。** 所有读写共用一把锁，热点 Topic 上订阅者多了就是瓶颈；要缩小粒度只能先把不变量拆开，比如每个订阅者一条独立队列，这时背压的含义也跟着变了。
