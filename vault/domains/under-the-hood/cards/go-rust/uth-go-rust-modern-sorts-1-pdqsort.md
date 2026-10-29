---
id: uth-go-rust-modern-sorts-1-pdqsort
node: go-rust.modern-sorts
type: qa
step: 1
---
## Q
**pdqsort 怎么躲开快排的最坏情况**｜Go · 1.19 起

`sort.Sort` 用的抗模式快排（pattern-defeating quicksort，pdqsort）比普通快排多做了什么？

## A
**结构。** 快速排序加一套“情况不对就换招”的检查，另有堆排序兜底。

**细节。**

- 长度 ≤ 12 用插入排序；长度 ≥ 50 用 Tukey ninther（九个数取中位数）选枢轴
- 划分后较短一侧不足 1/8，就随机交换几个元素打乱规律
- 不平衡划分累计超过 `bits.Len(n)` 次，改用堆排序
- 枢轴等于祖先枢轴时，一次把相等元素归到一边，应对大量重复值

**为什么。** 它识别已排序、逆序、大量重复这些常见输入模式并专门处理。

**对应 LeetCode：** LC 912 排序数组 · LC 75 颜色分类
