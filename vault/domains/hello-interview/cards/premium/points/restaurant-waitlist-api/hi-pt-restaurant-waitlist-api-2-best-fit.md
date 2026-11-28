---
id: hi-pt-restaurant-waitlist-api-2-best-fit
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 2
---
## Q
**餐厅候位 API · 最小够用的桌**｜必会 · 出自：餐厅候位 API › 深入 2

多张空桌都坐得下时选哪张？只取编号最小的空桌行不行？

## A
**选法。** 容量最小的够用桌，容量相同取编号小的。

```python
fit = min(((sizes[t], t) for t in free if sizes[t] >= size), default=None)
```
**为什么。** 编号最小的空桌会让 2 个人占掉 6 人桌，后来的大团只能干等；最小够用保住大桌。**代价。** 这是贪心，不是全局最优。
