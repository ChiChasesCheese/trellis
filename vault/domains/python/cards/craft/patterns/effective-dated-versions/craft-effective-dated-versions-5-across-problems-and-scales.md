---
id: craft-effective-dated-versions-5-across-problems-and-scales
node: craft.patterns.effective-dated-versions
type: qa
step: 5
---
## Q
**生效时间版本 · 时间键值库、费率表、云账单、账本历史余额里的同一次二分**｜模式

Time Based Key-Value Store、手续费规则版本、云服务价格表、账本的历史余额，看起来是四个领域。它们共享什么？放大到数据库和配置系统，同一个想法有哪些名字？

## A
**要点。** 都是「按时间排序的只追加列表 + 一次 `bisect_right` 找出当时生效的那一项」。键是时间（或单调序号），值是当时的规则、价格或余额。

```python
# Time Based Key-Value Store（LeetCode）
i = bisect_right(self.ts[key], timestamp)
return self.vals[key][i - 1] if i else ""

# billing-tax-engine：版本号 = 个数
v = bisect_right(sched.starts, txn.ts)

# double-entry-ledger.balance_at：键是分录序号，值是当时的余额
i = bisect_right(hist, seq, key=lambda line: line.seq)
return hist[i - 1].balance_after if i else 0
```

**见于。** time-based-key-value-store、billing-tax-engine、amz-aws-billing、double-entry-ledger、amz-occupancy-tracker。

**不变的。** 左闭右开的区间约定（恰好等于生效时间属于新版本）、`0` 个表示「还没有」、结果只取决于（时间，版本表）。**变化的。** 版本里放的是什么（一个字符串、一条规则链、一个余额）；以及是否允许补录。

**信号。** 需求里出现「按交易发生时的价格」「某个时刻的值」「历史上某一刻的余额」「生效日期」；或者你的代码里有 `current_rate` 这种全局变量，却要处理迟到的数据。

**尺度对照。** 力扣：每个 key 一个有序数组，二分。低层设计：不可变的版本表，快照读。分布式：数据库的时态表（temporal table）和缓慢变化维度（SCD type 2，每行带 `valid_from`/`valid_to`）；MVCC 的快照读（读事务看到的是它开始时刻的版本）；带生效时间的配置发布。变化：单机里「版本表只追加」是一个约束，多机里要变成约定：所有副本用同一个事件时间，而不是各自的本地时钟；迟到的数据与补录的版本一起，把「追加调整」变成对账流程的一部分。
