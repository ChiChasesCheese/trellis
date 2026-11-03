---
id: craft-entity-vs-value-object-5-two-tables
node: craft.architecture.entity-vs-value-object
type: qa
step: 5
---
## Q
**实体 vs 值对象 · 数据库里「物理资产」与「库存占用」为什么是两张表**｜架构

订座系统落到数据库，一张 `seat` 表加一个 `booked_by` 列最省事，为什么实际系统几乎都拆成「座位」和「某班某座的库存」两张表？拆开之后，防超卖的约束写在哪里？

## A
**要点。** 对应领域驱动设计（DDD）里的值对象与实体/聚合：物理资产几乎不变，所有班次共用，是一张静态表；占用状态按（班次，座位）一行，是会变的库存表，同一班同一座位只能有一行由唯一约束保证。这样周一订座不会动周二，也不用在座位表上做会互相冲突的更新。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
-- 物理资产：几乎不变，所有班次共用（值）
CREATE TABLE seat (aircraft TEXT, seat_no TEXT, cabin TEXT, PRIMARY KEY (aircraft, seat_no));
-- 库存占用：每一班每个座位一行（实体的状态）
CREATE TABLE seat_inventory (
  flight_id TEXT, seat_no TEXT, booking TEXT,
  PRIMARY KEY (flight_id, seat_no)          -- 唯一约束：同一班同一座位只能被一个订单占
);
INSERT INTO seat VALUES ('A320', '12C', 'ECON');
""")
db.execute("INSERT INTO seat_inventory VALUES ('MU5100@07-01', '12C', 'B1')")
for flight in ("MU5100@07-01", "MU5100@07-02"):
    try:
        db.execute("INSERT INTO seat_inventory VALUES (?, '12C', 'B2')", (flight,))
        print(flight, "12C 订到")
    except sqlite3.IntegrityError:
        print(flight, "12C 已被占")
print("座位表仍是", db.execute("SELECT * FROM seat").fetchall())
```

先在 7 月 1 日那班把 12C 给订单 B1，再分别尝试在两个班次订 B2，用 SQLite 实际输出：

```
MU5100@07-01 12C 已被占
MU5100@07-02 12C 订到
座位表仍是 [('A320', '12C', 'ECON')]
```

**为什么。** 这时「谁抢到座位」由数据库的唯一约束裁决，和进程内「锁放在航班实例上」是同一个想法：竞争范围正好是（班次，座位）。

**代价。** 查「这班还剩多少空位」要把静态表和库存表连接起来，或者预先插入全部空座位行；用哪种取决于读多还是写多，不能凭感觉定。
