---
id: leetcode-c-roaring-bitmap-containers-application
node: topics.uncategorised
type: qa
anki: 1787361365097
tags: [algorithm::bitset, algorithm::container-switching, algorithm::popcount, algorithm::set-algebra, application, case, case::roaring-bitmap-containers, category::runtimes-os, chapter::05, chapter::08, chapter::16, leetcode, system::roaringbitmap]
---
## Q
Roaring Bitmap 为什么同时需要 array、bitmap 和 run containers？

## A
稀疏块用有序 array 更省空间，稠密块用 bitmap 让 AND/OR/popcount 按机器字并行，连续区间用 run container 压缩。高位 key 先定位同一块，再做容器级集合运算。

**Evidence**

Roaring 官方格式规范定义高位分块及 array、bitmap、run containers 的编码与集合语义。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FRoaring%20Bitmap%EF%BC%9A%E5%88%86%E5%9D%97%E5%8E%8B%E7%BC%A9%E4%B8%8E%E9%9B%86%E5%90%88%E4%BD%8D%E8%BF%90%E7%AE%97)
