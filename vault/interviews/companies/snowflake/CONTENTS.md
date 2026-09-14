# 目录 — 按轮次读，按分数练

> 由 `python3 tools/contents.py` 从 `loop/tree/interview-loop.yaml` + `catalog/RANK.md` 生成，**勿手改**。
> 每个技能下的题按 28 法则分数（#refs × 时效 × 轮次权重）降序；**★ = cut line 以内**（累计 80% 流出次数）。
> 每题：题集目录（题面 + 测试 + 参考解）→ 题解文章（先做后读）。LeetCode 原题的公司标签全表见 `../../core/leetcode/companies/snowflake.md`。

## 00_ai_screen · Chakra AI 语音筛（20 min，BQ + 项目）

先读：[00-ai-screen](study/10-rounds/00-ai-screen.md)

- **headline → mechanism → number → learning；rubric 关键词说出口** — 题库：`loop/rounds/01_recruiter/`
- **口述场景题骨架（clarify → 3 步 → 真实例子 → trade-off）** — 题库：`loop/rounds/01_recruiter/`

## 01_recruiter · Recruiter / HR call

先读：[01-recruiter](study/10-rounds/01-recruiter.md)

- **具体化的 why Snowflake（产品/技术方向 + 自己的桥）** — 题库：`loop/rounds/01_recruiter/`
- **时间线、地点、level/薪资不报数字、team matching 问 headcount** — 题库：`loop/rounds/01_recruiter/`

## 02_oa · HackerRank OA（2–3 题 / 90–135 min）

先读：[02-oa](study/10-rounds/02-oa.md) · [02-dp-patterns](study/00-essentials/02-dp-patterns.md) · [03-graph-tree-patterns](study/00-essentials/03-graph-tree-patterns.md)

### 计数/最优化 DP（元音游程、paid/free server、加权区间调度、2D DP）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **q02** Vowel-Run DP — counting strings and substrings by consecutive-vowel runs | [`problems/q02_vowel_run_dp/`](problems/q02_vowel_run_dp/) | [题解](study/30-articles/q02_vowel_run_dp.md) | 5 | 2026-06 | MED-HIGH |
| ★ | **q04** Maximum Order Volume — weighted interval scheduling | [`problems/q04_maximum_order_volume/`](problems/q04_maximum_order_volume/) | [题解](study/30-articles/q04_maximum_order_volume.md) | 4 | 2026-01 | MED |
| ★ | **q01** Task Scheduling — paid server vs free server | [`problems/q01_task_scheduling_paid_free_server/`](problems/q01_task_scheduling_paid_free_server/) | [题解](study/30-articles/q01_task_scheduling_paid_free_server.md) | 3 | 2026-03 | HIGH |
|  | **q09** Server Selection with switching cost — **(reconstructed)** | [`problems/q09_server_selection/`](problems/q09_server_selection/) | [题解](study/30-articles/q09_server_selection.md) | 2 | 2023-02 | MED |

### 树高压缩（删叶子 / 换根 / 计数）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **q03** Tree Height Reduction (三合一：删叶子 / 剪子树 / 换根) | [`problems/q03_tree_height_reduction/`](problems/q03_tree_height_reduction/) | [题解](study/30-articles/q03_tree_height_reduction.md) | 4 | 2026-08 | MED-HIGH |

### 图 BFS / 拓扑排序 / valid tree

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **q08** Course Schedule II — topological order + minimum parallel semesters | [`problems/q08_course_schedule_ii/`](problems/q08_course_schedule_ii/) | [题解](study/30-articles/q08_course_schedule_ii.md) | 3 | 2026-03 | MED-HIGH |
| ★ | **q10** Wiki Minimum Clicks — 有向图 BFS 最短路 + 路径重建 | [`problems/q10_wiki_min_clicks/`](problems/q10_wiki_min_clicks/) | [题解](study/30-articles/q10_wiki_min_clicks.md) | 1 | 2026-09 | MED |

### 区间与计数（Paint the Ceiling、Patching Array、Inorder/Morris）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **q05** Paint the Ceiling — generated sequence, counting pairs | [`problems/q05_paint_the_ceiling/`](problems/q05_paint_the_ceiling/) | [题解](study/30-articles/q05_paint_the_ceiling.md) | 2 | 2026-03 | MED |
|  | **q06** Patching Array — LC 484 原题 + 追问返回值列表 | [`problems/q06_patching_array/`](problems/q06_patching_array/) | [题解](study/30-articles/q06_patching_array.md) | 2 | 2023-02 | HIGH |
|  | **q07** Inorder Traversal — recursive → iterative → Morris (constant space) | [`problems/q07_inorder_morris/`](problems/q07_inorder_morris/) | [题解](study/30-articles/q07_inorder_morris.md) | 2 | 2023-02 | MED-HIGH |

### 贪心正确性 + 位运算（翻倍全给一个元素）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **q19** Maximize OR-Sum — 至多 k 次翻倍，让整个数组的按位或最大 | [`problems/q19_maximize_or_sum/`](problems/q19_maximize_or_sum/) | [题解](study/30-articles/q19_maximize_or_sum.md) | 2 | 2026-05 | MED-HIGH |

### LC 原题复用（区间、并查集、回文位掩码、词典 DP、堆）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **q12** Merge Intervals — 合并重叠区间 | [`problems/q12_merge_intervals/`](problems/q12_merge_intervals/) | [LC 56](https://leetcode.com/problems/merge-intervals/) | 2 | 2026-02 | MED |
|  | **q17** Remove Stones to Minimize the Total — 反复对半去掉最大堆，最小化总量 | [`problems/q17_remove_stones_minimize_total/`](problems/q17_remove_stones_minimize_total/) | [LC 1962](https://leetcode.com/problems/remove-stones-to-minimize-the-total/) | 1 | 2024-12 | MED |
|  | **q13** Minimum Interval to Include Each Query — 每个查询最小的覆盖区间 | [`problems/q13_min_interval_each_query/`](problems/q13_min_interval_each_query/) | [LC 1851](https://leetcode.com/problems/minimum-interval-to-include-each-query/) | 1 | 2023-02 | MED |
|  | **q14** Maximum Product of the Length of Two Palindromic Subsequences — 两个不相交回文子序列的最大长度积 | [`problems/q14_palindromic_subsequences_product/`](problems/q14_palindromic_subsequences_product/) | [LC 2002](https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/) | 1 | 2023-02 | MED |
|  | **q15** Graph Valid Tree — 判断无向图是否构成一棵树 | [`problems/q15_graph_valid_tree/`](problems/q15_graph_valid_tree/) | [LC 261](https://leetcode.com/problems/graph-valid-tree/) | 1 | 2023-02 | MED |
|  | **q16** Number of Ways to Form a Target String Given a Dictionary — 从词典拼出目标串的方案数 | [`problems/q16_form_target_from_dictionary/`](problems/q16_form_target_from_dictionary/) | [LC 1639](https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/) | 1 | 2023-02 | MED |

### 计数与扫描（前缀计数凑排列、双向扫描最近距离、枚举预算）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **q21** Maximum Profit Query Selection — 只跑一种查询类型，怎么选最赚 | [`problems/q21_max_profit_query_selection/`](problems/q21_max_profit_query_selection/) | [题解](study/30-articles/q21_max_profit_query_selection.md) | 1 | 2026-01 | MED |
|  | **q20** Sequential String — 磁带只能顺序读，前缀最短要多长才能拼出排列 | [`problems/q20_sequential_string/`](problems/q20_sequential_string/) | [题解](study/30-articles/q20_sequential_string.md) | 1 | 2024 | MED |
|  | **q25** Distance to Nearest Two — 每个 1 到最近的 2 有多远 | [`problems/q25_distance_to_nearest_two/`](problems/q25_distance_to_nearest_two/) | [题解](study/30-articles/q25_distance_to_nearest_two.md) | 1 | 未知 | MED |

### 多窗口限流、`?` 填充枚举 / 计数 DP、二分答案

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **q22** Dropped Requests — 三条滑动窗口限流规则，谁被拒了 | [`problems/q22_dropped_requests/`](problems/q22_dropped_requests/) | [题解](study/30-articles/q22_dropped_requests.md) | 1 | 2025-11 | MED |
|  | **q23** Work Schedule — 一周 7 天的 `?` 填法，凑出总工时 | [`problems/q23_work_schedule/`](problems/q23_work_schedule/) | [题解](study/30-articles/q23_work_schedule.md) | 1 | 2025-07 | MED |
|  | **q24** Maximum Throughput — 预算内升级流水线，最大化瓶颈吞吐 | [`problems/q24_maximum_throughput/`](problems/q24_maximum_throughput/) | [题解](study/30-articles/q24_maximum_throughput.md) | 1 | 未知 | MED |


## 03_phone_coding · 技术电面 coding（60 min：10 介绍 / 40 题 / 10 反问）

先读：[03-phone-coding](study/10-rounds/03-phone-coding.md) · [01-solving-framework](study/00-essentials/01-solving-framework.md) · [03-graph-tree-patterns](study/00-essentials/03-graph-tree-patterns.md)

### RBAC / DAG 权限继承（继承 → deny 覆盖 → 反向查询）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc01** RBAC / DAG Permissions — role/node inheritance over a DAG, deny-overrides-allow, reverse queries | [`loop/rounds/03_phone_coding/pc01_rbac_dag_permissions/`](loop/rounds/03_phone_coding/pc01_rbac_dag_permissions/) | [题解](study/30-articles/pc01_rbac_dag_permissions.md) | 6 | 2026-09 | MED-HIGH |

### 网格多源 BFS 与路径重建

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc02** Closest Facility Grid — multi-source BFS, tie-broken source tracking, walls | [`loop/rounds/03_phone_coding/pc02_closest_facility_grid/`](loop/rounds/03_phone_coding/pc02_closest_facility_grid/) | [题解](study/30-articles/pc02_closest_facility_grid.md) | 3 | 2026-09 | MED-HIGH |
| ★ | **pc04** Wiki Shortest Click Path — BFS distance, lexicographically smallest reconstruction, lazy crawl with failures | [`loop/rounds/03_phone_coding/pc04_wiki_shortest_click_path/`](loop/rounds/03_phone_coding/pc04_wiki_shortest_click_path/) | [题解](study/30-articles/pc04_wiki_shortest_click_path.md) | 3 | 2026-09 | MED |

### 事件流滑窗（去重计数 / 最频 key）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc03** Recent Event Stream — sliding window over the most recent m events, count/top queries | [`loop/rounds/03_phone_coding/pc03_recent_event_stream/`](loop/rounds/03_phone_coding/pc03_recent_event_stream/) | [题解](study/30-articles/pc03_recent_event_stream.md) | 4 | 2026-08 | MED |

### 消息传递状态机 / 分布式聚合模拟

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc10** Distributed Tree Count — 只靠消息传递数出一棵树有多少节点 | [`loop/rounds/03_phone_coding/pc10_distributed_tree_count/`](loop/rounds/03_phone_coding/pc10_distributed_tree_count/) | [题解](study/30-articles/pc10_distributed_tree_count.md) | 4 | 2026-07 | MED |

### LC 原题 + 更难 follow-up（1751 变体、Happy Number O(1)）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc05** Max Events II — 至多参加 k 个不重叠活动的最大价值（LC 1751 + 两个追问） | [`loop/rounds/03_phone_coding/pc05_max_events_ii/`](loop/rounds/03_phone_coding/pc05_max_events_ii/) | [题解](study/30-articles/pc05_max_events_ii.md) | 2 | 2026-06 | HIGH |
| ★ | **pc06** Happy Number — O(n) → O(1) 空间 → 推广到任意进制与幂次 | [`loop/rounds/03_phone_coding/pc06_happy_number/`](loop/rounds/03_phone_coding/pc06_happy_number/) | [题解](study/30-articles/pc06_happy_number.md) | 2 | 2026-07 | HIGH |

### Trie + 回溯剪枝（Word Search II）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc07** Word Search II（LC 212）— trie + 剪枝 DFS | [`loop/rounds/03_phone_coding/pc07_word_search_ii/`](loop/rounds/03_phone_coding/pc07_word_search_ii/) | [LC 212](https://leetcode.com/problems/word-search-ii/) | 2 | 2026-02 | HIGH |

### 拓扑序 + DAG 最长路 / 启动顺序 / 环检测

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc09** Parallel Courses III（LC 2050）— 带权 DAG 上的关键路径 | [`loop/rounds/03_phone_coding/pc09_parallel_courses_iii/`](loop/rounds/03_phone_coding/pc09_parallel_courses_iii/) | [LC 2050](https://leetcode.com/problems/parallel-courses-iii/) | 2 | 2026-08 | MED-HIGH |
|  | **pc13** 服务启动顺序（Kahn 拓扑排序）— 环检测要指名道姓 | [`loop/rounds/03_phone_coding/pc13_service_startup_order/`](loop/rounds/03_phone_coding/pc13_service_startup_order/) | [题解](study/30-articles/pc13_service_startup_order.md) | 1 | 2026-03 | LOW-MED |

### 字符串解析、栈与括号、分段反转

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc15** 括号匹配（栈）— 校验 / 补全 / 最长合法子串 | [`loop/rounds/03_phone_coding/pc15_parentheses_matching/`](loop/rounds/03_phone_coding/pc15_parentheses_matching/) | [LC 20 / 921 / 32](https://leetcode.com/problems/valid-parentheses/) | 2 | 2026-03 | LOW-MED |
| ★ | **pc11** 字符频率统计 — 跨字符串 / 跨任意深度嵌套列表 | [`loop/rounds/03_phone_coding/pc11_character_frequencies/`](loop/rounds/03_phone_coding/pc11_character_frequencies/) | [题解](study/30-articles/pc11_character_frequencies.md) | 1 | 2026-06 | MED |
| ★ | **pc16** Reverse Alphanumeric Segments — 双指针分段翻转 → 原地 O(1) 空间 | [`loop/rounds/03_phone_coding/pc16_reverse_alphanumeric_segments/`](loop/rounds/03_phone_coding/pc16_reverse_alphanumeric_segments/) | [题解](study/30-articles/pc16_reverse_alphanumeric_segments.md) | 2 | 2026 | MED |

### 聚合排序 Top-K（金额精度、去重用户、流式）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc12** Top Two Users by Total Purchase Amount — 分组求和 + 排名 | [`loop/rounds/03_phone_coding/pc12_top_two_users_by_purchase/`](loop/rounds/03_phone_coding/pc12_top_two_users_by_purchase/) | [题解](study/30-articles/pc12_top_two_users_by_purchase.md) | 1 | 2026-06 | MED |
|  | **pc26** Top K Hashtags — 去重用户数的热度排名 + 流式类 + 滑动时间窗 | [`loop/rounds/03_phone_coding/pc26_top_k_hashtags/`](loop/rounds/03_phone_coding/pc26_top_k_hashtags/) | [题解](study/30-articles/pc26_top_k_hashtags.md) | 1 | 2026-02 | MED |

### 区间 + 堆（会议室）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **pc14** Meeting Rooms II（LC 253）— 最少会议室 + 分配房间号 | [`loop/rounds/03_phone_coding/pc14_meeting_rooms_ii/`](loop/rounds/03_phone_coding/pc14_meeting_rooms_ii/) | [LC 253](https://leetcode.com/problems/meeting-rooms-ii/) | 2 | 2026 | LOW-MED |

### 树的数组表示：parent 数组删点、子树和、带过滤前序

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc17** Forest Parent Array Delete Node — 重新压缩下标 → 删子树 → 批量同时删除 | [`loop/rounds/03_phone_coding/pc17_forest_parent_array_delete/`](loop/rounds/03_phone_coding/pc17_forest_parent_array_delete/) | [题解](study/30-articles/pc17_forest_parent_array_delete.md) | 1 | 2026-06 | MED |
|  | **pc19** Rewrite Tree With Subtree Sums — 完全二叉树数组反向扫描 → 一般二叉树迭代后序 | [`loop/rounds/03_phone_coding/pc19_rewrite_tree_subtree_sums/`](loop/rounds/03_phone_coding/pc19_rewrite_tree_subtree_sums/) | [题解](study/30-articles/pc19_rewrite_tree_subtree_sums.md) | 1 | 2026-06 | MED |
|  | **pc28** Preorder Without Invalid Nodes — 澄清一个歧义题面，两种读法都实现并测试 | [`loop/rounds/03_phone_coding/pc28_preorder_without_invalid_nodes/`](loop/rounds/03_phone_coding/pc28_preorder_without_invalid_nodes/) | [题解](study/30-articles/pc28_preorder_without_invalid_nodes.md) | 1 | 2025-12 | MED |

### 状态搜索（数字变换路径、找零 DP、井字棋可达性）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc18** Number Transformation Path — 任意路径（宇称推理）→ 有界 BFS 求最短 | [`loop/rounds/03_phone_coding/pc18_number_transformation_path/`](loop/rounds/03_phone_coding/pc18_number_transformation_path/) | [题解](study/30-articles/pc18_number_transformation_path.md) | 1 | 2026-06 | MED |
|  | **pc23** Min Coins with Change — 找零最小化的“付 + 找”双向 DP | [`loop/rounds/03_phone_coding/pc23_min_coins_with_change/`](loop/rounds/03_phone_coding/pc23_min_coins_with_change/) | [题解](study/30-articles/pc23_min_coins_with_change.md) | 1 | 2026-02 | MED |
|  | **pc29** Valid Tic-Tac-Toe (Extended) — LC 794 推广到 N×N/K 连、外加原因码与"双赢"的真正条件 | [`loop/rounds/03_phone_coding/pc29_valid_tic_tac_toe_nk/`](loop/rounds/03_phone_coding/pc29_valid_tic_tac_toe_nk/) | [题解](study/30-articles/pc29_valid_tic_tac_toe_nk.md) | 1 | 2025-11 | MED |

### 棋盘连子判定 + 小型 OOD（Connect Four）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **pc20** Connect Four — canPlayWin → 加重力 drop → OOD 设计整个游戏 | [`loop/rounds/03_phone_coding/pc20_connect_four/`](loop/rounds/03_phone_coding/pc20_connect_four/) | [题解](study/30-articles/pc20_connect_four.md) | 1 | 2026-06 | MED |

### 小语言解释器 / 布尔查询引擎（仿射合成、递归下降、倒排索引）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **pc21** Accumulator Interpreter — String-Command Calculator → SnowCal → 仿射映射记忆化 | [`loop/rounds/03_phone_coding/pc21_accumulator_interpreter/`](loop/rounds/03_phone_coding/pc21_accumulator_interpreter/) | [题解](study/30-articles/pc21_accumulator_interpreter.md) | 1 | 2026-05 | MED |
|  | **pc22** Document Predicate Search Engine — 倒排索引 OR → AND/OR 优先级 → NOT/括号 + 删除 | [`loop/rounds/03_phone_coding/pc22_document_predicate_search/`](loop/rounds/03_phone_coding/pc22_document_predicate_search/) | [题解](study/30-articles/pc22_document_predicate_search.md) | 1 | 2026-04 | MED |

### 日志与依赖图（二分最早错误、级联失败、grep 上下文）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **pc24** Service Failure Forensics — 三段式故障排查：二分找日志、传播 BFS、最长链 DAG | [`loop/rounds/03_phone_coding/pc24_service_failure_forensics/`](loop/rounds/03_phone_coding/pc24_service_failure_forensics/) | [题解](study/30-articles/pc24_service_failure_forensics.md) | 1 | 2026-02 | MED |
|  | **pc25** Grep With Context Lines — 实现 `grep -C`：窗口合并、GNU 分组、流式 O(1) 内存 | [`loop/rounds/03_phone_coding/pc25_grep_with_context/`](loop/rounds/03_phone_coding/pc25_grep_with_context/) | [题解](study/30-articles/pc25_grep_with_context.md) | 1 | 2026-02 | MED |

### 连续子序列匹配（KMP / 滚动哈希 / O(1) 空间）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **pc27** Recipe Sequence Matcher — 连续子序列匹配：预处理 vs O(1) 空间 vs 共享前缀 Trie | [`loop/rounds/03_phone_coding/pc27_recipe_sequence_matcher/`](loop/rounds/03_phone_coding/pc27_recipe_sequence_matcher/) | [题解](study/30-articles/pc27_recipe_sequence_matcher.md) | 1 | 2026-01 | MED |


## 04_ood · OOD / 类设计（电面或 onsite，默认并发追问）

先读：[04-ood](study/10-rounds/04-ood.md) · [04-class-design-and-concurrency](study/00-essentials/04-class-design-and-concurrency.md)

### 优先级任务调度器（tie-break、重复 ID 抑制、并发、持久化）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od01** Priority Task Scheduler — tie-breaks, duplicate-ID suppression, concurrency, persistence | [`loop/rounds/04_ood/od01_priority_task_scheduler/`](loop/rounds/04_ood/od01_priority_task_scheduler/) | [题解](study/30-articles/od01_priority_task_scheduler.md) | 3 | 2026-08 | HIGH |

### 内存文件系统（trie、rm、分块、锁、WAL）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od02** In-Memory File System — LC 588, rm/rmdir, chunked content, per-path locks | [`loop/rounds/04_ood/od02_in_memory_file_system/`](loop/rounds/04_ood/od02_in_memory_file_system/) | [题解](study/30-articles/od02_in_memory_file_system.md) | 5 | 2026-08 | HIGH-MED |

### 事务 KV（嵌套 begin/commit/rollback、每线程事务栈）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od03** Transactional In-Memory KV Store — nested transactions, per-thread linearizable reads | [`loop/rounds/04_ood/od03_transactional_kv_store/`](loop/rounds/04_ood/od03_transactional_kv_store/) | [题解](study/30-articles/od03_transactional_kv_store.md) | 2 | 2026-08 | HIGH-MED |

### 限流器（滑窗单规则 → 多规则排队 → 线程安全）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od04** Rate Limiter — sliding window, multi-rule FIFO queueing, thread-safe try_acquire | [`loop/rounds/04_ood/od04_rate_limiter/`](loop/rounds/04_ood/od04_rate_limiter/) | [题解](study/30-articles/od04_rate_limiter.md) | 3 | 2026-08 | MED |

### Cron 调度器类（schedule/pause/resume/tick、多副本 lease）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od05** Cron Scheduler — schedule/pause/resume/tick, pause-vs-claim race, multi-instance lease | [`loop/rounds/04_ood/od05_cron_scheduler/`](loop/rounds/04_ood/od05_cron_scheduler/) | [题解](study/30-articles/od05_cron_scheduler.md) | 2 | 2026-06 | LOW-MED |

### 队列类 → 云端队列服务（故障语义）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od09** Queue → Service — deque API, at-least-once ack/visibility timeout, crash redelivery | [`loop/rounds/04_ood/od09_queue_to_service/`](loop/rounds/04_ood/od09_queue_to_service/) | [题解](study/30-articles/od09_queue_to_service.md) | 2 | 2026-08 | HIGH |

### 审计日志类（时间窗访问查询 / 未访问集合）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **od06** Query Audit Log — record_access / accessed_in_range / unaccessed_since | [`loop/rounds/04_ood/od06_query_audit_log/`](loop/rounds/04_ood/od06_query_audit_log/) | [题解](study/30-articles/od06_query_audit_log.md) | 1 | 2024-02 | HIGH |

### LRU / TTL 缓存（warehouse SSD cache 框架）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od08** LRU Cache — O(1) LRU, TTL expiry, two-tier hot/cold with promotion | [`loop/rounds/04_ood/od08_lru_ttl_cache/`](loop/rounds/04_ood/od08_lru_ttl_cache/) | [题解](study/30-articles/od08_lru_ttl_cache.md) | 3 | 2026 | LOW-MED |

### 继承、校验、封装、Decimal（OA 内嵌 OOP）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od10** Student / Result — OA 里内嵌的继承与封装题 | [`loop/rounds/04_ood/od10_student_result_oop/`](loop/rounds/04_ood/od10_student_result_oop/) | [题解](study/30-articles/od10_student_result_oop.md) | 2 | 2026-05 | MED |

### 继承顺序类（多叉树前序、死亡标记、迭代遍历）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od07** Throne Inheritance without an initial king — 空族谱起步的 LC 1600 变体 | [`loop/rounds/04_ood/od07_throne_inheritance/`](loop/rounds/04_ood/od07_throne_inheritance/) | [LC 1600](https://leetcode.com/problems/throne-inheritance/) | 2 | 2026 | MED |

### 双流黑名单过滤（引用计数、通配、读写锁）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **od11** Dynamic Blacklist Filter System — 双流黑名单过滤器 | [`loop/rounds/04_ood/od11_dynamic_blacklist_filter/`](loop/rounds/04_ood/od11_dynamic_blacklist_filter/) | [题解](study/30-articles/od11_dynamic_blacklist_filter.md) | 2 | 2026-06 | MED |

### 累计销量榜（堆 + 惰性失效、rank 查询）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **od12** Top K Book Sales — 累计销量榜的懒失效堆 | [`loop/rounds/04_ood/od12_top_k_book_sales/`](loop/rounds/04_ood/od12_top_k_book_sales/) | [题解](study/30-articles/od12_top_k_book_sales.md) | 1 | 2026-02 | MED |

### 序列化：trie 编解码、持久化 KV 分块与原子性、JSON 解析

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **od13** Dictionary Trie Codec — 紧凑编码 + 不重建整棵树的前缀流式查询 | [`loop/rounds/04_ood/od13_dictionary_trie_codec/`](loop/rounds/04_ood/od13_dictionary_trie_codec/) | [题解](study/30-articles/od13_dictionary_trie_codec.md) | 1 | 2025-12 | MED |
|  | **od14** Durable Key-Value Store Serialization — 长度前缀编码 + 分块落盘 + 崩溃原子性 | [`loop/rounds/04_ood/od14_durable_kv_serialization/`](loop/rounds/04_ood/od14_durable_kv_serialization/) | [题解](study/30-articles/od14_durable_kv_serialization.md) | 1 | 2025-11 | MED |
|  | **od15** JSON Parser — 手写 JSON 语法 + 迭代深度 + 路径查询 | [`loop/rounds/04_ood/od15_json_parser/`](loop/rounds/04_ood/od15_json_parser/) | [题解](study/30-articles/od15_json_parser.md) | 1 | 未知 | MED |


## 05_system_design · 系统设计（45–60 min，infra/data 题）

先读：[05-system-design](study/10-rounds/05-system-design.md) · [05-sd-framework-snowflake-primitives](study/00-essentials/05-sd-framework-snowflake-primitives.md)

### KV store（版本、time travel、Raft、跨分区事务）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd01** Distributed KV Store（含 time travel / Raft） | [`loop/rounds/05_system_design/sd01_kv_store/`](loop/rounds/05_system_design/sd01_kv_store/) | [model_answer](loop/rounds/05_system_design/sd01_kv_store/model_answer.md) | 5 | 2026-09 | HIGH-MED |

### 调度器 / 队列（cron、幂等重试、多副本、背压）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd02** Cron / Job Scheduler（"SQL engine as cron job" + Reliable Job Scheduler） | [`loop/rounds/05_system_design/sd02_cron_job_scheduler/`](loop/rounds/05_system_design/sd02_cron_job_scheduler/) | [model_answer](loop/rounds/05_system_design/sd02_cron_job_scheduler/model_answer.md) | 5 | 2026-07 | HIGH |
| ★ | **sd05** Distributed Queue Service（从 deque 类到云端队列服务） | [`loop/rounds/05_system_design/sd05_distributed_queue_service/`](loop/rounds/05_system_design/sd05_distributed_queue_service/) | [model_answer](loop/rounds/05_system_design/sd05_distributed_queue_service/model_answer.md) | 2 | 2026-08 | HIGH |

### SQL notebook / 查询结果分发（异步、流式、排队）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd03** SQL Notebook / 查询结果分发 | [`loop/rounds/05_system_design/sd03_sql_notebook_query_results/`](loop/rounds/05_system_design/sd03_sql_notebook_query_results/) | [model_answer](loop/rounds/05_system_design/sd03_sql_notebook_query_results/model_answer.md) | 3 | 2026-08 | HIGH |

### 配额与限流（强一致 vs 本地缓存、多区域）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd04** Quota Service（多租户配额，多个上游服务共用） | [`loop/rounds/05_system_design/sd04_quota_service/`](loop/rounds/05_system_design/sd04_quota_service/) | [model_answer](loop/rounds/05_system_design/sd04_quota_service/model_answer.md) | 4 | 2026-06 | MED |
| ★ | **sd07** Distributed Rate Limiter（per-second、多规则叠加） | [`loop/rounds/05_system_design/sd07_distributed_rate_limiter/`](loop/rounds/05_system_design/sd07_distributed_rate_limiter/) | [model_answer](loop/rounds/05_system_design/sd07_distributed_rate_limiter/model_answer.md) | 4 | 2026-09 | MED |

### 审计日志 / 访问治理（多租户、防篡改、时间窗）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd06** Audit / Query-Event Log Service（多租户、防篡改） | [`loop/rounds/05_system_design/sd06_audit_query_log_service/`](loop/rounds/05_system_design/sd06_audit_query_log_service/) | [model_answer](loop/rounds/05_system_design/sd06_audit_query_log_service/model_answer.md) | 4 | 2026-06 | MED-HIGH |

### DAG 缓存 / 物化视图（≈ Dynamic Tables）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd08** DAG Cache for Query Views / Materialized Views（对照 Snowflake Dynamic Tables） | [`loop/rounds/05_system_design/sd08_dag_materialized_view_cache/`](loop/rounds/05_system_design/sd08_dag_materialized_view_cache/) | [model_answer](loop/rounds/05_system_design/sd08_dag_materialized_view_cache/model_answer.md) | 2 | 2026-03 | LOW-MED |

### Jira→PR 自动化（异步任务、人审门）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd11** Automated Jira-Ticket-to-PR System | [`loop/rounds/05_system_design/sd11_jira_ticket_to_pr_automation/`](loop/rounds/05_system_design/sd11_jira_ticket_to_pr_automation/) | [model_answer](loop/rounds/05_system_design/sd11_jira_ticket_to_pr_automation/model_answer.md) | 3 | 2026-06 | MED-HIGH |

### 密码存储 / 对象存储去重

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd12** Object Store with Deduplication（带内容去重的对象存储） | [`loop/rounds/05_system_design/sd12_object_store_dedup/`](loop/rounds/05_system_design/sd12_object_store_dedup/) | [model_answer](loop/rounds/05_system_design/sd12_object_store_dedup/model_answer.md) | 3 | 2025-12 | LOW |
| ★ | **sd09** User Password Storage（密码存储系统设计） | [`loop/rounds/05_system_design/sd09_password_storage/`](loop/rounds/05_system_design/sd09_password_storage/) | [model_answer](loop/rounds/05_system_design/sd09_password_storage/model_answer.md) | 1 | 2026-07 | HIGH |

### PB 级数据库同步（快照 + CDC 拼接、不许澄清需求）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **sd22** Petabyte-Scale Database Sync（两个 PB 级数据库之间同步数据） | [`loop/rounds/05_system_design/sd22_petabyte_database_sync/`](loop/rounds/05_system_design/sd22_petabyte_database_sync/) | [model_answer](loop/rounds/05_system_design/sd22_petabyte_database_sync/model_answer.md) | 1 | 2026-03 | HIGH |

### 并发爬虫（去重、分片、礼貌性）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd10** Concurrent Web Crawler（去重/礼貌性/分片/扩展） | [`loop/rounds/05_system_design/sd10_concurrent_web_crawler/`](loop/rounds/05_system_design/sd10_concurrent_web_crawler/) | [model_answer](loop/rounds/05_system_design/sd10_concurrent_web_crawler/model_answer.md) | 4 | 2026-03 | LOW-MED |

### 鉴权与授权（ACL / deny 优先、第三方 token 不稳定）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd13** ACL Authorization Checking Service（集中式权限校验服务） | [`loop/rounds/05_system_design/sd13_acl_authorization_service/`](loop/rounds/05_system_design/sd13_acl_authorization_service/) | [model_answer](loop/rounds/05_system_design/sd13_acl_authorization_service/model_answer.md) | 2 | 2026-02 | LOW-MED |
|  | **sd16** Resilient Auth with Flaky Third-Party Tokens（应对不可靠第三方鉴权的多区域认证层） | [`loop/rounds/05_system_design/sd16_resilient_auth_flaky_tokens/`](loop/rounds/05_system_design/sd16_resilient_auth_flaky_tokens/) | [model_answer](loop/rounds/05_system_design/sd16_resilient_auth_flaky_tokens/model_answer.md) | 1 | 2025-09 | LOW |

### 元数据目录 / 多租户分析平台（快照、隔离、结果缓存）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **sd14** Distributed Metadata Catalog and Schema Registry（分布式元数据目录与 Schema 注册中心） | [`loop/rounds/05_system_design/sd14_metadata_catalog_schema_registry/`](loop/rounds/05_system_design/sd14_metadata_catalog_schema_registry/) | [model_answer](loop/rounds/05_system_design/sd14_metadata_catalog_schema_registry/model_answer.md) | 1 | 2025-09 | LOW |
|  | **sd15** Multi-Tenant Interactive Analytics Platform（多租户交互式分析平台） | [`loop/rounds/05_system_design/sd15_multi_tenant_analytics_platform/`](loop/rounds/05_system_design/sd15_multi_tenant_analytics_platform/) | [model_answer](loop/rounds/05_system_design/sd15_multi_tenant_analytics_platform/model_answer.md) | 1 | 2025-09 | LOW |

### 地理搜索、事件订阅投递、REST SDK 抽象、日志库

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd19** REST API Abstraction Layer / Internal Service-Client SDK（REST API 的 RPC 抽象层） | [`loop/rounds/05_system_design/sd19_rest_api_abstraction_layer/`](loop/rounds/05_system_design/sd19_rest_api_abstraction_layer/) | [model_answer](loop/rounds/05_system_design/sd19_rest_api_abstraction_layer/model_answer.md) | 2 | 2026-05 | MED |
|  | **sd17** Geolocation Search Service（地理位置搜索服务） | [`loop/rounds/05_system_design/sd17_geolocation_search/`](loop/rounds/05_system_design/sd17_geolocation_search/) | [model_answer](loop/rounds/05_system_design/sd17_geolocation_search/model_answer.md) | 1 | 2026-07 | LOW |
|  | **sd23** Cross-Platform Logging Library（跨平台日志库） | [`loop/rounds/05_system_design/sd23_cross_platform_logging_library/`](loop/rounds/05_system_design/sd23_cross_platform_logging_library/) | [model_answer](loop/rounds/05_system_design/sd23_cross_platform_logging_library/model_answer.md) | 1 | 2026-03 | MED |
|  | **sd18** Event Subscription System（事件订阅与通知系统，1M events/s） | [`loop/rounds/05_system_design/sd18_event_subscription/`](loop/rounds/05_system_design/sd18_event_subscription/) | [model_answer](loop/rounds/05_system_design/sd18_event_subscription/model_answer.md) | 1 | 2026 | LOW |


## 06_project_deep_dive · Expertise / 项目深挖（早期职业：coding 前 15–20 min + resume 轮）

先读：[06-project-deep-dive](study/10-rounds/06-project-deep-dive.md)

- **每个决策的 why + 被否方案 + 现在怎么重做** — 题库：`loop/rounds/06_project_deep_dive/`
- **可用性 / 容错 / 扩展性 / 监控** — 题库：`loop/rounds/06_project_deep_dive/`

## 07_hm_behavioral · HM / Behavioral（8 条价值观）

先读：[07-hm-behavioral](study/10-rounds/07-hm-behavioral.md)

- **故事 ↔ 8 条价值观映射（Own It / Get It Done / Integrity Always 优先）** — 题库：`loop/rounds/07_hm_behavioral/`
- **分歧 / pushback / disagree-and-commit** — 题库：`loop/rounds/07_hm_behavioral/`

## 08_team_matching · Team matching（GenSWE 最后一步）

先读：[08-team-matching](study/10-rounds/08-team-matching.md)

- **偏好方向与理由；问 headcount** — 题库：`loop/rounds/08_team_matching/`
