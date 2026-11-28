---
id: hi-c-sd-uber-n05-api
node: sd.problem-breakdowns.uber.notes
type: qa
step: 5
---
## Q
**网约车 · 四个接口与安全红线**｜摘要 · 必会

网约车的估价、叫车、司机上报位置、司机接单四个接口怎么设计？哪些数据绝不能由客户端传？

## A
- **估价：** `POST /fare`，body 是起点和终点，返回 Fare；用 POST 因为会新建一条 Fare 记录。
- **叫车：** `POST /rides`，body 只带 `fareId`，创建 Ride 并触发匹配。匹配在后端发生，不单列接口。
- **司机上报位置：** `POST /drivers/location`，body 是经纬度，由司机客户端周期性调用；司机 ID 来自会话 Cookie 或 JWT，不放在 body 或路径里。
- **接单：** `PATCH /rides/:rideId`，body 是接受或拒绝；Ride 对象里带上车点和目的地，供司机端显示。
- **安全红线：** 客户端传来的一切都不可信。用户身份放令牌里；时间戳由服务端生成；估价按 `fareId` 从库里读，不能让客户端提交价格，否则可以改价。面试官常专门盯这一点。
