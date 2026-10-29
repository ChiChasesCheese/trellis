# TikTok 字节高频题：总表

TikTok 和字节（美国与国内）面试里最常出现的编程题，按学习顺序排列：A 档最高频，B 档次之，档内按热度降序。点开每一行就是该题的完整标准答案（识别信号、推导、代码、复杂度、易错点、追问）。Anki 里同样的内容在 `LeetCode Tops::24 TikTok 字节高频 · 整题答案`，拆成小卡的版本在 `::25 … · 拆分背诵`。先刷模式识别 [[interviews/core/leetcode/tiktok/map/patterns|patterns]] 和 Python 工具箱 [[interviews/core/leetcode/tiktok/map/python|python]]。

## A 档：最高频

| 题 | 难度 | 主要考点 |
|---|---|---|
| [[tlc-lru-cache-0-whole\|LC 146 LRU 缓存（LRU Cache）]] | Medium | 哈希、链表、设计 |
| [[tlc-longest-substring-without-repeating-characters-0-whole\|LC 3 无重复字符的最长子串（Longest Substring Without Repeating Characters）]] | Medium | 哈希、字符串、滑动窗口 |
| [[tlc-tt-lru-cache-ttl-0-whole\|带 TTL 的 LRU 缓存（含 LFU / 加权 / 线程安全追问）]] | — | — |
| [[tlc-number-of-islands-0-whole\|LC 200 岛屿数量（Number of Islands）]] | Medium | 数组、DFS、BFS、并查集、矩阵 |
| [[tlc-reverse-nodes-in-k-group-0-whole\|LC 25 K 个一组翻转链表（Reverse Nodes in k-Group）]] | Hard | 链表、递归 |
| [[tlc-tt-islands-follow-ups-0-whole\|岛屿数量及其追问集合]] | — | — |
| [[tlc-course-schedule-0-whole\|LC 207 课程表（Course Schedule）]] | Medium | DFS、BFS、图、拓扑排序 |
| [[tlc-tt-course-schedule-output-path-0-whole\|课程表：输出可行学习路径 / 最短路径]] | — | — |
| [[tlc-tt-reverse-k-group-variants-0-whole\|K 个一组翻转链表的变体（尾部、从尾部起、偶数长度组）]] | — | — |
| [[tlc-reverse-linked-list-0-whole\|LC 206 反转链表（Reverse Linked List）]] | Easy | 链表、递归 |
| [[tlc-longest-palindromic-substring-0-whole\|LC 5 最长回文子串（Longest Palindromic Substring）]] | Medium | 双指针、字符串、动态规划 |
| [[tlc-kth-largest-element-in-an-array-0-whole\|LC 215 数组中的第K个最大元素（Kth Largest Element in an Array）]] | Medium | 数组、分治、排序、堆 |
| [[tlc-merge-intervals-0-whole\|LC 56 合并区间（Merge Intervals）]] | Medium | 数组、排序 |
| [[tlc-binary-tree-level-order-traversal-0-whole\|LC 102 二叉树的层序遍历]] | Medium | — |
| [[tlc-best-time-to-buy-and-sell-stock-0-whole\|LC 121 买卖股票的最佳时机（Best Time to Buy and Sell Stock）]] | Easy | 数组、动态规划 |
| [[tlc-lfu-cache-0-whole\|LC 460 LFU缓存]] | Hard | — |
| [[tlc-3sum-0-whole\|LC 15 三数之和（3Sum）]] | Medium | 数组、双指针、排序 |
| [[tlc-top-k-frequent-elements-0-whole\|LC 347 前 K 个高频元素（Top K Frequent Elements）]] | Medium | 数组、哈希、分治、排序、堆 |
| [[tlc-search-in-rotated-sorted-array-0-whole\|LC 33 搜索旋转排序数组（Search in Rotated Sorted Array）]] | Medium | 数组、二分 |
| [[tlc-max-area-of-island-0-whole\|LC 695 岛屿的最大面积（Max Area of Island）]] | Medium | 数组、DFS、BFS、并查集、矩阵 |
| [[tlc-merge-k-sorted-lists-0-whole\|LC 23 合并 K 个升序链表（Merge k Sorted Lists）]] | Hard | 链表、分治、堆 |
| [[tlc-tt-rate-limiter-implementation-0-whole\|手写限流器（滑动窗口 / 令牌桶）]] | — | — |
| [[tlc-number-of-distinct-islands-0-whole\|LC 694 不同岛屿的数量（Number of Distinct Islands）]] | Medium | 数组、哈希、DFS、BFS、并查集、排序、矩阵 |
| [[tlc-binary-tree-right-side-view-0-whole\|LC 199 二叉树的右视图（Binary Tree Right Side View）]] | Medium | 树、DFS、BFS |
| [[tlc-making-a-large-island-0-whole\|LC 827 最大人工岛（Making A Large Island）]] | Hard | 数组、DFS、BFS、并查集、矩阵 |
| [[tlc-lowest-common-ancestor-of-a-binary-tree-0-whole\|LC 236 二叉树的最近公共祖先（Lowest Common Ancestor of a Binary Tree）]] | Medium | 树、DFS |
| [[tlc-binary-tree-zigzag-level-order-traversal-0-whole\|LC 103 二叉树的锯齿形层序遍历（Binary Tree Zigzag Level Order Traversal）]] | Medium | 树、BFS |
| [[tlc-valid-parentheses-0-whole\|LC 20 有效的括号（Valid Parentheses）]] | Easy | 字符串、栈 |
| [[tlc-trapping-rain-water-0-whole\|LC 42 接雨水（Trapping Rain Water）]] | Hard | 数组、双指针、动态规划、栈、单调栈 |
| [[tlc-remove-nth-node-from-end-of-list-0-whole\|LC 19 删除链表的倒数第N个节点]] | Medium | — |
| [[tlc-merge-sorted-array-0-whole\|LC 88 合并两个有序数组]] | Easy | — |
| [[tlc-binary-tree-maximum-path-sum-0-whole\|LC 124 二叉树中的最大路径和（Binary Tree Maximum Path Sum）]] | Hard | 动态规划、树、DFS |
| [[tlc-longest-increasing-subsequence-0-whole\|LC 300 最长递增子序列（Longest Increasing Subsequence）]] | Medium | 数组、二分、动态规划 |
| [[tlc-number-of-distinct-islands-ii-0-whole\|LC 711 不同岛屿的数量 II（Number of Distinct Islands II）]] | — | — |
| [[tlc-multiply-strings-0-whole\|LC 43 字符串相乘（Multiply Strings）]] | Medium | 数学、字符串、模拟 |
| [[tlc-basic-calculator-0-whole\|LC 224 基本计算器（Basic Calculator）]] | Hard | 数学、字符串、栈、递归 |
| [[tlc-numbers-at-most-n-given-digit-set-0-whole\|LC 902 最大为 N 的数字组合（Numbers At Most N Given Digit Set）]] | Hard | 数组、数学、字符串、二分、动态规划 |
| [[tlc-min-stack-0-whole\|LC 155 最小栈]] | Easy | — |
| [[tlc-spiral-matrix-0-whole\|LC 54 螺旋矩阵（Spiral Matrix）]] | Medium | 数组、矩阵、模拟 |
| [[tlc-course-schedule-ii-0-whole\|LC 210 课程表 II（Course Schedule II）]] | Medium | DFS、BFS、图、拓扑排序 |
| [[tlc-restore-ip-addresses-0-whole\|LC 93 复原 IP 地址（Restore IP Addresses）]] | Medium | 字符串、回溯 |
| [[tlc-house-robber-0-whole\|LC 198 打家劫舍（House Robber）]] | Medium | 数组、动态规划 |
| [[tlc-tt-largest-number-below-n-from-digits-0-whole\|用给定数字组成小于 N 的最大数]] | — | — |
| [[tlc-tt-basic-calculator-ladder-0-whole\|计算器梯度题（无括号 -> 括号与一元负号，先校验再求值）]] | — | — |
| [[tlc-meeting-rooms-ii-0-whole\|LC 253 会议室 II（Meeting Rooms II）]] | Medium | 数组、双指针、贪心、排序、堆、前缀和 |
| [[tlc-parallel-courses-iii-0-whole\|LC 2050 并行课程 III（Parallel Courses III）]] | — | — |
| [[tlc-two-sum-0-whole\|LC 1 两数之和（Two Sum）]] | Easy | 数组、哈希 |
| [[tlc-find-median-from-data-stream-0-whole\|LC 295 数据流的中位数（Find Median from Data Stream）]] | Hard | 双指针、设计、排序、堆 |
| [[tlc-path-sum-iii-0-whole\|LC 437 路径总和 III（Path Sum III）]] | Medium | 树、DFS |
| [[tlc-add-strings-0-whole\|LC 415 字符串相加（Add Strings）]] | Easy | 数学、字符串、模拟 |
| [[tlc-permutations-0-whole\|LC 46 全排列（Permutations）]] | Medium | 数组、回溯 |
| [[tlc-reverse-nodes-in-even-length-groups-0-whole\|LC 2074 反转偶数长度组的节点（Reverse Nodes in Even Length Groups）]] | — | — |
| [[tlc-subarray-sum-equals-k-0-whole\|LC 560 和为 K 的子数组（Subarray Sum Equals K）]] | Medium | 数组、哈希、前缀和 |
| [[tlc-linked-list-cycle-0-whole\|LC 141 环形链表]] | Easy | — |
| [[tlc-intersection-of-two-linked-lists-0-whole\|LC 160 相交链表（Intersection of Two Linked Lists）]] | Easy | 哈希、链表、双指针 |
| [[tlc-tt-deep-merge-nested-json-0-whole\|合并两个嵌套 JSON]] | — | — |
| [[tlc-alien-dictionary-0-whole\|LC 269 火星词典（Alien Dictionary）]] | Hard | 数组、字符串、DFS、BFS、图、拓扑排序 |
| [[tlc-sliding-window-maximum-0-whole\|LC 239 滑动窗口最大值（Sliding Window Maximum）]] | Hard | 数组、滑动窗口、堆 |
| [[tlc-word-ladder-0-whole\|LC 127 单词接龙（Word Ladder）]] | Hard | 哈希、字符串、BFS |
| [[tlc-implement-trie-prefix-tree-0-whole\|LC 208 实现 Trie (前缀树)]] | Medium | — |
| [[tlc-maximum-subarray-0-whole\|LC 53 最大子数组和（Maximum Subarray）]] | Medium | 数组、分治、动态规划 |
| [[tlc-tt-max-path-sum-with-path-0-whole\|二叉树最大路径和并还原 / 打印路径]] | — | — |
| [[tlc-tt-path-sum-n-ary-prefix-sum-0-whole\|N 叉树路径和计数（暴力被拒，要前缀和）]] | — | — |
| [[tlc-subtree-of-another-tree-0-whole\|LC 572 另一个树的子树]] | Easy | — |
| [[tlc-longest-valid-parentheses-0-whole\|LC 32 最长有效括号（Longest Valid Parentheses）]] | Hard | 字符串、动态规划、栈 |
| [[tlc-minimum-path-sum-0-whole\|LC 64 最小路径和（Minimum Path Sum）]] | Medium | 数组、动态规划、矩阵 |
| [[tlc-regular-expression-matching-0-whole\|LC 10 正则表达式匹配（Regular Expression Matching）]] | Hard | 字符串、动态规划、递归 |
| [[tlc-sqrtx-0-whole\|LC 69 x 的平方根 （Sqrt(x)）]] | Easy | 数学、二分 |
| [[tlc-best-time-to-buy-and-sell-stock-ii-0-whole\|LC 122 买卖股票的最佳时机 II（Best Time to Buy and Sell Stock II）]] | Medium | 数组、动态规划、贪心 |
| [[tlc-shortest-path-in-a-grid-with-obstacles-elimination-0-whole\|LC 1293 网格中的最短路径（Shortest Path in a Grid with Obstacles Elimination）]] | Hard | 数组、BFS、矩阵 |
| [[tlc-longest-common-subsequence-0-whole\|LC 1143 最长公共子序列（Longest Common Subsequence）]] | Medium | 字符串、动态规划 |
| [[tlc-median-of-two-sorted-arrays-0-whole\|LC 4 寻找两个正序数组的中位数]] | Hard | — |
| [[tlc-next-permutation-0-whole\|LC 31 下一个排列（Next Permutation）]] | Medium | — |
| [[tlc-generate-parentheses-0-whole\|LC 22 括号生成（Generate Parentheses）]] | Medium | 字符串、动态规划、回溯 |
| [[tlc-decode-string-0-whole\|LC 394 字符串解码（Decode String）]] | Medium | 字符串、栈、递归 |
| [[tlc-remove-duplicate-letters-0-whole\|LC 316 去除重复字母（Remove Duplicate Letters）]] | Medium | 字符串、栈、贪心、单调栈 |
| [[tlc-basic-calculator-ii-0-whole\|LC 227 基本计算器 II（Basic Calculator II）]] | Medium | 数学、字符串、栈 |
| [[tlc-maximal-square-0-whole\|LC 221 最大正方形（Maximal Square）]] | Medium | 数组、动态规划、矩阵 |
| [[tlc-design-in-memory-file-system-0-whole\|LC 588 设计内存文件系统（Design In-Memory File System）]] | Hard | 哈希、字符串、设计、字典树、排序 |
| [[tlc-implement-queue-using-stacks-0-whole\|LC 232 用栈实现队列]] | Easy | — |
| [[tlc-word-break-0-whole\|LC 139 单词拆分（Word Break）]] | Medium | 数组、哈希、字符串、动态规划、字典树 |
| [[tlc-edit-distance-0-whole\|LC 72 编辑距离（Edit Distance）]] | Medium | 字符串、动态规划 |
| [[tlc-design-circular-queue-0-whole\|LC 622 设计循环队列（Design Circular Queue）]] | — | — |
| [[tlc-tt-fixed-array-deque-o1-0-whole\|定长数组实现双端队列 / 列表（全部操作 O(1)）]] | — | — |
| [[tlc-tt-grid-min-cost-fuel-recharge-0-whole\|网格最小代价路径（障碍 / 加油站 / 油量 K）]] | — | — |
| [[tlc-longest-substring-with-at-most-k-distinct-characters-0-whole\|LC 340 至多包含 K 个不同字符的最长子串（Longest Substring with At Most K Distinct Characters）]] | Medium | 哈希、字符串、滑动窗口 |
| [[tlc-best-time-to-buy-and-sell-stock-iii-0-whole\|LC 123 买卖股票的最佳时机 III]] | Hard | — |
| [[tlc-minimum-window-substring-0-whole\|LC 76 最小覆盖子串（Minimum Window Substring）]] | Hard | 哈希、字符串、滑动窗口 |
| [[tlc-reverse-words-in-a-string-0-whole\|LC 151 翻转字符串里的单词]] | Medium | — |
| [[tlc-merge-two-sorted-lists-0-whole\|LC 21 合并两个有序链表]] | Easy | — |
| [[tlc-implement-rand10-using-rand7-0-whole\|LC 470 用 Rand7() 实现 Rand10()]] | Medium | — |
| [[tlc-best-time-to-buy-and-sell-stock-iv-0-whole\|LC 188 买卖股票的最佳时机 IV（Best Time to Buy and Sell Stock IV）]] | — | — |
| [[tlc-maximum-product-subarray-0-whole\|LC 152 乘积最大子数组]] | Medium | — |
| [[tlc-design-tic-tac-toe-0-whole\|LC 348 设计井字棋（Design Tic-Tac-Toe）]] | — | — |
| [[tlc-reorder-list-0-whole\|LC 143 重排链表（Reorder List）]] | Medium | 链表、双指针、栈、递归 |
| [[tlc-validate-binary-search-tree-0-whole\|LC 98 验证二叉搜索树]] | Medium | — |
| [[tlc-word-search-ii-0-whole\|LC 212 单词搜索 II（Word Search II）]] | Hard | 数组、字符串、回溯、字典树、矩阵 |
| [[tlc-sort-list-0-whole\|LC 148 排序链表（Sort List）]] | Medium | 链表、双指针、分治、排序 |
| [[tlc-basic-calculator-iii-0-whole\|LC 772 基本计算器 III（Basic Calculator III）]] | Hard | 数学、字符串、栈、递归 |
| [[tlc-minimum-size-subarray-sum-0-whole\|LC 209 长度最小的子数组（Minimum Size Subarray Sum）]] | Medium | 数组、二分、滑动窗口、前缀和 |
| [[tlc-largest-number-0-whole\|LC 179 最大数]] | Medium | — |
| [[tlc-symmetric-tree-0-whole\|LC 101 对称二叉树]] | Easy | — |
| [[tlc-unique-paths-0-whole\|LC 62 不同路径（Unique Paths）]] | Medium | 数学、动态规划 |
| [[tlc-maximum-height-by-stacking-cuboids-0-whole\|LC 1691 堆叠长方体的最大高度（Maximum Height by Stacking Cuboids）]] | — | — |
| [[tlc-n-queens-0-whole\|LC 51 N 皇后（N-Queens）]] | Hard | 数组、回溯 |
| [[tlc-tt-kv-store-snapshot-restore-0-whole\|内存 KV 存储：快照与恢复（序列化）]] | — | — |
| [[tlc-transpose-matrix-0-whole\|LC 867 转置矩阵（Transpose Matrix）]] | — | — |
| [[tlc-accounts-merge-0-whole\|LC 721 账户合并（Accounts Merge）]] | Medium | 数组、哈希、字符串、DFS、BFS、并查集、排序 |
| [[tlc-design-hashmap-0-whole\|LC 706 设计哈希映射（Design HashMap）]] | Easy | 数组、哈希、链表、设计 |
| [[tlc-combination-sum-0-whole\|LC 39 组合总和（Combination Sum）]] | Medium | 数组、回溯 |
| [[tlc-reverse-linked-list-ii-0-whole\|LC 92 反转链表 II（Reverse Linked List II）]] | Medium | 链表 |
| [[tlc-linked-list-cycle-ii-0-whole\|LC 142 环形链表 II（Linked List Cycle II）]] | Medium | 哈希、链表、双指针 |
| [[tlc-tt-concurrency-limited-runner-0-whole\|限制并发数的异步任务执行器]] | — | — |
| [[tlc-tt-array-min-heap-0-whole\|用数组手写最小堆（并用它按先修关系排课）]] | — | — |
| [[tlc-subsets-0-whole\|LC 78 子集（Subsets）]] | Medium | 数组、回溯、位运算 |
| [[tlc-possible-bipartition-0-whole\|LC 886 可能的二分法（Possible Bipartition）]] | Medium | DFS、BFS、并查集、图 |
| [[tlc-find-first-and-last-position-of-element-in-sorted-array-0-whole\|LC 34 在排序数组中查找元素的第一个和最后一个位置（Find First and Last Position of Element in Sorted Array）]] | Medium | 数组、二分 |
| [[tlc-count-primes-0-whole\|LC 204 计数质数（Count Primes）]] | — | — |
| [[tlc-valid-parenthesis-string-0-whole\|LC 678 有效的括号字符串（Valid Parenthesis String）]] | Medium | 字符串、动态规划、栈、贪心 |
| [[tlc-construct-binary-tree-from-preorder-and-inorder-traversal-0-whole\|LC 105 从前序与中序遍历序列构造二叉树（Construct Binary Tree from Preorder and Inorder Traversal）]] | Medium | 数组、哈希、分治、树 |
| [[tlc-group-anagrams-0-whole\|LC 49 字母异位词分组（Group Anagrams）]] | Medium | 数组、哈希、字符串、排序 |
| [[tlc-max-consecutive-ones-iii-0-whole\|LC 1004 最大连续1的个数 III]] | Medium | — |
| [[tlc-word-search-0-whole\|LC 79 单词搜索（Word Search）]] | Medium | 数组、字符串、回溯、DFS、矩阵 |
| [[tlc-tt-ring-walk-count-0-whole\|环上走 n 步回到起点的方案数]] | — | — |
| [[tlc-design-memory-allocator-0-whole\|LC 2502 设计内存分配器（Design Memory Allocator）]] | Medium | 数组、哈希、设计、模拟 |
| [[tlc-compare-version-numbers-0-whole\|LC 165 比较版本号（Compare Version Numbers）]] | Medium | 双指针、字符串 |
| [[tlc-tt-delete-window-balance-even-odd-0-whole\|删除长度 k 的窗口使奇偶下标和相等]] | — | — |
| [[tlc-serialize-and-deserialize-binary-tree-0-whole\|LC 297 二叉树的序列化与反序列化（Serialize and Deserialize Binary Tree）]] | Hard | 字符串、树、DFS、BFS、设计 |
| [[tlc-make-costs-of-paths-equal-in-a-binary-tree-0-whole\|LC 2673 使二叉树所有路径值相等的最小代价（Make Costs of Paths Equal in a Binary Tree）]] | — | — |
| [[tlc-coin-change-0-whole\|LC 322 零钱兑换（Coin Change）]] | Medium | 数组、动态规划、BFS |
| [[tlc-find-the-duplicate-number-0-whole\|LC 287 寻找重复数]] | Medium | — |
| [[tlc-maximum-width-of-binary-tree-0-whole\|LC 662 二叉树最大宽度（Maximum Width of Binary Tree）]] | Medium | 树、DFS、BFS |
| [[tlc-find-minimum-in-rotated-sorted-array-0-whole\|LC 153 寻找旋转排序数组中的最小值（Find Minimum in Rotated Sorted Array）]] | Medium | 数组、二分 |
| [[tlc-koko-eating-bananas-0-whole\|LC 875 爱吃香蕉的珂珂（Koko Eating Bananas）]] | Medium | 数组、二分 |
| [[tlc-diameter-of-binary-tree-0-whole\|LC 543 二叉树的直径]] | Easy | — |
| [[tlc-longest-consecutive-sequence-0-whole\|LC 128 最长连续序列（Longest Consecutive Sequence）]] | Medium | 数组、哈希、并查集 |
| [[tlc-first-missing-positive-0-whole\|LC 41 缺失的第一个正数]] | Hard | — |
| [[tlc-water-and-jug-problem-0-whole\|LC 365 水壶问题（Water and Jug Problem）]] | Medium | 数学、DFS、BFS |
| [[tlc-climbing-stairs-0-whole\|LC 70 爬楼梯（Climbing Stairs）]] | Easy | 数学、动态规划 |
| [[tlc-add-two-numbers-ii-0-whole\|LC 445 两数相加 II]] | Medium | — |
| [[tlc-evaluate-division-0-whole\|LC 399 除法求值（Evaluate Division）]] | Medium | 数组、字符串、DFS、BFS、并查集、图 |
| [[tlc-count-number-of-nice-subarrays-0-whole\|LC 1248 统计「优美子数组」（Count Number of Nice Subarrays）]] | Medium | 数组、哈希、数学、滑动窗口、前缀和 |
| [[tlc-shortest-unsorted-continuous-subarray-0-whole\|LC 581 最短无序连续子数组（Shortest Unsorted Continuous Subarray）]] | Medium | 数组、双指针、栈、贪心、排序、单调栈 |
| [[tlc-palindrome-partitioning-0-whole\|LC 131 分割回文串（Palindrome Partitioning）]] | — | — |
| [[tlc-jump-game-0-whole\|LC 55 跳跃游戏（Jump Game）]] | Medium | 数组、动态规划、贪心 |
| [[tlc-largest-rectangle-in-histogram-0-whole\|LC 84 柱状图中最大的矩形（Largest Rectangle in Histogram）]] | Hard | 数组、栈、单调栈 |
| [[tlc-meeting-rooms-iii-0-whole\|LC 2402 会议室 III（Meeting Rooms III）]] | Hard | 数组、哈希、排序、堆、模拟 |
| [[tlc-house-robber-iii-0-whole\|LC 337 打家劫舍 III（House Robber III）]] | — | — |
| [[tlc-text-justification-0-whole\|LC 68 文本左右对齐（Text Justification）]] | Hard | 数组、字符串、模拟 |
| [[tlc-add-two-numbers-0-whole\|LC 2 两数相加（Add Two Numbers）]] | Medium | — |
| [[tlc-find-peak-element-0-whole\|LC 162 寻找峰值（Find Peak Element）]] | Medium | 数组、二分 |
| [[tlc-remove-duplicates-from-sorted-list-ii-0-whole\|LC 82 删除排序链表中的重复元素 II]] | Medium | — |
| [[tlc-shu-de-zi-jie-gou-lcof-0-whole\|剑指 Offer 26 树的子结构]] | Medium | — |
| [[tlc-k-th-smallest-in-lexicographical-order-0-whole\|LC 440 字典序的第K小数字]] | Hard | — |
| [[tlc-delete-node-in-a-bst-0-whole\|LC 450 删除二叉搜索树中的节点（Delete Node in a BST）]] | Medium | 树 |
| [[tlc-sparse-matrix-multiplication-0-whole\|LC 311 稀疏矩阵的乘法（Sparse Matrix Multiplication）]] | — | — |
| [[tlc-path-sum-ii-0-whole\|LC 113 路径总和 II]] | Medium | — |
| [[tlc-tt-valid-parenthesis-string-print-all-0-whole\|含星号的有效括号 + 输出所有合法字符串]] | — | — |
| [[tlc-non-overlapping-intervals-0-whole\|LC 435 无重叠区间（Non-overlapping Intervals）]] | — | — |
| [[tlc-longest-repeating-character-replacement-0-whole\|LC 424 替换后的最长重复字符（Longest Repeating Character Replacement）]] | Medium | 哈希、字符串、滑动窗口 |
| [[tlc-fruit-into-baskets-0-whole\|LC 904 水果成篮（Fruit Into Baskets）]] | Medium | 数组、哈希、滑动窗口 |
| [[tlc-rotate-array-0-whole\|LC 189 轮转数组（Rotate Array）]] | Medium | 数组、数学、双指针 |
| [[tlc-surrounded-regions-0-whole\|LC 130 被围绕的区域（Surrounded Regions）]] | — | — |
| [[tlc-letter-combinations-of-a-phone-number-0-whole\|LC 17 电话号码的字母组合]] | Medium | — |
| [[tlc-distinct-subsequences-0-whole\|LC 115 不同的子序列]] | Hard | — |
| [[tlc-wildcard-matching-0-whole\|LC 44 通配符匹配]] | Hard | — |
| [[tlc-binary-search-0-whole\|LC 704 二分查找]] | Easy | — |
| [[tlc-stickers-to-spell-word-0-whole\|LC 691 贴纸拼词（Stickers to Spell Word）]] | — | — |
| [[tlc-coin-change-ii-0-whole\|LC 518 零钱兑换 II]] | Medium | — |
| [[tlc-sum-root-to-leaf-numbers-0-whole\|LC 129 求根到叶子节点数字之和]] | Medium | — |
| [[tlc-path-sum-0-whole\|LC 112 路径总和]] | Easy | — |
| [[tlc-longest-increasing-path-in-a-matrix-0-whole\|LC 329 矩阵中的最长递增路径（Longest Increasing Path in a Matrix）]] | Hard | 数组、动态规划、DFS、BFS、图、拓扑排序、矩阵 |
| [[tlc-find-minimum-in-rotated-sorted-array-ii-0-whole\|LC 154 寻找旋转排序数组中的最小值 II（Find Minimum in Rotated Sorted Array II）]] | — | — |
| [[tlc-single-number-0-whole\|LC 136 只出现一次的数字（Single Number）]] | — | — |
| [[tlc-tt-number-to-string-0-whole\|手写数字转字符串（含符号与小数）]] | — | — |
| [[tlc-target-sum-0-whole\|LC 494 目标和（Target Sum）]] | — | — |
| [[tlc-tt-currency-conversion-queries-0-whole\|汇率换算查询（多跳 / 无解返回 -1）]] | — | — |
| [[tlc-kth-smallest-element-in-a-sorted-matrix-0-whole\|LC 378 有序矩阵中第 K 小的元素（Kth Smallest Element in a Sorted Matrix）]] | Medium | 数组、二分、排序、堆、矩阵 |
| [[tlc-flip-string-to-monotone-increasing-0-whole\|LC 926 将字符串翻转到单调递增（Flip String to Monotone Increasing）]] | — | — |
| [[tlc-tt-hyper-operation-0-whole\|手写超运算（加、乘、幂、迭代幂次……）]] | — | — |
| [[tlc-tt-tool-call-success-rate-0-whole\|工具调用日志：每个工具的成功率与失败最多的工具]] | — | — |
| [[tlc-gas-station-0-whole\|LC 134 加油站（Gas Station）]] | Medium | 数组、贪心 |
| [[tlc-shortest-path-in-binary-matrix-0-whole\|LC 1091 二进制矩阵中的最短路径（Shortest Path in Binary Matrix）]] | — | — |
| [[tlc-word-break-ii-0-whole\|LC 140 单词拆分 II（Word Break II）]] | Hard | 数组、哈希、字符串、动态规划、回溯、字典树 |
| [[tlc-tt-fish-decaying-ponds-0-whole\|鱼塘捕鱼：产量递减时的最大收获]] | — | — |
| [[tlc-container-with-most-water-0-whole\|LC 11 盛最多水的容器（Container With Most Water）]] | Medium | 数组、双指针、贪心 |
| [[tlc-random-pick-with-weight-0-whole\|LC 528 按权重随机选择（Random Pick with Weight）]] | Medium | 数组、数学、二分、前缀和 |
| [[tlc-find-all-anagrams-in-a-string-0-whole\|LC 438 找到字符串中所有字母异位词（Find All Anagrams in a String）]] | Medium | 哈希、字符串、滑动窗口 |
| [[tlc-search-a-2d-matrix-ii-0-whole\|LC 240 搜索二维矩阵 II]] | Medium | — |
| [[tlc-all-nodes-distance-k-in-binary-tree-0-whole\|LC 863 二叉树中所有距离为 K 的结点（All Nodes Distance K in Binary Tree）]] | Medium | 哈希、树、DFS、BFS |
| [[tlc-cheapest-flights-within-k-stops-0-whole\|LC 787 K 站中转内最便宜的航班（Cheapest Flights Within K Stops）]] | Medium | 动态规划、DFS、BFS、图、堆 |
| [[tlc-yong-liang-ge-zhan-shi-xian-dui-lie-lcof-0-whole\|剑指 Offer 09 用两个栈实现队列]] | Easy | — |
| [[tlc-tt-spiral-matrix-constant-space-0-whole\|螺旋矩阵：O(1) 额外空间且不修改输入]] | — | — |
| [[tlc-trapping-rain-water-ii-0-whole\|LC 407 接雨水 II（Trapping Rain Water II）]] | Hard | — |
| [[tlc-partition-to-k-equal-sum-subsets-0-whole\|LC 698 划分为k个相等的子集]] | Medium | — |
| [[tlc-interleaving-string-0-whole\|LC 97 交错字符串]] | Medium | — |
| [[tlc-single-number-iii-0-whole\|LC 260 只出现一次的数字 III（Single Number III）]] | — | — |
| [[tlc-substring-with-concatenation-of-all-words-0-whole\|LC 30 串联所有单词的子串]] | Hard | — |
| [[tlc-find-the-most-competitive-subsequence-0-whole\|LC 1673 找出最具竞争力的子序列]] | Medium | — |
| [[tlc-maximum-subarray-sum-with-one-deletion-0-whole\|LC 1186 删除一次得到子数组最大和]] | Medium | — |

## B 档：次高频

| 题 | 难度 | 主要考点 |
|---|---|---|
| [[tlc-lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof-0-whole\|剑指 Offer 22 链表中倒数第k个节点]] | Easy | — |
| [[tlc-word-ladder-ii-0-whole\|LC 126 单词接龙 II（Word Ladder II）]] | — | — |
| [[tlc-swap-nodes-in-pairs-0-whole\|LC 24 两两交换链表中的节点]] | Medium | — |
| [[tlc-subarray-sums-divisible-by-k-0-whole\|LC 974 和可被 K 整除的子数组（Subarray Sums Divisible by K）]] | Medium | 数组、哈希、前缀和 |
| [[tlc-permutation-in-string-0-whole\|LC 567 字符串的排列（Permutation in String）]] | — | — |
| [[tlc-combination-sum-ii-0-whole\|LC 40 组合总和 II（Combination Sum II）]] | Medium | 数组、回溯 |
| [[tlc-combinations-0-whole\|LC 77 组合（Combinations）]] | Medium | — |
| [[tlc-copy-list-with-random-pointer-0-whole\|LC 138 复制带随机指针的链表]] | Medium | — |
| [[tlc-longest-mountain-in-array-0-whole\|LC 845 数组中的最长山脉（Longest Mountain in Array）]] | Medium | 数组、双指针、动态规划 |
| [[tlc-remove-k-digits-0-whole\|LC 402 移掉 K 位数字（Remove K Digits）]] | Medium | 字符串、栈、贪心、单调栈 |
| [[tlc-tt-seller-task-scheduler-0-whole\|卖家任务调度器（轮转 + VIP + 优先级）]] | — | — |
| [[tlc-3sum-closest-0-whole\|LC 16 最接近的三数之和（3Sum Closest）]] | Medium | 数组、双指针、排序 |
| [[tlc-daily-temperatures-0-whole\|LC 739 每日温度（Daily Temperatures）]] | Medium | 数组、栈、单调栈 |
| [[tlc-jump-game-ii-0-whole\|LC 45 跳跃游戏 II（Jump Game II）]] | Medium | 数组、动态规划、贪心 |
| [[tlc-search-insert-position-0-whole\|LC 35 搜索插入位置（Search Insert Position）]] | — | — |
| [[tlc-rotate-image-0-whole\|LC 48 旋转图像（Rotate Image）]] | Medium | 数组、数学、矩阵 |
| [[tlc-tt-removable-timestamp-task-scheduler-0-whole\|可删除任务的时间戳调度器（popTask）]] | — | — |
| [[tlc-candy-0-whole\|LC 135 分发糖果]] | Hard | — |
| [[tlc-tt-pythagorean-triple-in-array-0-whole\|整数数组中的勾股三元组]] | — | — |
| [[tlc-create-binary-tree-from-descriptions-0-whole\|LC 2196 根据描述创建二叉树（Create Binary Tree From Descriptions）]] | — | — |
| [[tlc-longest-substring-with-at-least-k-repeating-characters-0-whole\|LC 395 至少有 K 个重复字符的最长子串（Longest Substring with At Least K Repeating Characters）]] | Medium | 哈希、字符串、分治、滑动窗口 |
| [[tlc-tt-nested-comment-tree-0-whole\|由扁平记录构建嵌套评论树]] | — | — |
| [[tlc-shu-zu-zhong-de-ni-xu-dui-lcof-0-whole\|剑指 Offer 51 数组中的逆序对]] | Hard | — |
| [[tlc-longest-common-prefix-0-whole\|LC 14 最长公共前缀（Longest Common Prefix）]] | Easy | 数组、字符串、字典树 |
| [[tlc-maximum-swap-0-whole\|LC 670 最大交换（Maximum Swap）]] | Medium | 数学、贪心 |
| [[tlc-tt-ai-assisted-order-validator-0-whole\|AI 辅助编码：OrderValidator（规则 DAG）]] | — | — |
| [[tlc-insert-delete-getrandom-o1-0-whole\|LC 380 O(1) 时间插入、删除和获取随机元素（Insert Delete GetRandom O(1)）]] | Medium | 数组、哈希、数学、设计 |
| [[tlc-time-based-key-value-store-0-whole\|LC 981 基于时间的键值存储（Time Based Key-Value Store）]] | — | — |
| [[tlc-move-zeroes-0-whole\|LC 283 移动零（Move Zeroes）]] | Easy | 数组、双指针 |
| [[tlc-all-oone-data-structure-0-whole\|LC 432 全 O(1) 的数据结构（All O`one Data Structure）]] | Hard | 哈希、链表、设计 |
| [[tlc-super-egg-drop-0-whole\|LC 887 鸡蛋掉落（Super Egg Drop）]] | Hard | 数学、二分、动态规划 |
| [[tlc-number-of-connected-components-in-an-undirected-graph-0-whole\|LC 323 无向图中连通分量的数目（Number of Connected Components in an Undirected Graph）]] | — | — |
| [[tlc-sort-colors-0-whole\|LC 75 颜色分类（Sort Colors）]] | Medium | 数组、双指针、排序 |
| [[tlc-balanced-binary-tree-0-whole\|LC 110 平衡二叉树]] | Easy | — |
| [[tlc-product-of-array-except-self-0-whole\|LC 238 除了自身以外数组的乘积（Product of Array Except Self）]] | — | — |
| [[tlc-maximum-depth-of-binary-tree-0-whole\|LC 104 二叉树的最大深度]] | Easy | — |
| [[tlc-pacific-atlantic-water-flow-0-whole\|LC 417 太平洋大西洋水流问题（Pacific Atlantic Water Flow）]] | Medium | 数组、DFS、BFS、矩阵 |
| [[tlc-flatten-a-multilevel-doubly-linked-list-0-whole\|LC 430 扁平化多级双向链表（Flatten a Multilevel Doubly Linked List）]] | — | — |
| [[tlc-decode-ways-0-whole\|LC 91 解码方法]] | Medium | — |
| [[tlc-smallest-subsequence-of-distinct-characters-0-whole\|LC 1081 不同字符的最小子序列（Smallest Subsequence of Distinct Characters）]] | Medium | 字符串、栈、贪心、单调栈 |
| [[tlc-first-day-where-you-have-been-in-all-the-rooms-0-whole\|LC 1997 访问完所有房间的第一天（First Day Where You Have Been in All the Rooms）]] | Medium | 数组、动态规划 |
| [[tlc-subarray-with-elements-greater-than-varying-threshold-0-whole\|LC 2334 元素值大于变化阈值的子数组（Subarray With Elements Greater Than Varying Threshold）]] | Hard | — |
| [[tlc-search-a-2d-matrix-0-whole\|LC 74 搜索二维矩阵]] | Medium | — |
| [[tlc-24-game-0-whole\|LC 679 24 点游戏]] | Hard | — |
| [[tlc-single-element-in-a-sorted-array-0-whole\|LC 540 有序数组中的单一元素（Single Element in a Sorted Array）]] | Medium | 数组、二分 |
| [[tlc-longest-common-suffix-queries-0-whole\|LC 3093 最长公共后缀查询（Longest Common Suffix Queries）]] | — | — |
| [[tlc-permutations-ii-0-whole\|LC 47 全排列 II（Permutations II）]] | Medium | 数组、回溯、排序 |
| [[tlc-remove-all-adjacent-duplicates-in-string-ii-0-whole\|LC 1209 删除字符串中的所有相邻重复项 II（Remove All Adjacent Duplicates in String II）]] | Medium | 字符串、栈 |
| [[tlc-maximum-length-of-a-concatenated-string-with-unique-characters-0-whole\|LC 1239 串联字符串的最大长度（Maximum Length of a Concatenated String with Unique Characters）]] | — | — |
| [[tlc-tt-sorted-array-more-than-n-over-3-0-whole\|有序数组中出现次数超过 n/3 的数]] | — | — |
| [[tlc-partition-equal-subset-sum-0-whole\|LC 416 分割等和子集（Partition Equal Subset Sum）]] | Medium | 数组、动态规划 |
| [[tlc-product-of-the-last-k-numbers-0-whole\|LC 1352 最后 K 个数的乘积（Product of the Last K Numbers）]] | Medium | 数组、数学、设计、前缀和 |
| [[tlc-maximum-length-of-repeated-subarray-0-whole\|LC 718 最长重复子数组]] | Medium | — |
| [[tlc-palindrome-linked-list-0-whole\|LC 234 回文链表]] | Easy | — |
| [[tlc-count-of-interesting-subarrays-0-whole\|LC 2845 统计趣味子数组的数目（Count of Interesting Subarrays）]] | — | — |
| [[tlc-tt-contiguous-memory-allocator-0-whole\|连续内存分配器（first-fit、拆分与合并）]] | — | — |
| [[tlc-serialize-and-deserialize-n-ary-tree-0-whole\|LC 428 序列化和反序列化 N 叉树（Serialize and Deserialize N-ary Tree）]] | Hard | 字符串、树、DFS、BFS |
| [[tlc-partition-array-for-maximum-sum-0-whole\|LC 1043 分隔数组以得到最大和（Partition Array for Maximum Sum）]] | Medium | 数组、动态规划 |
| [[tlc-simplify-path-0-whole\|LC 71 简化路径（Simplify Path）]] | Medium | 字符串、栈 |
| [[tlc-minimum-swaps-to-group-all-1s-together-0-whole\|LC 1151 最少交换次数来组合所有的 1（Minimum Swaps to Group All 1's Together）]] | Medium | 数组、滑动窗口 |
| [[tlc-shortest-bridge-0-whole\|LC 934 最短的桥（Shortest Bridge）]] | Medium | 数组、DFS、BFS、矩阵 |
| [[tlc-diagonal-traverse-0-whole\|LC 498 对角线遍历]] | Medium | — |
| [[tlc-unique-binary-search-trees-0-whole\|LC 96 不同的二叉搜索树]] | Medium | — |
| [[tlc-permutation-sequence-0-whole\|LC 60 排列序列（Permutation Sequence）]] | — | — |
| [[tlc-longest-happy-string-0-whole\|LC 1405 最长快乐字符串（Longest Happy String）]] | Medium | 字符串、贪心、堆 |
| [[tlc-snapshot-array-0-whole\|LC 1146 快照数组（Snapshot Array）]] | Medium | 数组、哈希、二分、设计 |
| [[tlc-tt-water-jug-shortest-operations-0-whole\|水壶问题：输出最短操作序列]] | — | — |
| [[tlc-find-all-duplicates-in-an-array-0-whole\|LC 442 数组中重复的数据（Find All Duplicates in an Array）]] | Medium | — |
| [[tlc-flatten-binary-tree-to-linked-list-0-whole\|LC 114 二叉树展开为链表]] | Medium | — |
| [[tlc-beautiful-arrangement-ii-0-whole\|LC 667 优美的排列 II（Beautiful Arrangement II）]] | — | — |
| [[tlc-remove-invalid-parentheses-0-whole\|LC 301 删除无效的括号（Remove Invalid Parentheses）]] | Hard | 字符串、回溯、BFS |
| [[tlc-remove-duplicates-from-sorted-list-0-whole\|LC 83 删除排序链表中的重复元素]] | Easy | — |
| [[tlc-number-of-atoms-0-whole\|LC 726 原子的数量]] | Hard | — |
| [[tlc-minimum-add-to-make-parentheses-valid-0-whole\|LC 921 使括号有效的最少添加（Minimum Add to Make Parentheses Valid）]] | — | — |
| [[tlc-reorganize-string-0-whole\|LC 767 重构字符串（Reorganize String）]] | Medium | — |
| [[tlc-rotting-oranges-0-whole\|LC 994 腐烂的橘子（Rotting Oranges）]] | Medium | 数组、BFS、矩阵 |
| [[tlc-remove-duplicates-from-sorted-array-ii-0-whole\|LC 80 删除排序数组中的重复项 II]] | Medium | — |
| [[tlc-remove-zero-sum-consecutive-nodes-from-linked-list-0-whole\|LC 1171 从链表中删去总和值为零的连续节点（Remove Zero Sum Consecutive Nodes from Linked List）]] | Medium | 哈希、链表 |
| [[tlc-bus-routes-0-whole\|LC 815 公交路线（Bus Routes）]] | Hard | 数组、哈希、BFS |
| [[tlc-longest-duplicate-substring-0-whole\|LC 1044 最长重复子串]] | Hard | — |
| [[tlc-maximum-value-at-a-given-index-in-a-bounded-array-0-whole\|LC 1802 有界数组中指定下标处的最大值（Maximum Value at a Given Index in a Bounded Array）]] | Medium | 数学、二分、贪心 |
| [[tlc-incremental-memory-leak-0-whole\|LC 1860 增长的内存泄露（Incremental Memory Leak）]] | Medium | 数学、模拟 |
| [[tlc-count-the-hidden-sequences-0-whole\|LC 2145 统计隐藏数组数目（Count the Hidden Sequences）]] | Medium | 数组、前缀和 |
| [[tlc-length-of-the-longest-alphabetical-continuous-substring-0-whole\|LC 2414 最长的字母序连续子字符串的长度（Length of the Longest Alphabetical Continuous Substring）]] | Medium | 字符串 |
| [[tlc-most-popular-video-creator-0-whole\|LC 2456 最流行的视频创作者（Most Popular Video Creator）]] | Medium | 数组、哈希、字符串、排序、堆 |
| [[tlc-closest-prime-numbers-in-range-0-whole\|LC 2523 范围内最接近的两个质数（Closest Prime Numbers in Range）]] | Medium | 数学 |
| [[tlc-find-the-score-of-all-prefixes-of-an-array-0-whole\|LC 2640 一个数组所有前缀的分数（Find the Score of All Prefixes of an Array）]] | Medium | 数组、前缀和 |
| [[tlc-count-complete-subarrays-in-an-array-0-whole\|LC 2799 统计完全子数组的数目（Count Complete Subarrays in an Array）]] | Medium | 数组、哈希、滑动窗口 |
| [[tlc-minimum-moves-to-pick-k-ones-0-whole\|LC 3086 拾起 K 个 1 需要的最少行动次数（Minimum Moves to Pick K Ones）]] | Hard | 数组、贪心、滑动窗口、前缀和 |
| [[tlc-minimum-operations-to-make-character-frequencies-equal-0-whole\|LC 3389 使字符频率相等的最少操作次数（Minimum Operations to Make Character Frequencies Equal）]] | Hard | 哈希、字符串、动态规划 |
| [[tlc-minimum-cost-good-caption-0-whole\|LC 3441 变成好标题的最少代价（Minimum Cost Good Caption）]] | Hard | 字符串、动态规划 |
| [[tlc-lexicographically-smallest-generated-string-0-whole\|LC 3474 字典序最小的生成字符串（Lexicographically Smallest Generated String）]] | Hard | 字符串、贪心 |
| [[tlc-set-matrix-zeroes-0-whole\|LC 73 矩阵置零（Set Matrix Zeroes）]] | — | — |
| [[tlc-most-frequent-subtree-sum-0-whole\|LC 508 出现次数最多的子树元素和（Most Frequent Subtree Sum）]] | — | — |
| [[tlc-minimum-number-of-arrows-to-burst-balloons-0-whole\|LC 452 用最少数量的箭引爆气球]] | Medium | — |
| [[tlc-missing-ranges-0-whole\|LC 163 缺失的区间（Missing Ranges）]] | — | — |
| [[tlc-swim-in-rising-water-0-whole\|LC 778 水位上升的泳池中游泳（Swim in Rising Water）]] | — | — |
| [[tlc-invert-binary-tree-0-whole\|LC 226 翻转二叉树]] | Easy | — |
| [[tlc-design-add-and-search-words-data-structure-0-whole\|LC 211 添加与搜索单词 - 数据结构设计（Design Add and Search Words Data Structure）]] | Medium | 字符串、DFS、设计、字典树 |
| [[tlc-binary-tree-inorder-traversal-0-whole\|LC 94 二叉树的中序遍历]] | Easy | — |
| [[tlc-convert-binary-search-tree-to-sorted-doubly-linked-list-0-whole\|LC 426 将二叉搜索树转化为排序的双向链表（Convert Binary Search Tree to Sorted Doubly Linked List）]] | Medium | 链表、栈、树、DFS |
| [[tlc-minimum-remove-to-make-valid-parentheses-0-whole\|LC 1249 移除无效的括号（Minimum Remove to Make Valid Parentheses）]] | Medium | 字符串、栈 |
| [[tlc-score-of-parentheses-0-whole\|LC 856 括号的分数（Score of Parentheses）]] | Medium | 字符串、栈 |
| [[tlc-brightest-position-on-street-0-whole\|LC 2021 街上最亮的位置（Brightest Position on Street）]] | Medium | 数组、排序、前缀和 |
| [[tlc-kth-missing-positive-number-0-whole\|LC 1539 第 k 个缺失的正整数（Kth Missing Positive Number）]] | Easy | 数组、二分 |
| [[tlc-binary-tree-longest-consecutive-sequence-0-whole\|LC 298 二叉树最长连续序列（Binary Tree Longest Consecutive Sequence）]] | Medium | 树、DFS |
| [[tlc-matchsticks-to-square-0-whole\|LC 473 火柴拼正方形（Matchsticks to Square）]] | Medium | 数组、动态规划、回溯、位运算 |
| [[tlc-mini-parser-0-whole\|LC 385 迷你语法分析器（Mini Parser）]] | — | — |
| [[tlc-triangle-0-whole\|LC 120 三角形最小路径和]] | Medium | — |
| [[tlc-check-completeness-of-a-binary-tree-0-whole\|LC 958 二叉树的完全性检验]] | Medium | — |
| [[tlc-capacity-to-ship-packages-within-d-days-0-whole\|LC 1011 在 D 天内送达包裹的能力（Capacity To Ship Packages Within D Days）]] | Medium | — |
| [[tlc-tt-login-count-per-user-per-day-0-whole\|日志流中统计每个用户每天登录次数]] | — | — |
| [[tlc-meeting-rooms-0-whole\|LC 252 会议室（Meeting Rooms）]] | Easy | 数组、排序 |
| [[tlc-walls-and-gates-0-whole\|LC 286 墙与门（Walls and Gates）]] | Medium | 数组、BFS、矩阵 |
| [[tlc-convert-sorted-array-to-binary-search-tree-0-whole\|LC 108 将有序数组转换为二叉搜索树]] | Easy | — |
| [[tlc-clone-graph-0-whole\|LC 133 克隆图（Clone Graph）]] | Medium | 哈希、DFS、BFS、图 |
| [[tlc-asteroid-collision-0-whole\|LC 735 小行星碰撞（Asteroid Collision）]] | Medium | 数组、栈、模拟 |
| [[tlc-course-schedule-iv-0-whole\|LC 1462 课程表 IV（Course Schedule IV）]] | Medium | DFS、BFS、图、拓扑排序 |
| [[tlc-frog-jump-0-whole\|LC 403 青蛙过河（Frog Jump）]] | Hard | 数组、动态规划 |
| [[tlc-number-of-days-between-two-dates-0-whole\|LC 1360 日期之间隔几天（Number of Days Between Two Dates）]] | — | — |
| [[tlc-shortest-distance-from-all-buildings-0-whole\|LC 317 离建筑物最近的距离（Shortest Distance from All Buildings）]] | Hard | 数组、BFS、矩阵 |
| [[tlc-minimize-malware-spread-0-whole\|LC 924 尽量减少恶意软件的传播（Minimize Malware Spread）]] | Hard | 数组、哈希、DFS、BFS、并查集、图 |
| [[tlc-minimum-area-rectangle-0-whole\|LC 939 最小面积矩形（Minimum Area Rectangle）]] | Medium | — |
| [[tlc-greatest-common-divisor-of-strings-0-whole\|LC 1071 字符串的最大公因子（Greatest Common Divisor of Strings）]] | Easy | — |
| [[tlc-reorder-routes-to-make-all-paths-lead-to-the-city-zero-0-whole\|LC 1466 重新规划路线（Reorder Routes to Make All Paths Lead to the City Zero）]] | Medium | DFS、BFS、图 |
| [[tlc-number-of-good-leaf-nodes-pairs-0-whole\|LC 1530 好叶子节点对的数量（Number of Good Leaf Nodes Pairs）]] | Medium | 树、DFS |
| [[tlc-min-cost-to-connect-all-points-0-whole\|LC 1584 连接所有点的最小费用（Min Cost to Connect All Points）]] | Medium | 数组、并查集、图 |
| [[tlc-minimum-swaps-to-group-all-1s-together-ii-0-whole\|LC 2134 最少交换次数来组合所有的 1 II（Minimum Swaps to Group All 1's Together II）]] | Medium | — |
| [[tlc-split-message-based-on-limit-0-whole\|LC 2468 根据限制分割消息（Split Message Based on Limit）]] | Hard | 字符串 |
| [[tlc-minimum-moves-to-spread-stones-over-grid-0-whole\|LC 2850 将石头分散到网格图的最少移动次数（Minimum Moves to Spread Stones Over Grid）]] | Medium | 数组、动态规划、回溯、位运算、矩阵 |
| [[tlc-find-the-length-of-the-longest-common-prefix-0-whole\|LC 3043 最长公共前缀的长度（Find the Length of the Longest Common Prefix）]] | Medium | — |
| [[tlc-minimum-operations-to-write-the-letter-y-on-a-grid-0-whole\|LC 3071 在矩阵上写出字母 Y 所需的最少操作次数（Minimum Operations to Write the Letter Y on a Grid）]] | Medium | 数组、哈希、矩阵 |
| [[tlc-min-cost-climbing-stairs-0-whole\|LC 746 使用最小花费爬楼梯（Min Cost Climbing Stairs）]] | — | — |
| [[tlc-amount-of-time-for-binary-tree-to-be-infected-0-whole\|LC 2385 感染二叉树需要的总时间（Amount of Time for Binary Tree to Be Infected）]] | — | — |
| [[tlc-shortest-subarray-with-sum-at-least-k-0-whole\|LC 862 和至少为 K 的最短子数组]] | Hard | — |
| [[tlc-tt-flatten-multilevel-list-skip-empty-0-whole\|展平多级链表（值为空的嵌套节点要排除）]] | — | — |
| [[tlc-string-to-integer-atoi-0-whole\|LC 8 字符串转换整数 (atoi)]] | Medium | — |
| [[tlc-kth-smallest-subarray-sum-0-whole\|LC 1918 第 K 小的子数组和（Kth Smallest Subarray Sum）]] | — | — |
| [[tlc-robot-bounded-in-circle-0-whole\|LC 1041 困于环中的机器人（Robot Bounded In Circle）]] | Medium | 数学、字符串、模拟 |
| [[tlc-populating-next-right-pointers-in-each-node-0-whole\|LC 116 填充每个节点的下一个右侧节点指针（Populating Next Right Pointers in Each Node）]] | — | — |
| [[tlc-kth-smallest-element-in-a-bst-0-whole\|LC 230 二叉搜索树中第K小的元素]] | Medium | — |
| [[tlc-longest-string-chain-0-whole\|LC 1048 最长字符串链（Longest String Chain）]] | — | — |
| [[tlc-successful-pairs-of-spells-and-potions-0-whole\|LC 2300 咒语和药水的成功对数（Successful Pairs of Spells and Potions）]] | — | — |
| [[tlc-maximize-amount-after-two-days-of-conversions-0-whole\|LC 3387 两天自由外汇交易后的最大货币数（Maximize Amount After Two Days of Conversions）]] | — | — |
| [[tlc-tt-subarray-max-min-plus-max-0-whole\|长度至少为 2 的子数组，最大化 min + max]] | — | — |
| [[tlc-minimum-swaps-to-make-strings-equal-0-whole\|LC 1247 交换字符使得字符串相同（Minimum Swaps to Make Strings Equal）]] | — | — |
| [[tlc-vertical-order-traversal-of-a-binary-tree-0-whole\|LC 987 二叉树的垂序遍历（Vertical Order Traversal of a Binary Tree）]] | — | — |
| [[tlc-tt-inorder-string-iterator-0-whole\|二叉树中序字符迭代器]] | — | — |
| [[tlc-tt-chat-message-window-merge-0-whole\|聊天消息窗口合并（get_chat_messages）]] | — | — |
| [[tlc-tt-percentile-finder-0-whole\|PercentileFinder：实时维护数字并返回第 p 百分位]] | — | — |
| [[tlc-ip-to-cidr-0-whole\|LC 751 IP 到 CIDR（IP to CIDR）]] | — | — |
| [[tlc-binary-tree-cameras-0-whole\|LC 968 监控二叉树（Binary Tree Cameras）]] | — | — |
| [[tlc-max-submatrix-lcci-0-whole\|面试题 17.24 最大子矩阵]] | Hard | — |
| [[tlc-subsets-ii-0-whole\|LC 90 子集 II（Subsets II）]] | — | — |
| [[tlc-additive-number-0-whole\|LC 306 累加数]] | Medium | — |
| [[tlc-summary-ranges-0-whole\|LC 228 汇总区间（Summary Ranges）]] | — | — |
| [[tlc-tt-weighted-sampler-dynamic-update-0-whole\|按权重采样器（支持动态修改权重）]] | — | — |
| [[tlc-nested-list-weight-sum-0-whole\|LC 339 嵌套列表加权和（Nested List Weight Sum）]] | — | — |
| [[tlc-tt-ip-range-to-cidr-0-whole\|IP 区间转最少 CIDR 列表]] | — | — |
| [[tlc-binary-tree-level-order-traversal-ii-0-whole\|LC 107 二叉树的层次遍历 II]] | Medium | — |
| [[tlc-number-of-submatrices-that-sum-to-target-0-whole\|LC 1074 元素和为目标值的子矩阵数量]] | Hard | — |
| [[tlc-shortest-path-with-alternating-colors-0-whole\|LC 1129 颜色交替的最短路径]] | Medium | — |
| [[tlc-last-stone-weight-ii-0-whole\|LC 1049 最后一块石头的重量 II]] | Medium | — |
| [[tlc-xun-bao-0-whole\|LCP 13 寻宝]] | Hard | — |
| [[tlc-day-of-the-week-0-whole\|LC 1185 一周中的第几天]] | Easy | — |
| [[tlc-maximum-of-absolute-value-expression-0-whole\|LC 1131 绝对值表达式的最大值]] | Medium | — |
| [[tlc-majority-element-0-whole\|LC 169 多数元素]] | Easy | — |
| [[tlc-longest-repeating-substring-0-whole\|LC 1062 最长重复子串]] | Medium | — |
| [[tlc-codetop-supp-4-0-whole\|补充题4 手撕快速排序]] | Medium | — |
| [[tlc-codetop-supp-1-0-whole\|补充题1 排序奇升偶降链表]] | Medium | — |
| [[tlc-codetop-supp-23-0-whole\|补充题23 检测循环依赖]] | Medium | — |
| [[tlc-codetop-supp-2-0-whole\|补充题2 圆环回原点问题]] | Medium | — |
| [[tlc-codetop-supp-9-0-whole\|补充题9 36进制加法]] | Medium | — |
| [[tlc-single-threaded-cpu-0-whole\|LC 1834 单线程 CPU（Single-Threaded CPU）]] | Medium | 数组、排序、堆 |
| [[tlc-block-placement-queries-0-whole\|LC 3161 物块放置查询（Block Placement Queries）]] | Hard | 数组、二分 |
