---
id: hl-j17-why-offheap-answer
node: java21.j17-ffm-api
type: qa
step: 22
---
## Q
面试问：「为什么用堆外内存做这个哈希表？」
(Why use off-heap memory for this hash map?) 怎么答？

## A
答案骨架：
- **GC 完全看不见**：不管表有多大，GC 扫描/整理的工作量都不变，低延迟系统避免 GC 抖动的常见手段；
- **布局连续并对齐缓存行**（`allocate(size, 64)`）；
- 可换成共享内存。

代价要说：**手动 `close()`**、**固定容量**（没有自动扩容，超过就报错）、**每次访问有边界检查**（JIT 能消掉大部分）。

版本：「JDK 21 里 FFM 还是预览，22 转正，生产环境我会先评估版本。」
