---
id: errors-retry-at-least-once
node: errors.retry
type: qa
step: 6
---
## Q
新片上映要通知关注的用户：通知既要写数据库、又要发给下游。“先投递、再标记已发”，崩溃在两步之间会怎样？接收端为什么必须去重？

## A
**至少一次投递，接收端按键去重**

- **发件箱（outbox）**：业务数据和待发通知在同一个事务里写成两行，通知行先是 `pending`；
- **先投递，再标记**：崩在两步之间，重启后会再发一遍，宁可重复也不丢；
- **反过来先标记再投递**：崩了就永久丢一条，没人会发现；
- **所以是“至少一次”（at-least-once）**，做不到“恰好一次”，重复要由接收端消化；
- **去重键是业务含义**：（用户，电影 id），不是发送次数或时间。

```python
outbox = [{"user": "a", "movie": 7, "sent": False}]
inbox: set[tuple[str, int]] = set()

def pump(crash_before_mark: bool = False) -> None:
    for row in outbox:
        if not row["sent"]:
            inbox.add((row["user"], row["movie"]))   # 1 投递（接收端用集合去重）
            if crash_before_mark: raise RuntimeError("crash")
            row["sent"] = True                       # 2 标记

try: pump(crash_before_mark=True)
except RuntimeError: pass
pump()                                               # 重启后重发
print(len(inbox), outbox[0]["sent"])                 # 1 True：收到一条，没有重复
```

**知识点：**重试与退避（Retry & Backoff）
