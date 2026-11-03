---
id: craft-immutable-snapshot-publish-3-writers-still-lock
node: craft.patterns.immutable-snapshot-publish
type: qa
step: 3
---
## Q
**不可变快照整体替换 · 读者不需要锁，写者为什么还要锁**｜模式

发布时的操作是「读旧快照 → 校验（新版本生效时间必须晚于已有的）→ 造新快照 → 换引用」。两个写者同时发布，读者无锁就够了，写者也能不加锁吗？

## A
**要点。** 不能。读者只做读，写者做的是读-改-写（read-modify-write）：两个写者各自读到同一个旧快照，各自造出「旧 + 自己」，后换上去的覆盖先换的，先发布的版本悄悄丢了，校验也失效。写者之间要用一把锁互相排队，把读旧快照、校验、换引用放进同一个临界区。

```python
def publish(self, start):
    with self.lock:                                   # 写者之间互斥
        old = self.sched                              # 读
        if old.starts and start <= old.starts[-1]:
            return False                              # 校验：必须晚于已有版本
        self.sched = Schedule(old.starts + (start,))  # 写
        return True
```

两个写者同时发布 10 和 20，不加锁与加锁：

```
写者不加锁 -> 最终版本表 (20,)
写者加锁 -> 最终版本表 (10, 20)
```

**为什么。** 无锁读、有锁写是读多写少场景的标准分工：写者吃锁的代价，换读者零等待。

**易错。** 把锁加到读者身上是多余的；把锁漏在写者身上，丢失更新不会报错。校验（是否晚于已有版本）也必须在锁内，否则校验的依据已经过期。
