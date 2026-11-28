---
id: hi-c-sd-flash-sale-n03-entities-api
node: sd.problem-breakdowns.flash-sale.notes
type: qa
step: 3
---
## Q
**限时抢购 · 实体与接口**｜摘要 · 必会

有哪些核心实体和接口？预留接口返回什么？

## A
- **实体：** Product（商品、价格、开售与结束时间、可用单元数；一双鞋是一个单元）；Reservation（对一个单元的临时占用：用户、商品、过期时间、状态）；Purchase（成功购买的记录：用户、商品、预留、金额、支付状态）；User。
- **接口：** `GET /products/:productId` 返回商品和剩余数量；`POST /products/:productId/reservations` 尝试创建预留；`POST /reservations/:reservationId/purchases` 扣款并把预留变成购买。
- **预留的返回：** reservationId、productId、expiresAt，足以让客户端显示倒计时并去调购买接口。它**不代表买到了**，只是给用户一个有限的结账窗口。
- **购买失败：** 预留已过期或支付失败则请求失败，单元最终回到库存供别人买。
- **范围：** 这里只写到这个粒度，字段可由实体和需求推出；怎样在争抢中安全创建预留，才是后面的难点。
