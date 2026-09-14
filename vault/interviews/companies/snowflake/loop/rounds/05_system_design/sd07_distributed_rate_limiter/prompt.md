# Distributed Rate Limiter（per-second、多规则叠加）

我们平台对外暴露了一批 API，调用方是各种各样的客户端和第三方集成，请求量非常大而且不均匀——有些客户端会突发地在很短时间内打出一波密集请求。我们需要一个限流系统来保护后端不被打垮，同时保证限流本身是公平和精确的：限制的粒度是**每秒**级别（比如"这个 API key 每秒最多 100 个请求"），而且限制条件可能不是单一的一条规则，是好几条规则同时叠加生效——比如同时有"每个 API key 每秒不超过 100 个请求"和"整个系统全局每秒不超过 10 万个请求"这样的规则，一个请求要所有相关规则都还有余量才能放行，只要有一条不满足就要被拒绝或者排队。这个限流服务本身是多台机器组成的集群（不是单机），所以限流状态必须在多台机器之间共享和保持一致，不能出现"客户端明明已经用超了配额，但因为请求碰巧被分发到了不同的限流节点，各个节点各自觉得没超"这种情况。而且要考虑两种典型的坏场景：第一种是某个 key 突然被打爆（hot key），限流判断本身的开销不能成为新的瓶颈；第二种是限流窗口临界点前后可能出现大量请求同时涌入（thundering herd），比如很多客户端都设了在整点重试。当系统压力太大、限流本身撑不住的时候，应该怎么优雅降级而不是直接宕机。请设计这个分布式限流器。

---

**面试环境说明**：这是 Snowflake 技术电面或 onsite 的 System Design 轮，时长 45–60 分钟。白板工具未证实；面试官风格两极分化。这道题在电面/onsite 池里都出现过，且与一道具体的"滑窗单规则限流器" coding 题（`loop/rounds/04_ood/od04`）共享同一个题目家族，如果面试官先给了 coding 版本再要求"现在把它变成分布式的"，可以直接复用本题的思路展开。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.12）：
- **Onsite 一手/半一手**：滑窗限流器，"processing request timestamps in order, every request at time t is allowed only when fewer than limit previously allowed requests have timestamps in the half-open interval (t - windowSeconds, t]"，FastPrep 标注为 **Snowflake Onsite Interview** 题目 —— fastprep.io（**中**，培训站转述但题面具体到公式级别，疑似真实拿到原题）。
- **分布式版**（更像 SD 而非 coding）：Design a distributed rate limiter，"enforces a per-second throttling limit"，重点"如何在不产生 hot-spotting 或 thundering herd 的前提下让限流尽量精确" —— staffengprep.com（**中**）。
- **复用材料**：`../../raw/process_research.md` §3.2 #13 引用 PracHub 汇总 "thread-safe multi-rule rate limiter"（**低-中**）。
- 归类页面标签 "Distributed-Systems Access-Control/Caching/Throttling"（60 min，另有 1 篇独立报告）—— staffengprep.com（**中**）。
- 整体置信度 **MED**。追问汇总（原文已给出）：token bucket vs sliding window 精度/内存权衡；多实例共享限流状态（Redis 原子操作）；多规则（per-user + per-IP + 全局）如何叠加；限流后的降级策略。
