---
id: hi-sd-distributed-rate-limiter-6-reject-429
node: sd.problem-breakdowns.distributed-rate-limiter
type: qa
step: 6
---
## Q
**超限时：快速失败与响应头**｜系统设计 · 问题拆解

超过限额时应该直接拒绝还是排队？429 响应要带什么信息？

## A
**快速失败。** 多数限流器立即返回 429。排队看着友好，实则更糟：排队请求占内存与处理资源；用户以为失败而重试，带来更多负载；队列延迟使响应时间不可预测。只有能等待的批处理系统才有排队的场景。

**响应头。**
- `X-RateLimit-Limit`：上限
- `X-RateLimit-Remaining`：当前窗口剩余次数
- `X-RateLimit-Reset`：重置时间（Unix 时间戳）
- `Retry-After`：多少秒后再试（部分系统提供）

响应体再给一句可读的错误说明。

**为什么。** 这些信息让守规矩的客户端能做退避，而不是对 API 反复轰炸。

**说法。** 面试里只需点明返回 429 加合适的头。
