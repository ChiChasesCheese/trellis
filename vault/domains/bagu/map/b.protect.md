%% trellis:begin %%
# 服务保护
*B 其余知识点*

限流、熔断、降级、重试、超时、隔离与流量突增。

## Topics
- [[domains/bagu/map/b.protect.why-protect|为什么要做服务保护：雪崩与重试放大（Cascading Failure）]]
- [[domains/bagu/map/b.protect.distributed-limit|分布式限流怎么实现（Redis + Lua、本地配额）]]
- [[domains/bagu/map/b.protect.limiter-handwrite|手写限流器（令牌桶 / 滑动窗口）]]
- [[domains/bagu/map/b.protect.breaker|熔断器的三态与触发条件（Circuit Breaker）]]
- [[domains/bagu/map/b.protect.degrade|降级怎么做（Degradation, Fallback）]]
- [[domains/bagu/map/b.protect.timeout|超时时间怎么设置（Timeout, Deadline Propagation）]]
- [[domains/bagu/map/b.protect.bulkhead|隔离（Bulkhead）：线程池隔离与信号量]]
- [[domains/bagu/map/b.protect.ha-redundancy|高可用架构：冗余、容灾、多活与故障转移（RTO/RPO）]]
- [[domains/bagu/map/b.protect.observability-loadtest|可观测性与压测：Metrics / Trace / Log、全链路压测]]
%% trellis:end %%

## Notes
