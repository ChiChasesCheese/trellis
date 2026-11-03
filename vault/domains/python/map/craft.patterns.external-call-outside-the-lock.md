%% trellis:begin %%
# 外部调用不持锁：占位 → 调用 → 提交（claim, call, commit）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

慢 IO（支付、风控、回源、下游服务）永远在锁外；前后两段持锁，中间用租约/占位保证窗口内不被抢。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]]

## Cards (5)
1. [[craft-external-call-outside-the-lock-1-claim-call-commit]]
2. [[craft-external-call-outside-the-lock-2-window-must-be-recoverable]]
3. [[craft-external-call-outside-the-lock-3-logger-put-deadlock]]
4. [[craft-external-call-outside-the-lock-4-across-problems]]
5. [[craft-external-call-outside-the-lock-5-scales-no-http-in-transaction]]
%% trellis:end %%

## Notes
