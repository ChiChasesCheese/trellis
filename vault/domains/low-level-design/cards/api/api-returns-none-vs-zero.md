---
id: api-returns-none-vs-zero
node: api.returns
type: qa
step: 2
---
## Q
`total_paid(account_id)` 对“账户存在但从没付过款”和“账户根本不存在”应该分别返回什么？实现里 SQL 的 `SUM` 会怎样干扰这个区分？

## A
**零是一个答案，`None` 是没有答案，两者不能混**

- **存在但没有付款**：`0`。这是个确定的值，调用方可以直接累加；
- **账户不存在**：`None`（或抛 `NotFound`，合同里选一个）。把它也返回 `0` 会让拼错 id 的调用方得到“余额为零”；
- **SQL 的陷阱**：空集上的 `SUM` 是 `NULL`，到 Python 里就是 `None`，于是“没付款”被误写成“不存在”；
- **补法**：先查账户存不存在，再用 `COALESCE(SUM(...), 0)` 把“有账户没付款”落成 `0`。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("create table acct(id); create table pay(acct, amt);"
                 "insert into acct values (1);")
print(db.execute("select sum(amt) from pay where acct = 1").fetchone())   # (None,)

def total_paid(i: int) -> int | None:
    if db.execute("select 1 from acct where id = ?", (i,)).fetchone() is None:
        return None                                  # 不存在
    return db.execute("select coalesce(sum(amt), 0) from pay where acct = ?", (i,)).fetchone()[0]

print(total_paid(1), total_paid(9))     # 0 None
```

<details class="pt"><summary>延伸</summary>

`None` 与 `0` 都是假值，调用方写 `if not total:` 会把两者混在一起。返回类型是 `int | None` 时，合同要写明调用方应该用 `is None` 判断。

</details>

**知识点：**返回值设计（Return Values）
