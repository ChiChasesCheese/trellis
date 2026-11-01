---
id: hi-pt-rate-limiter-system-1-structure
node: qb.lld.rate-limiter-system.points
type: qa
step: 1
---
## Q
**限流器（单机类设计） · 类结构与策略模式**｜出自：限流器（单机类设计） › 核心实体与接口

单机限流器怎么划分类？算法差异和按 key 管理分别放哪？

## A
**要点。** `Limiter` 抽象类只管单个 key 的状态和判定 `try_acquire(now) -> Decision`，算法差异全在子类（`FixedWindow`、`SlidingWindowLog`、`TokenBucket`）；`RateLimiter` 入口持有 key 到（锁，Limiter）的映射和时钟；`Decision` 不可变，含 `allowed`、`remaining`、`retry_after`。
**模式。** 策略、工厂（为新 key 建 Limiter）、依赖注入（时钟）。
