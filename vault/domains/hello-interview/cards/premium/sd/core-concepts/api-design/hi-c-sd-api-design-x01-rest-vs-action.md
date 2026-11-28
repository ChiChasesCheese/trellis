---
id: hi-c-sd-api-design-x01-rest-vs-action
node: sd.core-concepts.api-design.exam
type: qa
step: 1
---
## Q
**API 设计 · 改写动作式接口**｜考点 · 必会
一个团队设计了外卖平台接口：`POST /cancelOrder`、`GET /getRestaurantMenu?id=9`、`POST /applyCoupon`。指出每个违反了什么原则，并改写成资源式。

## A
- **共同问题：** 路径里是动词，违反"围绕资源而非动作"，方法本身已能表达动作。
- **`POST /cancelOrder`：** 取消是订单状态的改变，改成 `PATCH /orders/{id}` 带 `{"status":"cancelled"}`，或 `DELETE /orders/{id}`（若业务上取消等于删除）。`status` 设为定值，重试幂等。
- **动词多余，id 进路径：** `GET /getRestaurantMenu?id=9`：动词多余，且餐厅编号是必需的，应进路径：`GET /restaurants/9/menu`。
- **`POST /applyCoupon`：** 优惠券是挂在订单上的东西，改成 `POST /orders/{id}/coupons`。
- **加分：** 优惠券这个 POST 不幂等，用户连点两次会叠加两张，所以让同一券码重复提交返回"已应用"，或带幂等键。
