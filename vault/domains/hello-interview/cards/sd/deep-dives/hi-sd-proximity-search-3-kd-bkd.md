---
id: hi-sd-proximity-search-3-kd-bkd
node: qb.sd.driver-heatmap-backend.pre-sd-deep-dives-proximity-search
type: qa
step: 3
---
## Q
**k-d 树与 BKD 树**｜系统设计 · 深入专题

k-d 树相对四叉树的关键改进是什么？BKD 树又解决了什么，Elasticsearch 用的是哪个？

## A
**k-d 树。** 逐层交替按 x、y 切分，在中位数处切，成为平衡的二叉树。关键差别：每次切分减半的是点数而不是面积。10 个司机里 9 个挤在东边，四叉树的第一刀落在几何中点，把一个孤零零的司机和 9 个挤在一起的人分开，还得反复切；k-d 树在中位数处切，两边各 5 个，深度恒为 log n。

**遗留问题。** 仍是指针结构，没法对应磁盘页。

**BKD 树。** 块 k-d 树：点打包成磁盘页大小的块，一次性对一批数据建好，基本是一次写入、不再改动。Elasticsearch 的地理字段用的就是它。

**易错。** 正因为基本不可变，它不擅长持续移动的数据。
