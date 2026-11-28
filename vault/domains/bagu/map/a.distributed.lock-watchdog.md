%% trellis:begin %%
# 锁过期了业务没完：看门狗续期与可重入（Watchdog, Reentrant）
*A 高频追问链 / 分布式基础*

TTL 难以预估时用看门狗自动续期，但续期无法防住 GC 停顿，根治靠 fencing token。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[bagu-lock-watchdog-1-expire-early]]
2. [[bagu-lock-watchdog-2-redisson]]
3. [[bagu-lock-watchdog-3-gc-pause]]
4. [[bagu-lock-watchdog-4-fencing]]
5. [[bagu-lock-watchdog-5-redis-token]]
%% trellis:end %%

## Notes
