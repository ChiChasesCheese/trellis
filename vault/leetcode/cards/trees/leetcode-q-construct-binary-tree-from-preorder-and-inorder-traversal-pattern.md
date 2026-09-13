---
id: leetcode-q-construct-binary-tree-from-preorder-and-inorder-traversal-pattern
node: trees.binary-tree
type: qa
anki: 1787613690616
tags: [lc::105, leetcode, pattern, recall]
---
## Q
如何用 O(n) 时间根据前序(preorder)和中序(inorder)遍历重建二叉树？

## A
用哈希表 val2idx 记录每个值在 inorder 中的下标(O(1)查找)，再用一个全局/闭包变量 pre_idx 顺序消费 preorder：每次递归取 preorder[pre_idx] 作为当前子树根，pre_idx += 1，然后用该值在 inorder 中的下标切分左右区间，先递归构建左子树、再构建右子树(顺序不能反，因为 preorder 是「根-左-右」，只有先走完左子树才会轮到右子树对应的值)。递归函数只传 (l, r) 区间下标，不传子数组，避免切片开销。

**Evidence**

def buildTree(...): val2idx = {val: idx for idx, val in enumerate(inorder)}; pre_idx = 0; def build(l, r): nonlocal pre_idx; ... mid = preorder[pre_idx]; pre_idx += 1 # 下面 build 先左后右，每次 build, global pre_idx += 1. 正好符合 preorder 顺序

[原文 ↗](obsidian://open?vault=lc&file=questions%2F105%20-%20Construct%20Binary%20Tree%20from%20Preorder%20and%20Inorder%20Traversal)
