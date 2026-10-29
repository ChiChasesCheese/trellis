---
id: uth-devtools-compression-1-deflate
node: devtools.compression
type: qa
step: 1
---
## Q
**gzip 的 DEFLATE：LZ77 加哈夫曼**｜zlib · 1.3.2

gzip 怎么把重复的文本压小？

## A
**结构。** DEFLATE（RFC 1951）分两步：LZ77 在最近 32 KB 的窗口里找重复串，换成（距离，长度）；再用哈夫曼编码压缩字面量和这些（距离，长度）。

**细节。**

- 距离 1 到 32768，长度 3 到 258，哈夫曼码长最多 15 位
- zlib 用哈希链找匹配：以 3 字节为键的哈希表，同键的位置串成链
- 默认级别 6 最多沿链找 128 个候选，级别 9 是 4096，所以更慢更省

**为什么。** 窗口小，匹配找得快、内存少，代价是看不到更远的重复。

**对应 LeetCode：** LC 187 重复的DNA序列 · LC 1044 最长重复子串
