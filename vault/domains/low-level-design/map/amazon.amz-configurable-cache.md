%% trellis:begin %%
# 可配置缓存（Configurable Cache）
*Amazon 专项（Amazon OOD）*

淘汰策略（LRU / LFU）与存储后端（内存、文件）可互换：两条独立变化的轴。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.strategy|策略模式与可替换算法（Strategy）]], [[domains/low-level-design/map/patterns.structural|结构型模式（Structural）]]

## Readings
- [[solution-amz-configurable-cache|设计题解：可配置缓存（Configurable Cache）]]
- [[src-1p3a-amz-configurable-cache|一亩三分地：Amazon SDE II 电面（第一题 LRU 缓存）]]
- [[src-hellointerview-amz-configurable-cache|Hello Interview 社区题库：Amazon（题目 configurable-cache-design）]]
- [[src-pythondocs-amz-configurable-cache|collections — OrderedDict objects（Python 标准库文档）]]

## Drills
- [[design-amz-configurable-cache|Drill：可配置缓存（Configurable Cache）]]

## Cards (9)
1. [[amz-configurable-cache-prompt-and-three-questions]]
2. [[amz-configurable-cache-objects-and-one-job-each]]
3. [[amz-configurable-cache-stage1-put-flow-code]]
4. [[amz-configurable-cache-lfu-frequency-buckets]]
5. [[amz-configurable-cache-bridge-vs-subclass-explosion]]
6. [[amz-configurable-cache-followup-add-fifo-policy]]
7. [[amz-configurable-cache-failed-write-policy-store-disagree]]
8. [[amz-configurable-cache-concurrency-lock-covers-reads]]
9. [[amz-configurable-cache-lfu-new-key-evicted-immediately]]
%% trellis:end %%

## Notes
