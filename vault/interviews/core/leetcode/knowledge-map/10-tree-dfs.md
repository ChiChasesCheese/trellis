# 二叉树 DFS：递归的返回值

递归思维的主战场：后序返回子树信息（高度、路径和、是否平衡），前序向下传参数，全局量记录跨节点的答案。是回溯、树形 DP、图 DFS 的共同起点。

**先做（TikTok P1–P4 与经典题单，43 道）**

- [[lct-binary-tree-level-order-traversal|LC 102 二叉树的层序遍历]]（中等）· TikTok P1 · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-binary-tree-right-side-view|LC 199 二叉树的右视图]]（中等）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-path-sum-iii|LC 437 路径总和 III]]（中等）· TikTok P1 · Amazon · LeetCode Hot 100
- [[lct-all-nodes-distance-k-in-binary-tree|LC 863 二叉树中所有距离为 K 的结点]]（中等）· TikTok P1 · Amazon
- [[lct-lowest-common-ancestor-of-a-binary-tree|LC 236 二叉树的最近公共祖先]]（中等）· TikTok P2 · Amazon · LeetCode Hot 100 · Top Interview 150
- [[lct-binary-tree-maximum-path-sum|LC 124 二叉树中的最大路径和]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-serialize-and-deserialize-n-ary-tree|LC 428 序列化和反序列化 N 叉树]]（困难）· TikTok P2
- [[lct-serialize-and-deserialize-binary-tree|LC 297 二叉树的序列化与反序列化]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150
- [[lct-subtree-of-another-tree|LC 572 另一棵树的子树]]（简单）· TikTok P3 · Blind 75 · NeetCode 150
- [[lct-diameter-of-binary-tree|LC 543 二叉树的直径]]（简单）· TikTok P4 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-make-costs-of-paths-equal-in-a-binary-tree|LC 2673 使二叉树所有路径值相等的最小代价]]（中等）· TikTok P4
- [[lct-delete-node-in-a-bst|LC 450 删除二叉搜索树中的节点]]（中等）· TikTok P4
- [[lct-symmetric-tree|LC 101 对称二叉树]]（简单）· TikTok P4 · LeetCode Hot 100 · Top Interview 150
- [[lct-validate-binary-search-tree|LC 98 验证二叉搜索树]]（中等）· TikTok P4 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-amount-of-time-for-binary-tree-to-be-infected|LC 2385 感染二叉树需要的总时间]]（中等）· TikTok P4
- [[lct-populating-next-right-pointers-in-each-node|LC 116 填充每个节点的下一个右侧节点指针]]（中等）· TikTok P4 · Amazon
- [[lct-construct-binary-tree-from-preorder-and-postorder-traversal|LC 889 从前序与后序遍历序列构造二叉树]]（中等）· TikTok P4
- [[lct-create-binary-tree-from-descriptions|LC 2196 根据描述创建二叉树]]（中等）· TikTok P4
- [[lct-flatten-a-multilevel-doubly-linked-list|LC 430 扁平化多级双向链表]]（中等）· TikTok P4
- [[lct-recover-binary-search-tree|LC 99 恢复二叉搜索树]]（中等）· TikTok P4
- [[lct-kth-smallest-element-in-a-bst|LC 230 二叉搜索树中第 K 小的元素]]（中等）· TikTok P4 · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-most-frequent-subtree-sum|LC 508 出现次数最多的子树元素和]]（中等）· TikTok P4
- [[lct-binary-tree-inorder-traversal|LC 94 二叉树的中序遍历]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- LC 100 相同的树（简单）· Amazon · Blind 75 · NeetCode 150 · Top Interview 150
- [[lct-binary-tree-zigzag-level-order-traversal|LC 103 二叉树的锯齿形层序遍历]]（中等）· TikTok B · Amazon · Top Interview 150
- [[lct-maximum-depth-of-binary-tree|LC 104 二叉树的最大深度]]（简单）· TikTok B · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-construct-binary-tree-from-preorder-and-inorder-traversal|LC 105 从前序与中序遍历序列构造二叉树]]（中等）· TikTok B · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-construct-binary-tree-from-inorder-and-postorder-traversal|LC 106 从中序与后序遍历序列构造二叉树]]（中等）· TikTok C · Top Interview 150
- [[lct-convert-sorted-array-to-binary-search-tree|LC 108 将有序数组转换为二叉搜索树]]（简单）· TikTok B · LeetCode Hot 100 · Top Interview 150
- [[lct-balanced-binary-tree|LC 110 平衡二叉树]]（简单）· TikTok B · Amazon · NeetCode 150
- [[lct-path-sum|LC 112 路径总和]]（简单）· TikTok B · Top Interview 150
- [[lct-flatten-binary-tree-to-linked-list|LC 114 二叉树展开为链表]]（中等）· TikTok B · LeetCode Hot 100 · Top Interview 150
- LC 117 填充每个节点的下一个右侧节点指针 II（中等）· Top Interview 150
- [[lct-sum-root-to-leaf-numbers|LC 129 求根节点到叶节点数字之和]]（中等）· TikTok B · Top Interview 150
- LC 173 二叉搜索树迭代器（中等）· Top Interview 150
- LC 222 完全二叉树的节点个数（中等）· Top Interview 150
- [[lct-invert-binary-tree|LC 226 翻转二叉树]]（简单）· TikTok B · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-lowest-common-ancestor-of-a-binary-search-tree|LC 235 二叉搜索树的最近公共祖先]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150
- LC 427 建立四叉树（中等）· Top Interview 150
- LC 530 二叉搜索树的最小绝对差（简单）· Top Interview 150
- LC 637 二叉树的层平均值（简单）· Top Interview 150
- LC 703 数据流中的第 K 大元素（简单）· NeetCode 150
- LC 1448 统计二叉树中好节点的数目（中等）· NeetCode 150

**再做（其余牌组里的题，32 道）**

- [[lct-unique-binary-search-trees-ii|LC 95 不同的二叉搜索树 II]]（中等）· TikTok B
- [[lct-unique-binary-search-trees|LC 96 不同的二叉搜索树]]（中等）· TikTok B
- [[lct-binary-tree-level-order-traversal-ii|LC 107 二叉树的层序遍历 II]]（中等）· TikTok B
- LC 109 有序链表转换二叉搜索树（中等）· Amazon
- [[lct-minimum-depth-of-binary-tree|LC 111 二叉树的最小深度]]（简单）· TikTok B
- [[lct-path-sum-ii|LC 113 路径总和 II]]（中等）· TikTok B
- [[lct-verify-preorder-sequence-in-binary-search-tree|LC 255 验证二叉搜索树的前序遍历序列]]（中等）· TikTok C
- [[lct-binary-tree-longest-consecutive-sequence|LC 298 二叉树最长连续序列]]（中等）· TikTok B
- [[lct-house-robber-iii|LC 337 打家劫舍 III]]（中等）· TikTok B · Amazon
- LC 341 扁平化嵌套列表迭代器（中等）· Amazon
- [[lct-convert-binary-search-tree-to-sorted-doubly-linked-list|LC 426 将二叉搜索树转化为排序的双向链表]]（中等）· TikTok B
- [[lct-find-largest-value-in-each-tree-row|LC 515 在每个树行中找最大值]]（中等）· TikTok B
- [[lct-construct-string-from-binary-tree|LC 606 根据二叉树创建字符串]]（中等）· TikTok C
- [[lct-merge-two-binary-trees|LC 617 合并二叉树]]（简单）· TikTok B
- [[lct-maximum-width-of-binary-tree|LC 662 二叉树最大宽度]]（中等）· TikTok B · Amazon
- [[lct-minimum-distance-between-bst-nodes|LC 783 二叉搜索树节点最小距离]]（简单）· TikTok B
- [[lct-check-completeness-of-a-binary-tree|LC 958 二叉树的完全性检验]]（中等）· TikTok B
- [[lct-binary-tree-cameras|LC 968 监控二叉树]]（困难）· TikTok B
- [[lct-vertical-order-traversal-of-a-binary-tree|LC 987 二叉树的垂序遍历]]（困难）· TikTok B · Amazon
- LC 1038 从二叉搜索树到更大和树（中等）· Amazon
- [[lct-lowest-common-ancestor-of-deepest-leaves|LC 1123 最深叶节点的最近公共祖先]]（中等）· TikTok B
- [[lct-tree-diameter|LC 1245 树的直径]]（中等）· TikTok C
- [[lct-deepest-leaves-sum|LC 1302 层数最深叶子节点的和]]（中等）· TikTok C
- [[lct-maximum-product-of-splitted-binary-tree|LC 1339 分裂二叉树的最大乘积]]（中等）· TikTok B
- LC 1373 二叉搜索子树的最大键值和（困难）· Amazon
- LC 1376 通知所有员工所需的时间（中等）· Amazon
- [[lct-number-of-good-leaf-nodes-pairs|LC 1530 好叶子节点对的数量]]（中等）· TikTok B
- [[lct-lowest-common-ancestor-of-a-binary-tree-iii|LC 1650 二叉树的最近公共祖先 III]]（中等）· TikTok C · Amazon
- [[lct-lowest-common-ancestor-of-a-binary-tree-iv|LC 1676 二叉树的最近公共祖先 IV]]（中等）· TikTok C
- [[lct-find-distance-in-a-binary-tree|LC 1740 找到二叉树中的距离]]（中等）· TikTok B
- [[lct-step-by-step-directions-from-a-binary-tree-node-to-another|LC 2096 从二叉树一个节点到另一个节点每一步的方向]]（中等）· TikTok C
- LC 2603 收集树中金币（困难）· 
