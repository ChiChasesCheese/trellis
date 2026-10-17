# Amazon 编码题单：16 个模式，81 道题

按模式分组的练习清单。每个模式先读对应讲义的第 1–3 节、默写模板，再按表里的顺序做题；每组都带 1–2 道 Hard，因为你要按 senior 的标准准备。Medium 题计时 40 分钟，做完回答讲义里的「资深追问」。
排期见 [[plan]]，评分标准与答题节奏见 [[amazon_bar]]。

## 01 哈希表计数与前缀和

讲义：[[01_hash_map_counting]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | 哈希表存「还需要的另一半」，一遍扫描 |
| 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | 排序后的字符串（或 26 位计数）做 key 分组 |
| 128 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | 只从连续段的起点往右数，哈希集合 O(n) |
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | 前缀和 + 哈希计数，初值 `{0: 1}` |
| 41 | [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | Hard | 把数放回下标 `v-1`（原地哈希），第一个对不上的位置就是答案 |

## 02 双指针与滑动窗口

讲义：[[02_two_pointers_sliding_window]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | 滑动窗口 + 每个字符最后出现的位置 |
| 42 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | 双指针，哪边矮就结算哪边的水 |
| 15 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | 排序 + 固定一个数 + 双指针，跳过重复 |
| 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | 双指针，移动较矮的一边 |
| 76 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | 可变窗口：先扩到覆盖，再缩到最小 |

## 03 区间

讲义：[[03_intervals]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 56 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | 按起点排序，与最后一个区间比较后合并或新增 |
| 253 | [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Medium | 按起点排序 + 最小堆存结束时间（或扫描线） |
| 1235 | [Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Hard | 按结束时间排序 + DP + 二分找上一个不冲突的任务 |
| 435 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | 按终点排序的贪心，数重叠的个数 |

## 04 栈与单调栈

讲义：[[04_stack_monotonic_stack]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 20 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | 栈：遇到右括号弹出并检查配对 |
| 239 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | 单调递减双端队列存下标 |
| 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | 单调栈存「还在等更高温度」的下标 |
| 84 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | 单调递增栈，弹出时结算以它为高的矩形 |

## 05 堆与 Top-K

讲义：[[05_heap_top_k]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 767 | [Reorganize String](https://leetcode.com/problems/reorganize-string/) | Medium | 按剩余次数的最大堆，每次取不同于上一个的两个 |
| 23 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | 大小为 k 的最小堆，每次弹出最小并推入其后继 |
| 347 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | 大小为 k 的最小堆，或桶排序 |
| 295 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | 大顶堆 + 小顶堆，保持大小差不超过 1 |

## 06 图：BFS / DFS / 拓扑排序

讲义：[[06_graph_bfs_dfs_topo]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | 遍历格子，遇到陆地就 BFS/DFS 淹掉整座岛 |
| 994 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | 多源 BFS，按层数计时间 |
| 127 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | BFS 求最短变换序列，用通配符分桶建邻接 |
| 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Kahn 拓扑排序，处理的节点数等于课程数就无环 |
| 269 | [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | Hard | 由相邻单词的第一个不同字符建边，再拓扑排序 |

## 07 二分查找（含对答案二分）

讲义：[[07_binary_search_on_answer]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 4 | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | 在短数组上二分切分点，使左右两半大小相等且交叉有序 |
| 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | 每次二分，判断哪一半有序再决定去向 |
| 875 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | 对答案（速度）二分，用可行性检查函数 |
| 410 | [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Hard | 对答案（最大子数组和）二分 + 贪心检查可行 |

## 08 链表

讲义：[[08_linked_list]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 2 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | 哑结点 + 逐位相加带进位 |
| 138 | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | 哈希表映射旧节点到新节点，两遍复制 |
| 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | 哑结点 + 双指针拼接 |
| 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | 三个指针 prev/cur/next 逐个反转 |
| 25 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Hard | 每 k 个一组原地反转，接回前后 |

## 09 二叉树与 LCA

讲义：[[09_trees_lca]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 236 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | 后序 DFS：左右都非空的节点就是分叉点 |
| 124 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | 返回单边最大下行和，用左 + 根 + 右更新答案 |
| 199 | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | Medium | 层序遍历取每层最后一个 |
| 297 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | 前序遍历 + 显式空标记 |

## 10 动态规划

讲义：[[10_dp_1d_2d]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | 维护历史最低价，枚举卖出日 |
| 5 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | 从每个中心向两边扩展，奇偶两种 |
| 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | Kadane：以当前位置结尾的最大和 |
| 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | `dp[i] = dp[i-1] + dp[i-2]`，滚动两个变量 |
| 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | `dp[a] = min(dp[a-c]) + 1`，贪心会在 `[1,3,4]` 上失败 |
| 10 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard | 二维 DP：`*` 表示零次或多次前一个字符 |
| 312 | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Hard | 区间 DP：枚举最后一个被戳破的气球 |

## 11 设计题：LRU / LFU / 迭代器

讲义：[[11_design_lru_lfu_iterators]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 146 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | 哈希表 + 双向链表，节点里存 key |
| 460 | [LFU Cache](https://leetcode.com/problems/lfu-cache/) | Hard | key→节点 + 频率→有序字典 + 最小频率 |
| 380 | [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | Medium | 数组 + 哈希表，删除时与末尾元素交换 |
| 588 | [Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system/) | Hard | 目录树，路径按 `/` 切分，目录用 dict |

## 12 回溯

讲义：[[12_backtracking]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 22 | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | 两个计数器（左括号数、右括号数）剪枝 |
| 17 | [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Medium | 按位置逐位选字母，路径到达长度即记录 |
| 79 | [Word Search](https://leetcode.com/problems/word-search/) | Medium | 格子上 DFS，标记再还原 |
| 78 | [Subsets](https://leetcode.com/problems/subsets/) | Medium | 选或不选（或按 start 枚举）每个元素 |
| 51 | [N-Queens](https://leetcode.com/problems/n-queens/) | Hard | 按行放皇后，用列/两条对角线集合判冲突 |
| 37 | [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) | Hard | 选候选最少的格子，行/列/宫掩码 |

## 13 贪心

讲义：[[13_greedy]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 55 | [Jump Game](https://leetcode.com/problems/jump-game/) | Medium | 维护能到达的最远下标 |
| 621 | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Medium | 最大频次 `m` 决定框架：`(m-1)*(n+1) + 并列数` |
| 134 | [Gas Station](https://leetcode.com/problems/gas-station/) | Medium | 总油量够用，油箱为负就把起点移到下一站 |
| 179 | [Largest Number](https://leetcode.com/problems/largest-number/) | Medium | 自定义比较 `a+b > b+a` |
| 135 | [Candy](https://leetcode.com/problems/candy/) | Hard | 左右各扫一遍，取较大值 |
| 871 | [Minimum Number of Refueling Stops](https://leetcode.com/problems/minimum-number-of-refueling-stops/) | Hard | 最大堆存路过的加油站油量，没油了才后悔地加最大的 |

## 14 字典树

讲义：[[14_trie]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 14 | [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | Easy | 逐列比较，或排序后只比较首尾 |
| 139 | [Word Break](https://leetcode.com/problems/word-break/) | Medium | `dp[i]` = 前 i 个字符能否被切分 |
| 1268 | [Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/) | Medium | 排序 + 二分，或 trie 每个节点存前三个 |
| 211 | [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | trie + 遇到 `.` 时对所有孩子递归 |
| 212 | [Word Search II](https://leetcode.com/problems/word-search-ii/) | Hard | trie 剪枝的棋盘 DFS，找到就删除分支 |
| 472 | [Concatenated Words](https://leetcode.com/problems/concatenated-words/) | Hard | 对每个词做 Word Break，至少拆成两段 |

## 15 并查集

讲义：[[15_union_find]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 547 | [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Medium | 并查集数连通块，或 DFS |
| 130 | [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | Medium | 从边界的 O 出发标记，其余翻转 |
| 399 | [Evaluate Division](https://leetcode.com/problems/evaluate-division/) | Medium | 带权并查集，或图上 BFS 乘边权 |
| 721 | [Accounts Merge](https://leetcode.com/problems/accounts-merge/) | Medium | 按邮箱并查集合并账号 |
| 827 | [Making A Large Island](https://leetcode.com/problems/making-a-large-island/) | Hard | 先给每座岛标号并记大小，再枚举 0 求相邻不同岛之和 + 1 |
| 305 | [Number of Islands II](https://leetcode.com/problems/number-of-islands-ii/) | Hard | 稀疏并查集（dict），每加一格先 +1 再对每个邻居成功合并 -1 |

## 16 矩阵与模拟

讲义：[[16_matrix_simulation]]

| LC | 题目 | 难度 | 一句话思路 |
|---:|---|---|---|
| 54 | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Medium | 四条收缩的边界，或方向数组加转向 |
| 48 | [Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | 转置后每行翻转 |
| 36 | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | Medium | 行、列、宫三组集合（或位掩码） |
| 73 | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Medium | 用首行首列做标记，注意先读后写的顺序 |
| 348 | [Design Tic-Tac-Toe](https://leetcode.com/problems/design-tic-tac-toe/) | Medium | 每行、每列、两条对角线各一个计数器 |
| 68 | [Text Justification](https://leetcode.com/problems/text-justification/) | Hard | 先贪心决定每行放哪些词，再均分空格，最后一行左对齐 |
