---
id: cc-chrono-intervals-merge-sweep
node: chrono.intervals
type: qa
---
## Q
Up to 10^5 unsorted ranges must be merged into a minimal set. Write the loop, and say what changes on an integer domain.

## A
**Sort by start, then extend or emit.**

```python
out = []
for s, e in sorted(intervals):
    if out and s <= out[-1][1] + adj:      # adj=0: overlap only; adj=1: also adjacent
        out[-1][1] = max(out[-1][1], e)
    else:
        out.append([s, e])
```

- The `max` matters: a fully contained interval must not shrink the current one.
- On a continuous domain `[1,4]` and `[4,5]` touch and merge (`adj = 0`). On an **integer** domain `[1,4]` and `[5,9]` are adjacent with no integer between them — they merge only if the spec says so, which is `adj = 1`.
- Different labels do not merge even when they overlap; merge per label, or key the output by label.
- O(n log n), dominated by the sort. A pairwise "does this overlap anything" scan is O(n²) and times out at 10^5.

## Q zh
最多 10^5 个无序区间要合并成最简集合。写出循环，并说明在整数域上有什么不同。

## A zh
**按起点排序，然后扩展或新开一段。**

```python
out = []
for s, e in sorted(intervals):
    if out and s <= out[-1][1] + adj:      # adj=0：仅重叠；adj=1：相邻也算
        out[-1][1] = max(out[-1][1], e)
    else:
        out.append([s, e])
```

- `max` 很关键：被完全包含的区间不能把当前段缩短。
- 在连续域上 `[1,4]` 与 `[4,5]` 相接并合并（`adj = 0`）。在**整数**域上 `[1,4]` 与 `[5,9]` 之间没有整数，属于相邻 —— 只有 spec 这么规定时才合并，即 `adj = 1`。
- 标签不同的区间即使重叠也不合并；按标签分别合并，或让输出以标签为 key。
- O(n log n)，由排序主导。两两判断「是否与谁重叠」是 O(n²)，在 10^5 规模会超时。
