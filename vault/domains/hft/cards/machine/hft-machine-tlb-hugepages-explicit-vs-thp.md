---
id: hft-machine-tlb-hugepages-explicit-vs-thp
node: machine.tlb-hugepages
type: qa
step: 3
---
## Q
Linux 上显式大页（explicit huge pages）和透明大页（Transparent Huge Pages，THP）有什么区别？低延迟系统通常选哪个，为什么？

## A
两者都是让进程用 2 MB（或 1 GB）的页，区别在于由谁决定、什么时候分配。

| | 显式大页 | 透明大页（THP） |
|---|---|---|
| 分配 | 管理员提前预留（如 `vm.nr_hugepages`），程序主动申请（`hugetlbfs`） | 内核后台自动把相邻的 4 KB 页合并成 2 MB |
| 可预测性 | 启动时就占好，运行时不变 | 合并/拆分发生在运行时 |
| 能否被换出 | 不会被换出到磁盘 | 可能被拆分、换出 |

THP 的问题是：内核的后台线程（`khugepaged`）和缺页时的整理（compaction，挪动内存腾出连续的 2 MB）可能在交易途中让线程停顿**几毫秒**，造成延迟尖刺。

所以低延迟系统通常**显式预留大页**，并关闭或限制 THP。Java 里用 `-XX:+UseLargePages` 让堆使用显式大页。

代价：预留的内存不能挪作他用，大小要提前规划。
