---
id: concurrency-depth-cas-retry
node: concurrency-depth.atomics
type: qa
step: 1
---
## Q
比较并交换（compare-and-swap，CAS）是什么？库存表加一列 `ver`，更新时 `WHERE ver=?`，为什么能不加锁就保证不丢更新？冲突多的时候它的代价是什么？

## A
**读出值和版本，写回时带上版本，版本变了就重读重算**

- **CAS 的语义**：“当前值仍等于我读到的，才改成新值，否则失败”，检查和写入是一步原子操作；
- **数据库里的写法**：`UPDATE … SET qty=?, ver=ver+1 WHERE id=? AND ver=?`，`rowcount == 1` 才生效，0 说明别人先改了，回到第一步重读；
- **不持锁地计算**：读和写之间可以做任意耗时的计算，不挡别人；这是乐观并发（optimistic concurrency），适合冲突少的场景；
- **代价是重试**：冲突多时大家反复白算。实测（3.11，每个线程一个连接，读和写之间停 1 ms 模拟计算，每线程成功 20 次）：1 个线程 20 次尝试，2 个线程 58 次尝试完成 40 次，8 个线程 362 次尝试完成 160 次；没有计算间隔时 8 线程 1605 次尝试完成 1600 次，几乎不冲突；
- **必须有上限和退避**（示例为了展示形状没写）：无限重试在热点行上会饿死一部分调用方，设最大次数，超过就报“冲突”让调用方决定；
- **Python 进程内没有对整数的原子 CAS**：标准库不提供，自己写的 `compare_and_set` 内部也是一把锁；CAS 的价值主要在数据库和 Redis 这类不能长时间持锁的地方。

```python
import sqlite3

def update_stock(db, item, fn):
    while True:
        qty, ver = db.execute("SELECT qty, ver FROM stock WHERE id=?", (item,)).fetchone()
        cur = db.execute("UPDATE stock SET qty=?, ver=ver+1 WHERE id=? AND ver=?",
                         (fn(qty), item, ver))
        if cur.rowcount == 1:              # 版本没变：这次写入生效
            return

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE stock(id INTEGER PRIMARY KEY, qty INT, ver INT)")
db.execute("INSERT INTO stock VALUES (1, 10, 0)")
update_stock(db, 1, lambda q: q - 3)
print(db.execute("SELECT qty, ver FROM stock").fetchone())     # (7, 1)
```

<details class="pt"><summary>延伸</summary>

上面的循环没有上限，是为了展示形状；生产代码要加最大重试次数。

</details>

**知识点：**原子操作与无锁（Atomics & Lock-Free）
