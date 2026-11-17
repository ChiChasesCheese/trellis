---
id: errors-cleanup-transaction
node: errors.cleanup
type: qa
step: 5
---
## Q
预约服务一次成功的操作要同时改预约状态、剩余名额、审计记录三处。怎么保证三处同成同败？`with conn:` 做了什么，又没做什么？

## A
**三处写入放进同一个事务，退出时一次提交或回滚**

- **`with conn:` 成功就 `commit`，抛异常就 `rollback`**：异常回滚之后继续往上传，调用方照样知道失败；
- **它不关闭连接**：`sqlite3` 的 `with` 只管事务，连接要另外 `close()`（或用 `contextlib.closing`）；
- **只在最后提交一次**：写完状态就 `commit`、再写名额，中间崩溃就是半截状态；
- **返回之前已经提交**：函数返回时别的连接就能读到，否则第二个实例看到旧数据；
- **用测试逼出失败路径**：给审计表加一个恒假的 `CHECK`，让第三步必然失败，断言前两步的改动都不见了。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("create table t (id integer primary key)")
try:
    with db:                                          # 成功提交，异常回滚
        db.execute("insert into t values (1)")
        db.execute("insert into t values (1)")        # 主键冲突
except sqlite3.IntegrityError:
    print(db.execute("select count(*) from t").fetchone())   # (0,)：第一条也撤销了
```

<details class="pt"><summary>延伸</summary>

`sqlite3` 的默认模式只在 `INSERT/UPDATE/DELETE` 前隐式开事务；建表等语句不在事务里。要一组语句整体原子，别靠隐式行为：在 `with` 里把它们都写在一起，或者显式 `BEGIN`。

</details>

**知识点：**所有路径上的清理（Cleanup on Every Path）
