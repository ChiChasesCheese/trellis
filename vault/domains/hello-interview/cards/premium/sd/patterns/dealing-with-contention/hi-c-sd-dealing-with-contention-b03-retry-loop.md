---
id: hi-c-sd-dealing-with-contention-b03-retry-loop
node: sd.patterns.dealing-with-contention.beyond
type: qa
step: 3
---
## Q
**处理竞争 · 乐观重试要怎么写**｜拓展 · 加分

乐观并发和 SERIALIZABLE 都要求应用重试，一个正确的重试循环要注意什么？

## A
```python
import random
import sqlite3
import time


def buy(conn: sqlite3.Connection, concert: str, retries: int = 5) -> bool:
    for attempt in range(retries):
        # 每次重试都重新读：用上一轮读到的旧版本再写只会再失败一次
        seats, ver = conn.execute(
            "SELECT available_seats, version FROM concerts WHERE id = ?", (concert,)
        ).fetchone()
        if seats <= 0:
            return False  # 业务上售罄，重试没有意义
        cur = conn.execute(
            "UPDATE concerts SET available_seats = available_seats - 1, version = version + 1 "
            "WHERE id = ? AND version = ?",
            (concert, ver),
        )
        if cur.rowcount == 1:  # 受影响行数是唯一的成败信号
            conn.commit()
            return True
        conn.rollback()
        # 带抖动的退避，避免一批失败者同时重试再次互撞
        time.sleep(random.uniform(0, 0.01 * 2**attempt))
    return False
```
- **整个事务重来：** 重试要重新读再算，不能只重发那条 UPDATE。
- **区分失败原因：** 业务失败（售罄）直接返回；并发失败（0 行、序列化错误 40001、死锁 40P01）才重试。
- **有上限加抖动：** 无上限会在热点上形成重试风暴，反而让吞吐更低。
