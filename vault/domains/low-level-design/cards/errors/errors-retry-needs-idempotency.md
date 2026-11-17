---
id: errors-retry-needs-idempotency
node: errors.retry
type: qa
step: 4
---
## Q
扣款请求超时了，客户端重试，为什么可能扣两次？重试之前，服务端必须具备什么？

## A
**超时不等于失败，重试要靠幂等键**

- **超时只说明没收到回复**：服务端可能已经扣了款，只是响应丢了，客户端无从知道；
- **天然幂等的操作随便重试**：读取、把库存设成绝对值 7、按 id 删除；
- **增量操作不幂等**：库存减 3、扣款 20，重发一次就多做一次；
- **给操作一个键**（付款号、请求号）：服务端按键记录结果，同键再来直接回放，不再执行；
- **登记和业务写入要同一个事务，键上加唯一约束**：否则两个并发的重试仍然各做一次。

```python
acct = {"balance": 100}
done: dict[str, int] = {}

def charge(key: str, amount: int) -> int:
    if key not in done:                  # 同键第二次：不再扣
        acct["balance"] -= amount
        done[key] = acct["balance"]
    return done[key]

print(charge("p1", 20), charge("p1", 20))   # 80 80：超时后重发，只扣一次
print(charge("p2", 20))                     # 60：新键才是新的一笔
```

<details class="pt"><summary>延伸</summary>

这段代码在多线程下仍有“检查后再动手”的缝隙：两个线程同时发现 `key not in done`。真正的实现把“键插入”和“扣款”放进同一个数据库事务，靠唯一约束让第二个失败。

</details>

**知识点：**重试与退避（Retry & Backoff）
