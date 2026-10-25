---
id: pay-card-lifecycle-3ds-sca-failure-abandoned-challenge
node: card-lifecycle.3ds-sca
type: qa
step: 7
---
## Q
用户在 3DS 挑战页面完成验证后关掉了浏览器，平台收到了授权成功的回调但订单还是"待支付"。怎么发生的？如何设计才不丢单？

## A
**事故过程**
1. 订单进入 requires_action，前端弹出银行验证页，计划验证后跳回平台的 return_url，由前端触发"确认支付"。
2. 用户完成验证，银行页面正在跳转时，用户关了标签页（或网络中断）。
3. PSP 其实已经完成认证和授权，发卡行已冻结额度，webhook 也发到了平台。
4. 如果平台只靠前端回跳驱动确认，不处理 webhook 或把它忽略（认为状态不是预期的），订单就一直停在待支付，库存超时释放，用户被冻结了额度却没有订单。

**根因**：状态的推进依赖用户端行为，而不是渠道的最终事实。

**设计**
- 以服务端状态为准：webhook 与主动查询是推进状态的主要来源，前端回跳只做展示。
- requires_action 状态必须能被 webhook 推进到 authorized 或 failed。
- 对 requires_action 超过一定时间的支付单，主动向 PSP 查询最新状态，而不是只等回调。
- 发现"订单已过期，但渠道授权成功"：自动撤销授权（或在库存允许时恢复订单）。
- 监控 requires_action 的放弃率和过期率，异常升高说明认证页面有问题（加载慢、短信延迟）。
