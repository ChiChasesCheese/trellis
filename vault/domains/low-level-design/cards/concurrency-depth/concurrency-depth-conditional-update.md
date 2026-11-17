---
id: concurrency-depth-conditional-update
node: concurrency-depth.compound-actions
type: qa
step: 6
---
## Q
放款服务有多个实例（或多个进程），两个请求同时放同一笔 `pending` 贷款。先 `SELECT` 状态、再 `UPDATE`，为什么不行？进程内的 `threading.Lock` 能救吗？

## A
**检查和修改写进同一条带条件的 UPDATE，看 rowcount**

- **先查后改**：两个连接都查到 `pending`，都执行了 `UPDATE`，两个调用方都以为自己放款成功；
- **实测（3.11，8 个线程各开一个连接，文件库，100 轮）**：先查后改在 88/100 轮出现不止一个赢家（`sqlite3` 执行时释放 GIL，所以默认间隔下就会出现）；带条件 UPDATE 是 0/100；
- **锁救不了**：`threading.Lock` 只在一个进程里有效，别的进程或实例看不到它；裁决要放在大家共享的存储里；
- **做法**：`UPDATE … SET state='active' WHERE id=? AND state='pending'`，`rowcount == 1` 才算抢到，0 就是别人先了或状态不对；
- **同理**：扣库存写 `WHERE qty >= n`，一次性验证码写条件 `DELETE`，创建写唯一约束并接住 `IntegrityError`。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE loans(id INTEGER PRIMARY KEY, state TEXT)")
db.execute("INSERT INTO loans VALUES (1, 'pending')")

def disburse(loan_id) -> bool:
    cur = db.execute(
        "UPDATE loans SET state='active' WHERE id=? AND state='pending'",
        (loan_id,))
    return cur.rowcount == 1                 # 只有一个调用方看到 1

print(disburse(1), disburse(1))              # True False
```

<details class="pt"><summary>延伸</summary>

条件 UPDATE 是数据库版的比较并交换（compare-and-swap），把版本号加进条件（`AND ver=?`），读到的值和版本一起比对，就是乐观并发的完整形式。

</details>

**知识点：**复合操作（Compound Actions）
