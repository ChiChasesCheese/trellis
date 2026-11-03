%% trellis:begin %%
# 确定性 tie-break：排序键里写全规则，输出可复现
*编码功力（Coding Craft） / 跨题模式（Patterns）*

所有「选一个」的地方都把平局规则写进键：(-可售数, 仓库名)、(容量, 桌号)、(到期时间, 发放时间, id)、首次出现序号。

**Requires:** [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]]

## Cards (5)
1. [[craft-deterministic-tie-break-1-sets-are-not-ordered]]
2. [[craft-deterministic-tie-break-2-tuple-keys]]
3. [[craft-deterministic-tie-break-3-heap-sequence]]
4. [[craft-deterministic-tie-break-4-stable-is-not-deterministic]]
5. [[craft-deterministic-tie-break-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
