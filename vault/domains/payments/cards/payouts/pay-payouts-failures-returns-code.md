---
id: pay-payouts-failures-returns-code
node: payouts.failures-returns
type: qa
step: 5
---
## Q
请写出打款单状态转移的守卫（state transition guard）：只允许合法转移，并用版本号做条件更新，使并发或重复的回调不会把状态改乱。

## A
```python
ALLOWED = {"created": {"submitted"}, "submitted": {"paid", "failed"}, "paid": {"returned"}}

def move(row: dict, new: str, version: int) -> bool:
    """Conditional update: only if version matches and the move is legal."""
    if row["version"] != version or new not in ALLOWED.get(row["state"], set()):
        return False
    row["state"], row["version"] = new, version + 1
    return True

p = {"state": "created", "version": 0}
print(move(p, "submitted", 0), move(p, "paid", 1), move(p, "paid", 1))
print(move(p, "failed", 2), move(p, "returned", 2), p)
```
实际输出：
```
True True False
False True {'state': 'returned', 'version': 3}
```
逐项解读：
- 第一行：`created → submitted` 成功，`submitted → paid` 成功，第二次重复的 `paid`（版本号已变为 2）被拒绝，这就是重复回调被安全吞掉。
- 第二行：`paid → failed` 不合法，返回 False，状态不变；`paid → returned` 合法，成功，版本号变为 3。

**在数据库中**，等价于一条条件更新：`UPDATE payout SET state=?, version=version+1 WHERE id=? AND state=? AND version=?`，影响行数为 1 才算成功，为 0 说明被别的线程抢先或转移非法。

**设计意图**：`paid` 不是终态，它还能转到 `returned`，反映了退票晚到的现实。失败与退票是不同的转移，处理逻辑和账务动作也不同，把它们放进同一张转移表里，非法转移就会立刻暴露。
