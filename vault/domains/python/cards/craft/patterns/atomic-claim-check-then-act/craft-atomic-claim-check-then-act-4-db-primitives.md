---
id: craft-atomic-claim-check-then-act-4-db-primitives
node: craft.patterns.atomic-claim-check-then-act
type: qa
step: 4
---
## Q
**原子占位 · 数据库里的同一个想法：唯一约束与比较并交换**｜模式

进程里用一把锁把「查」和「占」合成一步。服务有多个实例、锁无法共享时，同样的占位怎么在数据库里做？它们和内存锁比，保证了什么、又让出了什么？

## A
**要点。** 数据库里没有「锁一下再看」，而是让写入语句自己带上条件，由数据库的原子写入来判定谁赢：唯一约束（`INSERT ... ON CONFLICT DO NOTHING`）、条件更新（`UPDATE ... WHERE status='AVAILABLE'`，即比较并交换，CAS）。返回影响行数就是「我占到了吗」。

```python
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE idem (k TEXT PRIMARY KEY, owner TEXT)")

def claim(key: str, who: str) -> bool:
    cur = db.execute("INSERT INTO idem VALUES (?, ?) ON CONFLICT(k) DO NOTHING", (key, who))
    return cur.rowcount == 1          # 1 = 我占到了

def cas_offer(driver: str, offer: str) -> bool:
    cur = db.execute("UPDATE drivers SET status='OFFERED', held_by=? "
                     "WHERE id=? AND status='AVAILABLE'", (offer, driver))
    return cur.rowcount == 1          # WHERE 里的旧状态就是比较，rowcount 就是交换是否成功

db.execute("CREATE TABLE drivers (id TEXT PRIMARY KEY, status TEXT, held_by TEXT)")
db.execute("INSERT INTO drivers VALUES ('d1','AVAILABLE',NULL)")
print(claim("pay-42", "worker-1"), claim("pay-42", "worker-2"))
print(cas_offer("d1", "offer-A"), cas_offer("d1", "offer-B"))
```

对同一个键调用两次，对同一位司机提两次要约，实际输出：

```
True False
True False
```

**尺度对照。** 一个进程：`with lock` 包住 `if/赋值`；多个进程：唯一约束或 CAS，赢家由存储决定；多个机器且存储也分布：Redis `SETNX`、租约（lease），占用要带过期时间，否则持有者宕机后永远占着。

**代价。** 内存锁只在进程内有效；数据库做法多一次往返，但换来跨实例的唯一赢家。占位不带过期，宕机会留下永久占位（见预留-确认-过期）。
