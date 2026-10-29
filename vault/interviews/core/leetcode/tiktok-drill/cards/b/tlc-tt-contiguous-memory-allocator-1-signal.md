---
id: tlc-tt-contiguous-memory-allocator-1-signal
node: b.tt-contiguous-memory-allocator
type: qa
step: 1
---
## Q
**连续内存分配器**｜Medium · TikTok 高频

实现管理连续地址空间 `[0, capacity)` 的分配器：`alloc(size)` 用 first-fit（最左能放下的空闲块）分配，返回起始地址，`size` 为 `0`、负数或大于 `capacity` 抛 `ValueError`，放不下返回 `-1`；`free(addr)` 释放该次分配，并与相邻空闲块合并，对已释放或从未分配的地址抛 `ValueError`。可选 `alignment`：地址必须是它的倍数。`1 <= capacity <= 10^9`，最多 `10^5` 次操作。例：`capacity = 10`，`alloc(3)`、`alloc(4)`、`alloc(2)` → `0, 3, 7`，`alloc(2)` → `-1`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「first-fit、释放后合并相邻空闲块」→ 空闲区间列表（free list）：按起始地址排序，只存空闲区间。
- `capacity` 到 `10^9`：不能逐单元标记，状态必须与“块的个数”成正比，不与容量成正比。
- 「double free、非法地址要报错」→ 另用字典登记已分配块（起始地址 → 大小），释放前先校验。
- 「释放要合并」→ 有序结构上二分定位，只看左右两个邻居是否紧挨；列表始终保持“互不相邻”。
- 「地址对齐」→ 分配时把块首向上取整到 `alignment` 的倍数，被跳过的空隙仍是空闲块。

**推导链。**
1. 暴力：长度 `capacity` 的数组逐格标记，`alloc` 线性找连续空闲段，`O(capacity)`，`10^9` 不可行。
2. 浪费：大段连续的空闲或占用都被逐格存储。
3. 洞察：只存空闲区间；`alloc` 扫区间列表，取第一个够用的并切分；`free` 用 `bisect` 定位，与左右邻居合并。
4. 最优：`alloc` 为 `O(F)`，`free` 为 `O(log F)` 定位加列表插入，`F` 是空闲块数。

**同模式的题**：LC 2502 设计内存分配器、LC 705 设计哈希集合、LC 981 基于时间的键值存储、LC 56 合并区间。
