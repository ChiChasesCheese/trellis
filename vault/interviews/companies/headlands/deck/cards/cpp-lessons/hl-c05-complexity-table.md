---
id: hl-c05-complexity-table
node: cpp-lessons.c05-stl-containers
type: qa
step: 3
---
## Q
`vector`、`deque`、`list`、`map`/`set`、`unordered_map`/`set`、`array` 的内存布局和主要操作复杂度分别是什么？

## A
- `vector`：一整块连续内存；随机访问 O(1)；尾插摊销 O(1)；中间插删 O(n) 搬移；查找 O(n)，有序时二分 O(log n)。
- `deque`：固定大小块的数组；随机访问 O(1)；首尾摊销 O(1)；中间 O(n)。
- `list`：双向链表节点；不能随机访问；尾插 O(1)；已有迭代器时中间插删 O(1)；查找 O(n)。
- `map`/`set`：红黑树节点；插入、删除、查找都 O(log n)，可有序遍历。
- `unordered_map`/`set`：桶数组 + 链；插入、删除、查找平均 O(1)，最坏 O(n)。
- `array`：内联，大小固定；随机访问 O(1)。
