---
id: uth-go-rust-modern-sorts-2-drift-ipn
node: go-rust.modern-sorts
type: qa
step: 2
---
## Q
**Rust 的 sort 与 sort_unstable 是什么算法**｜Rust · 1.81 起

Rust 1.81 换掉了标准库的排序，稳定与不稳定的分别是什么？

## A
**结构。** 稳定的 `sort` 是 driftsort；不稳定的 `sort_unstable` 是 ipnsort（快排加堆排序兜底）。

**细节。**

- driftsort：先找输入里已有的升序或降序段（run），按 powersort 的启发式决定归并顺序
- 无序的段交给稳定快排
- ipnsort：长度 ≤ 20 用插入排序；整个数组是一整段有序或逆序，就 O(n) 结束
- 否则快排，不平衡划分超过 `2·⌊log₂ n⌋` 次就改堆排序

**为什么。** 真实数据常常部分有序，利用已有的顺序比无视它更快。

**对应 LeetCode：** LC 56 合并区间 · LC 148 排序链表
