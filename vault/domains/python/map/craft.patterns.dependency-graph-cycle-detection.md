%% trellis:begin %%
# 依赖图与环检测：拓扑排序、可达性、祖先链
*编码功力（Coding Craft） / 跨题模式（Patterns）*

依赖关系都是图：Kahn 算法给出执行序并报出具体的环；改动前用可达性拒绝成环的赋值；遍历时用祖先链检测环。

**Requires:** [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]], [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]]

## Cards (5)
1. [[craft-dependency-graph-cycle-detection-1-kahn-and-the-concrete-cycle]]
2. [[craft-dependency-graph-cycle-detection-2-check-before-mutate]]
3. [[craft-dependency-graph-cycle-detection-3-ancestors-not-visited]]
4. [[craft-dependency-graph-cycle-detection-4-recalc-once]]
5. [[craft-dependency-graph-cycle-detection-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
