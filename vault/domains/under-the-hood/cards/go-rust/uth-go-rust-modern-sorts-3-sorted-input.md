---
id: uth-go-rust-modern-sorts-3-sorted-input
node: go-rust.modern-sorts
type: qa
step: 3
---
## Q
**对已经有序的数据排序有多快**｜Go / Rust · 现代标准库

给 100 万个已经升序或逆序的整数排序，要比较多少次？

## A
**结构。** pdqsort、driftsort、ipnsort 都先检测“输入已有序”，直接走 O(n) 的快路径。

**细节。**

- Rust 实测：升序、逆序的 `sort_by` 与 `sort_unstable_by` 都恰好 999999 次，即 n-1
- Go 实测：`sort.Slice` 升序、逆序都约 1000011 次
- Go 遇到逆序会先整体反转，再按有序处理

**为什么。** 检测只要扫一趟，却把常见的“已排好”场景降到线性；老式快排对有序输入可能退化到 O(n²)。

**坑。** Rust 1.81 起，比较函数不满足全序（total order）时，排序可能直接 panic，而不是悄悄返回乱序结果。

**对应 LeetCode：** LC 88 合并两个有序数组 · LC 912 排序数组
