---
id: problems-rate-limiter-sliding-log-vs-counter-memory
node: problems.foundations.rate-limiter
type: qa
step: 4
tags: [grown]
---
## Q
In a rate limiter with 5 million API keys, each enforcing a 100 req/s sustained limit over a 60-second sliding window plus a 200 req/1s burst limit, why does storing every request's timestamp (a sliding window log) cost roughly 331x more memory than storing two constant-size counters per key per tier (a sliding window counter)?

## A
A sliding window log must retain one 8-byte timestamp per admitted request within the window: the 60-second sustained window can hold up to 100*60=6,000 timestamps (48,000 bytes/key) and the 1-second burst window up to 200 timestamps (1,600 bytes/key), totaling about 248GB across 5 million keys. A sliding window counter instead stores a fixed number of small counters per key per tier regardless of the limit or window size — about 15 million counters (5M keys x 3 tiers) at roughly 50 bytes each, totaling about 0.75GB. The ratio (248GB / 0.75GB is approximately 331) shows the log's memory cost scales with the limit and window size while the counter's does not, which is why constant-space approximations, not exact logs, are the default choice at this scale.

## Q zh
在一个有 500 万 API key 的速率限制器里，每个 key 都要执行 60 秒滑动窗口内 100 req/s 的 sustained 限制，加上 1 秒窗口内 200 req 的 burst 限制，为什么给每个请求存一条时间戳（滑动窗口日志）比每个 key 每层只存两个固定大小的计数器（滑动窗口计数器）多耗费约 331 倍内存？

## A zh
滑动窗口日志必须为窗口内每个被放行的请求保留一条 8 字节时间戳：60 秒的 sustained 窗口最多容纳 100×60=6,000 条时间戳（每 key 48,000 字节），1 秒的 burst 窗口最多 200 条（每 key 1,600 字节），500 万 key 合计约 248GB。滑动窗口计数器则不管限额或窗口大小多大，每个 key 每层只存固定数量的小计数器——约 1,500 万个计数器（500 万 key × 3 层），每个约 50 字节，合计约 0.75GB。这个比例（248GB / 0.75GB 约等于 331）说明日志方案的内存开销随限额和窗口大小线性增长，而计数器方案不会——这正是这个规模下默认选择常数空间近似算法、而不是精确日志的原因。
