%% trellis:begin %%
# LMAX Disruptor：环形数组 + 序号
*数据结构组合：开源框架里的类设计*

高性能的生产者-消费者队列：长度为 2 的幂的环形数组，生产者和消费者用只增不减的序号推进，下标用位与取模；预先分配、对缓存友好，单生产者时可以完全不加锁。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-ring-buffer-1-spec]]
2. [[uth-compose-ring-buffer-2-sequences]]
3. [[uth-compose-ring-buffer-3-core-code]]
4. [[uth-compose-ring-buffer-4-disruptor]]
5. [[uth-compose-ring-buffer-5-interview]]
%% trellis:end %%

## Notes
