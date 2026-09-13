---
id: leetcode-q-construct-binary-tree-from-preorder-and-inorder-traversal-mistake
node: trees.binary-tree
type: qa
anki: 1787613690716
tags: [lc::105, leetcode, mistake, recall]
---
## Q
为什么 buildTree0 版本(用 inorder.index() 和数组切片)在这类重建二叉树问题里是错误/低效的写法？

## A
inorder.index(mid) 每次都是 O(n) 线性查找，且每层递归都对 preorder/inorder 做切片(left_in、right_in、left_pre、right_pre)，切片本身也是 O(n)，导致整体复杂度退化为 O(n²)。正确做法是预先建 val→idx 哈希表把查找降到 O(1)，并用下标区间代替真正的数组切片，从而做到 O(n)。

**Evidence**

buildTree0 中的注释："每层都在切片 复杂度 n**2 => 优化用 hash"，且代码里确实用了 inorder.index(mid) 以及 inorder[:idx]/inorder[idx+1:]/preorder[1:1+l_len] 等多处切片。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F105%20-%20Construct%20Binary%20Tree%20from%20Preorder%20and%20Inorder%20Traversal)
