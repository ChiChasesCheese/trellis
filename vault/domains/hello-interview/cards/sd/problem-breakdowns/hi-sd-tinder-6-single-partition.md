---
id: hi-sd-tinder-6-single-partition
node: sd.problem-breakdowns.tinder
type: qa
step: 6
---
## Q
**Tinder：用户对分区实现原子匹配**｜系统设计 · 问题拆解

怎样在 Cassandra 里让互相滑动落在同一分区，从而原子检查匹配？这种做法有什么运维风险？

## A
**做法。** 表的分区键用 user_pair，由两个用户 ID 排序后拼成（小 ID:大 ID），聚簇键为 from_user、to_user。这样 A 到 B 和 B 到 A 两条记录必然同分区，在一个批处理中写入并读取对方方向，就是单分区的原子操作。

```python
def get_user_pair(a: str, b: str) -> str:
    # 排序后 (A->B) 和 (B->A) 得到同一个键，所以落在同一分区
    lo, hi = sorted([a, b])
    return f"{lo}:{hi}"
```

**为什么有效。** 原子性只需要在单个分区里成立，避开了跨分区分布式事务。

**风险。** 一对用户的滑动记录会随时间累积，分区可能无限增长；极活跃的用户可能带来热点分区。所以需要清理策略，把旧滑动归档或删除，同时保留必要的历史。
