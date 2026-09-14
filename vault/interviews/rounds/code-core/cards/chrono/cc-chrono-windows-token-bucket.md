---
id: cc-chrono-windows-token-bucket
node: chrono.windows
type: qa
---
## Q
A bucket refills at 2 tokens/second and a request arrives 600 ms after the last one. Integer refill gives 1 token. What is wrong — and what should happen to a client idle for a day?

## A
**Fractional accrual must not be rounded away, and accrual must be capped.** 600 ms × 2/s = 1.2 tokens; truncating every refill to 1 loses 0.2 each time and starves a client that is under its rate.

- Hold tokens in a scaled integer (milli-tokens): `tokens = min(cap*1000, tokens + elapsed_ms * rate)`. No floats, no drift.
- Cap on every refill — an idle client must not bank a day's worth of burst. That cap is the whole difference between a bucket and a counter.
- Refill **lazily** on access from a stored `last_ts`; a timer per client does not scale and is not reproducible.
- Compare `tokens >= cost*1000`: 1.2 tokens covers one request, 0.2 does not.
- Unlike a rolling window ([[cc-chrono-windows-bucket-vs-rolling]]) this is O(1) memory per client — no event list at all.

## Q zh
一个桶以每秒 2 个 token 的速率补充，某请求在上一次之后 600 ms 到达。整数补充给出 1 个 token。哪里错了 —— 而一个空闲了一整天的客户端应该发生什么？

## A zh
**小数累积不能被舍掉，而且累积必须封顶。** 600 ms × 2/s = 1.2 个 token；每次补充都截断成 1，就每次丢掉 0.2，让本来没超速的客户端被饿死。

- 用放大的整数保存 token（毫 token）：`tokens = min(cap*1000, tokens + elapsed_ms * rate)`。没有浮点，没有漂移。
- 每次补充都封顶 —— 空闲的客户端不该攒下一整天的突发额度。这个上限正是桶与计数器的全部区别。
- 从存下的 `last_ts` **惰性**补充；每客户端一个定时器既不可扩展也不可复现。
- 比较 `tokens >= cost*1000`：1.2 个 token 够一个请求，0.2 个不够。
- 与滚动窗口（[[cc-chrono-windows-bucket-vs-rolling]]）不同，这里每个客户端只占 O(1) 内存 —— 完全不需要事件列表。
