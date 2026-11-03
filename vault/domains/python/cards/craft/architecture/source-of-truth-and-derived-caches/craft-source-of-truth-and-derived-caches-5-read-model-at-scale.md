---
id: craft-source-of-truth-and-derived-caches-5-read-model-at-scale
node: craft.architecture.source-of-truth-and-derived-caches
type: qa
step: 5
---
## Q
**真相与派生缓存 · 从内存缓存到 CQRS 读模型**｜架构

钱包的余额缓存在一个进程里，写路径同步更新它。系统拆成多个服务后，读余额的服务和写账本的服务不在同一台机器，没法在同一把锁里更新。同样的「真相 + 投影」怎么落地？投影落后时读者会看到什么？

## A
**要点。** 做法是 CQRS（命令查询职责分离）的读模型（read model）：写端只追加日志（真相），读端是一个消费日志的投影，只记自己应用到哪条（偏移量 offset）。变的是同步更新变成异步追赶，因此读端会短暂落后，这是最终一致（eventual consistency）；不变的是投影可丢弃、可从头重放重建。

```python
log = [("A", +100), ("A", -30), ("B", +30), ("A", -20)]    # 真相：只追加的日志

class Projection:
    """读模型：每个账户一个余额。只记自己读到日志的哪个位置。"""
    def __init__(self) -> None:
        self.balance: dict[str, int] = {}
        self.offset = 0                          # 已经应用到第几条

    def catch_up(self, upto: int | None = None) -> None:
        for acct, d in log[self.offset:upto]:      # 从上次的位置继续
            self.balance[acct] = self.balance.get(acct, 0) + d
        self.offset = len(log) if upto is None else upto

p = Projection()
p.catch_up(2)
print("读模型落后:", p.balance, "offset", p.offset, "/", len(log))
p.catch_up()
print("追上之后  :", p.balance)

rebuilt = Projection()                           # 读模型丢了也无妨：从头重放
rebuilt.catch_up()
print("丢掉重建一致:", rebuilt.balance == p.balance)
```

日志为 `A+100, A-30, B+30, A-20`，实际输出：

```
读模型落后: {'A': 70} offset 2 / 4
追上之后  : {'A': 50, 'B': 30}
丢掉重建一致: True
```

**为什么。** 缓存与数据库的关系同理：缓存（cache-aside 或 write-through）是数据库的投影，对账 = 比较两边并以数据库为准。

**代价。** 异步投影意味着「刚转完账、马上查余额」可能读到旧值；需要强一致的场景（比如扣款前判断余额）必须读真相或带版本号读，不能读投影。
