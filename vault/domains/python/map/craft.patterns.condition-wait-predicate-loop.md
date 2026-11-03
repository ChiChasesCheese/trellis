%% trellis:begin %%
# 条件变量：谓词 while 循环 + 精确通知（Condition wait loop）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

等待永远写成 `while 谓词不成立: cond.wait()`；两类等待者各配一个 Condition；超时用绝对截止时间。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]]

## Cards (5)
1. [[craft-condition-wait-predicate-loop-1-while-not-if]]
2. [[craft-condition-wait-predicate-loop-2-two-conditions]]
3. [[craft-condition-wait-predicate-loop-3-close-notify-all]]
4. [[craft-condition-wait-predicate-loop-4-predicate-across-problems]]
5. [[craft-condition-wait-predicate-loop-5-scales-backpressure]]
%% trellis:end %%

## Notes
