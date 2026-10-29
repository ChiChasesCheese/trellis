---
id: uth-storage-inverted-index-3-term-dict
node: storage.inverted-index
type: qa
step: 3
---
## Q
**词典：从 FST 到前缀树**｜Lucene · 10.5

几千万个词怎么快速查到它的列表位置？Lucene 的词典索引不只是个排序数组吗？

## A
**结构。** 词典分块存在 `.tim`（默认每块 25–48 个词），索引 `.tip` 只记各块的前缀。Lucene 10.2 及之前它是 FST（有限状态转换器，finite state transducer）：把共享前缀、后缀的词压成自动机，输出块的文件位置；10.3 起换成专用前缀树（trie）。

**细节。**

- FST 要求词按序输入，建出的是最小自动机。
- 查询时一个字节一个字节地沿边走，代价只与词长有关，与词的个数无关。

**为什么。** 比排序数组少了整词比较，比哈希表多了有序性，能做前缀查找。

**对应 LeetCode：** LC 208 实现 Trie (前缀树) · LC 720 词典中最长的单词
