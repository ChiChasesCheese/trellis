# 二叉树 BFS 与 BST

层序遍历（BFS 的最简形态）和 BST 的有序性：中序有序、上下界验证、第 k 小。BST 的有序性和二分查找是同一个思想。

**先做（TikTok P1–P4 与经典题单，24 道）**

- [[lct-binary-tree-level-order-traversal|LC 102 二叉树的层序遍历]]（中等）· TikTok P1 · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-binary-tree-right-side-view|LC 199 二叉树的右视图]]（中等）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-all-nodes-distance-k-in-binary-tree|LC 863 二叉树中所有距离为 K 的结点]]（中等）· TikTok P1 · Amazon
- [[lct-lowest-common-ancestor-of-a-binary-tree|LC 236 二叉树的最近公共祖先]]（中等）· TikTok P2 · Amazon · LeetCode Hot 100 · Top Interview 150
- [[lct-serialize-and-deserialize-n-ary-tree|LC 428 序列化和反序列化 N 叉树]]（困难）· TikTok P2
- [[lct-serialize-and-deserialize-binary-tree|LC 297 二叉树的序列化与反序列化]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150
- [[lct-diameter-of-binary-tree|LC 543 二叉树的直径]]（简单）· TikTok P4 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-delete-node-in-a-bst|LC 450 删除二叉搜索树中的节点]]（中等）· TikTok P4
- [[lct-validate-binary-search-tree|LC 98 验证二叉搜索树]]（中等）· TikTok P4 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-amount-of-time-for-binary-tree-to-be-infected|LC 2385 感染二叉树需要的总时间]]（中等）· TikTok P4
- [[lct-populating-next-right-pointers-in-each-node|LC 116 填充每个节点的下一个右侧节点指针]]（中等）· TikTok P4 · Amazon
- [[lct-construct-binary-tree-from-preorder-and-postorder-traversal|LC 889 从前序与后序遍历序列构造二叉树]]（中等）· TikTok P4
- [[lct-create-binary-tree-from-descriptions|LC 2196 根据描述创建二叉树]]（中等）· TikTok P4
- [[lct-recover-binary-search-tree|LC 99 恢复二叉搜索树]]（中等）· TikTok P4
- [[lct-kth-smallest-element-in-a-bst|LC 230 二叉搜索树中第 K 小的元素]]（中等）· TikTok P4 · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-binary-tree-inorder-traversal|LC 94 二叉树的中序遍历]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- [[lct-binary-tree-zigzag-level-order-traversal|LC 103 二叉树的锯齿形层序遍历]]（中等）· TikTok B · Amazon · Top Interview 150
- [[lct-construct-binary-tree-from-preorder-and-inorder-traversal|LC 105 从前序与中序遍历序列构造二叉树]]（中等）· TikTok B · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-convert-sorted-array-to-binary-search-tree|LC 108 将有序数组转换为二叉搜索树]]（简单）· TikTok B · LeetCode Hot 100 · Top Interview 150
- [[lct-flatten-binary-tree-to-linked-list|LC 114 二叉树展开为链表]]（中等）· TikTok B · LeetCode Hot 100 · Top Interview 150
- LC 173 二叉搜索树迭代器（中等）· Top Interview 150
- [[lct-lowest-common-ancestor-of-a-binary-search-tree|LC 235 二叉搜索树的最近公共祖先]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150
- LC 530 二叉搜索树的最小绝对差（简单）· Top Interview 150
- LC 703 数据流中的第 K 大元素（简单）· NeetCode 150

**再做（其余牌组里的题，9 道）**

- [[lct-unique-binary-search-trees-ii|LC 95 不同的二叉搜索树 II]]（中等）· TikTok B
- [[lct-unique-binary-search-trees|LC 96 不同的二叉搜索树]]（中等）· TikTok B
- LC 109 有序链表转换二叉搜索树（中等）· Amazon
- [[lct-verify-preorder-sequence-in-binary-search-tree|LC 255 验证二叉搜索树的前序遍历序列]]（中等）· TikTok C
- [[lct-convert-binary-search-tree-to-sorted-doubly-linked-list|LC 426 将二叉搜索树转化为排序的双向链表]]（中等）· TikTok B
- [[lct-maximum-width-of-binary-tree|LC 662 二叉树最大宽度]]（中等）· TikTok B · Amazon
- [[lct-minimum-distance-between-bst-nodes|LC 783 二叉搜索树节点最小距离]]（简单）· TikTok B
- LC 1038 从二叉搜索树到更大和树（中等）· Amazon
- LC 1373 二叉搜索子树的最大键值和（困难）· Amazon
