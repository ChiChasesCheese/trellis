---
id: hl-javaq-d-q17-numbers
node: java-questions.d-memory
type: qa
step: 25
---
## Q
对 1200 万个元素求和，`long[]`、按分配顺序遍历的 `Long[]`、打乱引用顺序的 `Long[]` 各约多少毫秒？这解释了 Java 集合的什么现象？

## A
- 第 1 次：`long[]` 约 **2 ms**，`Long[]`（分配顺序）约 3 ms，`Long[]`（打乱）约 **34 ms**。
- 第 2 次：8 ms / 7 ms / **29 ms**。
- `Long[]` 按**分配顺序**遍历时，对象本来就连续放（TLAB 指针碰撞），所以接近 `long[]`；**打乱后慢约 10 倍**。
- 这解释了为什么 Java 的 `HashMap`、`LinkedList`、`TreeMap` 在大数据量下比 C++ 同类慢——节点散落在堆里。
- GC 压缩 / 复制后对象邻近关系可能变化，对遍历有利或不利，不要承诺。
