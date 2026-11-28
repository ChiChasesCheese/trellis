---
id: hi-c-sd-problem-breakdowns-n05-hard-b
node: sd.in-a-hurry.problem-breakdowns.notes
type: qa
step: 5
---
## Q
**常见题目拆解 · 困难题下半（5 道）**｜摘要 · 必会

困难级的 Payment System、Metrics Monitoring、Online Chess、ChatGPT、Flash Sale 各自的考点是什么？

## A
- **Payment System：** 幂等（重复请求只扣一次）、账本与对账、与支付渠道的异步回调、状态机与一致性。
- **Metrics Monitoring：** 时序数据的高写入、降采样与保留、告警、高基数标签带来的存储压力。
- **Online Chess：** 双方实时对局、走子的顺序与合法性、计时、观战与断线重连。
- **ChatGPT：** 流式逐 token 返回、推理资源（GPU）调度与排队、对话历史存储、并发与成本。
- **Flash Sale：** 瞬间高并发抢有限库存、防超卖、排队 / 限流保护后端、热点商品。
