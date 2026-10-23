---
id: hl-cache-pointer-chasing-sum
node: foundations.cpu-cache-locality
type: qa
step: 15
---
## Q
对 10⁷ 个元素求和，`long[]`、按分配顺序的 `ArrayList<Long>`、被打乱的 `ArrayList<Long>` 各耗时多少？这个实验的陷阱是什么？

## A
- `long[]`：2.09 ms（0.21 ns/元素）。顺序读，预取器全程命中，还可能被 JIT 向量化。
- `ArrayList<Long>`（分配顺序）：2.98 ms（0.30 ns），只慢 1.4 倍。**这是陷阱**：JVM 给每线程一块私有分配缓冲（TLAB），`new Long` 就是指针递增，连续创建的对象恰好紧挨着，访问地址仍顺序。
- `ArrayList<Long>`（打乱）：34.01 ms（3.40 ns），是 `long[]` 的 **16 倍**。这才是真实系统：对象经历多次 GC 搬移、由不同代码在不同时间创建，物理顺序与逻辑顺序几乎无关，每次访问都是随机缓存缺失。

原因：遍历要先读引用、再跳到那个地址，第二步的地址取决于第一步的结果，CPU 无法预取。
