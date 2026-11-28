---
id: hi-pt-credit-token-balance-11-revoke
node: qb.lld.credit-token-balance.points
type: qa
step: 11
---
## Q
**额度账本 · 作废额度包**｜加分 · 出自：额度账本 › 逐步扩展 2

要支持作废一个额度包：从某一刻起它剩余的额度失效，已经扣掉的不追回。怎么在现有设计里加？

## A
**做法。** 作废等价于把到期时间提前到 `at`：`replace` 出新的包，复用 `_commit` 的"副本重放、通过再提交"，会让某笔已有扣费凑不够就拒绝。

```python
# 换上"提前到 at 到期"的新包，其余不变；_commit 重放不通过就拒绝
self._commit(grants={**self._grants, grant_id: replace(grant, expires_at=at)})
```
**边界。** 已更早失效则什么都不做；`at <= 发放时间` 抛 `ValueError`；不认识的包抛 `UnknownGrantError`。
