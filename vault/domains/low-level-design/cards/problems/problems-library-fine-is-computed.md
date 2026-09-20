---
id: problems-library-fine-is-computed
node: problems.booking.library
type: qa
step: 6
tags: [grown]
---
## Q
图书馆管理（Library Management）的逾期罚金，为什么不能在还书那一刻算好、存进一个 `fine` 字段？

## A
因为柜台要回答的问题是「这位读者**现在**欠多少」——书还在他手上、还没还的时候就要答得出。存字段就只能在还书那一刻更新，之后立刻过期。

正确做法是按时刻算，而且同一个方法要覆盖两种语义：

```python
def days_overdue(self, now: datetime) -> int:
    moment = self.returned_at or now     # 还着：按现在算；还了：冻结在归还时刻
    if moment <= self.due_at:
        return 0
    return max(1, math.ceil((moment - self.due_at).total_seconds() / 86400))
```

「欠款总额」＝已结算的历史罚金 ＋ 手上逾期书**正在**产生的罚金。

两个配套要求：时钟必须**注入**（`clock: Callable[[], datetime]`），不然测试只能靠 `sleep`；金额用**整数分**或 `Decimal`，不要 `float`。不足一天按一天算，所以用向上取整。
