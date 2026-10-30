---
id: tlc-tt-idempotent-versioned-update-0-whole
node: p4.tt-idempotent-versioned-update
type: qa
---
## Q
**幂等、带版本号的数据更新**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-09（面试记录）

实现内存键值存储 `VersionedStore`：
- `update(request_id, key, value, expected_version)`：只有当 `key` 的当前版本等于 `expected_version` 时才写入，版本加 1，返回 `(True, 新版本)`；版本不对就不写，返回 `(False, 当前版本)`（冲突）。
- 同一个 `request_id` 重复调用（客户端超时后重试）时不能重复写，要**原样返回第一次的结果**。
- `get(key)` 返回 `(value, version)`；不存在的 key 返回 `(None, 0)`，所以新建 key 时 `expected_version = 0`。

调用总数 `<= 10^5`。例：`update("r1","a","x",0)` → `(True, 1)`；重试 `update("r1","a","x",0)` → `(True, 1)`（不再写）；`update("r2","a","y",0)` → `(False, 1)`；`update("r3","a","y",1)` → `(True, 2)`；`get("a")` → `("y", 2)`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两层保护：版本号做**乐观并发控制**（optimistic concurrency control，比较并更新 compare-and-set，CAS），挡住基于旧数据的写；`request_id → 第一次结果` 的表做**幂等**（idempotency），让重试直接拿回原结果。顺序固定：先查幂等表，再做比较并更新，最后把结果（无论成功还是冲突）记进表里。

**识别。** 「只有当前版本等于期望版本才写」= CAS，防的是两个客户端并发「读-改-写」时后写覆盖先写（丢失更新，lost update）。「超时重试不能重复写、原样返回」= 幂等键，防的是**同一个**客户端的重复请求。两个机制解决的是不同问题，缺一不可。

**推导。** 只有 CAS 而没有幂等表：第一次请求其实写成功了，只是响应丢了；客户端用同样的参数重试，此时版本已经是 `expected + 1`，返回冲突，客户端误以为写失败。只有幂等表而没有 CAS：两个客户端都读到版本 1，各自写入，后写的覆盖先写的。所以两者都要；幂等检查必须放在 CAS 之前，否则重试仍会先去比较版本。冲突的结果也要记住：第一次冲突的请求，重试时即使版本恰好对上了，也必须返回冲突，否则同一请求出现两种结果。

```python
class VersionedStore:
    def __init__(self) -> None:
        self.data: dict[str, tuple[str, int]] = {}           # key -> (value, version)
        self.done: dict[str, tuple[bool, int]] = {}          # request_id -> 第一次的结果

    def get(self, key: str) -> tuple[str | None, int]:
        return self.data.get(key, (None, 0))                 # 不存在的 key 版本为 0

    def update(self, request_id: str, key: str, value: str, expected_version: int) -> tuple[bool, int]:
        """返回 (是否写入, 版本)：成功时是新版本，冲突时是当前版本。"""
        if (prev := self.done.get(request_id)) is not None:
            return prev                                      # 重试：原样返回，不再写
        _, version = self.get(key)
        if version == expected_version:                      # 比较并更新（compare-and-set）
            self.data[key] = (value, version + 1)
            result = (True, version + 1)
        else:
            result = (False, version)
        self.done[request_id] = result                       # 冲突结果也要记住
        return result
```

运行：按例子顺序依次得到 `(True, 1)`、`(True, 1)`、`(False, 1)`、`(True, 2)`；`get("a")` → `('y', 2)`，`get("b")` → `(None, 0)`；此后重试 `update("r2","a","y",2)`（版本已经对上）→ 仍然 `(False, 1)`。

**复杂度。** 每次 `update` / `get` 都是 `O(1)`（两次字典查找加一次写）；空间 `O(key 数 + request_id 数)`。

**易错点。**
- 没有幂等表：`update("r1","a","x",0)` 成功后客户端重试，得到 `(False, 1)`，客户端以为失败（正确是 `(True, 1)`）。
- 只缓存成功结果：`r2` 第一次冲突得到 `(False, 1)`，之后带着同一个 `request_id`、`expected_version = 2` 重试，会真的写入并返回 `(True, 3)`，同一个请求出现两种结果。
- 冲突时返回 `(False, expected_version)`：客户端拿不到当前版本，只能再 `get` 一次；返回当前版本可以直接用来重新读-改-写。

**追问。**
- `request_id` 表无限增长：只保留最近 `T` 秒（重试窗口）的记录，按时间顺序从最旧的一端淘汰；过期之后的重试由 CAS 兜底，只会冲突，不会重复写。
- 多线程：「查幂等表 → CAS → 记结果」必须在同一个锁里完成；锁粒度可以细化到按 key 分段加锁。
- 落到数据库：`UPDATE kv SET value = ?, version = version + 1 WHERE key = ? AND version = ?`，影响行数 1 为成功、0 为冲突；幂等表以 `request_id` 为主键，和更新放在同一个事务里。

**同模式。** LC 981 基于时间的键值存储、LC 146 LRU 缓存（设计类：字典 + 不变量）、LC 1146 快照数组（版本号）、LC 2502 设计内存分配器。
