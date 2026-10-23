---
id: hl-cache-hierarchy
node: foundations.cpu-cache-locality
type: qa
step: 3
---
## Q
内存层级（memory hierarchy）从寄存器到 DRAM 各层的容量和延迟大致是多少？

## A
- 寄存器（registers）：约几百字节，≤ 1 周期；
- L1 缓存：每核 32–128 KB，约 4 周期（约 1 ns）；
- L2 缓存：每核或每簇 256 KB–20 MB，约 12–15 周期（约 3–7 ns）；
- L3 / 系统级缓存：几 MB 到几十 MB，约 40 周期（约 10–15 ns）；
- 主内存 DRAM：GB 级，约 100 ns；
- SSD / 磁盘 / 网络：微秒到毫秒。

从上到下速度越来越慢、容量越来越大、单价越来越便宜。面试记量级：L1 约 1 ns、L2 约几 ns、L3 约 10 ns、DRAM 约 100 ns。
