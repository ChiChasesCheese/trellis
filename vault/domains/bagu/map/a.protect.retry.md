%% trellis:begin %%
# 重试的原则与为什么不能无限重试（Backoff, Budget）
*A 高频追问链 / 服务保护*

只重试幂等的临时错误，指数退避加抖动，设置总预算，防止逐层重试放大。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[bagu-retry-1-what-to-retry]]
2. [[bagu-retry-2-backoff-jitter]]
3. [[bagu-retry-3-why-not-unlimited]]
4. [[bagu-retry-4-layered-retry-budget]]
5. [[bagu-retry-5-retry-and-idempotency]]
%% trellis:end %%

## Notes
