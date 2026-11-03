%% trellis:begin %%
# 转移表状态机：把「哪个状态能去哪」写成数据（State machine as a table）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

合法转移是一张表，非法转移统一拒绝；表有三种编码，守卫（数据够不够）与转移（流程合不合法）分开。

**Requires:** [[domains/python/map/classes.enums|枚举（Enum）：`Enum`/`IntEnum`/`StrEnum`/`Flag`、`auto()` 与唯一性]], [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]

## Cards (5)
1. [[craft-transition-table-state-machine-1-table-instead-of-ifs]]
2. [[craft-transition-table-state-machine-2-guards-vs-table]]
3. [[craft-transition-table-state-machine-3-three-encodings]]
4. [[craft-transition-table-state-machine-4-assert-vs-raise]]
5. [[craft-transition-table-state-machine-5-scales-optimistic-cas]]
%% trellis:end %%

## Notes
