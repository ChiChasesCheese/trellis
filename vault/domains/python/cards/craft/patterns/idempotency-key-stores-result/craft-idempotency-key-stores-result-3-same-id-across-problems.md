---
id: craft-idempotency-key-stores-result-3-same-id-across-problems
node: craft.patterns.idempotency-key-stores-result
type: qa
step: 3
---
## Q
**幂等键存结果 · 账本、计费、额度里同一种「同 ID 同内容」**｜模式

账本的分录、云计费的用量记录、额度系统的发放，都可能被重复投递（至少一次，at-least-once）。它们各自怎么判重？存下来的「结果」是什么，三者有什么不同？

## A
**要点。** 都用一个业务 ID 做键：没见过就写入；见过且内容完全相同就当成功地「什么都不做」；见过但内容不同就抛冲突。变的只是「返回什么」。

```python
# double-entry-ledger.post
if (seq := self._by_id.get(entry.id)) is not None:
    if self._journal[seq - 1] != entry:
        raise ConflictError(f"分录 {entry.id} 被复用但内容不同")
    return seq                          # 结果 = 原来的序号

# amz-aws-billing.add
old = self._records.get(record.usage_id)
if old is None:
    self._records[record.usage_id] = record
    return True
if old != record:
    raise InvalidUsage(f"usage_id {record.usage_id} 的内容与之前不同")
self._duplicates += 1
return False                            # 结果 = 「这次是重复」

# credit-token-balance.grant
old = self._grants.get(grant_id)
if old is not None:
    if old != new:
        raise ConflictError(...)
    return                              # 结果 = 无
```

判重所以便宜，因为数据对象是冻结的值对象：`old != new` 一个运算符就完成「内容是否相同」。

**见于。** idempotent-transfer、digital-wallet、double-entry-ledger、notification-service、amz-aws-billing、credit-token-balance。

**信号。** 消息或请求带有调用方生成的 ID；上游会重试或至少一次投递；「执行两次」会造成金额、库存、通知的重复。
