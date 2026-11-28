%% trellis:begin %%
# 用 Redis 实现分布式锁（SET NX PX + Lua）
*A 高频追问链 / 分布式基础*

SET key uuid NX PX 加锁、Lua 比对 value 再删除释放，是最基础的 Redis 分布式锁。

**Core** — part of the first pass through this subject.

## Cards (6)
1. [[bagu-lock-redis-setnx-1-basic]]
2. [[bagu-lock-redis-setnx-2-nx-px-value]]
3. [[bagu-lock-redis-setnx-3-lua-release]]
4. [[bagu-lock-redis-setnx-5-ttl-qps]]
5. [[bagu-lock-redis-setnx-6-db-instead]]
6. [[bagu-lock-redis-setnx-4-retry-reentrant]]
%% trellis:end %%

## Notes
