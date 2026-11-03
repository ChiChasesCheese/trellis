%% trellis:begin %%
# 标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`
*解释器与执行模型*

建立"该去哪个模块找"的索引：`deque`/`Counter`/`defaultdict`、堆与二分、时区感知的 datetime、pickle 的安全边界与 `copyreg`、logging 的层级与处理器。

**Unlocks:** [[domains/python/map/craft.patterns.lazy-deletion-heap|惰性删除堆：墓碑 + 压实（lazy deletion with tombstones and compaction）]], [[domains/python/map/craft.patterns.hash-map-plus-ordered-structure|哈希表 + 有序结构：O(1) 定位，O(log n) 或 O(1) 取序]], [[domains/python/map/craft.patterns.dependency-graph-cycle-detection|依赖图与环检测：拓扑排序、可达性、祖先链]], [[domains/python/map/craft.patterns.effective-dated-versions|生效时间版本表：按事件发生时刻取规则（effective-dated lookup）]], [[domains/python/map/craft.idioms.heapq-tuple-ordering|heapq 的元组序与 tie-break：计数器、负号、dataclass(order=True)]], [[domains/python/map/craft.idioms.time-types|时间类型选型：monotonic / aware datetime / 整数时间戳]], [[domains/python/map/craft.idioms.bisect-sorted-lists|bisect 与有序列表：floor/ceiling、key=、只查邻居]], [[domains/python/map/craft.idioms.bounded-deque|deque(maxlen) 做有界历史；list 头部删除是 O(n)]]

## Readings
- [[effective-04-dictionaries|Effective Python 3e · 第 4 章 字典]]
- [[effective-12-data-structures-algorithms|Effective Python 3e · 第 12 章 数据结构与算法]]
- [[pydocs-bisect-module|bisect 模块：有序数组二分查找]]
- [[pydocs-collections-module|collections 模块：专用容器数据类型]]
- [[pydocs-datetime-module|datetime 模块：日期时间完整参考]]
- [[pydocs-heapq-module|heapq 模块：堆队列算法]]
- [[pydocs-pickle-module|pickle 模块：Python 对象序列化]]

## Cards (6)
1. [[bisect-left-vs-right-insertion-point]]
2. [[datetime-naive-vs-aware]]
3. [[defaultdict-factory-only-via-missing]]
4. [[deque-vs-list-both-end-ops]]
5. [[heapq-default-is-min-heap]]
6. [[pickle-untrusted-data-is-code-execution-risk]]
%% trellis:end %%

## Notes
