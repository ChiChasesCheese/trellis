---
id: hi-pt-feature-flags-service-10-local-vs-central
node: qb.sd.feature-flags-service.points
type: qa
step: 10
---
## Q
**功能开关服务 · 本地判定还是集中判定**｜追问 · 出自：功能开关服务 › 取舍与追问

追问：每次问服务判定，与 SDK 本地判定怎么取舍？匿名用户怎么分桶？

## A
**取舍。** 集中判定规则永远最新，但有网络延迟和单点；本地判定延迟极低、抗故障，代价是传播延迟。热路径几乎一律本地判定。数据库做每次判定读 QPS 过高，开关也不该成为业务的可用性依赖。
**匿名。** 用设备 ID 或 Cookie；登录后键变化会翻转，要用同一个稳定标识或指定 `bucketBy` 属性。
