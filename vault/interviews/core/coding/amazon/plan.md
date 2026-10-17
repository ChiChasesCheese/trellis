# 编码冲刺计划：5 天主线 + 3 个可选模块

每天 2 道必做题，按模式顺序练，每天开始前先读指定的讲义。全部用 Python，不用 IDE：面试要求在在线编辑器里写出语法正确的代码，不写伪代码。题单在 [[top_list]]，评分标准和答题节奏在 [[amazon_bar]]。5 天主线覆盖讲义 01–11，可选模块覆盖 12–16。所有参考解都能离线运行，飞机上也能练。

## 每天的固定节奏（约 4.5–5 小时）

| 时间 | 做什么 |
|---|---|
| 60–75 分钟 | 读当天的讲义：先读第 1、2、3 节（为什么存在 → 模板 → 手算），读完合上，凭记忆把模板默写一遍 |
| 2 × 40 分钟 | 做当天 2 道必做题：先不看讲义里的解法，按 [[amazon_bar]] 第 6 节的 45 分钟节奏边说边写，计时 40 分钟，包含自己测试 |
| 20 分钟 | 把这两题的「资深追问」逐条出声回答，再对照讲义里的答案要点补漏 |
| 10 分钟 | 打开 `solutions/<题号>_*.py`，和自己的实现对比；记下 2 个 bug 或疏漏，写进下面的错题本 |
| 选做 | 当天的加练（Hard 或高频题），时间有就做 |

做完一题的验收标准：(1) 不看资料写出可运行代码；(2) 说得出时间、空间复杂度和原因；(3) 至少回答 3 条资深追问；(4) 自己列出并跑过边界用例。

## 日程

### Day 1：哈希 + 双指针 / 滑动窗口

- 先读：`patterns/01_hash_map_counting.md`，再读 `patterns/02_two_pointers_sliding_window.md`
- 必做 1：LC 560 Subarray Sum Equals K（Medium）——前缀和 + 哈希计数；讲义 01 §4.4
- 必做 2：LC 3 Longest Substring Without Repeating Characters（Medium）——滑动窗口；讲义 02 §4.1
- 加练：LC 1 Two Sum（热身 5 分钟）；LC 76 Minimum Window Substring（Hard）；LC 41 First Missing Positive（Hard）
- 要能口述：为什么 560 不能用滑动窗口；为什么窗口里 `last[ch] >= left` 不能省。

### Day 2：区间 + 栈 / 单调栈

- 先读：`patterns/03_intervals.md`，再读 `patterns/04_stack_monotonic_stack.md`
- 必做 1：LC 253 Meeting Rooms II（Medium）——扫描线 / 最小堆；讲义 03 §4.2
- 必做 2：LC 739 Daily Temperatures（Medium）——单调栈；讲义 04 §4.2
- 加练：LC 56 Merge Intervals；LC 84 Largest Rectangle in Histogram（Hard）；LC 239 Sliding Window Maximum（Hard）
- 要能口述：区间题里 `<` / `<=` 的约定；单调栈为什么是 O(n)。

### Day 3：堆 / Top-K + 图（BFS / DFS / 拓扑）

- 先读：`patterns/05_heap_top_k.md`，再读 `patterns/06_graph_bfs_dfs_topo.md`
- 必做 1：LC 347 Top K Frequent Elements（Medium）——大小为 k 的堆，再写桶排序版本；讲义 05 §4.1
- 必做 2：LC 207 Course Schedule（Medium）——Kahn 拓扑排序，顺手写 LC 210；讲义 06 §4.4
- 加练：LC 200 Number of Islands（BFS 版本）；LC 994 Rotting Oranges（多源 BFS）；LC 23 Merge k Sorted Lists（Hard）；LC 295 Find Median from Data Stream（Hard）；LC 127 Word Ladder（Hard）
- 要能口述：Python `heapq` 的最小堆、取负、tie-breaker；BFS 为什么要在入队时标记已访问。

### Day 4：二分（含对答案二分）+ 动态规划

- 先读：`patterns/07_binary_search_on_answer.md`，再读 `patterns/10_dp_1d_2d.md`
- 必做 1：LC 875 Koko Eating Bananas（Medium）——对答案二分；讲义 07 §4.1
- 必做 2：LC 322 Coin Change（Medium）——1D DP，并解释贪心反例；讲义 10 §4.4
- 加练：LC 33 Search in Rotated Sorted Array；LC 53 Maximum Subarray；LC 121 Best Time to Buy and Sell Stock；LC 4 Median of Two Sorted Arrays（Hard）；LC 410 Split Array Largest Sum（Hard）；LC 10 Regular Expression Matching（Hard）
- 要能口述：`while lo < hi`、`hi = mid`、下中位三者为什么必须配套；DP 五步法（状态 → 转移 → 初值 → 顺序 → 答案）。

### Day 5：链表 + 树 / LCA + 设计（LRU）

- 先读：`patterns/08_linked_list.md`，再读 `patterns/09_trees_lca.md`，最后读 `patterns/11_design_lru_lfu_iterators.md`（LRU 用到第 08 讲的双向链表，所以 08 必须先读）
- 必做 1：LC 236 Lowest Common Ancestor of a Binary Tree（Medium）——后序 DFS；讲义 09 §4.1
- 必做 2：LC 146 LRU Cache（Medium）——哈希表 + 双向链表，手写，不用 `OrderedDict`；讲义 11 §4.1
- 加练：LC 2 Add Two Numbers；LC 206 Reverse Linked List；LC 25 Reverse Nodes in k-Group（Hard）；LC 124 Binary Tree Maximum Path Sum（Hard）；LC 460 LFU Cache（Hard）
- 要能口述：反转链表四步的顺序；树递归里「返回给父节点的值」与「更新答案的值」的区别；LRU 为什么节点里必须存 key。

### 最后一晚：模拟一轮（30–45 分钟）

- 从 [[top_list]] 里随机抽一道还没做过的 Medium，完全按 [[amazon_bar]] 第 6 节的 45 分钟节奏出声做一遍；最后 5 分钟回答 3 条资深追问（规模 ×1000 / 流式 / 并发 / 测试任选）。
- 重读 [[amazon_bar]] 第 3 节的英文句型和第 5 节的 senior 对照表。

## 可选模块：模式 12–16（回溯 · 贪心 · 字典树 · 并查集 · 矩阵模拟）

5 天主线做完（或某天提前做完）还有时间，就按下面三个模块补，每个模块 2–2.5 小时。时间只够一个模块时，先做模块 A，其次模块 C。节奏同上：先读讲义第 1–3 节、默写模板；必做题先不看解法，计时 40 分钟；然后口述资深追问。

| 模块 | 先读 | 必做 1（40 分钟） | 必做 2（40 分钟） | 加练 | 要能口述 |
|---|---|---|---|---|---|
| A · 约 2.5 小时 | `patterns/12_backtracking.md`，再读 `patterns/13_greedy.md` | LC 22 Generate Parentheses——两个计数器的剪枝；讲义 12 §4.1 | LC 55 Jump Game——`farthest` 和一句话证明；讲义 13 §4.1 | LC 79 Word Search；LC 78 Subsets（含 90、46）；LC 51 N-Queens（Hard）；LC 621 Task Scheduler；LC 135 Candy（Hard）；LC 871 Refueling Stops（Hard） | 回溯为什么要撤销、为什么记录答案要拷贝；贪心的交换论证，以及硬币 `[1,3,4]` 为什么贪心失败 |
| B · 约 2.5 小时 | `patterns/14_trie.md`，再读 `patterns/15_union_find.md` | LC 211 Design Add and Search Words 或 LC 1268——手写 trie；讲义 14 §4.4 / §4.3 | LC 547 Number of Provinces——手写并查集（路径减半 + 按大小）；讲义 15 §4.1 | LC 212 Word Search II（Hard）；LC 399 Evaluate Division（带权）；LC 721 Accounts Merge；LC 827 Making A Large Island（Hard）；LC 472 Concatenated Words（Hard）；LC 305 Number of Islands II（Hard） | trie 的内存代价与替代方案；为什么 `union` 要合并根、要返回布尔值；`find` 为什么不是线程安全的 |
| C · 约 2 小时 | `patterns/16_matrix_simulation.md` | LC 54 Spiral Matrix——四条边界 + 两个保护条件；讲义 16 §4.1 | LC 48 Rotate Image——转置 + 翻转，并写出下标公式；讲义 16 §4.2 | LC 73 Set Matrix Zeroes；LC 36 Valid Sudoku；LC 348 Design Tic-Tac-Toe；LC 68 Text Justification（Hard）；回到 LC 37 Sudoku Solver（Hard） | 为什么 `[[0]*c]*r` 是错的；73 的顺序；矩阵题的固定边界测试清单 |

每个模块结束后，把两道必做题的「资深追问」各回答 3 条（规模 ×1000 / 流式 / 内存 / 并发 / 接口 / 测试任选），并在错题本里记 2 条。回溯、贪心、矩阵模拟题在白板上最容易漏边界，面试时可以主动说「我会写一个暴力解做随机对拍」。

## 错题本（做题时填）

| 日期 | 题号 | 错在哪里 | 下次怎么避免 |
|---|---|---|---|
| | | | |
