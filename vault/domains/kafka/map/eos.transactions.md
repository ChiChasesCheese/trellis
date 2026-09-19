%% trellis:begin %%
# 事务：应用场景、隔离与实现原理
*精确一次语义（exactly-once semantics）*

掌握事务如何跨多个分区实现原子写入、事务ID与隔离级别的作用，以及事务能解决与不能解决的问题。

**Core** — part of the first pass through this subject.

## Readings
- [[kafka-8-2-transactions|事务：跨分区的原子写入]]

## Cards (6)
1. [[kafka-eos-transactions-why-needed-duplicates]]
2. [[kafka-eos-transactions-atomic-multipartition-write]]
3. [[kafka-eos-transactions-two-phase-commit-mechanism]]
4. [[kafka-eos-transactions-zombie-fencing-epoch]]
5. [[kafka-eos-transactions-isolation-level-tradeoff]]
6. [[kafka-eos-transactions-external-side-effects-not-covered]]
%% trellis:end %%

## Notes
