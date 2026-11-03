%% trellis:begin %%
# 重试、退避与死信：可靠性写一份，渠道只管怎么发
*编码功力（Coding Craft） / 跨题模式（Patterns）*

区分可重试与不可重试；指数退避带上限；重试用尽进死信；订阅者的故障不能拖垮发布者。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]], [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]]

## Cards (5)
1. [[craft-retry-backoff-dead-letter-1-backoff-as-pure-function]]
2. [[craft-retry-backoff-dead-letter-2-transient-vs-permanent]]
3. [[craft-retry-backoff-dead-letter-3-clock-not-sleep]]
4. [[craft-retry-backoff-dead-letter-4-dead-letter-is-a-record]]
5. [[craft-retry-backoff-dead-letter-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
