---
id: problems-flash-sale-lua-atomic-check-and-decrement
node: problems.commerce.flash-sale
type: qa
step: 4
tags: [grown]
---
## Q
In a flash sale's inventory counter, why is a bare `DECR` command (with an after-the-fact check for a negative result) less safe than wrapping 'read remaining, check it's positive, decrement' inside a single Redis Lua script, even though `DECR` itself is atomic?

## A
`DECR` atomically decrements, but the decision of whether decrementing was even allowed (remaining > 0) happens as a separate step afterward — under high concurrency the counter can be driven negative by many simultaneous DECRs before any of them notices, requiring an extra corrective step to push it back up, which itself needs concurrency protection. A Lua script that reads, checks, and conditionally decrements in one call is executed as a single uninterruptible unit by Redis (Redis guarantees a script's atomic execution — all other server activity is blocked for its duration), so there is never a window where two concurrent requests both see a positive count and both succeed.

## Q zh
在秒杀的库存计数器里，为什么一条裸的 `DECR` 命令（配合事后判断结果是否为负）比把'读取剩余、判断是否为正、扣减'包进一条 Redis Lua 脚本更不安全，即使 `DECR` 本身是原子的？

## A zh
`DECR` 本身的扣减是原子的，但'是否允许扣减'（剩余是否 > 0）这个判断是事后单独发生的一步——在高并发下，计数器可能在任何一次调用意识到之前就被多条并发的 DECR 打成负数，需要额外一步把它纠正回来，而这一步本身又需要新的并发保护。把「读取、判断、条件扣减」包进一条 Lua 脚本，Redis 会把它当成一个不可分割的整体来执行（Redis 保证脚本的原子执行——脚本运行期间服务器所有其他活动都被阻塞），因此不存在两个并发请求都读到正数、都判断成功的窗口。
