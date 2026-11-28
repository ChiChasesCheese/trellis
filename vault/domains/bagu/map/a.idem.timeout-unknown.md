%% trellis:begin %%
# 调用扣款接口超时了，到底扣了没有（Unknown Outcome）
*A 高频追问链 / 幂等与分布式事务*

超时不等于失败：先查询最终状态，再用同一个幂等键重试，最后靠对账兜底。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[bagu-timeout-unknown-1-not-failure]]
2. [[bagu-timeout-unknown-2-pending-query]]
3. [[bagu-timeout-unknown-3-safe-retry]]
4. [[bagu-timeout-unknown-5-limit-fallback]]
5. [[bagu-timeout-unknown-4-no-support]]
%% trellis:end %%

## Notes
