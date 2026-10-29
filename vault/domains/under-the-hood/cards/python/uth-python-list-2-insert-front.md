---
id: uth-python-list-2-insert-front
node: python.list
type: qa
step: 2
---
## Q
**insert(0) 和 pop(0) 为什么慢**｜Python · CPython 3.14

在 100 万元素的 `list` 头部 `insert(0, x)` 再 `pop(0)`，比在尾部 `append` 再 `pop` 慢多少？

## A
**结构。** 数组必须保持连续，头部没有空位可用。

**细节。**

- `insert(0)` 把后面所有指针逐个后移一格；`pop(0)` 用一次 `memmove` 前移一格。都是 O(n)。
- 本机实测（100 万元素）：

```
insert(0)+pop(0)  约 226 微秒
append+pop        约 0.023 微秒
```

**为什么。** 数组换来了 O(1) 随机访问和紧凑内存，代价是头部操作线性。两端都要频繁操作就换 `collections.deque`。

**对应 LeetCode：** LC 283 移动零 · LC 622 设计循环队列
