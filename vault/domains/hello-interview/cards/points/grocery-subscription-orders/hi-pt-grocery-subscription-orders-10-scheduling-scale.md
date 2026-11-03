---
id: hi-pt-grocery-subscription-orders-10-scheduling-scale
node: qb.lld.grocery-subscription-orders.points
type: qa
step: 9
---
## Q
**生鲜订阅转订单服务 · 调度、时区与订阅修改**｜追问 · 出自：生鲜订阅转订单服务 › 取舍与追问

订阅服务的调度规模变大后怎么并行？`next_run` 用哪个时区？转换期间用户修改订阅怎么办？

## A
**调度。** `run_due` 由定时任务调用，按订阅 ID 分片并行，幂等键保证多实例重叠时不重复。
**时区。** `next_run` 用用户所在时区的日期，不用服务器时间，否则午夜附近会错一天。
**修改。** 转换读取订阅快照（版本号），修改只影响下一期；要立即生效则转换前重新读取并检查版本。
