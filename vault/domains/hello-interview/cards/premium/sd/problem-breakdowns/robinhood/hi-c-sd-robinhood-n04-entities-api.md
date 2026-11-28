---
id: hi-c-sd-robinhood-n04-entities-api
node: sd.problem-breakdowns.robinhood.notes
type: qa
step: 4
---
## Q
**股票交易平台 · 实体与接口**｜摘要 · 必会

股票交易平台的实体和接口怎么设计？价格为什么用整数，身份为什么不能信请求里的 userId？

## A
- **实体：** 用户（User）、股票符号（Symbol）、订单（Order，用户创建的买或卖）。先报短清单，补字段留到设计成形后。
- **接口：**
  - `GET /symbol/:name` 返回符号详情与价格；
  - `POST /order`，体含 `position`（buy、sell）、`symbol`、`priceInCents`、`numShares`，返回订单；
  - `DELETE /order/:id`，返回 `{ok: true}`；
  - `GET /orders`，返回分页的订单列表。
- **价格用整数分：** `priceInCents` 而不是浮点数，浮点有精度误差，金融应用用整数，避免对账错误与资金损失。
- **身份：** 涉及账户或订单的请求带会话令牌或 JWT，服务端验证后得知是谁，再判断此人能否查看或修改这些订单。不能信请求头或体里的 userId，因为客户端可以随意改。
- **后续变化：** 行情接口后来改成 `GET /subscribe?symbols=...` 的 SSE 长连接。
