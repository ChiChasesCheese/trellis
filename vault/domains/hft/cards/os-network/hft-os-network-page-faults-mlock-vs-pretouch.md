---
id: hft-os-network-page-faults-mlock-vs-pretouch
node: os-network.page-faults
type: qa
step: 3
---
## Q
预触内存之后，为什么还要用 `mlock` 锁住内存、关掉交换（swap）？两者分别防的是什么？

## A
两者防的是缺页的两个不同原因：

- **预触**防的是"第一次访问"：内存还没分配时的缺页。做完之后，页都在物理内存里了。
- **`mlock` / `mlockall`** 防的是"被换出"：操作系统在物理内存紧张时，可能把很久没用的页写到磁盘上的交换区（swap），腾出空间给别人。后来你再访问这一页，就要触发主要缺页，从磁盘读回，耗时**毫秒**，对交易是灾难。`mlock` 告诉内核这些页永远留在物理内存，不许换出。

实践：
- C/C++：启动时 `mlockall(MCL_CURRENT | MCL_FUTURE)`，并确认进程的 `ulimit -l`（可锁内存上限）足够大；
- Java：没有直接的 `mlock`，通常用 `swapoff -a` 或把 `vm.swappiness` 设为 0，再配合预触；用显式大页（hugetlbfs）时，大页本身就不会被换出；
- 同样的思路适用于内存映射文件：先访问一遍，预先载入。

两者缺一不可：只预触，页仍可能被换出；只锁定，第一次访问仍会缺页。
