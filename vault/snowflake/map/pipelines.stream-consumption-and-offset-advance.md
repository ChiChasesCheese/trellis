%% trellis:begin %%
# 偏移量仅在消费 DML 内前移
*流（Stream）、任务（Task）与动态表（Dynamic Table）*

为何偏移量只有在读取该 Stream 的事务同时提交时才会前移，这使得一个崩溃的消费者会重新尝试完全相同的一组变更。

**Requires:** [[pipelines.stream-offset-bookmark|作为偏移量书签的流（Stream）]]

## Readings
- [[snowflak-streams|流对象(Stream)的偏移量、类型与消费语义]]

## Cards (5)
- [[stream-advance-without-consuming]]
- [[stream-crash-before-commit-retries-same]]
- [[stream-explicit-txn-repeatable-read]]
- [[stream-read-committed-vs-repeatable-read]]
- [[stream-select-does-not-advance]]
%% trellis:end %%

## Notes
