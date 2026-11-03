---
id: hi-pt-recently-viewed-items-10-multi-instance-test
node: qb.lld.recently-viewed-items.points
type: qa
step: 9
---
## Q
**"最近浏览"记录 · 多实例与测试点**｜追问 · 出自："最近浏览"记录 › 取舍与追问

"最近浏览"部署多实例时视图会不一致吗？测试要覆盖哪些点？

## A
**多实例。** 同一客户请求粘性路由到同一实例，或统一放 Redis。
**测试点。** 重复浏览提前、恰好达到上限、超限丢最老、不存在的客户返回空列表、limit=1、并发浏览同一客户。
