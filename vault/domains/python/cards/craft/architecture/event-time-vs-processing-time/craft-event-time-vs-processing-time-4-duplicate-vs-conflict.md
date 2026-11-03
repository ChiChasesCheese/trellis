---
id: craft-event-time-vs-processing-time-4-duplicate-vs-conflict
node: craft.architecture.event-time-vs-processing-time
type: qa
step: 4
---
## Q
**事件时间 vs 处理时间 · 重复上报的事件，什么时候该忽略，什么时候该报错**｜架构

配送员的 App 在弱网下会重复上报「已取餐」。一种是把同一条原样再发一次（至少一次投递的重复），另一种是同一个订单的「已取餐」这次带了不同的时间。两种情况服务该怎么处理？

## A
**要点。** 完全相同的重复：忽略，当作成功，调用方重试是安全的，状态不变。同类事件但内容不同：报冲突错误，不能悄悄覆盖，也不能悄悄忽略，因为这说明上游有 bug 或数据被改过，需要人来看。判据和「幂等键存结果」同源：同一个标识 + 同内容 = 没发生过第二次；同标识 + 不同内容 = 错误。

```python
class Conflict(Exception): ...

events: dict[str, dict[str, int]] = {}

def record(delivery: str, kind: str, at: int) -> str:
    seen = events.setdefault(delivery, {})
    if kind in seen:
        if seen[kind] == at:
            return "重复上报：忽略"
        raise Conflict(f"{kind} 已记录为 {seen[kind]}，这次是 {at}")
    seen[kind] = at
    return "记录"

print(record("d1", "PICKED_UP", 10))
print(record("d1", "PICKED_UP", 10))               # 至少一次投递的重复
try:
    record("d1", "PICKED_UP", 12)                  # 同类事件，不同时间
except Conflict as e:
    print("冲突:", e)
```

同一个订单先记 `PICKED_UP@10`，再记一次同样的，再记 `PICKED_UP@12`，实际输出：

```
记录
重复上报：忽略
冲突: PICKED_UP 已记录为 10，这次是 12
```

**为什么。** 人流统计里对「与上一事件完全相同」的重复同样返回 `False`（被忽略，不是错误），而时间倒流抛 `OutOfOrder`；每种异常情况的名字都不同，上游才知道是重试成功还是要改代码。

**代价。** 判重需要保存每个事件的标识和内容（或其摘要），保留多久、怎么清理要有明确的策略；事后确实要更正某个时间，应走专门的「更正」操作，而不是重新上报。
