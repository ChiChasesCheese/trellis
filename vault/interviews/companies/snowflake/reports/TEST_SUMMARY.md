# TEST_SUMMARY — Snowflake kit

> 生成：`uv run --project <trellis 根> --with pytest python tools/summary.py --run`（2026-09-13）。覆盖 `problems/`（OA）、`loop/rounds/03_phone_coding/`、`loop/rounds/04_ood/`。表中 "tests" 列按 part 标记计数；最右列是实际运行结果。
> 验收门：`python3 tools/verify_suites.py . "<glob>"` —— 参考解全绿 **且** 空 starter 必红（非空洞测试）。27/27 通过。

**实际通过的测试总数：557**（全部参考解；0 失败）

| dir | title | tests | p1/p2/p3/p4/p5 | edge | fmt | perf | io | measured | status |
|---|---|---:|---|---:|---:|---:|---:|---|---|
| q01_task_scheduling_paid_free_server | Task Scheduling — paid server vs free server | 14 | 3/11/0/0/0 | 8 | 1 | 1 | 4 | — | 14 passed in 0.49s |
| q02_vowel_run_dp | Vowel-Run DP — counting strings and substrings by consecutiv | 29 | 8/8/13/0/0 | 13 | 0 | 3 | 5 | — | 29 passed in 0.50s |
| q03_tree_height_reduction | Tree Height Reduction (三合一：删叶子 / 剪子树 / 换根) | 26 | 9/8/9/0/0 | 13 | 1 | 3 | 6 | — | 26 passed in 0.71s |
| q04_maximum_order_volume | Maximum Order Volume — weighted interval scheduling | 17 | 10/7/0/0/0 | 8 | 0 | 1 | 3 | — | 17 passed in 0.17s |
| q05_paint_the_ceiling | Paint the Ceiling — generated sequence, counting pairs | 12 | 4/8/0/0/0 | 5 | 0 | 1 | 3 | — | 12 passed in 0.24s |
| q06_patching_array | Patching Array — LC 484 原题 + 追问返回值列表 | 21 | 11/10/0/0/0 | 9 | 0 | 1 | 4 | — | 21 passed in 0.09s |
| q07_inorder_morris | Inorder Traversal — recursive → iterative → Morris (constant | 19 | 9/4/6/0/0 | 8 | 0 | 1 | 5 | — | 19 passed in 0.13s |
| q08_course_schedule_ii | Course Schedule II — topological order + minimum parallel se | 22 | 12/10/0/0/0 | 10 | 1 | 2 | 3 | — | 22 passed in 0.15s |
| q09_server_selection | Server Selection with switching cost — **(reconstructed)** | 21 | 8/13/0/0/0 | 8 | 1 | 1 | 3 | — | 21 passed in 0.40s |
| q10_wiki_min_clicks | Wiki Minimum Clicks — 有向图 BFS 最短路 + 路径重建 | 21 | 10/11/0/0/0 | 9 | 1 | 2 | 3 | — | 21 passed in 0.25s |
| q19_maximize_or_sum | Maximize OR-Sum — 至多 k 次翻倍，让整个数组的按位或最大 | 14 | 8/6/0/0/0 | 8 | 1 | 2 | 2 | — | 20 passed in 0.20s |
| pc01_rbac_dag_permissions | RBAC / DAG Permissions — role/node inheritance over a DAG, d | 29 | 10/5/5/9/0 | 16 | 2 | 2 | 4 | — | 28 passed in 0.40s |
| pc02_closest_facility_grid | Closest Facility Grid — multi-source BFS, tie-broken source  | 19 | 8/6/5/0/0 | 11 | 1 | 1 | 3 | — | 19 passed in 0.57s |
| pc03_recent_event_stream | Recent Event Stream — sliding window over the most recent m  | 18 | 11/7/0/0/0 | 11 | 1 | 1 | 2 | — | 17 passed in 0.29s |
| pc04_wiki_shortest_click_path | Wiki Shortest Click Path — BFS distance, lexicographically s | 21 | 5/9/7/0/0 | 11 | 1 | 1 | 3 | — | 21 passed in 0.18s |
| pc05_max_events_ii | Max Events II — 至多参加 k 个不重叠活动的最大价值（LC 1751 + 两个追问） | 19 | 9/5/5/0/0 | 10 | 1 | 2 | 3 | — | 22 passed in 0.38s |
| pc06_happy_number | Happy Number — O(n) → O(1) 空间 → 推广到任意进制与幂次 | 16 | 5/7/4/0/0 | 9 | 1 | 1 | 3 | — | 25 passed in 0.48s |
| pc10_distributed_tree_count | Distributed Tree Count — 只靠消息传递数出一棵树有多少节点 | 17 | 10/7/0/0/0 | 9 | 1 | 1 | 2 | — | 22 passed in 0.19s |
| od01_priority_task_scheduler | Priority Task Scheduler — tie-breaks, duplicate-ID suppressi | 22 | 11/4/2/5/0 | 10 | 1 | 1 | 3 | — | 22 passed in 0.18s |
| od02_in_memory_file_system | In-Memory File System — LC 588, rm/rmdir, chunked content, p | 22 | 11/5/4/2/0 | 12 | 1 | 1 | 3 | — | 22 passed in 0.08s |
| od03_transactional_kv_store | Transactional In-Memory KV Store — nested transactions, per- | 17 | 8/6/3/0/0 | 6 | 1 | 1 | 2 | — | 17 passed in 0.17s |
| od04_rate_limiter | Rate Limiter — sliding window, multi-rule FIFO queueing, thr | 18 | 8/7/3/0/0 | 8 | 1 | 1 | 2 | — | 18 passed in 0.15s |
| od05_cron_scheduler | Cron Scheduler — schedule/pause/resume/tick, pause-vs-claim  | 16 | 11/2/3/0/0 | 8 | 1 | 1 | 2 | — | 16 passed in 0.23s |
| od06_query_audit_log | Query Audit Log — record_access / accessed_in_range / unacce | 16 | 9/7/0/0/0 | 9 | 1 | 2 | 3 | — | 16 passed in 0.33s |
| od08_lru_ttl_cache | LRU Cache — O(1) LRU, TTL expiry, two-tier hot/cold with pro | 22 | 8/7/7/0/0 | 12 | 1 | 2 | 3 | — | 22 passed in 0.26s |
| od09_queue_to_service | Queue → Service — deque API, at-least-once ack/visibility ti | 21 | 5/10/6/0/0 | 14 | 1 | 1 | 2 | — | 21 passed in 0.14s |
| od10_student_result_oop | Student / Result — OA 里内嵌的继承与封装题 | 17 | 8/9/0/0/0 | 11 | 1 | 1 | 2 | — | 27 passed in 0.23s |

**27 problems · 526 tests** (edge 266 · fmt 23 · perf 38 · io 83)
