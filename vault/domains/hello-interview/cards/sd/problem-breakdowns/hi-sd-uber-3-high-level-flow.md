---
id: hi-sd-uber-3-high-level-flow
node: sd.problem-breakdowns.uber
type: qa
step: 3
---
## Q
**网约车的高层设计与主流程**｜系统设计 · 问题拆解

网约车的高层设计怎样依次满足估价、叫车、匹配、司机接单四个功能？每一步引入哪些组件，数据怎么流动？

## A
**要点。** 按功能需求逐条叠加组件：
1. **估价。** 客户端经 API 网关（鉴权、限流）到叫车服务（Ride Service）；它调用第三方地图 API 算距离和耗时，套用定价模型，把 Fare 写库后返回
2. **叫车。** 不需要新服务，只加 Ride 表：用 fareId 创建 Ride，状态为 requested，然后触发匹配
3. **匹配。** 加入司机客户端、位置服务（Location Service，接收并保存司机位置）、匹配服务（Ride Matching Service，按距离、可用性、评分给司机排序）
4. **接单。** 加入通知服务（Notification Service），通过 APNs / FCM 推送给排名第一的司机；司机接受则 Ride Service 把状态改为 accepted 并返回上车点，拒绝则推给下一位

**取舍。** 先搭出能跑通的简单版，已知的问题（位置写入量、重复派单、丢单）留给深挖。面试官问到推送方式时，可套用实时更新模式（长轮询、SSE、WebSocket）。
