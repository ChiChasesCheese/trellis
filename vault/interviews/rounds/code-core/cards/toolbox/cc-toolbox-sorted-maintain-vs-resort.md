---
id: cc-toolbox-sorted-maintain-vs-resort
node: toolbox.sorted
type: qa
---
## Q
A leaderboard changes after every event, and the top entry is read after every event too. Re-sort, or maintain?

## A
**Choose by which operation the spec repeats.** Re-sorting is O(n log n) per event → O(m·n log n) overall, and that is the single most common timeout shape in a timed round.

- Only the extreme is read → a heap, O(log n) per update ([[cc-toolbox-heap-lazy-invalidation]]).
- Rank or range queries are read → keep the list sorted with `bisect`/`insort`, or a Fenwick tree once n and m are both large ([[cc-toolbox-sorted-insort-cost]]).
- Everything is read, but rarely → collect into a plain list and sort **once**, at output time.
- The whole collection is read after every event → you cannot beat O(n) per event anyway, so a re-sort of an almost-sorted list is fine.

Decide before writing the loop; retrofitting the structure afterwards costs more minutes than choosing did ([[cc-algorithms-recognition-optimize-hot-operation]]).

## Q zh
排行榜在每个事件后都变化，而榜首也在每个事件后被读取。重排还是维护？

## A zh
**按 spec 重复执行的那个操作来选。** 每个事件重排是 O(n log n) → 整体 O(m·n log n)，这是限时轮次里最常见的超时形态。

- 只读极值 → 用堆，每次更新 O(log n)（[[cc-toolbox-heap-lazy-invalidation]]）。
- 读的是名次或区间查询 → 用 `bisect`/`insort` 维护有序列表，n 和 m 都很大时用树状数组（[[cc-toolbox-sorted-insort-cost]]）。
- 全量读取但很少发生 → 收进普通 list，在输出时**只排一次**。
- 每个事件后都要读整个集合 → 反正每事件都逃不掉 O(n)，那么对近乎有序的列表重排是可以的。

在写循环之前就决定；事后改结构花的时间比当初选它多得多（[[cc-algorithms-recognition-optimize-hot-operation]]）。
