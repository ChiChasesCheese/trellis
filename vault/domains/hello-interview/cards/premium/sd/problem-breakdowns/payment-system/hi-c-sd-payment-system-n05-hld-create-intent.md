---
id: hi-c-sd-payment-system-n05-hld-create-intent
node: sd.problem-breakdowns.payment-system.notes
type: qa
step: 5
---
## Q
**支付系统 · 高层设计一：创建 PaymentIntent**｜摘要 · 必会

商户创建收款意图的流程和组件是什么？这一步为什么还没有任何扣款？

## A
- **组件：**
  - API 网关：商户请求的入口，负责认证、限流、路由；
  - 支付（意图）服务：创建和管理 PaymentIntent，对接数据库；
  - 数据库：存意图（状态、金额、币种、元数据）和商户信息（API 密钥、业务信息、配置）。
- **流程：** 商户 POST → 网关认证 → 转给意图服务 → 创建状态为 `created` 的记录写库 → 生成唯一 ID 并返回。
- **ID 的作用：** 商户把它嵌入结账页或前端代码，后续收集卡信息时带上。
- **此时没有扣款：** 只是记录了"想收这笔钱"的意图和追踪它的引用，意图处于 `created`，等待下一步提供支付信息才开始处理。
