%% trellis:begin %%
# 数据驱动的分派表：operator 表、方向表、转换表
*编码功力（Coding Craft） / 高级写法（Idioms）*

把「若干 if 分支」写成 dict：_OPS、_DIRECTIONS、TRANSITIONS、CANCELLABLE_BY、PolicyTable.overrides。

**Requires:** [[domains/python/map/functions.first-class|一等函数：作为对象传递、高阶函数与 lambda]], [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[domains/python/map/functions.functools|`functools`：`lru_cache`、`partial`、`singledispatch`、`cached_property`]]

## Cards (5)
1. [[craft-dispatch-tables-1-operator-table]]
2. [[craft-dispatch-tables-2-direction-table]]
3. [[craft-dispatch-tables-3-transition-table]]
4. [[craft-dispatch-tables-4-specificity-fallback]]
5. [[craft-dispatch-tables-5-scales-rules-as-data]]
%% trellis:end %%

## Notes
