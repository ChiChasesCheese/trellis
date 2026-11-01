---
id: hi-pt-donations-website-charities-12-counter-hotspot
node: qb.sd.donations-website-charities.points
type: qa
step: 12
---
## Q
**限时捐款网站 · 累计金额的热点行**｜出自：限时捐款网站 › 整体设计

若要展示每家机构的累计金额，只有 5 家机构，直接 `UPDATE total = total + 10` 有什么问题？怎么解决？

## A
**问题。** 5 家机构就是 5 个热点行，写入争用。
**方案。** 分片计数器：每家机构 N 个子计数器，写入时随机选一个，读取时求和；或消费捐款成功事件，批量累加到 Redis。
**取舍。** 展示允许延迟几秒，账目真相仍是捐款表。
