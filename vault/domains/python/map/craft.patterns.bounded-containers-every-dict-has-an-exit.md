%% trellis:begin %%
# 每个只增不减的容器都要有出口：purge / sweep / compact / maxlen
*编码功力（Coding Craft） / 跨题模式（Patterns）*

任何随 key 数、请求数增长的容器都要有回收机制和可观测的大小指标，否则是保证会发生的 OOM。

**Requires:** [[domains/python/map/memory.leaks-tracemalloc|长驻进程的内存泄漏：来源、`tracemalloc` 与 `gc.get_referrers`]], [[domains/python/map/memory.weakref|弱引用：`weakref`、`WeakValueDictionary` 与缓存]], [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]]

## Cards (5)
1. [[craft-bounded-containers-every-dict-has-an-exit-1-abandoned-keys]]
2. [[craft-bounded-containers-every-dict-has-an-exit-2-amortized-trigger]]
3. [[craft-bounded-containers-every-dict-has-an-exit-3-orphaned-secondary-index]]
4. [[craft-bounded-containers-every-dict-has-an-exit-4-ghost-cursor]]
5. [[craft-bounded-containers-every-dict-has-an-exit-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
