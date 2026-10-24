---
id: tlc-design-memory-allocator-3-why
node: b.design-memory-allocator
type: qa
step: 3
---
## Q
**LC 2502 设计内存分配器**｜正确性

`allocate` 里「`run` 在遇到占用单元时清零，第一次 `run == size` 就返回」为什么刚好得到最左侧的块？同一个 `mID` 为什么必须全表扫描释放？

## A
**不变量。** 扫描到下标 `i` 时，`run` 等于以 `i` 结尾的最长连续空闲段的长度（`i` 被占用则为 `0`）。

**为什么是最左。** 块 `[s, s + size - 1]` 全空闲当且仅当扫到 `i = s + size - 1` 时 `run >= size`。从左往右扫，`run` 第一次等于 `size` 的 `i` 对应的块，其起点 `i - size + 1` 是所有满足条件的块中最小的。后面更靠右的块都在它之后才会被扫到。

**为什么必须扫全表释放。** 同一个 `mID` 可以通过多次 `allocate` 占用互不相邻的多个块，数组里没有「这个 `mID` 的块列表」，所以需要全表过滤；（想 `O(块数)` 就要额外维护 `mID -> 块列表`）。

**反例。**
- 只释放第一个块：`Allocator(5)`，依次 `allocate(1,1)`、`allocate(1,2)`、`allocate(1,1)`，`freeMemory(1)`：内存是 `[1,2,1,0,0]`，应释放 `2` 个，只释放第一块得 `1`。
- 最佳适配：`Allocator(5)`，`allocate(3,1)` → `0`，`allocate(1,2)` → `3`，`freeMemory(1)` → `3`，此时空闲是下标 `0..2` 和 `4`；`allocate(1,3)` 最左是 `0`，最佳适配会选更小的空隙 `[4]` 返回 `4`。
