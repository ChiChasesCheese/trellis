---
id: hi-c-lld-rate-limiter-n06-limiter-interface
node: lld.problem-breakdowns.rate-limiter.notes
type: qa
step: 6
---
## Q
**限流器 · Limiter 为什么是接口、不是抽象基类**｜摘要 · 必会

不同算法都实现 `allow(key)`。为什么用接口而不是带共同字段的抽象基类？

## A
- **接口：** 只有一个方法 `allow(key) -> RateLimitResult`；`key` 在本系统里就是客户端 ID。
- **每种算法的每键状态完全不同：**
  - 令牌桶：`tokens`（浮点）和 `lastRefillTime`，两个字段
  - 滑动窗口日志：一个时间戳队列
  - 固定窗口计数器：计数和窗口起点
- **没有可抽出的共同结构：** 硬做基类会得到一个既没有字段也没有共享方法的抽象类，等于多绕一圈的接口。接口不强求虚假的共性。
- **推论：** 状态由各个限流器自己持有和管理（"每键一份状态"在各算法内部），`RateLimiter` 不集中保存任何客户端数据，也不关心算法细节。
- **Python 对应：** 用 `typing.Protocol` 描述接口即可，不必继承。
