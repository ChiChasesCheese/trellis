---
id: correctness-dedup-window
node: correctness.idempotency
type: qa
---
## Q
How long do you retain idempotency keys / dedup records, and what goes wrong at each extreme?

## A
Retention must **exceed the maximum retry horizon** of every client and queue in front of you — including delayed retries from DLQ redrives and mobile clients replaying after days offline. Stripe retains keys ~24h; payment systems with async retries often keep 7–30 days.

- **Too short**: a retry after expiry is treated as new → duplicate charge. This is the silent failure mode.
- **Too long / forever**: unbounded storage, and a hot unique index; mitigate with TTL + moving dedup responsibility to a natural business key (e.g. one charge per `order_id`) which never expires.

## Q zh
幂等性 key / 去重记录保留多久，两个极端各会出什么问题？

## A zh
保留时间必须**超过所有客户端和你前面的队列的最大重试窗口** — 包括 DLQ 重驱的延迟重试和离线数天后重放的移动客户端。Stripe 保留 key ~24 小时；带异步重试的支付系统通常保留 7-30 天。

- **太短**：过期后重试被当作新请求 → 重复扣款。这是无声失败。
- **太长 / 永远**：无界存储，热 unique index；用 TTL + 将去重职责转移到自然业务 key（如每个 `order_id` 一笔扣款）来缓解，这种 key 永不过期。
