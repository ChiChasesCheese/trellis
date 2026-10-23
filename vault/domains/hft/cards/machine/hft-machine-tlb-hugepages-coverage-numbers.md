---
id: hft-machine-tlb-hugepages-coverage-numbers
node: machine.tlb-hugepages
type: qa
step: 2
---
## Q
用 4 KB 页时，一个核的 TLB 大约能"覆盖"多少内存？换成 2 MB 大页后又是多少？请用数字算一下。

## A
TLB 容量很小：一个核的 L1 TLB 约几十项，第二级 TLB 约 **1000–2000 项**（具体型号不同）。

一项翻译覆盖一页，所以覆盖范围 = 项数 × 页大小：
- 4 KB 页：1500 项 × 4 KB ≈ **6 MB**。
- 2 MB 大页（huge page）：1500 项 × 2 MB ≈ **3 GB**。

对比一下：一个 8 GB 的堆，用 4 KB 页要 8 GB / 4 KB ≈ **200 万页**，用 2 MB 页只要 **4096 页**。

意义：热数据只要超过 6 MB 左右，4 KB 页下随机访问就会频繁 TLB 未命中，每次额外页表遍历；改用大页后，同样的数据只占很少几项，几乎不再未命中。订单簿、行情缓冲、大堆内存都常常超过 6 MB，所以大页对 HFT 有实际收益。
