---
id: hi-c-lld-rate-limiter-n07-result
node: lld.problem-breakdowns.rate-limiter.notes
type: qa
step: 7
---
## Q
**限流器 · RateLimitResult 的字段设计**｜摘要 · 必会

结果对象三个字段 `allowed`、`remaining`、`retryAfterMs` 各自怎么定义？为什么重试时间用可空而不用 0？

## A
- **不可变：** 创建后不再变，是值对象。
- **`allowed`：** 本次是否放行。
- **`remaining`：** 处理完本次之后还剩多少额度。限额 100、这是第 3 个请求，就是 97。令牌桶里令牌是浮点数，对外取整（向下）。
- **`retryAfterMs`：** 被拒时客户端至少要等多少毫秒；放行时为空（`null`/`None`）。可空比用 0 当哨兵更清楚：0 既可能是"现在就能重试"也可能是"不用重试"，语义混淆。
- **单位写进字段名：** `Ms` 防止读者猜是秒还是绝对时间戳。
- **被拒时 `remaining` 为 0。**
- **语言适配：** 用你的语言最自然的方式（dataclass、struct、type）；面试官在意的是类型安全地返回多个值，不是写一个 Java 式的 getter 类。
