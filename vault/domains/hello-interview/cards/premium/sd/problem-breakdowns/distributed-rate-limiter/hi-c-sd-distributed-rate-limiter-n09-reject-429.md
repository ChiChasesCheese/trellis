---
id: hi-c-sd-distributed-rate-limiter-n09-reject-429
node: sd.problem-breakdowns.distributed-rate-limiter.notes
type: qa
step: 9
---
## Q
**分布式限流器 · 超限时怎么响应**｜摘要 · 必会

超限的请求应该直接拒绝还是排队？429 响应里要带哪些信息？

## A
- **快速失败（fail fast）：** 多数限流器立刻返回 429 Too Many Requests。
- **为什么不排队：** 排队看起来友好，但会带来更多问题——排队的请求占用内存和处理资源；用户以为失败而重试，制造更多负载；队列等待让 API 延迟不可预测。只有能等的批处理系统才适合排队，交互式 API 几乎总是快速失败。
- **响应头：**
  - `X-RateLimit-Limit`：这条规则的上限，如 100；
  - `X-RateLimit-Remaining`：当前窗口还剩多少，被拒时为 0；
  - `X-RateLimit-Reset`：重置时间，Unix 时间戳；
  - `Retry-After`：建议客户端等待的秒数（有些系统才有）。
- **响应体：** 一段 JSON 说明"超过限额、多久后再试"。
- **目的：** 让守规矩的客户端能据此做退避，而不是对 API 不断重试轰炸。
- **面试里：** 一般只需说"返回 429 和这些头"。
