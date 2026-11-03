---
id: craft-replace-for-state-change-6-scales-optimistic-lock
node: craft.idioms.replace-for-state-change
type: qa
step: 6
---
## Q
**用 replace 表达状态变化 · 从锁内整条替换到数据库的版本号乐观锁**｜写法

进程内，`hold` 在一把锁里检查再替换。多台服务器同时更新同一行数据库记录时，没有进程内的锁，同样的「检查—替换」怎么做到没有缝隙？

## A
**要点。** 把「检查旧值」放进写入语句本身：`UPDATE ... WHERE id = ? AND version = ?`。读到记录时带上版本号，写回时只有版本还是读到的那一版才更新，并把版本加一；`rowcount == 0` 说明有人先改了，调用方重读再决定。这就是乐观并发控制（optimistic concurrency control）：不加锁，冲突时重试。

```python
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE res (id TEXT PRIMARY KEY, status TEXT, version INTEGER)")
db.execute("INSERT INTO res VALUES ('r1', 'active', 1)")
db.commit()

@dataclass(frozen=True)
class Res:
    id: str
    status: str
    version: int

def load(rid: str) -> Res:
    return Res(*db.execute("SELECT id, status, version FROM res WHERE id=?", (rid,)).fetchone())

def save(old: Res, new: Res) -> bool:
    # 整行替换 + 比较并交换: 只有版本还是读到的那一版才写入
    cur = db.execute("UPDATE res SET status=?, version=? WHERE id=? AND version=?",
                     (new.status, old.version + 1, old.id, old.version))
    db.commit()
    return cur.rowcount == 1

a, b = load("r1"), load("r1")                       # 两个请求读到同一版本
print("A 确认:", save(a, replace(a, status="confirmed")))
print("B 取消:", save(b, replace(b, status="cancelled")), "<- 版本已变, 写入失败, B 重读再决定")
print("最终:", load("r1"))
```

实际输出：

```
A 确认: True
B 取消: False <- 版本已变, 写入失败, B 重读再决定
最终: Res(id='r1', status='confirmed', version=2)
```

**变化。** 进程内是「持锁，读、比较、整条替换」；数据库是「读，带版本比较并写」，原子性由数据库的单条语句提供，不需要应用持有锁。令牌（`held_by`）与版本号是同一件事的两种形态：写操作必须证明自己基于最新的状态。

**代价。** 乐观锁在冲突少时便宜，冲突频繁时大量重试，浪费甚至活锁；热点行（秒杀库存）更适合悲观锁（`SELECT ... FOR UPDATE`）或把冲突变成队列。重试逻辑还必须保证业务操作幂等（见幂等键）。

**信号。** 多个写者可能同时基于同一份旧状态更新同一条记录。
