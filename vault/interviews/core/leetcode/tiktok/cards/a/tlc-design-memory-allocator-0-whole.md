---
id: tlc-design-memory-allocator-0-whole
node: a.design-memory-allocator
type: qa
---
## Q
**LC 2502 设计内存分配器**｜Medium · LC TikTok 热度 46/100 · 近一年被问：美国 2 次、国内 0 次 · 最近 2026-06-11（面试记录）

给整数 `n`，表示下标从 `0` 开始的内存数组的大小，所有内存单元开始都空闲。设计一个内存分配器：**分配**一块大小为 `size` 的连续空闲内存单元并赋 id `mID`；**释放**给定 id `mID` 对应的所有内存单元。注意：多个块可以被分配到同一个 `mID`；你必须释放 `mID` 对应的所有内存单元，即使它们分布在不同的块中。

`Allocator(int n)` 初始化大小为 `n` 的内存数组；`int allocate(int size, int mID)` 找出大小为 `size` 个连续空闲单元且位于**最左侧**的块，分配并赋 id `mID`，返回块的第一个下标，不存在则返回 `-1`；`int freeMemory(int mID)` 释放 id 为 `mID` 的所有内存单元，返回释放的单元数。

约束：`1 <= n, size, mID <= 1000`，最多调用 `allocate` 和 `freeMemory` 共 `1000` 次。

例：`Allocator(10)`；`allocate(1,1)` → `0`；`allocate(1,2)` → `1`；`allocate(1,3)` → `2`；`freeMemory(2)` → `1`；`allocate(3,4)` → `3`；`allocate(1,1)` → `1`；`allocate(1,1)` → `6`；`freeMemory(1)` → `3`；`allocate(10,2)` → `-1`；`freeMemory(7)` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 直接用长度为 `n` 的数组表示内存，`0` 表示空闲、否则存 `mID`；`allocate` 扫描时统计当前连续空闲的长度，第一次达到 `size` 就是最左侧的块；`freeMemory` 扫描并清掉所有等于 `mID` 的单元。因为 `n` 和调用次数都只有 `1000`，`O(n)` 每次操作完全够用。

**识别。** 「设计一个内存 / 资源分配器」题先看规模：`n ≤ 1000`、调用 `≤ 1000` 次 → 朴素模拟 `O(n)` 每次，总共 `10^6`，是**期望的答案**；不要过度设计成线段树。面试官常常的下一问才是 `n` 很大时怎么办。信号：「最左侧」（first-fit，扫描时第一个够的就是）、「同一个 `mID` 可对应多个块」（释放要扫全体）。

**推导。** 朴素：数组 + 线性扫描。`allocate` 需要找第一个长度 `≥ size` 的连续空闲段：扫描时维护 `run`（当前连续空闲数），遇到非空闲清零，`run == size` 的那一刻，块的起点是 `i - size + 1`。`freeMemory` 扫全数组把 `mID` 的单元清零并计数。若 `n` 达到 `10^9`，数组放不下：改成**区间表示**，只存已分配块 `(起点, 终点, mID)`，按起点排序；`allocate` 在相邻块之间的空隙里找第一个够大的，`freeMemory` 过滤掉 `mID` 的块。复杂度取决于块的个数，而不是 `n`。

```python
class Allocator:
    def __init__(self, n: int) -> None:
        self.mem = [0] * n             # mem[i] 是占用该单元的 mID；mID >= 1，所以 0 表示空闲

    def allocate(self, size: int, mID: int) -> int:
        run = 0                        # 当前连续空闲单元的个数
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0
            if run == size:            # 第一次凑够 size 个，就是最左侧的块
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size   # 切片赋值，一次写入整块
                return start
        return -1

    def freeMemory(self, mID: int) -> int:
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:           # 同一个 mID 可能分散在多个块里，全部释放
                self.mem[i] = 0
                freed += 1
        return freed
```

运行：`示例的 11 个调用` → `[None, 0, 1, 2, 1, 3, 1, 6, 3, -1, 0]`，`n=5：同一 mID 分到两个块，再一次性释放` → `[None, 0, 2, 3, 4]`，`n=1000 一次占满，再分配 1 个` → `[None, 0, -1]`。

**复杂度。** `allocate` 与 `freeMemory` 都是 `O(n)`：一遍扫描整个数组；`1000` 次调用总计约 `10^6` 次单元访问。空间 `O(n)`。

**易错点。**
- 只释放第一个块：同一 `mID` 可能有多个块。`Allocator(5)`，`allocate(1,1)`、`allocate(1,2)`、`allocate(1,1)`，`freeMemory(1)` 应返回 `2`，只释放第一块得 `1`。
- 用最佳适配（挑最小的够用空隙）而不是最左：`Allocator(5)`，`allocate(3,1)`，`allocate(1,2)`，`freeMemory(1)`，`allocate(1,3)` 应返回 `0`（最左空闲），最佳适配会返回 `4`。
- 起点算错：第一次 `run == size` 的下标是块的**末尾** `i`，起点是 `i - size + 1`，写成 `i - size` 会错位一格。
- `size > n` 或没有足够长的空闲段：循环结束返回 `-1`，不能漏掉；`run` 要在遇到被占用的单元时清零，否则会把被占用单元隔开的两段空闲拼成一段。

**追问。**
- `n` 很大（`10^9`）而调用不多：改用区间表 `blocks`（按起点排序），`allocate` 扫描相邻块的空隙，`freeMemory` 过滤；时间 `O(块数)`，与 `n` 无关。
- 调用非常多、要求 `O(log n)`：线段树维护每段「最长连续空闲 / 前缀空闲 / 后缀空闲」，`allocate` 在树上找最左满足的位置；`freeMemory` 需要按 `mID` 记录块位置。
- 要支持碎片整理（compaction）或合并相邻空闲块：区间表里删除 / 插入后合并相邻空隙；数组版直接扫描即可。

**同模式。** LC 2276 统计区间中的整数数目、LC 715 Range 模块、LC 729 / 731 / 732 我的日程安排表、LC 146 LRU 缓存、LC 1146 快照数组。
