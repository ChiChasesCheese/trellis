---
id: hft-java-tuning-hugepages
node: java.tuning
type: qa
step: 2
---
## Q
为什么把 JVM 堆放在大页（huge pages）上能降低延迟？怎么开启？

## A
默认内存页是 4 KB。CPU 用 **TLB**（地址翻译缓存）缓存“虚拟地址到物理地址”的映射，而 TLB 的条目数有限（几十到几千）。8 GB 的堆有 8 GB / 4 KB ≈ 200 万个页，TLB 经常未命中，每次未命中要走多级页表，可能多次访问内存。换成 2 MB 的大页，8 GB 只需 4096 个页，TLB 命中率大幅提高。

开启方式：
- `-XX:+UseLargePages`：用显式预留的大页，需要操作系统先预留（`vm.nr_hugepages`），行为最可预测；
- `-XX:+UseTransparentHugePages`：由内核透明合并大页，省事，但内核后台合并和整理页可能引起不可预测的停顿，有些低延迟场景会关掉它。
