---
id: cc-toolbox-sorted-insort-cost
node: toolbox.sorted
type: qa
---
## Q
Events arrive out of order and every read needs the list sorted. `insort` per event, or append-then-sort at each read?

## A
**`insort` finds the position in O(log n) but inserts in O(n)** — the shift is a fast memmove, so ~10^5 insertions are comfortable and 10^6 are not.

- Append plus `list.sort()` at read time is O(n log n) per read on paper, but Timsort is nearly linear on an already-sorted list with a short unsorted tail. That is the right shape when writes are bulk and reads are rare.
- If both are frequent at 10^6 scale, stop keeping a sorted list: a heap (when only the extreme is read), bucketing, or a Fenwick tree over compressed coordinates.
- Never call `sort()` **inside** the per-event loop — that is the quadratic-with-a-log version of the same bug ([[cc-toolbox-sorted-maintain-vs-resort]]).
- `insort` on a list of tuples compares the whole tuple, so the tie-break field must already be in it.

## Q zh
事件乱序到达，而每次读取都需要列表有序。是每个事件 `insort`，还是读的时候 append 再 sort？

## A zh
**`insort` 用 O(log n) 找位置，但插入是 O(n)** —— 移动是很快的 memmove，所以约 10^5 次插入很轻松，10^6 次就不行。

- 读时 append 加 `list.sort()` 理论上每次读 O(n log n)，但 Timsort 在「已排好序 + 一小段乱序尾巴」的列表上几乎是线性的。写入成批、读取稀少时这才是对的形态。
- 如果在 10^6 规模上读写都频繁，就别再维护有序列表：用堆（只读极值时）、分桶，或在压缩坐标上的树状数组。
- 绝不要在按事件的循环**内部**调用 `sort()` —— 那是同一个 bug 的「二次乘对数」版本（[[cc-toolbox-sorted-maintain-vs-resort]]）。
- 对 tuple 列表做 `insort` 会比较整个 tuple，所以 tie-break 字段必须已经在里面。
