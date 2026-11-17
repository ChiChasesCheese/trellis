---
id: api-error-contract-retryable
node: api.error-contract
type: qa
step: 5
---
## Q
客户端收到错误后怎么决定要不要重试？服务端该在合同里告诉它什么，才不会出现“同一个坏请求被重试三十次”或者“一次超时就放弃”？

## A
**重试由错误类别决定，类别写进合同**

- **4xx：不重试**：请求本身有问题，同样的请求再发一次得到同样的错误，只会浪费配额；
- **409 要看情形**：同键异请求这类冲突，重试没用；“版本已变”这类，客户端重读再发才有意义；
- **5xx、超时、被限流（429）：可重试**，带退避（backoff）和上限，并且遵守服务给的等待时间；
- **可重试的前提是幂等**：写操作要带幂等键，否则超时后的重试可能把钱扣两次；
- **合同里给一个字段**：每个错误码标明 `retryable`，客户端查表，而不是猜状态码。

```python
RETRYABLE = {"rate_limited": True, "upstream_timeout": True,
             "invalid_amount": False, "idempotency_conflict": False}

def should_retry(code: str, attempt: int, limit: int = 3) -> bool:
    # 未知的码默认不重试：宁可失败得明白
    return RETRYABLE.get(code, False) and attempt < limit

print(should_retry("rate_limited", 1), should_retry("invalid_amount", 1), should_retry("new_code", 1))
```

<details class="pt"><summary>延伸</summary>

被限流的响应应该带“多久以后再来”（例如 `Retry-After` 头或 `reset_after_ms` 字段）。客户端自己算退避，所有客户端会在同一时刻一起回来；加随机抖动（jitter）把它们错开。

</details>

**知识点：**接口的错误契约（Error Contract）
