---
id: tlc-tt-contiguous-memory-allocator-4-followup
node: p4.tt-contiguous-memory-allocator
type: qa
step: 4
---
## Q
**连续内存分配器**｜追问

连续内存分配器已经支持 first-fit、释放时合并、对齐、非法释放检测。面试官接着问：（1）加 `realloc(addr, new_size)`？（2）线程安全？（3）改成 best-fit 或伙伴系统？（4）新毕业生笔试版：每次分配有编号，`erase(id)` 释放该编号的所有块？

## A
1. **`realloc`**：先看 `addr` 后面紧挨着的空闲块够不够把块扩到 `new_size`，够就原地扩（切分那个空闲块、更新 `used[addr]`）；缩小就把尾部还给空闲列表并向右合并；都不行就 `alloc` 新块、拷贝数据、`free` 旧块，失败时旧块保持不变。
2. **线程安全**：所有公开方法持同一把 `threading.Lock`，`alloc` 与 `free` 的“检查加修改”必须在同一个临界区里；吞吐不够，按大小分级拆成多个独立分配器，各自一把锁。
3. **其他策略**：best-fit 选最小的够用块（碎片更少，但要扫描整个列表），worst-fit 选最大的；伙伴系统（buddy system）把块大小限定为 `2` 的幂，释放时只检查它的“伙伴”是否空闲，合并是 `O(1)`，代价是内部碎片。
4. **`alloc x` / `erase id` 版本**：记 `owner: dict[int, list[int]]`，`alloc` 时把返回的地址追加到这个编号名下，`erase(id)` 对该编号的每个地址调用 `free`，返回释放了多少个单元（LC 2502）。要求起始地址是 `8` 的倍数就是 `alignment = 8`。

**Python 提醒**：`free_list[idx:idx + 1] = pieces` 切片赋值可以用零到多个元素替换一个元素；列表的 `insert`、`pop(i)` 是 `O(n)`，空闲块非常多时换成 `sortedcontainers.SortedList` 或平衡树，`bisect` 本身只在已排序的列表上有意义。
