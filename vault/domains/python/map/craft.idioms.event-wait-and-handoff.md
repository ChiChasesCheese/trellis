%% trellis:begin %%
# Event / Condition 的惯用法：中断式睡眠、结果交接、截止时间
*编码功力（Coding Craft） / 高级写法（Idioms）*

Event.wait(interval) 当可中断的 sleep；一次性结果交接用 Event；等待永远写 while 谓词 + 剩余时间。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]], [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]]

## Cards (5)
1. [[craft-event-wait-and-handoff-1-interruptible-sleep]]
2. [[craft-event-wait-and-handoff-2-leader-sets-after-result]]
3. [[craft-event-wait-and-handoff-3-deadline-not-timeout]]
4. [[craft-event-wait-and-handoff-4-across-problems]]
5. [[craft-event-wait-and-handoff-5-scales-long-poll]]
%% trellis:end %%

## Notes
