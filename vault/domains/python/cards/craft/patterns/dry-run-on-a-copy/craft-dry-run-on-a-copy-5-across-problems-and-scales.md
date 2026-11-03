---
id: craft-dry-run-on-a-copy-5-across-problems-and-scales
node: craft.patterns.dry-run-on-a-copy
type: qa
step: 5
---
## Q
**在副本上试运行 · 等位预测、额度提交、棋局搜索、账单更正里的同一个动作**｜模式

这四个问题看起来毫无关联。它们共享的是什么？放大到数据库和发布系统，同一个思路叫什么？

## A
**要点。** 同一个动作：要回答「如果这样做会怎样」，就拿一份可丢弃的状态，跑与真实路径相同的函数，看结果；结果满意再对真身做一遍（或直接用候选状态替换）。差别只在于「看结果」看的是什么：一个数字、一次是否抛错、一个得分、一份差额。

```python
# restaurant-waitlist._simulate：看返回的等待时间，副本用完就丢
for w, table in _drain(queue, free, self._sizes, self._max_overtakes):   # queue / free 是复制品

# credit-token-balance：看有没有抛错，通过才替换
_replay(grants, charges)            # 用候选字典
self._grants, self._charges = grants, charges

# billing-tax-engine.reprice：看新旧差额，只返回有差的行
new = _totals(_run(_in_dependency_order(rules), txn, version))
old = _totals(previous)             # 旧各行不动，只追加调整行
```

**见于。** restaurant-waitlist（等位预测）、credit-token-balance（迟到事件提交）、connect-four（机器人搜索）、billing-tax-engine（更正后重算）。

**信号。** 需求里出现「预估」「先试一下」「会不会冲突」「如果……会怎样」「失败时原样不动」；或者你发现自己为同一条规则写了第二份。

**尺度对照。** 力扣没有直接对应。低层设计：一个纯函数加复制的状态。分布式系统：数据库事务里先做再回滚（`BEGIN … ROLLBACK`）、`kubectl apply --dry-run=server`（走完校验但不落盘）、影子流量（真实请求同时发给新版本，只比较不采用）。变化：单机副本很便宜；到了生产环境，「副本」要么是事务的隔离，要么是另一份基础设施，必须保证试运行没有副作用（不发邮件、不扣真钱），这是最容易被忽略的前提。
