%% trellis:begin %%
# 限流器（Rate Limiter）
*设计题（Design Problems） / 基础组件*

令牌桶、滑动窗口的类设计，可注入时钟，按用户隔离与线程安全。

**Requires:** [[domains/low-level-design/map/patterns.strategy|策略模式与可替换算法（Strategy）]], [[domains/low-level-design/map/concurrency.primitives|同步原语（threading）]]

## Readings
- [[solution-rate-limiter|设计题解：限流器（Rate Limiter）]]
- [[src-abhaypaswan-rate-limiter|abhaypaswan/lld-python — Design a Rate Limiter]]
- [[src-hellointerview-rate-limiter|Hello Interview — Rate Limiter（Low-Level Design Problem Breakdown）]]
- [[src-jkaus324-rate-limiter|jkaus324/machine-coding-interview-questions — API Rate Limiter]]

## Drills
- [[design-rate-limiter|Drill：限流器（Rate Limiter）]]

## Cards (8)
1. [[problems-rate-limiter-fixed-window-boundary-burst]]
2. [[problems-rate-limiter-decision-not-bool]]
3. [[problems-rate-limiter-used-is-the-seam]]
4. [[problems-rate-limiter-token-bucket-lazy-refill]]
5. [[problems-rate-limiter-state-map-must-shrink]]
6. [[problems-rate-limiter-amortised-threshold-trap]]
7. [[problems-rate-limiter-sharded-lock]]
8. [[problems-rate-limiter-composite-two-phase]]
%% trellis:end %%

## Notes
