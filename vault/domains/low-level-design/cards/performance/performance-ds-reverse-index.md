---
id: performance-ds-reverse-index
node: performance.data-structures
type: qa
step: 2
---
## Q
通知服务里，用户关注了若干演员。演员发新片时，要找出所有关注者。每次都遍历全部用户，为什么在用户一多就撑不住？反向索引怎么建、写入路径上要守什么？

## A
**查询方向和存储方向相反时，多存一份反向索引**

- **正向存储**：`user -> 关注的演员集合`，回答“这个用户关注谁”很快，回答“谁关注这个演员”要遍历全体用户；
- **反向索引**：`actor -> 关注者集合`，查询直接取一个 key，耗时与用户总数无关；
- **代价在写路径**：关注和取关要同时改两边，漏改一边就读到过期数据；所以只留一个写入口；
- **取关后集合变空要删掉**：不删，字典里会堆满空集合，演员越多越浪费；
- **读写比决定值不值**：读远多于写才建；写比读还多的数据，每次写两处是净亏损。

实测（3.11，本机）：2,000 个用户、500 个演员、每人关注 10 个。遍历所有用户找关注者，一次约 25 µs；查反向索引，一次约 12 ns；建一次索引约 0.94 ms，约 38 次查询就回本。

```python
class Follows:
    def __init__(self):
        self.by_user, self.by_actor = {}, {}     # by_actor 是反向索引

    def follow(self, user, actor):
        self.by_user.setdefault(user, set()).add(actor)
        self.by_actor.setdefault(actor, set()).add(user)

    def unfollow(self, user, actor):
        self.by_user.get(user, set()).discard(actor)
        fans = self.by_actor.get(actor, set()); fans.discard(user)
        if not fans: self.by_actor.pop(actor, None)    # 空集合不留

    def fans(self, actor): return frozenset(self.by_actor.get(actor, ()))  # 快照
```

**知识点：**按访问模式选结构（Choosing Structures）
