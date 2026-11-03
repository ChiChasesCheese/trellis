%% trellis:begin %%
# deque(maxlen) 做有界历史；list 头部删除是 O(n)
*编码功力（Coding Craft） / 高级写法（Idioms）*

死信、通知历史、失败记录、滑动窗口都用 deque(maxlen=N)：自动淘汰最旧，内存有上界。

**Requires:** [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]], [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]]

## Cards (5)
1. [[craft-bounded-deque-1-maxlen-is-the-exit]]
2. [[craft-bounded-deque-2-count-what-you-drop]]
3. [[craft-bounded-deque-3-sliding-window-incremental]]
4. [[craft-bounded-deque-4-deque-limits]]
5. [[craft-bounded-deque-5-scales-hit-counter-ring-buffer]]
%% trellis:end %%

## Notes
