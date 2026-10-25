---
id: pay-correctness-idempotency-store-code
node: correctness.idempotency
type: qa
step: 3
---
## Q
服务端怎么用数据库唯一约束实现幂等存储？请用一段代码演示同键同结果、同键不同内容的行为。

## A
核心：幂等键的主键约束 + 业务写入放在**同一个事务**里。第一次插入成功才执行业务；撞主键说明是重复请求，读出之前的结果。

```python
import sqlite3, json
db = sqlite3.connect(":memory:")
db.execute("create table idem(k text primary key, req_hash text, resp text)")
def charge(key: str, req_hash: str, amount: int) -> dict:
    try:
        with db:
            db.execute("insert into idem(k, req_hash) values (?,?)", (key, req_hash))
            resp = {"payment": "p_1", "amount": amount}      # business write, same transaction
            db.execute("update idem set resp=? where k=?", (json.dumps(resp), key))
        return resp
    except sqlite3.IntegrityError:
        h, r = db.execute("select req_hash, resp from idem where k=?", (key,)).fetchone()
        return {"error": 422} if h != req_hash else json.loads(r)
print(charge("k1", "h1", 5000)); print(charge("k1", "h1", 5000)); print(charge("k1", "h2", 9000))
```

实际输出：

```
{'payment': 'p_1', 'amount': 5000}
{'payment': 'p_1', 'amount': 5000}
{'error': 422}
```

**解读**
1. 第一次：插入键成功，执行业务，保存响应。
2. 第二次（同键同内容）：撞主键，回放第一次的结果，业务不再执行，金额仍是 5000。
3. 第三次（同键不同内容）：请求指纹不同，返回 422。

**生产版本还要补**：状态字段（processing / done）与锁超时（处理中崩溃的请求能被接管），并发的第二个请求读到 processing 时返回 409。
