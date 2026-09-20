---
nodes: [problems.components.rate-limiter, patterns.strategy, concurrency.primitives]
tags: [problem]
---
# Drill：限流器（Rate Limiter）

一个进程内的限流库：Web 服务的每个请求进来先问它一句"这次放不放"。
**不是分布式限流架构**——没有 Redis、没有集群、没有时钟同步，只有类、可注入的时钟和一把锁。
规模是单进程、几十个线程、上百万个不同的 key（用户 id、API key、IP）。
照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：一个限流器、一个 key、一个固定窗口，`allow(key)` 判定放行与否。
  写完之后**自己拆台**：用限额「每 10 秒 5 次」构造一段流量，让它在 0.2 秒内合法地放行 10 次，
  并把这笔算术写进一个通过的测试里。时钟从构造函数注入，整套测试里不许出现 `sleep`。
- 第 2 关（约 15 分钟）：把"怎么记住最近的流量"抽成一条接缝，让令牌桶、滑动窗口日志、
  滑动窗口计数与固定窗口共存。接缝切在哪里决定了你要写四遍还是一遍"够不够、剩多少、
  被拒不扣"——想清楚四种算法**唯一**的差别是什么。令牌桶不许起后台线程。
  同时把返回值从 bool 换掉：被拒的调用方需要知道多久之后再来，而这个数只有算法算得出来。
  最后列一张表：每个 key 的内存、精度、以及滑动窗口计数在什么情况下估错、错向哪一边。
- 第 3 关（约 15 分钟）：每个 key 一份状态。先回答"一百万个 IP 各来过一次，内存多大"，
  再回答"什么时候可以丢掉一份状态"——注意丢早了等于给客户端免费解封，所以判据要硬到
  "丢了和不丢结果完全一样"。写一个真的跑一百万个 key 的测试来证明它不涨。
  然后是线程安全：一把全局锁、每 key 一把锁、分片锁，选一个并说得出另外两个的代价；
  用屏障写一个"两百个线程抢五十个额度"的测试，断言放行数精确等于 50。
- 第 4 关（选做）：同时按用户和按接口限流，任一条拒绝即拒绝；再给每次请求加一个 `cost`
  （重接口消耗多份额度）。判分点只有一个：前三关的类一行都不许改。
  想清楚"被后一条规则拒掉时，前一条规则的额度扣了没有"，以及同时拿多把锁怎么不死锁。

**怎么练**：把 `vault/domains/low-level-design/problems/rate-limiter/starter.py` 的方法体补全，然后在
仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/rate-limiter -q`。

**评分点**
- 开口第一句就把"进程内库组件"和"分布式限流架构"分开，并且全程待在前者里。
- 当场算出固定窗口的边界突发：t=9.9 五次、t=10.1 五次，0.2 秒内 10 次 = 2 倍限额（[[problems-rate-limiter-fixed-window-boundary-burst]]）。
- 返回结构化的判定结果而不是裸 bool，并说得出"抛异常"为什么也不对（[[problems-rate-limiter-decision-not-bool]]）。
- 接缝切在"已占用多少"而不是切在 `allow`，于是判定规则只写一遍（[[problems-rate-limiter-used-is-the-seam]]、[[patterns-selection-cues]]）。
- 令牌桶惰性补充、不起线程，并夹住倒退的时钟；容量与速率分离（[[problems-rate-limiter-token-bucket-lazy-refill]]）。
- 状态字典会缩，判据是"与新建状态等价"而不是"多久没用过"（[[problems-rate-limiter-state-map-must-shrink]]）。
- 摊还扫描的门槛对着"上次整理后的规模"而不是当前规模（[[problems-rate-limiter-amortised-threshold-trap]]）。
- 锁用分片，说得出每 key 一把锁的陷阱，以及 GIL 保护不了 check-then-act（[[problems-rate-limiter-sharded-lock]]、[[concurrency-check-then-act]]）。
- 组合多条规则时用两阶段判定，并用固定的加锁顺序避免死锁（[[problems-rate-limiter-composite-two-phase]]、[[concurrency-lock-ordering-transfer]]）。

**题解**：[[solution-rate-limiter]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
