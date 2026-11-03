%% trellis:begin %%
# 只追加日志 + 派生状态：事实不可变，余额/视图可重算（event-sourced state）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

只存事实（分录、事件、时间点），余额、剩余额度、人数、应付金额都从事实现算或随写入同步更新。

**Requires:** [[domains/python/map/engineering.serialization|序列化：`json`、`pickle` 的安全与版本、`copyreg` 与 dataclass 的转换]], [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]

## Cards (5)
1. [[craft-append-only-log-derived-state-1-facts-not-totals]]
2. [[craft-append-only-log-derived-state-2-journal-and-index]]
3. [[craft-append-only-log-derived-state-3-across-problems]]
4. [[craft-append-only-log-derived-state-4-read-cost]]
5. [[craft-append-only-log-derived-state-5-scales-event-sourcing]]
%% trellis:end %%

## Notes
