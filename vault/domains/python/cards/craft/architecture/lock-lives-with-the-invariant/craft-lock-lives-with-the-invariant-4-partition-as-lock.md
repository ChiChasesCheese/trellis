---
id: craft-lock-lives-with-the-invariant-4-partition-as-lock
node: craft.architecture.lock-lives-with-the-invariant
type: qa
step: 4
---
## Q
**锁跟着不变量走 · 单机的锁和分布式的分区是同一件事吗**｜架构

订座服务要横向扩展到很多台机器。每个航班实例上的那把锁，在多机上怎么对应？不变量跨两个对象时（一条中转行程占两班飞机）又怎么办？

## A
**要点。** 对应「一个聚合（aggregate，一组必须一起保持不变量的数据）在一个分区里串行处理」。路由时让同一个 key（`航班号@日期`）永远落到同一个分片，由一个线程或进程顺序处理它的全部命令，检查和写入天然不交错，不需要锁。Actor 模型、Kafka 里「同 key 同分区」都是这个思路。

```python
class Shard:                                  # 一个 key 一个分片
    """一个 key 的所有命令进同一个队列，由一个线程顺序处理：没有锁，也没有竞态。"""
    def __init__(self, seats: int) -> None:
        self.seats, self.sold = seats, 0
        self.inbox: queue.Queue = queue.Queue()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self) -> None:
        while (reply := self.inbox.get()) is not None:
            if self.sold < self.seats:        # 检查 + 写入，天然串行
                self.sold += 1
                reply.put(True)
            else:
                reply.put(False)

shards: dict[str, Shard] = defaultdict(lambda: Shard(2))
def book(flight_key: str) -> bool:           # 路由：同 key 同分片
    reply: queue.Queue = queue.Queue()
    shards[flight_key].inbox.put(reply)
    return reply.get()

print([book("MU5100@07-01") for _ in range(4)])
print(book("MU5100@07-02"))
```

座位 2 个，同一班订 4 次，再订另一天的同一班，实际输出：

```
[True, True, False, False]
True
```

**为什么。** 锁是「谁拥有不变量就让谁串行」在单进程里的写法，分区是它在多机上的写法：两者的前提都是不变量的范围划得小，一个 key 内部串行，不同 key 之间并行。

**代价。** 不变量跨两个 key（中转行程）就越出了单分区：航班订票里两把实例锁按 `key` 排序后同时持有，多机上则要两阶段提交或补偿（saga）。能把两班合进同一个聚合就别拆，否则就接受协调的成本。
