---
id: hi-pt-restaurant-waitlist-api-7-starvation
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 7
---
## Q
**餐厅候位 API · 防饿死计数器**｜追问 · 出自：餐厅候位 API › 深入 4

队首的 6 人团一直被后来的 2 人团插队。怎么在不重写入座规则的前提下加公平？为什么用计数器而不是优先级？

## A
**做法。** 每个排队的人记 `skipped`（被后面的人越过的次数），`_drain` 里遇到次数达到 `max_overtakes` 的人，自己坐不了就停止：他之后的人不许再越过他。

```python
if max_overtakes is not None and w.skipped >= max_overtakes:
    return seated
```
**为什么。** 计数器的行为可以直接写进测试，优先级让规则难以预测。**代价。** 挡路时桌子空着、有人在等。`0` 是严格先来先坐。
