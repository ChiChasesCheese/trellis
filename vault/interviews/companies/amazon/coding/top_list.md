# Amazon 编码题单（Top list）：从 A 档挑出的 51 题，按 11 个模式分组

> 来源：`vault/interviews/core/leetcode/companies/amazon.md`（生成文件，2026-10-15 由 GitHub 两个仓库汇总：
> [liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems)、
> [snehasishroy/leetcode-companywise-interview-questions](https://github.com/snehasishroy/leetcode-companywise-interview-questions)）。
> 频率是 LeetCode Premium 的相对值（0–100），不是出现次数。
> 挑选脚本：`coding/pick.py`（可重复运行：`python3 -I coding/pick.py`），下面「脚本输出」一节是它的**原始输出**。
> Chi 的要求（2026-10-15）：bar 永远按 senior 准备 → 每个模式都至少带 1–2 道 A 档里的 Hard，每题的讲义里都有「资深追问」。

## 挑选规则（脚本里就是这样写的）

1. 只看 A 档（近 6 个月出现，或频率 ≥ 70），并且「近 ✓」和「双源 ✓」都满足，且有 LC 编号（A 档 821 行里有 21 行没有编号、也不是双源，被过滤）。
2. 去掉数据库题和只能用 JavaScript 做的题；用 `TAG_RULES`（按 LeetCode 标签）加上少量手工 `OVERRIDE` 把每题归到 11 个模式之一。归不进任何模式的（纯数学、字符串模拟、位运算、回溯、贪心）不选。
3. **按模式去重**：同一思想的变体（`FAMILIES`：例如 3Sum / 3Sum Closest / 4Sum / Two Sum II 是同一家族；Next Greater Element I / II 与 Daily Temperatures；Number of Islands 与 Flood Fill）只保留频率最高的一个。
4. 每个模式按频率取前 N（`QUOTA`；同频率时用 `PREFER` 打破平局，例如 739、460、206 这些「教学价值高」的题优先）。
5. **Senior bar 补强**：每个模式再补 Hard 到 2 道（若 A 档里有）：`HARD_PREFER` 顺序优先，其次按频率。这一步加入了 41、76、269、410、25、10、312、588，其余 Hard 本来就在频率榜上。

## 脚本输出（`python3 -I coding/pick.py`，2026-10-15）

- A-tier rows with LC number: 800
- recent+both: 756
- classified into a pattern: 594
- picked: 51

### 01 Hash map counting / prefix sum  (5 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | 100 | freq | Array, Hash Table |
| 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | 81 | freq | Array, Hash Table, String, Sorting |
| 128 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | 75 | freq | Array, Hash Table, Union-Find |
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | 75 | freq | Array, Hash Table, Prefix Sum |
| 41 | [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | Hard | 62 | Hard add-on | Array, Hash Table |

### 02 Two pointers / sliding window  (5 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | 88 | freq | Hash Table, String, Sliding Window |
| 42 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | 88 | freq | Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack |
| 15 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | 78 | freq | Array, Two Pointers, Sorting |
| 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | 77 | freq | Array, Two Pointers, Greedy |
| 76 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | 62 | Hard add-on | Hash Table, String, Sliding Window |

### 03 Intervals (sort + sweep)  (4 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 56 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | 77 | freq | Array, Sorting, Quicksort |
| 253 | [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Medium | 62 | freq | Array, Two Pointers, Greedy, Sorting, Heap (Priority Queue) |
| 1235 | [Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Hard | 51 | freq | Array, Binary Search, Dynamic Programming, Sorting |
| 435 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | 43 | freq | Array, Dynamic Programming, Greedy, Sorting |

### 04 Stack / monotonic stack  (4 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 20 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | 75 | freq | String, Stack, Bracket Sequences |
| 239 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | 66 | freq | Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue |
| 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | 62 | freq | Array, Stack, Monotonic Stack |
| 84 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | 62 | freq | Array, Stack, Monotonic Stack, Range Minimum/Maximum Query |

### 05 Heap / top-k  (4 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 767 | [Reorganize String](https://leetcode.com/problems/reorganize-string/) | Medium | 78 | freq | Hash Table, String, Greedy, Sorting, Heap (Priority Queue) |
| 23 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | 75 | freq | Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort, Tournament Sort |
| 347 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | 75 | freq | Array, Hash Table, Divide and Conquer, Sorting, Heap (Priority Queue) |
| 295 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | 63 | freq | Two Pointers, Design, Sorting, Heap (Priority Queue), Data Stream |

### 06 BFS / DFS on grids & graphs, topological sort  (5 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | 88 | freq | Array, Depth-First Search, Breadth-First Search, Union-Find, Matrix |
| 994 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | 75 | freq | Array, Breadth-First Search, Matrix |
| 127 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | 75 | freq | Hash Table, String, Breadth-First Search, Bidirectional Search |
| 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | 75 | freq | Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort, Directed Acyclic Graph |
| 269 | [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | Hard | 38 | Hard add-on | Array, String, Depth-First Search, Breadth-First Search, Graph Theory |

### 07 Binary search (incl. on the answer)  (4 picked; quota 3 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 4 | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | 77 | freq | Array, Binary Search, Divide and Conquer |
| 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | 75 | freq | Array, Binary Search |
| 875 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | 75 | freq | Array, Binary Search |
| 410 | [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Hard | 52 | Hard add-on | Array, Binary Search, Dynamic Programming, Greedy, Prefix Sum |

### 08 Linked list  (5 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 2 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | 80 | freq | Linked List, Math, Recursion |
| 138 | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | 75 | freq | Hash Table, Linked List |
| 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | 67 | freq | Linked List, Recursion |
| 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | 62 | freq | Linked List, Recursion |
| 25 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Hard | 62 | Hard add-on | Linked List, Recursion |

### 09 Trees / LCA  (4 picked; quota 4 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 236 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | 75 | freq | Tree, Depth-First Search, Binary Tree, Binary Lifting, Lowest Common Ancestor |
| 124 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | 62 | freq | Dynamic Programming, Tree, Depth-First Search, Binary Tree, DP on Trees |
| 199 | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | Medium | 62 | freq | Tree, Depth-First Search, Breadth-First Search, Binary Tree |
| 297 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | 62 | freq | String, Tree, Depth-First Search, Breadth-First Search, Design |

### 10 Dynamic programming 1D / 2D  (7 picked; quota 5 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | 88 | freq | Array, Dynamic Programming |
| 5 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | 78 | freq | Two Pointers, String, Dynamic Programming, Manacher |
| 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | 75 | freq | Array, Divide and Conquer, Dynamic Programming |
| 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | 67 | freq | Math, Dynamic Programming, Memoization |
| 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | 63 | freq | Array, Dynamic Programming, Breadth-First Search, Knapsack Problem, Complete Knapsack |
| 10 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard | 54 | Hard add-on | String, Dynamic Programming, Recursion |
| 312 | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Hard | 38 | Hard add-on | Array, Dynamic Programming |

### 11 Design: LRU / LFU / iterators  (4 picked; quota 3 + Hard add-ons)

| LC | Problem | Diff | Freq | Why | Tags |
|---:|---|---|---:|---|---|
| 146 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | 88 | freq | Hash Table, Linked List, Design, Doubly-Linked List |
| 460 | [LFU Cache](https://leetcode.com/problems/lfu-cache/) | Hard | 62 | freq | Hash Table, Linked List, Design, Doubly-Linked List |
| 380 | [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | Medium | 62 | freq | Array, Hash Table, Math, Design, Randomized |
| 588 | [Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system/) | Hard | 38 | Hard add-on | Hash Table, String, Design, Trie, Sorting |

order-by-frequency: 1(100), 3(88), 42(88), 121(88), 146(88), 200(88), 49(81), 2(80), 5(78), 15(78), 767(78), 4(77), 11(77), 56(77), 994(75), 20(75), 23(75), 33(75), 53(75), 127(75), 128(75), 138(75), 207(75), 236(75), 347(75), 560(75), 875(75), 21(67), 70(67), 239(66), 295(63), 322(63), 739(62), 84(62), 460(62), 380(62), 206(62), 25(62), 41(62), 76(62), 124(62), 199(62), 253(62), 297(62), 10(54), 410(52), 1235(51), 435(43), 269(38), 312(38), 588(38)

## 这份清单没有覆盖的东西（诚实说明）

- **回溯（backtracking）**：22 Generate Parentheses（75）、17 Letter Combinations（67）、78 Subsets（64）、46 Permutations（56）、79 Word Search（65）。它们在 A 档里频率很高，但不在你指定的 11 个模式里。如果 5 天后还有余力，最先补的就是这一组：同一个「选择 → 递归 → 撤销」模板。
- **贪心**：55 Jump Game（68）、45 Jump Game II（62）。435（区间）里已经用到「按终点排序」的贪心，其余按需补。
- **矩阵模拟 / 数学 / 字符串杂题**：54 Spiral Matrix（65）、48 Rotate Image（64）、14 Longest Common Prefix（75）、9 Palindrome Number（75）。这类题考的是细心和边界，不是模式；手写一遍各 10 分钟即可。
- **Trie、并查集（Union-Find）、位运算**：并查集在第 06 讲的追问里出现（岛屿 II、Tile 合并），Trie 在 588 的实现里隐含。没有单独成讲。
- 频率 < 50 的 Hard 里还有一批（例如 312 已入选；其他如 Word Search II、Candy 未入选）。

## 怎么用这份清单

- 先读 `plan.md`，按天读讲义、做每天的 2 道必做题。
- 每道题的参考解在 `solutions/<LC编号>_<slug>.py`，里面有 `assert` 和（多数题）与暴力解的随机对拍，用 `python3 -I coding/run_all.py` 一次全跑。
- 讲义编号与模式编号一一对应：`patterns/01_…` 到 `patterns/11_…`。
