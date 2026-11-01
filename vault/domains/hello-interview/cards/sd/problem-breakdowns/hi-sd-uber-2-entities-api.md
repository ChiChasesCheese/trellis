---
id: hi-sd-uber-2-entities-api
node: sd.problem-breakdowns.uber
type: qa
step: 2
---
## Q
**网约车的核心实体与接口**｜系统设计 · 问题拆解

网约车设计里要有哪些核心实体？乘客估价、叫车、司机上报位置、司机接单这四个接口怎么定义，为什么用户身份和价格不放在请求体里？

## A
**要点。** 实体：乘客（Rider）、司机（Driver，含车辆信息和可用状态）、费用估算（Fare，起终点、估价、预计到达时间）、行程（Ride，状态、乘客司机、实际费用、时间戳）、位置（Location，经纬度加更新时间）。Fare 也可以并入 Ride，没有标准答案。

**接口。**
- `POST /fare`，body 是起点和终点，返回 Fare（会新建 Fare 记录，所以用 POST）
- `POST /rides`，body 只带 fareId，创建 Ride 并触发匹配；匹配在后端发生，不单列接口
- `POST /drivers/location`，body 是经纬度
- `PATCH /rides/:rideId`，body 是接受或拒绝

**易错。** 客户端传来的任何数据都不可信。用户 ID 放会话 Cookie 或 JWT 里，时间戳由服务器生成，估价从数据库按 fareId 读取，绝不由客户端提交。这是面试官专门盯的安全红线。
