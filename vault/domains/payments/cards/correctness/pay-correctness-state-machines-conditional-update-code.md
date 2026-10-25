---
id: pay-correctness-state-machines-conditional-update-code
node: correctness.state-machines
type: qa
step: 3
---
## Q
怎么用条件更新（compare-and-set）在数据库里实现状态转移，保证并发或乱序的事件下状态只能合法前进？

## A
思路：先查转移表确认 A → B 合法，再用 `UPDATE ... WHERE id = ? AND state = A`，**影响行数为 1 才算转移成功**。数据库的行锁让并发请求排队，后到的发现状态已变，影响行数为 0。

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("create table pay(id int primary key, state text)"); db.execute("insert into pay values (1,'AUTHORIZED')")
LEGAL = {"AUTHORIZED": {"CAPTURED", "VOIDED"}, "CAPTURED": {"REFUNDED"}}
def move(pid: int, src: str, dst: str) -> bool:
    if dst not in LEGAL.get(src, set()): return False
    return db.execute("update pay set state=? where id=? and state=?", (dst, pid, src)).rowcount == 1
print(move(1, "AUTHORIZED", "CAPTURED"))   # first writer wins
print(move(1, "AUTHORIZED", "VOIDED"))     # late/concurrent writer: state already moved
print(move(1, "CAPTURED", "AUTHORIZED"))   # illegal backward move
print(db.execute("select state from pay").fetchone())
```

实际输出：

```
True
False
False
('CAPTURED',)
```

**解读**
1. 第一次转移成功，状态变 CAPTURED。
2. 并发或晚到的 `AUTHORIZED → VOIDED`：条件 `state = 'AUTHORIZED'` 已不成立，影响行数为 0，返回 False。
3. 非法的回退被转移表拒绝。

**生产版本要补**：转移成功时，在同一事务内写状态历史、分录和 outbox 事件；返回 False 时区分"已经在目标状态（幂等重复）"与"冲突或非法（需要告警）"。
