---
id: s16-sliding-window-token-bucket
node: stripe.balances-limits
type: qa
---

## Q
限流题里滑动窗口计数器和令牌桶该怎么实现？为什么令牌桶不能用定时器，长时间不活跃的 key 又该怎么处理？

## A
见 `05-time-and-intervals.md` §4 和 `08-algorithm-patterns.md` §3。要点：

- **滑动窗口**：每个 key 一个 `deque`，新事件进来先从左边弹出所有过期的。
  "过期"的判定是 `ts - dq[0] >= window`（还是 `>`？题面决定）。
- **令牌桶**：只存 `(tokens, last_refill_ts)`，用时再补：
  `tokens = min(cap, tokens + (now - last) * rate)`。**不要**用定时器。
- **空闲清理**：长时间没请求的 key 要从字典里删掉，否则 10^6 个 key 撑爆内存。
