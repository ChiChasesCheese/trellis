---
id: craft-default-forms-6-scales-cycle-detection
node: craft.idioms.default-forms
type: qa
step: 6
---
## Q
**省掉标志变量 · 从“找不到可执行的规则 = 有环”到 Course Schedule 与构建系统**｜写法

计费引擎里“剩下的规则没有一个能先跑”就是依赖成环。LeetCode 的 Course Schedule、构建系统的依赖解析、数据库的死锁检测是同一件事吗？

## A
**要点。** 是同一个判据：每一轮只取“没有未满足依赖”的节点，取完还有剩下的，剩下的节点互相等待，即有环。LLD 里是反复 `next(…, None)` 找 ready，O(n²)，规模小、代码短；LeetCode 里用入度数组和队列（Kahn 算法）做到 O(V+E)，判断 `done == n`。

```python
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE idem (k TEXT PRIMARY KEY, owner TEXT)")

def claim(key: str, who: str) -> bool:
    cur = db.execute("INSERT INTO idem VALUES (?, ?) ON CONFLICT(k) DO NOTHING", (key, who))
    return cur.rowcount == 1          # 1 = 我占到了；0 = 已有人占

def cas_offer(driver: str, offer: str) -> bool:
    cur = db.execute("UPDATE drivers SET status='OFFERED', held_by=? "
                     "WHERE id=? AND status='AVAILABLE'", (offer, driver))
    return cur.rowcount == 1          # WHERE 里的旧状态就是比较，rowcount 就是交换是否成功

db.execute("CREATE TABLE drivers (id TEXT PRIMARY KEY, status TEXT, held_by TEXT)")
db.execute("INSERT INTO drivers VALUES ('d1','AVAILABLE',NULL)")
print(claim("pay-42", "worker-1"), claim("pay-42", "worker-2"))
print(cas_offer("d1", "offer-A"), cas_offer("d1", "offer-B"))
```

实际输出：

```
True False
```

**变化。** 规模从几条规则到几万个任务，要从“每轮重新扫描”换成“入度计数 + 就绪队列”：谁变成就绪只在依赖被满足的那一刻发生，不再反复扫描。构建系统（Bazel、Make）、工作流调度（Airflow）、数据库的等待图死锁检测，都是在有向图上找环，只是节点换成任务、事务。

**代价。** 报错时要给出环里有哪些节点，调用方才能修：计费规则的排序把 `pending` 列表放进异常信息（剩下的集合不一定就是环本身，而是环加上依赖它的节点，仍然有助于定位）。

**信号。** 有“先后依赖”的一组东西需要排出一个执行顺序，或需要拒绝有环的配置。
