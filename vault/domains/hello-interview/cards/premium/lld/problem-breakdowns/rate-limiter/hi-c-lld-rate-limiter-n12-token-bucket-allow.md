---
id: hi-c-lld-rate-limiter-n12-token-bucket-allow
node: lld.problem-breakdowns.rate-limiter.notes
type: qa
step: 12
---
## Q
**限流器 · 令牌桶 allow 的四步算术**｜摘要 · 必会

令牌桶的 `allow(key)` 怎么写？补充量、放行、拒绝时的重试时间各怎么算？

## A
1. **取桶：** 没有就创建（满的，`lastRefillTime` 设为现在）。
2. **结算补充：** `now − last` 得到流逝毫秒，补充量 = 流逝 × 每秒速率 ÷ 1000，加到令牌数上，**封顶为容量**，再把 `last` 更新为 `now`。例如过了 1000 毫秒、速率 10/秒，补 10 个。
3. **放行：** 令牌数 ≥ 1 时扣 1，返回 `allowed=True`，`remaining=floor(令牌数)`，重试时间为空。
4. **拒绝：** 缺口 = 1 − 令牌数，重试等待 = `ceil(缺口 × 1000 ÷ 速率)` 毫秒。例：桶里 0.3 个，速率 10/秒，缺 0.7，要等 70 毫秒。向上取整是为了不让客户端过早重试再被拒；`remaining` 返回 0。
- **注意：** 被拒时也要把结算后的令牌数和时间写回，否则下次会重复结算同一段时间。
