---
id: pay-platform-routing-failover-code
node: platform.routing-failover
type: qa
step: 5
---
## Q
请写出渠道故障切换时的决策函数：什么情况下可以安全地换到渠道 B，什么情况下必须先查询渠道 A，不能换？

## A
```python
def next_step(attempt: str, psp_says: str | None) -> str:
    """What to do after the call to PSP A ends in `attempt`."""
    if attempt == "declined_hard":
        return "stop: show failure"
    if attempt == "failed_clean":          # PSP A confirmed nothing was charged
        return "route to PSP B (new attempt, same payment)"
    if attempt == "timeout":
        if psp_says is None:
            return "query PSP A by reference; do NOT call B"
        return {"succeeded": "mark succeeded", "none": "route to PSP B"}[psp_says]
    return "unknown"

for a, q in [("failed_clean", None), ("timeout", None), ("timeout", "succeeded"), ("timeout", "none")]:
    print(a, q, "->", next_step(a, q))
```
实际输出：
```
failed_clean None -> route to PSP B (new attempt, same payment)
timeout None -> query PSP A by reference; do NOT call B
timeout succeeded -> mark succeeded
timeout none -> route to PSP B
```
解读：
- `failed_clean`：渠道 A 明确返回"未扣款的失败"，可以换渠道 B，创建新尝试，仍属同一个支付单。
- `timeout` 且还没查询：结果未知，A 可能已经扣了款。必须先用保存好的引用号去查 A，**不能调用 B**。
- 查询后 A 说成功：直接标记成功，不再调用 B。
- 查询后 A 说没有这笔：这时才安全地换 B。
- 硬拒绝：不换，直接结束。

**设计要点**：切换的前提是**确认原渠道没有扣款**。"没有成功响应"不等于"没有扣款"。所以每次尝试在发出前就持久化引用号，才能在超时后查询。
