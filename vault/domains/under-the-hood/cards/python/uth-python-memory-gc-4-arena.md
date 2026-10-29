---
id: uth-python-memory-gc-4-arena
node: python.memory-gc
type: qa
step: 4
---
## Q
**del 之后内存为什么不降**｜Python · CPython 3.14.8

创建 200 万个小对象再 `del` 掉 99%，进程占用的内存会降多少？

## A
**结构。** 小对象归 pymalloc 管：64 位下向系统要 1 MiB 的竞技场（arena），切成 16 KiB 的内存页（pool）按大小分配。

**细节。**

- 实测 200 万个短字符串占 189 MB；只留 1%，其余 `del` 后仍是 189 MB。
- 剩下的也删掉，才降到 37 MB。
- 一个竞技场里只要还有一个活对象，整块就不能还给系统。

**为什么。** 整块腾空的竞技场才能归还系统；碎片化时空闲内存只留在进程里等着复用。

**对应 LeetCode：** LC 295 数据流的中位数 · LC 355 设计推特
