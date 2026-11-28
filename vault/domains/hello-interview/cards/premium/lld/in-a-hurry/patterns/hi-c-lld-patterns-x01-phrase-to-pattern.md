---
id: hi-c-lld-patterns-x01-phrase-to-pattern
node: lld.in-a-hurry.patterns.exam
type: qa
step: 1
---
## Q
**设计模式 · 需求措辞对应模式**｜考点 · 必会

五句需求：(1) "支持不同通知类型"；(2) "价格变动要通知多个显示窗口"；(3) "订单有待支付、已支付、已发货、已取消"；(4) "日志、加密、压缩可任意组合"；(5) "用不同折扣规则计价"。各对应哪个模式？

## A
| 措辞 | 模式 |
|---|---|
| 不同通知类型 | Factory（创建）或 Strategy（行为） |
| 通知多个显示窗口 | Observer |
| 订单有多个状态 | State Machine |
| 任意组合的增强 | Decorator |
| 不同折扣规则 | Strategy |

- **先说变化的是什么：** 先说清楚需求里"变化的是什么"（创建的类、行为、状态、叠加的功能），再选名字
