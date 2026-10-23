---
id: hl-cx-space-complexity
node: foundations.complexity
type: qa
step: 28
---
## Q
空间复杂度（space complexity）怎么算？递归占多少空间？举时间换空间的例子。

## A
空间复杂度指**额外**用的内存，同样用 Big-O：`sum(int[] a)` 只用几个变量，O(1)；复制数组 O(n)；建 `HashMap` 存 n 个元素 O(n)。

递归的空间：每层递归占一个栈帧，深度 d 占 O(d) 栈。二分查找的递归写法深度 log n，空间 O(log n)；朴素链表递归到 10⁵ 层可能 `StackOverflowError`。

时间和空间常常互换：`HashMap` 多花 O(n) 空间，换来 O(n²) → O(n) 的时间。
