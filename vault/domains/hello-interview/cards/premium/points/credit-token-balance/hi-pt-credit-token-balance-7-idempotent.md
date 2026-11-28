---
id: hi-pt-credit-token-balance-7-idempotent
node: qb.lld.credit-token-balance.points
type: qa
step: 7
---
## Q
**额度账本 · 幂等与冲突**｜追问 · 出自：额度账本 › 逐步扩展 1

网络重试让同一个 `charge_id` 到达两次。怎么处理？参数不同呢？被拒绝的扣费算"已见过"吗？

## A
**做法。** 同 id 同参数：返回第一次的分配，不再扣第二次；参数不同：抛 `ConflictError`。

```python
old = self._charges.get(charge_id)    # 该 charge_id 之前记过的扣费事件
if old is not None:
    if old != new:                    # new 是本次请求构造的事件，冻结数据类按字段比较
        raise ConflictError(f"charge {charge_id} already exists with different terms")
    return self.allocations(charge_id)
```
**被拒绝的。** 不入账，补了额度之后可以用同一个 id 重试。**易错。** 只按 id 去重：同 id 不同金额被悄悄忽略。
