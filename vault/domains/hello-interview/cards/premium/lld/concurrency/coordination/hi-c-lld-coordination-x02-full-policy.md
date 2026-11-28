---
id: hi-c-lld-coordination-x02-full-policy
node: lld.concurrency.coordination.exam
type: qa
step: 2
---
## Q
**并发协调 · 队列满了选哪种策略**｜考点 · 必会

三个生产者：(a) 夜间批量作业向处理阶段送数据；(b) 用户下单的 HTTP 接口；(c) 前端上报的点击分析事件。队列满时各用什么策略？

## A
| 生产者 | 策略 |
|---|---|
| 批处理 | 阻塞 `put`，慢点没关系 |
| 下单接口 | 超时后拒绝，返回 503 |
| 点击分析 | 立即丢弃并记录 |

- 判断依据：能不能让调用方等，丢了有没有代价
