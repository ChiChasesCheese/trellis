---
id: hi-c-sd-multi-step-processes-b04-idempotency-key-code
node: sd.patterns.multi-step-processes.beyond
type: qa
step: 4
---
## Q
**多步流程 · 幂等键的最小实现**｜拓展 · 加分

把"IN_PROGRESS 再 COMPLETED"的幂等保护写成一段代码，关键在哪一步必须是原子的？

## A
```python
import sqlite3


def run_once(db: sqlite3.Connection, key: str, action) -> str:
    # 关键：认领幂等键靠主键唯一约束，一条 INSERT 完成"检查并设置"，不是先 SELECT 再 INSERT
    try:
        db.execute("INSERT INTO idem(key, state) VALUES (?, 'IN_PROGRESS')", (key,))
        db.commit()
    except sqlite3.IntegrityError:
        (state,) = db.execute("SELECT state FROM idem WHERE key = ?", (key,)).fetchone()
        return "skipped" if state == "COMPLETED" else "needs-reconcile"
    action()  # 副作用：崩溃发生在这里之后、下一行之前，重试会看到 IN_PROGRESS
    db.execute("UPDATE idem SET state = 'COMPLETED' WHERE key = ?", (key,))
    db.commit()
    return "done"
```
- **原子点：** 用唯一约束把检查和占位合成一条语句；先查再写会让两个重试者同时通过。
- **IN_PROGRESS 不能盲目重发：** 要对账，向下游查这个键的动作是否发生过；能把键传给下游去重最好。
- **何时不用：** 下游本身支持幂等键（如支付接口）时直接传键，不必自己再记一份状态。
