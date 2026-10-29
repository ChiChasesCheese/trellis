%% trellis:begin %%
# Java 线程池：一个原子整数、一个任务队列、一组工人
*数据结构组合：开源框架里的类设计*

ThreadPoolExecutor 用一个 AtomicInteger 同时存运行状态和线程数；提交任务时先加核心线程、再进队列、再加到最大线程、最后拒绝；工人集合用锁保护。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-thread-pool-1-needs]]
2. [[uth-compose-thread-pool-2-structures]]
3. [[uth-compose-thread-pool-3-invariants-code]]
4. [[uth-compose-thread-pool-4-real]]
5. [[uth-compose-thread-pool-5-bounded-runner]]
%% trellis:end %%

## Notes
