# TEST_SUMMARY — Snowflake kit

> 生成：`uv run --project <trellis 根> --with pytest python tools/summary.py --run`（本文件由脚本写入，勿手改）。覆盖 `problems/`（OA）、`loop/rounds/03_phone_coding/`、`loop/rounds/04_ood/`。"tests" 列按 part 标记计数；最右列是实际运行结果。
> 验收门：`tools/verify_suites.py` —— 参考解全绿 **且** 空 starter 必红。

**实际运行：66 题 · 1421 通过 · 0 失败**

| dir | title | tests | p1/p2/p3/p4/p5 | edge | fmt | perf | io | measured | status |
|---|---|---:|---|---:|---:|---:|---:|---|---|
| q01_task_scheduling_paid_free_server | Task Scheduling — paid server vs free server | 14 | 3/11/0/0/0 | 8 | 1 | 1 | 4 | — | 14 passed in 0.47s |
| q02_vowel_run_dp | Vowel-Run DP — counting strings and substrings by consecutiv | 29 | 8/8/13/0/0 | 13 | 0 | 3 | 5 | — | 29 passed in 0.50s |
| q03_tree_height_reduction | Tree Height Reduction (三合一：删叶子 / 剪子树 / 换根) | 26 | 9/8/9/0/0 | 13 | 1 | 3 | 6 | — | 26 passed in 0.76s |
| q04_maximum_order_volume | Maximum Order Volume — weighted interval scheduling | 17 | 10/7/0/0/0 | 8 | 0 | 1 | 3 | — | 17 passed in 0.17s |
| q05_paint_the_ceiling | Paint the Ceiling — generated sequence, counting pairs | 12 | 4/8/0/0/0 | 5 | 0 | 1 | 3 | — | 12 passed in 0.24s |
| q06_patching_array | Patching Array — LC 484 原题 + 追问返回值列表 | 21 | 11/10/0/0/0 | 9 | 0 | 1 | 4 | — | 21 passed in 0.09s |
| q07_inorder_morris | Inorder Traversal — recursive → iterative → Morris (constant | 19 | 9/4/6/0/0 | 8 | 0 | 1 | 5 | — | 19 passed in 0.15s |
| q08_course_schedule_ii | Course Schedule II — topological order + minimum parallel se | 22 | 12/10/0/0/0 | 10 | 1 | 2 | 3 | — | 22 passed in 0.16s |
| q09_server_selection | Server Selection with switching cost — **(reconstructed)** | 21 | 8/13/0/0/0 | 8 | 1 | 1 | 3 | — | 21 passed in 0.40s |
| q10_wiki_min_clicks | Wiki Minimum Clicks — 有向图 BFS 最短路 + 路径重建 | 21 | 10/11/0/0/0 | 9 | 1 | 2 | 3 | — | 21 passed in 0.26s |
| q12_merge_intervals | Merge Intervals — 合并重叠区间 | 16 | 9/7/0/0/0 | 10 | 1 | 2 | 2 | — | 23 passed in 0.43s |
| q13_min_interval_each_query | Minimum Interval to Include Each Query — 每个查询最小的覆盖区间 | 16 | 10/6/0/0/0 | 10 | 1 | 2 | 2 | — | 20 passed in 0.43s |
| q14_palindromic_subsequences_product | Maximum Product of the Length of Two Palindromic Subsequence | 13 | 8/5/0/0/0 | 7 | 1 | 2 | 2 | — | 25 passed in 0.21s |
| q15_graph_valid_tree | Graph Valid Tree — 判断无向图是否构成一棵树 | 16 | 9/7/0/0/0 | 10 | 1 | 2 | 2 | — | 23 passed in 0.27s |
| q16_form_target_from_dictionary | Number of Ways to Form a Target String Given a Dictionary —  | 15 | 9/6/0/0/0 | 9 | 1 | 2 | 2 | — | 25 passed in 0.51s |
| q17_remove_stones_minimize_total | Remove Stones to Minimize the Total — 反复对半去掉最大堆，最小化总量 | 18 | 9/9/0/0/0 | 12 | 1 | 2 | 2 | — | 23 passed in 0.21s |
| q19_maximize_or_sum | Maximize OR-Sum — 至多 k 次翻倍，让整个数组的按位或最大 | 14 | 8/6/0/0/0 | 8 | 1 | 2 | 2 | — | 20 passed in 0.20s |
| q20_sequential_string | Sequential String — 磁带只能顺序读，前缀最短要多长才能拼出排列 | 16 | 11/5/0/0/0 | 10 | 1 | 2 | 2 | — | 16 passed in 0.39s |
| q21_max_profit_query_selection | Maximum Profit Query Selection — 只跑一种查询类型，怎么选最赚 | 16 | 8/8/0/0/0 | 10 | 1 | 2 | 2 | — | 14 passed in 0.18s |
| q22_dropped_requests | Dropped Requests — 三条滑动窗口限流规则，谁被拒了 | 17 | 10/7/0/0/0 | 9 | 1 | 2 | 2 | — | 14 passed in 0.17s |
| q23_work_schedule | Work Schedule — 一周 7 天的 `?` 填法，凑出总工时 | 19 | 11/8/0/0/0 | 12 | 2 | 2 | 2 | — | 17 passed in 0.98s |
| q24_maximum_throughput | Maximum Throughput — 预算内升级流水线，最大化瓶颈吞吐 | 15 | 9/6/0/0/0 | 9 | 1 | 2 | 2 | — | 14 passed in 0.53s |
| q25_distance_to_nearest_two | Distance to Nearest Two — 每个 1 到最近的 2 有多远 | 19 | 10/9/0/0/0 | 12 | 1 | 2 | 3 | — | 18 passed in 0.52s |
| pc01_rbac_dag_permissions | RBAC / DAG Permissions — role/node inheritance over a DAG, d | 29 | 10/5/5/9/0 | 16 | 2 | 2 | 4 | — | 28 passed in 0.42s |
| pc02_closest_facility_grid | Closest Facility Grid — multi-source BFS, tie-broken source  | 19 | 8/6/5/0/0 | 11 | 1 | 1 | 3 | — | 19 passed in 0.57s |
| pc03_recent_event_stream | Recent Event Stream — sliding window over the most recent m  | 18 | 11/7/0/0/0 | 11 | 1 | 1 | 2 | — | 17 passed in 0.31s |
| pc04_wiki_shortest_click_path | Wiki Shortest Click Path — BFS distance, lexicographically s | 21 | 5/9/7/0/0 | 11 | 1 | 1 | 3 | — | 21 passed in 0.18s |
| pc05_max_events_ii | Max Events II — 至多参加 k 个不重叠活动的最大价值（LC 1751 + 两个追问） | 19 | 9/5/5/0/0 | 10 | 1 | 2 | 3 | — | 22 passed in 0.40s |
| pc06_happy_number | Happy Number — O(n) → O(1) 空间 → 推广到任意进制与幂次 | 16 | 5/7/4/0/0 | 9 | 1 | 1 | 3 | — | 25 passed in 0.49s |
| pc07_word_search_ii | Word Search II（LC 212）— trie + 剪枝 DFS | 18 | 11/7/0/0/0 | 9 | 1 | 1 | 2 | — | 18 passed in 0.13s |
| pc09_parallel_courses_iii | Parallel Courses III（LC 2050）— 带权 DAG 上的关键路径 | 18 | 11/7/0/0/0 | 11 | 1 | 2 | 2 | — | 24 passed in 0.14s |
| pc10_distributed_tree_count | Distributed Tree Count — 只靠消息传递数出一棵树有多少节点 | 17 | 10/7/0/0/0 | 9 | 1 | 1 | 2 | — | 22 passed in 0.20s |
| pc11_character_frequencies | 字符频率统计 — 跨字符串 / 跨任意深度嵌套列表 | 23 | 9/8/6/0/0 | 14 | 1 | 1 | 3 | — | 23 passed in 0.10s |
| pc12_top_two_users_by_purchase | Top Two Users by Total Purchase Amount — 分组求和 + 排名 | 24 | 8/7/9/0/0 | 14 | 2 | 1 | 3 | — | 29 passed in 0.22s |
| pc13_service_startup_order | 服务启动顺序（Kahn 拓扑排序）— 环检测要指名道姓 | 26 | 13/5/8/0/0 | 16 | 1 | 1 | 3 | — | 26 passed in 0.11s |
| pc14_meeting_rooms_ii | Meeting Rooms II（LC 253）— 最少会议室 + 分配房间号 | 28 | 10/7/11/0/0 | 14 | 2 | 2 | 3 | — | 28 passed in 0.36s |
| pc15_parentheses_matching | 括号匹配（栈）— 校验 / 补全 / 最长合法子串 | 19 | 7/5/7/0/0 | 10 | 0 | 3 | 3 | — | 32 passed in 0.35s |
| pc16_reverse_alphanumeric_segments | Reverse Alphanumeric Segments — 双指针分段翻转 → 原地 O(1) 空间 | 14 | 9/5/0/0/0 | 8 | 1 | 1 | 3 | — | 23 passed in 0.13s |
| pc17_forest_parent_array_delete | Forest Parent Array Delete Node — 重新压缩下标 → 删子树 → 批量同时删除 | 21 | 7/7/7/0/0 | 14 | 1 | 1 | 3 | — | 24 passed in 0.19s |
| pc18_number_transformation_path | Number Transformation Path — 任意路径（宇称推理）→ 有界 BFS 求最短 | 16 | 9/7/0/0/0 | 7 | 1 | 1 | 2 | — | 21 passed in 0.29s |
| pc19_rewrite_tree_subtree_sums | Rewrite Tree With Subtree Sums — 完全二叉树数组反向扫描 → 一般二叉树迭代后序 | 17 | 9/8/0/0/0 | 11 | 1 | 2 | 2 | — | 17 passed in 0.18s |
| pc20_connect_four | Connect Four — canPlayWin → 加重力 drop → OOD 设计整个游戏 | 25 | 11/6/8/0/0 | 10 | 1 | 1 | 3 | — | 25 passed in 0.10s |
| pc21_accumulator_interpreter | Accumulator Interpreter — String-Command Calculator → SnowCa | 23 | 7/8/8/0/0 | 16 | 1 | 1 | 3 | — | 23 passed in 0.09s |
| pc22_document_predicate_search | Document Predicate Search Engine — 倒排索引 OR → AND/OR 优先级 → NO | 17 | 6/4/7/0/0 | 8 | 2 | 1 | 4 | — | 17 passed in 1.91s |
| pc23_min_coins_with_change | Min Coins with Change — 找零最小化的“付 + 找”双向 DP | 20 | 6/7/7/0/0 | 10 | 2 | 1 | 4 | — | 27 passed in 0.52s |
| pc24_service_failure_forensics | Service Failure Forensics — 三段式故障排查：二分找日志、传播 BFS、最长链 DAG | 22 | 8/6/8/0/0 | 13 | 2 | 1 | 4 | — | 22 passed in 0.26s |
| pc25_grep_with_context | Grep With Context Lines — 实现 `grep -C`：窗口合并、GNU 分组、流式 O(1) 内 | 21 | 9/6/6/0/0 | 13 | 1 | 1 | 3 | — | 21 passed in 0.13s |
| pc26_top_k_hashtags | Top K Hashtags — 去重用户数的热度排名 + 流式类 + 滑动时间窗 | 23 | 9/6/8/0/0 | 14 | 1 | 1 | 3 | — | 23 passed in 0.15s |
| pc27_recipe_sequence_matcher | Recipe Sequence Matcher — 连续子序列匹配：预处理 vs O(1) 空间 vs 共享前缀 Tri | 22 | 8/7/7/0/0 | 11 | 1 | 2 | 3 | — | 22 passed in 0.12s |
| pc28_preorder_without_invalid_nodes | Preorder Without Invalid Nodes — 澄清一个歧义题面，两种读法都实现并测试 | 15 | 8/7/0/0/0 | 7 | 1 | 1 | 3 | — | 15 passed in 0.14s |
| pc29_valid_tic_tac_toe_nk | Valid Tic-Tac-Toe (Extended) — LC 794 推广到 N×N/K 连、外加原因码与"双赢" | 18 | 6/6/6/0/0 | 8 | 1 | 1 | 3 | — | 18 passed in 1.30s |
| od01_priority_task_scheduler | Priority Task Scheduler — tie-breaks, duplicate-ID suppressi | 22 | 11/4/2/5/0 | 10 | 1 | 1 | 3 | — | 22 passed in 0.18s |
| od02_in_memory_file_system | In-Memory File System — LC 588, rm/rmdir, chunked content, p | 22 | 11/5/4/2/0 | 12 | 1 | 1 | 3 | — | 22 passed in 0.09s |
| od03_transactional_kv_store | Transactional In-Memory KV Store — nested transactions, per- | 17 | 8/6/3/0/0 | 6 | 1 | 1 | 2 | — | 17 passed in 0.18s |
| od04_rate_limiter | Rate Limiter — sliding window, multi-rule FIFO queueing, thr | 18 | 8/7/3/0/0 | 8 | 1 | 1 | 2 | — | 18 passed in 0.15s |
| od05_cron_scheduler | Cron Scheduler — schedule/pause/resume/tick, pause-vs-claim  | 16 | 11/2/3/0/0 | 8 | 1 | 1 | 2 | — | 16 passed in 0.23s |
| od06_query_audit_log | Query Audit Log — record_access / accessed_in_range / unacce | 16 | 9/7/0/0/0 | 9 | 1 | 2 | 3 | — | 16 passed in 0.36s |
| od07_throne_inheritance | Throne Inheritance without an initial king — 空族谱起步的 LC 1600  | 24 | 14/3/7/0/0 | 17 | 0 | 2 | 2 | — | 24 passed in 0.21s |
| od08_lru_ttl_cache | LRU Cache — O(1) LRU, TTL expiry, two-tier hot/cold with pro | 22 | 8/7/7/0/0 | 12 | 1 | 2 | 3 | — | 22 passed in 0.26s |
| od09_queue_to_service | Queue → Service — deque API, at-least-once ack/visibility ti | 21 | 5/10/6/0/0 | 14 | 1 | 1 | 2 | — | 21 passed in 0.14s |
| od10_student_result_oop | Student / Result — OA 里内嵌的继承与封装题 | 17 | 8/9/0/0/0 | 11 | 1 | 1 | 2 | — | 27 passed in 0.23s |
| od11_dynamic_blacklist_filter | Dynamic Blacklist Filter System — 双流黑名单过滤器 | 23 | 10/8/5/0/0 | 12 | 1 | 1 | 3 | — | 23 passed in 0.20s |
| od12_top_k_book_sales | Top K Book Sales — 累计销量榜的懒失效堆 | 19 | 9/3/7/0/0 | 10 | 1 | 1 | 2 | — | 19 passed in 0.31s |
| od13_dictionary_trie_codec | Dictionary Trie Codec — 紧凑编码 + 不重建整棵树的前缀流式查询 | 23 | 10/4/9/0/0 | 13 | 1 | 2 | 2 | — | 32 passed in 0.11s |
| od14_durable_kv_serialization | Durable Key-Value Store Serialization — 长度前缀编码 + 分块落盘 + 崩溃原子 | 20 | 8/7/5/0/0 | 7 | 2 | 1 | 2 | — | 20 passed in 0.08s |
| od15_json_parser | JSON Parser — 手写 JSON 语法 + 迭代深度 + 路径查询 | 30 | 18/3/9/0/0 | 19 | 1 | 3 | 2 | — | 36 passed in 0.27s |

**66 problems · 1291 tests** (edge 702 · fmt 67 · perf 99 · io 183)
