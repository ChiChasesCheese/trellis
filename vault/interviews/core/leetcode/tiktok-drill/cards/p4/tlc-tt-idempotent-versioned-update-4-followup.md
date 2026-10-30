---
id: tlc-tt-idempotent-versioned-update-4-followup
node: p4.tt-idempotent-versioned-update
type: qa
step: 4
---
## Q
**幂等、带版本号的数据更新**｜追问

`VersionedStore` 写完后，面试官接着问：（1）`request_id` 表会无限增长，怎么办？（2）多线程并发调用 `update`，锁怎么加？（3）落到真实数据库，怎样用一条 SQL 完成比较并更新？

## A
1. **限制幂等表。** 重试只发生在一个有限窗口内（如 24 小时），只保留最近 `ttl` 秒的记录。写入时间单调递增，`OrderedDict` 的插入顺序就是时间顺序，从最旧的一端淘汰，均摊 `O(1)`。记录过期后迟到的重试由版本号兜底：只会冲突，不会重复写。

```python
from collections import OrderedDict


class IdempotencyTable:
    def __init__(self, ttl: float) -> None:
        self.ttl = ttl
        self.items: OrderedDict[str, tuple[float, tuple[bool, int]]] = OrderedDict()

    def get(self, request_id: str, now: float) -> tuple[bool, int] | None:
        while self.items and next(iter(self.items.values()))[0] <= now - self.ttl:
            self.items.popitem(last=False)                # 淘汰最旧的记录
        hit = self.items.get(request_id)
        return hit[1] if hit else None

    def put(self, request_id: str, result: tuple[bool, int], now: float) -> None:
        self.items[request_id] = (now, result)
```

   运行（`ttl = 60`）：`put("r1", …, 0)`、`put("r2", …, 30)` 后，`get("r1", 59)` 命中，`get("r1", 60)` → `None`。

2. **加锁。** 「查幂等表 → 读版本 → 写入 → 记结果」必须在**同一个**临界区里：`with self.lock:` 包住整个 `update`。只锁写入不锁查表时，同一 `request_id` 的两个并发重试都会查不到记录，各自执行，一个成功一个冲突，同一请求得到两种结果。要提高并发可以按 `hash(key)` 分段加锁（锁分段，lock striping）：不同 key 的更新互不阻塞；前提是同一个 `request_id` 的重试总是带同一个 key，幂等表也随 key 分段存放。
3. **SQL。** 比较和更新合成一条语句，由数据库保证原子性：

```sql
UPDATE kv SET value = :v, version = version + 1
WHERE key = :k AND version = :expected;      -- 影响行数 1 = 成功，0 = 冲突
```

   幂等表 `idem(request_id PRIMARY KEY, result)` 与这条 `UPDATE` 放进同一个事务：先 `INSERT` 幂等记录，主键冲突就说明是重试，读出旧结果返回。

**Python 提醒**：`threading.Lock` 不可重入，`update` 内部如果调用了同样加锁的 `get`，会自己把自己锁死；要么内部读 `self.data` 不加锁，要么用 `RLock`。
