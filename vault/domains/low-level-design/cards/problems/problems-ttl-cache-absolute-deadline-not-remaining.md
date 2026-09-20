---
id: problems-ttl-cache-absolute-deadline-not-remaining
node: problems.components.ttl-cache
type: qa
step: 2
tags: [grown]
---
## Q
缓存里的一条数据，该存「还能活多久」还是「什么时刻死」？时钟又该怎么来？

## A
存**绝对截止时刻**（`expires_at = now + ttl`），不存剩余时间。

存剩余时间意味着必须有人定期去减它——那又绕回一个后台线程，而且它在任何时刻都只是近似值。存绝对时刻则是写入时算一次、之后永不改动的常量，判定就是一次比较。

如果还要支持「读一次续一次命」（滑动过期），就把原始的 `ttl` 也一起留着，续命等于用同一个 `ttl` 重新算一次截止时刻。是否续命应当是一个**构造参数**而不是两个类：会话缓存要续，价格缓存必须按绝对时效作废。

时钟一律**注入**，并且用 `time.monotonic`：

- 类内部硬编 `time.time()`，测试就只能靠 `sleep`，一套用例跑几十秒还不稳定；
- `time.time` 会被 NTP 往回拨，回拨那一刻整批过期数据会集体「复活」。
