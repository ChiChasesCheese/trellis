---
id: craft-bisect-sorted-lists-5-across-problems
node: craft.idioms.bisect-sorted-lists
type: qa
step: 5
---
## Q
**bisect 与有序列表 · 账本历史、计费版本、人数时间线里同一个 floor**｜写法

账本按序号取历史余额，计费引擎按交易时间取生效的规则版本，人数追踪器按时间取当时人数，云计费按时间取价格版本。四处的代码有什么共同点？

## A
**要点。** 四处都是同一个问题：**一个有序的「变化点」列表，查询某个点上的值就是最后一个不晚于它的变化**。变的只是变化点的含义（分录序号、生效时间、事件时间）和列表里存什么（余额、版本、人数）。

```python
# double-entry-ledger.balance_at：序号严格递增，列表天然有序
i = bisect_right(hist, seq, key=lambda line: line.seq)
return hist[i - 1].balance_after if i else 0

# billing-tax-engine.quote：恰好等于生效时间属于新版本
v = bisect_right(sched.starts, txn.ts)          # 生效版本的个数，也就是版本号
if v == 0: raise NoActiveRules(...)

# amz-occupancy-tracker.count_at：最后一个 time <= ts 的事件之后的前缀和
i = bisect.bisect_right(self._times, ts) - 1
return self._counts[i] if i >= 0 else 0

# amz-aws-billing.version_at：key= 直接在版本列表上二分
i = bisect_right(versions, at, key=lambda v: v.effective_from) - 1
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

四处都有「没有这样的变化点」的分支：余额得 0，规则版本抛 `NoActiveRules`，人数得 0，价格抛 `UnknownServiceError`。边界条件（`i == 0`、`-1`）比二分本身更容易出错。另外，订单簿的价位表也有序，取最优价就是取端点；最近门店索引的 floor / ceiling 用 `bisect_right / bisect_left`。

**见于。** double-entry-ledger、billing-tax-engine、amz-occupancy-tracker、amz-aws-billing、stock-brokerage、amz-closest-store、car-rental。

**信号。** 需求里有「在某个时间点生效的」「当时的余额」「最近的小于等于的」「历史快照查询」。
