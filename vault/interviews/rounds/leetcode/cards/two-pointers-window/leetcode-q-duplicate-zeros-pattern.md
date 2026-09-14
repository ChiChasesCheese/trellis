---
id: leetcode-q-duplicate-zeros-pattern
node: two-pointers-window.two-pointers
type: qa
anki: 1787175409784
tags: [lc::1089, leetcode, pattern, recall]
---
## Q
数组原地覆写类问题（如复制0并右移），为什么要从后往前遍历？

## A
先统计需要插入的总位移量（如zeros数量），再从数组末尾往前遍历赋值。因为从前往后写会覆盖尚未读取的原始数据，而从后往前写时，写入位置(i+偏移量)总是大于等于读取位置i，不会破坏还没处理的数据。这是原地数组变形题的通用技巧（双指针/无额外空间）。

**Evidence**

```
zeros = arr.count(0)
n = len(arr)
for i in range(n - 1, -1, -1):
    if i + zeros < n:
        arr[i + zeros] = arr[i]
    if arr[i] == 0:
        zeros -= 1
        if i + zeros < n:
            arr[i + zeros] = 0
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1089%20-%20Duplicate%20Zeros)
