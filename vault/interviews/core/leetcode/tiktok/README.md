# TikTok 字节高频题：总表

TikTok 和字节（美国与国内）面试里最常出现的编程题，按学习顺序排列：A 档最高频，B 档次之，档内按热度降序。点开每一行就是该题的完整标准答案（识别信号、推导、代码、复杂度、易错点、追问）。Anki 里同样的内容在 `LeetCode Tops::24 TikTok 字节高频 · 整题答案`，拆成小卡的版本在 `::25 … · 拆分背诵`。先刷模式识别 [[interviews/core/leetcode/tiktok/map/patterns|patterns]] 和 Python 工具箱 [[interviews/core/leetcode/tiktok/map/python|python]]。

## A 档：最高频

| 题 | 难度 | 主要考点 |
|---|---|---|
| [[tlc-tt-lru-cache-ttl-0-whole\|带 TTL 的 LRU 缓存（含 LFU / 加权 / 线程安全追问）]] | — | — |
| [[tlc-tt-rate-limiter-implementation-0-whole\|手写限流器（滑动窗口 / 令牌桶）]] | — | — |
| [[tlc-tt-islands-follow-ups-0-whole\|岛屿数量及其追问集合]] | — | — |
| [[tlc-tt-basic-calculator-ladder-0-whole\|计算器梯度题（无括号 -> 括号与一元负号，先校验再求值）]] | — | — |
| [[tlc-longest-substring-without-repeating-characters-0-whole\|LC 3 无重复字符的最长子串（Longest Substring Without Repeating Characters）]] | Medium | 哈希、字符串、滑动窗口 |
| [[tlc-lru-cache-0-whole\|LC 146 LRU 缓存（LRU Cache）]] | Medium | 哈希、链表、设计 |
| [[tlc-number-of-islands-0-whole\|LC 200 岛屿数量（Number of Islands）]] | Medium | 数组、DFS、BFS、并查集、矩阵 |
| [[tlc-reverse-nodes-in-k-group-0-whole\|LC 25 K 个一组翻转链表（Reverse Nodes in k-Group）]] | Hard | 链表、递归 |
| [[tlc-reverse-linked-list-0-whole\|LC 206 反转链表（Reverse Linked List）]] | Easy | 链表、递归 |
| [[tlc-kth-largest-element-in-an-array-0-whole\|LC 215 数组中的第K个最大元素（Kth Largest Element in an Array）]] | Medium | 数组、分治、排序、堆 |
| [[tlc-binary-tree-zigzag-level-order-traversal-0-whole\|LC 103 二叉树的锯齿形层序遍历（Binary Tree Zigzag Level Order Traversal）]] | Medium | 树、BFS |
| [[tlc-3sum-0-whole\|LC 15 三数之和（3Sum）]] | Medium | 数组、双指针、排序 |
| [[tlc-search-in-rotated-sorted-array-0-whole\|LC 33 搜索旋转排序数组（Search in Rotated Sorted Array）]] | Medium | 数组、二分 |
| [[tlc-best-time-to-buy-and-sell-stock-0-whole\|LC 121 买卖股票的最佳时机（Best Time to Buy and Sell Stock）]] | Easy | 数组、动态规划 |
| [[tlc-longest-palindromic-substring-0-whole\|LC 5 最长回文子串（Longest Palindromic Substring）]] | Medium | 双指针、字符串、动态规划 |
| [[tlc-spiral-matrix-0-whole\|LC 54 螺旋矩阵（Spiral Matrix）]] | Medium | 数组、矩阵、模拟 |
| [[tlc-trapping-rain-water-0-whole\|LC 42 接雨水（Trapping Rain Water）]] | Hard | 数组、双指针、动态规划、栈、单调栈 |
| [[tlc-lowest-common-ancestor-of-a-binary-tree-0-whole\|LC 236 二叉树的最近公共祖先（Lowest Common Ancestor of a Binary Tree）]] | Medium | 树、DFS |
| [[tlc-two-sum-0-whole\|LC 1 两数之和（Two Sum）]] | Easy | 数组、哈希 |
| [[tlc-permutations-0-whole\|LC 46 全排列（Permutations）]] | Medium | 数组、回溯 |
| [[tlc-maximum-subarray-0-whole\|LC 53 最大子数组和（Maximum Subarray）]] | Medium | 数组、分治、动态规划 |
| [[tlc-tt-largest-number-below-n-from-digits-0-whole\|用给定数字组成小于 N 的最大数]] | — | — |
| [[tlc-tt-reverse-k-group-variants-0-whole\|K 个一组翻转链表的变体（尾部、从尾部起、偶数长度组）]] | — | — |
| [[tlc-merge-k-sorted-lists-0-whole\|LC 23 合并 K 个升序链表（Merge k Sorted Lists）]] | Hard | 链表、分治、堆 |
| [[tlc-intersection-of-two-linked-lists-0-whole\|LC 160 相交链表（Intersection of Two Linked Lists）]] | Easy | 哈希、链表、双指针 |
| [[tlc-next-permutation-0-whole\|LC 31 下一个排列（Next Permutation）]] | Medium | — |
| [[tlc-longest-increasing-subsequence-0-whole\|LC 300 最长递增子序列（Longest Increasing Subsequence）]] | Medium | 数组、二分、动态规划 |
| [[tlc-valid-parentheses-0-whole\|LC 20 有效的括号（Valid Parentheses）]] | Easy | 字符串、栈 |
| [[tlc-merge-intervals-0-whole\|LC 56 合并区间（Merge Intervals）]] | Medium | 数组、排序 |
| [[tlc-merge-sorted-array-0-whole\|LC 88 合并两个有序数组]] | Easy | — |
| [[tlc-reorder-list-0-whole\|LC 143 重排链表（Reorder List）]] | Medium | 链表、双指针、栈、递归 |
| [[tlc-course-schedule-0-whole\|LC 207 课程表（Course Schedule）]] | Medium | DFS、BFS、图、拓扑排序 |
| [[tlc-course-schedule-ii-0-whole\|LC 210 课程表 II（Course Schedule II）]] | Medium | DFS、BFS、图、拓扑排序 |
| [[tlc-meeting-rooms-ii-0-whole\|LC 253 会议室 II（Meeting Rooms II）]] | Medium | 数组、双指针、贪心、排序、堆、前缀和 |
| [[tlc-remove-duplicate-letters-0-whole\|LC 316 去除重复字母（Remove Duplicate Letters）]] | Medium | 字符串、栈、贪心、单调栈 |
| [[tlc-number-of-distinct-islands-0-whole\|LC 694 不同岛屿的数量（Number of Distinct Islands）]] | Medium | 数组、哈希、DFS、BFS、并查集、排序、矩阵 |
| [[tlc-smallest-subsequence-of-distinct-characters-0-whole\|LC 1081 不同字符的最小子序列（Smallest Subsequence of Distinct Characters）]] | Medium | 字符串、栈、贪心、单调栈 |
| [[tlc-first-day-where-you-have-been-in-all-the-rooms-0-whole\|LC 1997 访问完所有房间的第一天（First Day Where You Have Been in All the Rooms）]] | Medium | 数组、动态规划 |
| [[tlc-subarray-with-elements-greater-than-varying-threshold-0-whole\|LC 2334 元素值大于变化阈值的子数组（Subarray With Elements Greater Than Varying Threshold）]] | Hard | — |
| [[tlc-block-placement-queries-0-whole\|LC 3161 物块放置查询（Block Placement Queries）]] | Hard | 数组、二分 |
| [[tlc-binary-tree-right-side-view-0-whole\|LC 199 二叉树的右视图（Binary Tree Right Side View）]] | Medium | 树、DFS、BFS |
| [[tlc-binary-tree-level-order-traversal-0-whole\|LC 102 二叉树的层序遍历]] | Medium | — |
| [[tlc-edit-distance-0-whole\|LC 72 编辑距离（Edit Distance）]] | Medium | 字符串、动态规划 |
| [[tlc-add-strings-0-whole\|LC 415 字符串相加（Add Strings）]] | Easy | 数学、字符串、模拟 |
| [[tlc-merge-two-sorted-lists-0-whole\|LC 21 合并两个有序链表]] | Easy | — |
| [[tlc-linked-list-cycle-0-whole\|LC 141 环形链表]] | Easy | — |
| [[tlc-reverse-linked-list-ii-0-whole\|LC 92 反转链表 II（Reverse Linked List II）]] | Medium | 链表 |
| [[tlc-binary-tree-maximum-path-sum-0-whole\|LC 124 二叉树中的最大路径和（Binary Tree Maximum Path Sum）]] | Hard | 动态规划、树、DFS |
| [[tlc-first-missing-positive-0-whole\|LC 41 缺失的第一个正数]] | Hard | — |
| [[tlc-text-justification-0-whole\|LC 68 文本左右对齐（Text Justification）]] | Hard | 数组、字符串、模拟 |
| [[tlc-compare-version-numbers-0-whole\|LC 165 比较版本号（Compare Version Numbers）]] | Medium | 双指针、字符串 |
| [[tlc-maximal-square-0-whole\|LC 221 最大正方形（Maximal Square）]] | Medium | 数组、动态规划、矩阵 |
| [[tlc-tt-deep-merge-nested-json-0-whole\|合并两个嵌套 JSON]] | — | — |
| [[tlc-longest-valid-parentheses-0-whole\|LC 32 最长有效括号（Longest Valid Parentheses）]] | Hard | 字符串、动态规划、栈 |
| [[tlc-search-insert-position-0-whole\|LC 35 搜索插入位置（Search Insert Position）]] | — | — |
| [[tlc-palindrome-partitioning-0-whole\|LC 131 分割回文串（Palindrome Partitioning）]] | — | — |
| [[tlc-sort-list-0-whole\|LC 148 排序链表（Sort List）]] | Medium | 链表、双指针、分治、排序 |
| [[tlc-design-tic-tac-toe-0-whole\|LC 348 设计井字棋（Design Tic-Tac-Toe）]] | — | — |
| [[tlc-design-circular-queue-0-whole\|LC 622 设计循环队列（Design Circular Queue）]] | — | — |
| [[tlc-transpose-matrix-0-whole\|LC 867 转置矩阵（Transpose Matrix）]] | — | — |
| [[tlc-reverse-nodes-in-even-length-groups-0-whole\|LC 2074 反转偶数长度组的节点（Reverse Nodes in Even Length Groups）]] | — | — |
| [[tlc-make-costs-of-paths-equal-in-a-binary-tree-0-whole\|LC 2673 使二叉树所有路径值相等的最小代价（Make Costs of Paths Equal in a Binary Tree）]] | — | — |
| [[tlc-median-of-two-sorted-arrays-0-whole\|LC 4 寻找两个正序数组的中位数]] | Hard | — |
| [[tlc-sqrtx-0-whole\|LC 69 x 的平方根 （Sqrt(x)）]] | Easy | 数学、二分 |
| [[tlc-generate-parentheses-0-whole\|LC 22 括号生成（Generate Parentheses）]] | Medium | 字符串、动态规划、回溯 |
| [[tlc-codetop-supp-4-0-whole\|补充题4 手撕快速排序]] | Medium | — |
| [[tlc-restore-ip-addresses-0-whole\|LC 93 复原 IP 地址（Restore IP Addresses）]] | Medium | 字符串、回溯 |
| [[tlc-symmetric-tree-0-whole\|LC 101 对称二叉树]] | Easy | — |
| [[tlc-combination-sum-0-whole\|LC 39 组合总和（Combination Sum）]] | Medium | 数组、回溯 |
| [[tlc-n-queens-0-whole\|LC 51 N 皇后（N-Queens）]] | Hard | 数组、回溯 |
| [[tlc-minimum-window-substring-0-whole\|LC 76 最小覆盖子串（Minimum Window Substring）]] | Hard | 哈希、字符串、滑动窗口 |
| [[tlc-word-search-0-whole\|LC 79 单词搜索（Word Search）]] | Medium | 数组、字符串、回溯、DFS、矩阵 |
| [[tlc-construct-binary-tree-from-preorder-and-inorder-traversal-0-whole\|LC 105 从前序与中序遍历序列构造二叉树（Construct Binary Tree from Preorder and Inorder Traversal）]] | Medium | 数组、哈希、分治、树 |
| [[tlc-basic-calculator-ii-0-whole\|LC 227 基本计算器 II（Basic Calculator II）]] | Medium | 数学、字符串、栈 |
| [[tlc-coin-change-0-whole\|LC 322 零钱兑换（Coin Change）]] | Medium | 数组、动态规划、BFS |
| [[tlc-top-k-frequent-elements-0-whole\|LC 347 前 K 个高频元素（Top K Frequent Elements）]] | Medium | 数组、哈希、分治、排序、堆 |
| [[tlc-decode-string-0-whole\|LC 394 字符串解码（Decode String）]] | Medium | 字符串、栈、递归 |
| [[tlc-subarray-sum-equals-k-0-whole\|LC 560 和为 K 的子数组（Subarray Sum Equals K）]] | Medium | 数组、哈希、前缀和 |
| [[tlc-making-a-large-island-0-whole\|LC 827 最大人工岛（Making A Large Island）]] | Hard | 数组、DFS、BFS、并查集、矩阵 |
| [[tlc-shortest-bridge-0-whole\|LC 934 最短的桥（Shortest Bridge）]] | Medium | 数组、DFS、BFS、矩阵 |
| [[tlc-longest-common-subsequence-0-whole\|LC 1143 最长公共子序列（Longest Common Subsequence）]] | Medium | 字符串、动态规划 |
| [[tlc-minimum-swaps-to-group-all-1s-together-0-whole\|LC 1151 最少交换次数来组合所有的 1（Minimum Swaps to Group All 1's Together）]] | Medium | 数组、滑动窗口 |
| [[tlc-sum-root-to-leaf-numbers-0-whole\|LC 129 求根到叶子节点数字之和]] | Medium | — |
| [[tlc-maximum-width-of-binary-tree-0-whole\|LC 662 二叉树最大宽度（Maximum Width of Binary Tree）]] | Medium | 树、DFS、BFS |
| [[tlc-implement-queue-using-stacks-0-whole\|LC 232 用栈实现队列]] | Easy | — |
| [[tlc-tt-course-schedule-output-path-0-whole\|课程表：输出可行学习路径 / 最短路径]] | — | — |
| [[tlc-remove-nth-node-from-end-of-list-0-whole\|LC 19 删除链表的倒数第N个节点]] | Medium | — |
| [[tlc-minimum-size-subarray-sum-0-whole\|LC 209 长度最小的子数组（Minimum Size Subarray Sum）]] | Medium | 数组、二分、滑动窗口、前缀和 |
| [[tlc-multiply-strings-0-whole\|LC 43 字符串相乘（Multiply Strings）]] | Medium | 数学、字符串、模拟 |
| [[tlc-basic-calculator-0-whole\|LC 224 基本计算器（Basic Calculator）]] | Hard | 数学、字符串、栈、递归 |
| [[tlc-find-median-from-data-stream-0-whole\|LC 295 数据流的中位数（Find Median from Data Stream）]] | Hard | 双指针、设计、排序、堆 |
| [[tlc-serialize-and-deserialize-binary-tree-0-whole\|LC 297 二叉树的序列化与反序列化（Serialize and Deserialize Binary Tree）]] | Hard | 字符串、树、DFS、BFS、设计 |
| [[tlc-design-hashmap-0-whole\|LC 706 设计哈希映射（Design HashMap）]] | Easy | 数组、哈希、链表、设计 |
| [[tlc-tt-currency-conversion-queries-0-whole\|汇率换算查询（多跳 / 无解返回 -1）]] | — | — |
| [[tlc-tt-kv-store-snapshot-restore-0-whole\|内存 KV 存储：快照与恢复（序列化）]] | — | — |
| [[tlc-tt-ring-walk-count-0-whole\|环上走 n 步回到起点的方案数]] | — | — |
| [[tlc-tt-delete-window-balance-even-odd-0-whole\|删除长度 k 的窗口使奇偶下标和相等]] | — | — |
| [[tlc-tt-contiguous-memory-allocator-0-whole\|连续内存分配器（first-fit、拆分与合并）]] | — | — |
| [[tlc-tt-path-sum-n-ary-prefix-sum-0-whole\|N 叉树路径和计数（暴力被拒，要前缀和）]] | — | — |
| [[tlc-tt-water-jug-shortest-operations-0-whole\|水壶问题：输出最短操作序列]] | — | — |
| [[tlc-tt-grid-min-cost-fuel-recharge-0-whole\|网格最小代价路径（障碍 / 加油站 / 油量 K）]] | — | — |
| [[tlc-tt-fixed-array-deque-o1-0-whole\|定长数组实现双端队列 / 列表（全部操作 O(1)）]] | — | — |
| [[tlc-tt-max-path-sum-with-path-0-whole\|二叉树最大路径和并还原 / 打印路径]] | — | — |
| [[tlc-tt-valid-parenthesis-string-print-all-0-whole\|含星号的有效括号 + 输出所有合法字符串]] | — | — |
| [[tlc-surrounded-regions-0-whole\|LC 130 被围绕的区域（Surrounded Regions）]] | — | — |
| [[tlc-best-time-to-buy-and-sell-stock-iv-0-whole\|LC 188 买卖股票的最佳时机 IV（Best Time to Buy and Sell Stock IV）]] | — | — |
| [[tlc-flatten-a-multilevel-doubly-linked-list-0-whole\|LC 430 扁平化多级双向链表（Flatten a Multilevel Doubly Linked List）]] | — | — |
| [[tlc-non-overlapping-intervals-0-whole\|LC 435 无重叠区间（Non-overlapping Intervals）]] | — | — |
| [[tlc-target-sum-0-whole\|LC 494 目标和（Target Sum）]] | — | — |
| [[tlc-stickers-to-spell-word-0-whole\|LC 691 贴纸拼词（Stickers to Spell Word）]] | — | — |
| [[tlc-flip-string-to-monotone-increasing-0-whole\|LC 926 将字符串翻转到单调递增（Flip String to Monotone Increasing）]] | — | — |
| [[tlc-create-binary-tree-from-descriptions-0-whole\|LC 2196 根据描述创建二叉树（Create Binary Tree From Descriptions）]] | — | — |
| [[tlc-longest-common-suffix-queries-0-whole\|LC 3093 最长公共后缀查询（Longest Common Suffix Queries）]] | — | — |
| [[tlc-rotate-array-0-whole\|LC 189 轮转数组（Rotate Array）]] | Medium | 数组、数学、双指针 |
| [[tlc-possible-bipartition-0-whole\|LC 886 可能的二分法（Possible Bipartition）]] | Medium | DFS、BFS、并查集、图 |
| [[tlc-tt-spiral-matrix-constant-space-0-whole\|螺旋矩阵：O(1) 额外空间且不修改输入]] | — | — |
| [[tlc-tt-seller-task-scheduler-0-whole\|卖家任务调度器（轮转 + VIP + 优先级）]] | — | — |
| [[tlc-tt-removable-timestamp-task-scheduler-0-whole\|可删除任务的时间戳调度器（popTask）]] | — | — |
| [[tlc-tt-pythagorean-triple-in-array-0-whole\|整数数组中的勾股三元组]] | — | — |
| [[tlc-tt-nested-comment-tree-0-whole\|由扁平记录构建嵌套评论树]] | — | — |
| [[tlc-tt-ai-assisted-order-validator-0-whole\|AI 辅助编码：OrderValidator（规则 DAG）]] | — | — |
| [[tlc-tt-flatten-multilevel-list-skip-empty-0-whole\|展平多级链表（值为空的嵌套节点要排除）]] | — | — |
| [[tlc-tt-sorted-array-more-than-n-over-3-0-whole\|有序数组中出现次数超过 n/3 的数]] | — | — |
| [[tlc-tt-login-count-per-user-per-day-0-whole\|日志流中统计每个用户每天登录次数]] | — | — |
| [[tlc-tt-subarray-max-min-plus-max-0-whole\|长度至少为 2 的子数组，最大化 min + max]] | — | — |
| [[tlc-tt-inorder-string-iterator-0-whole\|二叉树中序字符迭代器]] | — | — |
| [[tlc-tt-chat-message-window-merge-0-whole\|聊天消息窗口合并（get_chat_messages）]] | — | — |
| [[tlc-tt-percentile-finder-0-whole\|PercentileFinder：实时维护数字并返回第 p 百分位]] | — | — |
| [[tlc-tt-weighted-sampler-dynamic-update-0-whole\|按权重采样器（支持动态修改权重）]] | — | — |
| [[tlc-tt-ip-range-to-cidr-0-whole\|IP 区间转最少 CIDR 列表]] | — | — |
| [[tlc-all-nodes-distance-k-in-binary-tree-0-whole\|LC 863 二叉树中所有距离为 K 的结点（All Nodes Distance K in Binary Tree）]] | Medium | 哈希、树、DFS、BFS |
| [[tlc-path-sum-iii-0-whole\|LC 437 路径总和 III（Path Sum III）]] | Medium | 树、DFS |
| [[tlc-yong-liang-ge-zhan-shi-xian-dui-lie-lcof-0-whole\|剑指 Offer 09 用两个栈实现队列]] | Easy | — |
| [[tlc-serialize-and-deserialize-n-ary-tree-0-whole\|LC 428 序列化和反序列化 N 叉树（Serialize and Deserialize N-ary Tree）]] | Hard | 字符串、树、DFS、BFS |
| [[tlc-find-all-anagrams-in-a-string-0-whole\|LC 438 找到字符串中所有字母异位词（Find All Anagrams in a String）]] | Medium | 哈希、字符串、滑动窗口 |

## B 档：次高频

| 题 | 难度 | 主要考点 |
|---|---|---|
| [[tlc-permutation-sequence-0-whole\|LC 60 排列序列（Permutation Sequence）]] | — | — |
| [[tlc-set-matrix-zeroes-0-whole\|LC 73 矩阵置零（Set Matrix Zeroes）]] | — | — |
| [[tlc-subsets-ii-0-whole\|LC 90 子集 II（Subsets II）]] | — | — |
| [[tlc-populating-next-right-pointers-in-each-node-0-whole\|LC 116 填充每个节点的下一个右侧节点指针（Populating Next Right Pointers in Each Node）]] | — | — |
| [[tlc-word-ladder-ii-0-whole\|LC 126 单词接龙 II（Word Ladder II）]] | — | — |
| [[tlc-find-minimum-in-rotated-sorted-array-ii-0-whole\|LC 154 寻找旋转排序数组中的最小值 II（Find Minimum in Rotated Sorted Array II）]] | — | — |
