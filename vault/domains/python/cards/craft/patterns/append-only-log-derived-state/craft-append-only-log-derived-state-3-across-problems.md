---
id: craft-append-only-log-derived-state-3-across-problems
node: craft.patterns.append-only-log-derived-state
type: qa
step: 3
---
## Q
**只追加日志 + 派生状态 · 账本、额度、出入记录里同一种「只存事实」**｜模式

双分录账本、额度账户、区域出入追踪、银行事件表，数据结构各不相同。它们存的「事实」是什么？派生状态是什么时候算出来的？

## A
**要点。** 都是：事实表只追加；余额、分配、人数都是它的函数。差别只在派生的时机：写入时同步维护（账本的余额索引），每次读时重放（额度分配的纯函数），或者带时间上限地归约（银行事件表、人数的前缀和）。

```python
# double-entry-ledger：写入时维护派生索引
self._journal: list[Entry] = []           # 唯一事实来源，只追加
self._bal: dict[Key, int] = defaultdict(int)   # 派生索引：当前余额

# credit-token-balance：每次重放，纯函数
def _replay(grants, charges, until=None):
    """按 (时间, 先额度包后扣费, id) 的顺序重放事件"""
    events = sorted([*grants.values(), *charges.values()], key=lambda e: (e.at, ...))

# amz-occupancy-tracker：存进出事件，人数是前缀和
class Timeline:
    """times[i] 是第 i 个事件的时间，counts[i] 是处理完它之后的人数。"""
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

重放的版本中，乱序到达的事件只需要被排进正确位置，分配自然重算；银行事件表里一个账户被合并掉，只是不再有新事件写进它的历史，历史本身一直在，所以合并后依然能回答历史时点的余额，不需要专门代码。

**见于。** double-entry-ledger、credit-token-balance、dasher-payout、amz-occupancy-tracker、atm（流水只增不改）、bank-account。

**信号。** 需求里出现「更正」「冲正」「乱序到达」「某个历史时刻的余额」「审计」；你发现自己在写一个会被改来改去的总数。
