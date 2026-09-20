---
id: problems-car-rental-purge-absorbs-location
node: problems.booking.car-rental
type: qa
step: 6
tags: [grown]
---
## Q
租车系统（Car Rental）里每辆车的行程链必须会缩（否则开十年的租车行链会无限长大）。清理历史行程时有一个很容易漏的陷阱，是什么？

## A
陷阱：**位置是沿着链算出来的，删掉最后一段历史却不前移链的起点，这辆车就会凭空瞬移回基地门店。**

一辆基地在浦东的车，上个月异地还到了南京。如果把那段历史直接删掉，`location_at` 沿着（现在空的）链往前走，得到的答案又是浦东——于是系统开始在浦东卖一辆停在南京的车。

正确写法是先吸收再删：

```python
stale = self._ordered(l for l in self._legs if l.period.end <= cutoff)
if not stale:
    return 0
self._base = stale[-1].destination      # 先把"最后停在哪"吸收进起点
self._legs = [l for l in self._legs if l.period.end > cutoff]
```

一句话记住：**容器可以缩，但不能连它承载的状态一起丢。**同一个陷阱在数据库版的归档任务里一模一样，而且更难查。
