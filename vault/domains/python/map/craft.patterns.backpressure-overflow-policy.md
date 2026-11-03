%% trellis:begin %%
# 背压与溢出策略：丢最旧 / 阻塞 / 拒绝，必须当场选并可观测
*编码功力（Coding Craft） / 跨题模式（Patterns）*

有界队列满了怎么办是一等设计决策：丢弃（要计数）、阻塞（反压上游）、拒绝（让调用方决定）。

**Requires:** [[domains/python/map/concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]], [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Cards (5)
1. [[craft-backpressure-overflow-policy-1-three-answers-to-full]]
2. [[craft-backpressure-overflow-policy-2-drop-must-be-visible]]
3. [[craft-backpressure-overflow-policy-3-block-releases-lock]]
4. [[craft-backpressure-overflow-policy-4-what-to-drop]]
5. [[craft-backpressure-overflow-policy-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
