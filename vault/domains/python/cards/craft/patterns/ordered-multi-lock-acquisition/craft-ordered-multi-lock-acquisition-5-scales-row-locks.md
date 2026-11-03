---
id: craft-ordered-multi-lock-acquisition-5-scales-row-locks
node: craft.patterns.ordered-multi-lock-acquisition
type: qa
step: 5
---
## Q
**固定顺序加多把锁 · 要锁哪些对象在拿到锁之前不知道怎么办**｜模式

有时要锁的第二个对象是读了第一个对象才知道的（节点的父节点），而别的线程可能同时把它改挂到别处。拿锁顺序又怎么保证？数据库里同样的问题是怎么解决的？

## A
**要点。** 先无锁地读出猜测，按固定顺序拿锁，拿到后验证猜测仍成立，不成立就放掉所有锁重来（乐观重试）。数据库里等价的做法：按主键排序后加行锁，并配合死锁检测或锁等待超时，由数据库挑一个事务回滚重试。

```python
while True:
    guess = node.parent                           # 无锁读：只是猜测
    locks = sorted({node, guess} - {None}, key=lambda n: n.id)
    for n in locks:
        n.lock.acquire()                          # 按 id 固定顺序拿
    try:
        if node.parent is guess:                  # 拿到锁后再验证猜测仍成立
            ...                                   # 修改 node 和 guess
            return
    finally:
        for n in reversed(locks):
            n.lock.release()
    # 猜测过期了：放掉所有锁，重来
```

在第一次读猜测后让另一个线程把 `n` 改挂到 p2：

```
尝试次数: 2 | p1.total = 0 p2.total = 5
```

**尺度对照。** 内存里：按 id 排序（同层）加分层方向（跨层）；数据库里：事务按主键顺序更新行（两阶段锁，2PL）加死锁检测；分布式事务里：协调者按固定顺序请求各分片的锁，或用超时放弃。

**代价。** 乐观重试在冲突多时会反复重来（活锁）；排序要求每个对象有全局可比较的稳定键。

**信号。** 一个操作涉及多个独立加锁的对象，尤其是「转」「合并」「移动」这类两端对称的操作。
