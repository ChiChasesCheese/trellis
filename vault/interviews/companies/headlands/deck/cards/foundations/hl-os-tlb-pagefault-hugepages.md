---
id: hl-os-tlb-pagefault-hugepages
node: foundations.os-processes-threads-ipc
type: qa
step: 6
---
## Q
TLB、缺页（minor / major fault）、大页（huge pages）各是什么？低延迟系统怎么用它们？

## A
- **TLB**（Translation Lookaside Buffer）是页表缓存；TLB 未命中要走页表，几十到上百周期。进程切换（换页表）会使 TLB 失效（或靠 ASID / PCID 标签避免全清）。
- **缺页**：访问还没映射的页，CPU 陷入内核。minor fault 内核分配物理页，微秒级；major fault 从磁盘读，毫秒级。首次访问新分配或新映射内存时触发，所以低延迟系统常在启动时把热内存「摸一遍」（pre-touch）。
- **大页**：Linux 页变大到 2 MB / 1 GB，同样的 TLB 条目覆盖更多内存，TLB 未命中大减。JVM 参数 `-XX:+UseTransparentHugePages` / `-XX:+UseLargePages`，交易系统常见。
