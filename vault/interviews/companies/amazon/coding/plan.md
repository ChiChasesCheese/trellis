# 5 天编码冲刺计划（2026-10-15 → 10-19）

> 目标：onsite 约 2026-10-20/21（由 10/19 去程机票推断，招聘邮件未见——**未确认**）。每天 **2 道必做题**，按模式顺序（01 → 11），每天开始前**先读指定的讲义**。
> 全部使用 Python，不用 IDE（官方要求在线编辑器里写"syntactically correct code, no pseudo code"，见 `amazon_bar.md`）。
> 总量：11 讲 + 10 道必做题 + 每天一道加练的 Hard。题单与选题规则见 `top_list.md`；所有参考解在 `solutions/`，一次全跑：`python3 -I coding/run_all.py`（不需要网络，飞机上也能跑）。

## 每天的固定节奏（约 4.5–5 小时）

| 时间 | 做什么 |
|---|---|
| 60–75 分钟 | 读当天的讲义（先读第 1、2、3 节：为什么存在 → 模板 → 手算；读完合上，凭记忆把模板默写一遍） |
| 2 × 40 分钟 | 做当天 2 道必做题：**先不看讲义里的解法**，按 `amazon_bar.md` 第 6 节的 45 分钟节奏口述着写（计时 40 分钟，包含自己测试） |
| 20 分钟 | 把这两题的「资深追问」逐条**出声回答**，再对照讲义里的答案要点补漏 |
| 10 分钟 | 打开 `solutions/<题号>_*.py`，和自己的实现对比；记下 2 个 bug 或疏漏，写进下面的「错题本」 |
| 选做 | 当天的「加练」（Hard / 高频），时间有就做 |

做完一题的验收标准：(1) 能不看资料写出可运行代码；(2) 说得出时间/空间复杂度和为什么；(3) 至少回答了 3 条资深追问；(4) 自己列出并跑过边界用例。

## 日程

### Day 1 · 10/15（周四，今天）：哈希 + 双指针 / 滑动窗口

- **先读**：`patterns/01_hash_map_counting.md`，再读 `patterns/02_two_pointers_sliding_window.md`
- **必做 1**：LC 560 Subarray Sum Equals K（Medium，75）——前缀和 + 哈希计数；讲义 01 §4.4
- **必做 2**：LC 3 Longest Substring Without Repeating Characters（Medium，88）——滑动窗口；讲义 02 §4.1
- **加练**：LC 1 Two Sum（100，热身 5 分钟）；LC 76 Minimum Window Substring（Hard，62）；LC 41 First Missing Positive（Hard，62）
- **今天要能口述的**：为什么 560 不能用滑动窗口；为什么窗口里 `last[ch] >= left` 不能省。

### Day 2 · 10/16（周五）：区间 + 栈 / 单调栈

- **先读**：`patterns/03_intervals.md`，再读 `patterns/04_stack_monotonic_stack.md`
- **必做 1**：LC 253 Meeting Rooms II（Medium，62）——扫描线 / 最小堆（顺便预习第 05 讲的堆）；讲义 03 §4.2
- **必做 2**：LC 739 Daily Temperatures（Medium，62）——单调栈；讲义 04 §4.2
- **加练**：LC 56 Merge Intervals（77）；LC 84 Largest Rectangle in Histogram（Hard，62）；LC 239 Sliding Window Maximum（Hard，66）
- **今天要能口述的**：区间题里 `<` / `<=` 的契约；单调栈为什么是 O(n)。

### Day 3 · 10/17（周六）：堆 / Top-K + 图（BFS / DFS / 拓扑）

- **先读**：`patterns/05_heap_top_k.md`，再读 `patterns/06_graph_bfs_dfs_topo.md`
- **必做 1**：LC 347 Top K Frequent Elements（Medium，75）——大小为 k 的堆（并写出桶排序版本）；讲义 05 §4.1
- **必做 2**：LC 207 Course Schedule（Medium，75）——Kahn 拓扑排序（顺手写 LC 210）；讲义 06 §4.4
- **加练**：LC 200 Number of Islands（88，BFS 版本）；LC 994 Rotting Oranges（75，多源 BFS）；LC 23 Merge k Sorted Lists（Hard，75）；LC 295 Find Median from Data Stream（Hard，63）；LC 127 Word Ladder（Hard，75）
- **今天要能口述的**：Python `heapq` 的最小堆 / 取负 / tie-breaker；BFS 为什么要在**入队**时标记已访问。

### Day 4 · 10/18（周日）：二分（含对答案二分）+ 动态规划

- **先读**：`patterns/07_binary_search_on_answer.md`，再读 `patterns/10_dp_1d_2d.md`（注意：按计划是「先 07 后 10」，第 08、09 讲放在明天）
- **必做 1**：LC 875 Koko Eating Bananas（Medium，75）——对答案二分；讲义 07 §4.1
- **必做 2**：LC 322 Coin Change（Medium，63）——1D DP，并解释贪心反例；讲义 10 §4.4
- **加练**：LC 33 Search in Rotated Sorted Array（75）；LC 53 Maximum Subarray（75）；LC 121 Best Time to Buy and Sell Stock（88）；LC 4 Median of Two Sorted Arrays（Hard，77）；LC 410 Split Array Largest Sum（Hard，52）；LC 10 Regular Expression Matching（Hard，54）
- **今天要能口述的**：`while lo < hi` / `hi = mid` / 下中位三者为什么必须配套；DP 五步法（状态 → 转移 → 初值 → 顺序 → 答案）。

### Day 5 · 10/19（周一，预计去程日 `推断`）：链表 + 树 / LCA + 设计（LRU）

- **先读**：`patterns/08_linked_list.md`，再读 `patterns/09_trees_lca.md`，最后读 `patterns/11_design_lru_lfu_iterators.md`（LRU 用到第 08 讲的双向链表，所以 08 必须先读）
- **必做 1**：LC 236 Lowest Common Ancestor of a Binary Tree（Medium，75）——后序 DFS；讲义 09 §4.1
- **必做 2**：LC 146 LRU Cache（Medium，88）——哈希表 + 双向链表，手写（不用 `OrderedDict`）；讲义 11 §4.1
- **加练**：LC 2 Add Two Numbers（80）；LC 206 Reverse Linked List（62）；LC 25 Reverse Nodes in k-Group（Hard，62）；LC 124 Binary Tree Maximum Path Sum（Hard，62）；LC 460 LFU Cache（Hard，62）
- **今天要能口述的**：反转链表四步的顺序；树递归「返回给父节点的值」与「更新答案的值」的区别；LRU 为什么节点里必须存 key。
- **如果 10/19 是飞行日**：把 Day 5 的阅读放到飞机上（讲义是 markdown，离线可读），必做题在落地酒店写；`run_all.py` 不需要网络。

### Day 5 晚 / 10/20 早：模拟一轮（30–45 分钟）

- 从 `top_list.md` 里**随机抽一道**还没做过的 Medium，完全按 `amazon_bar.md` 第 6 节的 45 分钟节奏，出声做一遍；最后 5 分钟回答 3 条资深追问（规模 ×1000 / 流式 / 并发 / 测试任选）。
- 重读 `amazon_bar.md` 第 3 节的英文句型和第 5 节的 senior 对照表。

## 覆盖说明（诚实）

- 10 道必做题**覆盖 10 个模式**；第 08 讲（链表）靠 Day 5 的 LRU（双向链表）和加练覆盖，不单独占一道必做题。
- 回溯（Generate Parentheses、Subsets、Permutations、Word Search）**不在这 11 个模式里**，`top_list.md` 末尾列了出来；如果 Day 5 之后还有时间，补一个小时的回溯模板。
- 全部 51 道题都有讲义内的解答和 `solutions/` 里的可运行代码，但计划只要求做 10 道必做题 + 每天的加练；其余当作「读懂就行」。

## 错题本（做题时填）

| 日期 | 题号 | 错在哪里 | 下次怎么避免 |
|---|---|---|---|
| | | | |
