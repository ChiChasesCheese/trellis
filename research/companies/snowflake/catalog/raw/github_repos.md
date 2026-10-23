# GitHub 优先蒸馏（2026-09-13）

> 方法论第 0 步：**先查 GitHub 上别人已经整理好的**，再蒸馏。本文件记录这次扫描的来源、可信度、与本 kit 的映射、以及由此暴露的缺口。
> 扫描脚本：仓库搜索 11 个关键词（`snowflake interview` / `snowflake oa` / `company wise leetcode` …）+ 代码搜索 3 个（`"snowflake" "phone screen"` 等），按星数去重。

## 1. 来源与可信度

| 来源 | 内容 | 更新 | 可信度 | 用法 |
|---|---|---|---|---|
| [liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems)（30k★） | LeetCode Premium 公司标签：Snowflake 目录 30天/3月/6月/更早/全部 五个 CSV，带频率与 Topics | 2026-08-16 | **HIGH**（LC 官方标签镜像） | → 通用题单 [`core/leetcode/companies/snowflake.md`](../../../../core/leetcode/companies/snowflake.md)（104 题，只列链接 + 标签） |
| [snehasishroy/leetcode-companywise-interview-questions](https://github.com/snehasishroy/leetcode-companywise-interview-questions)（7.9k★） | 同上，独立抓取，带 LC 题号 | 2026-08-21 | **HIGH** | 交叉印证频率（`双源` 列） |
| [kevin-2023-code/Tech-Interview-Questions `companies/snowflake.md`](https://github.com/kevin-2023-code/Tech-Interview-Questions/blob/main/companies/snowflake.md) | TrueInterview 同步的 **87 题**，每题带格式（Algorithm / LLD / SD / SQL）与报告日期 | 2026-08-13 | **MED**（聚合站，但题面细节具体、日期新；题面付费，预览可见开头与分阶段提纲） | §2 映射；缺口题按预览重建，标 (reconstructed) |
| [harry-the-nerd/interview-notes-questions `snowflake/`](https://github.com/harry-the-nerd/interview-notes-questions)（darkinterview） | Design In-Memory File System 一题的讲义 | 2026-06 | MED | 已被 od02 覆盖（原 CATALOG 已引用） |
| [JoeBao22/SDE-OA-2024 `SnowFlakes/SequentialString.md`](https://github.com/JoeBao22/SDE-OA-2024) | 2024 OA「Sequential String」：前缀最短长度能凑出 arr[i] 的排列 | 2024 | MED（一手转述，参考解法有 bug） | 缺口 → q20 |
| [dhruday/Prep `…/Snowflake/01–10`](https://github.com/dhruday/Prep) | 10 篇 Principal/Staff/Senior 面经 | 2026 | **LOW**（模板化生成：Staff 后端岗却是 Promise polyfill / MobX，不采信） | 不入库 |
| [sumitsingh4411/interview-rounds](https://github.com/sumitsingh4411/interview-rounds) | 5 篇 "curated" 面经 | 2023 | **LOW**（通用题：Rotting Oranges、JWT，标注 source: curated） | 不入库 |
| [ssanjaysingam/snowflake_interview](https://github.com/ssanjaysingam/snowflake_interview)、[vennamprasad/DevCrack…](https://github.com/vennamprasad/DevCrack-Mobile-Interviews) | Snowflake 产品知识问答 / 空模板 | — | LOW | 产品问答已被 `study/20-cards/snowflake_internals.md` 覆盖 |

**结论**：GitHub 上**没有**像 stripeoa 那样针对 Snowflake 的完整题库仓库；可蒸馏的是 ① LC 公司标签（HIGH，通用化）② TrueInterview 同步清单（MED，暴露 26 个本 kit 未收的 Snowflake 自有题 id）。

## 2. TrueInterview 87 题 × 本 kit 映射

图例：kit 题号 = 已有；`LC n` = LeetCode 原题（进通用题单，不单独建 kit）；**GAP → id** = 本轮补建；`SQL` = 数据岗题，SDE 不建。

| # | 题 | 格式 | 报告 | 映射 |
|---:|---|---|---|---|
| 1 | Webinar Popularity | SQL | 2026-08 | SQL |
| 2 | Marketing Touch Streak | SQL | 2026-07 | SQL |
| 3 | Audit Logs Service | SD | 2026-06 | sd06 |
| 4 | Forest Parent Array Delete Node | Algo | 2026-06 | **GAP → pc17** |
| 5 | Distributed Tree Node Count | Algo | 2026-06 | pc10 |
| 6 | AI-Powered Jira Ticket Automation | SD | 2026-06 | sd11 |
| 7 | Project Duration & Budget per Employee | SQL | 2026-06 | SQL |
| 8 | Reverse Alphanumeric Segments | Algo | 2026-06 | **GAP → pc16** |
| 9 | Number Transformation Path | Algo | 2026-06 | **GAP → pc18** |
| 10 | Dynamic Blacklist Filter System | LLD | 2026-06 | **GAP → od11** |
| 11 | Calculate Amount Paid in Taxes | Algo | 2026-06 | LC 2303 |
| 12 | Rewrite Tree With Subtree Sums | Algo | 2026-06 | **GAP → pc19** |
| 13 | Parallel Courses III | LLD | 2026-06 | pc09 |
| 14 | Closest Cake and Global Assignment | Algo | 2026-06 | pc02（多源 BFS；全局分配部分见 pc02 追问） |
| 15 | Max Credits with K Classes | Algo | 2026-06 | pc05 |
| 16 | Four-in-a-row Game `canPlayWin` | Algo | 2026-06 | **GAP → pc20** |
| 17 | Time Range Event Counter | Algo | 2026-05 | pc03 |
| 18 | Design Connect Four | LLD | 2026-05 | **GAP → pc20 Part 3** |
| 19 | SnowCal（ADD/MUL/FUN/END/INV 小语言） | Algo | 2026-05 | **GAP → pc21** |
| 20 | DAG Allow / Disallow Propagation | Algo | 2026-05 | pc01 |
| 21 | Wiki Page Shortest-Click Path | Algo | 2026-05 | pc04 / q10 |
| 22 | RPC Abstraction Layer for REST APIs | SD | 2026-05 | sd19 |
| 23 | Role Privilege System | Algo | 2026-05 | pc01 |
| 24 | Real-Time Stock Price System | SD | 2026-04 | 通用 SD（`study/20-cards/sd_checklist.md` 覆盖推送 / 扇出） |
| 25 | Job Scheduler with Cron / Pause / Resume | SD | 2026-04 | sd02 / od05 |
| 26 | Document Predicate Search Engine | Algo | 2026-04 | **GAP → pc22** |
| 27 | Merge Two Sorted Lists | Algo | 2026-04 | LC 21 |
| 28 | Limit Tree Height by Deletions | Algo | 2026-04 | q03 |
| 29 | Merge K Sorted Lists | Algo | 2026-04 | LC 23 |
| 30 | Distributed Rate Limiter | Algo | 2026-04 | sd07 / od04 |
| 31 | Frontend Grid: Robot Eats Candies | Algo（前端 DOM） | 2026-03 | 前端岗，不建 |
| 32 | Cross-Platform Logging Library | SD | 2026-03 | **GAP → sd23** |
| 33 | Course Schedule | Algo | 2026-03 | q08 |
| 34 | String-Command Calculator | Algo | 2026-02 | **GAP → pc21 Part 1**（与 SnowCal 同族：累加器解释器） |
| 35 | Key-Value Store with Transactions | LLD | 2026-02 | od03 |
| 36 | Min Coins to Pay with Change Allowed | Algo | 2026-02 | **GAP → pc23** |
| 37 | Service Failure Forensics | Algo | 2026-02 | **GAP → pc24** |
| 38 | Design Access Management System | SD | 2026-02 | sd13 |
| 39 | Find All Anagrams in a String | Algo | 2026-02 | LC 438 |
| 40 | Grep With Context Lines | Algo | 2026-02 | **GAP → pc25** |
| 41 | Word Search II | Algo | 2026-02 | pc07 |
| 42 | N-Queens | Algo | 2026-02 | LC 51 |
| 43 | Design Quota Service | SD | 2026-02 | sd04 |
| 44 | Top K Hash Tags（按去重用户数） | Algo | 2026-02 | **GAP → pc26** |
| 45 | Valid Parentheses | Algo | 2026-02 | pc15 |
| 46 | Merge Intervals | Algo | 2026-02 | q12 |
| 47 | Top K Book Sales | LLD | 2026-02 | **GAP → od12** |
| 48 | Maximum Number of Events That Can Be Attended | Algo | 2026-01 | LC 1353 |
| 49 | Cheapest Flights Within K Stops | Algo | 2026-01 | LC 787 |
| 50 | Web URL Crawler at Scale | Algo | 2026-01 | sd10 |
| 51 | Design Circular Queue | LLD | 2026-01 | LC 622 |
| 52 | Throne Inheritance | LLD | 2026-01 | od07 |
| 53 | Recipe Sequence Matcher | Algo | 2026-01 | **GAP → pc27** |
| 54 | Maximum Profit Query Selection | Algo | 2026-01 | **GAP → q21** |
| 55 | Design News Feed | SD | 2026-01 | 通用 SD（sd_checklist 覆盖） |
| 56 | Maximum Profit in Job Scheduling | Algo | 2026-01 | q04（同型） |
| 57 | Find Median from Data Stream | Algo | 2026-01 | LC 295 |
| 58 | 01 Matrix | Algo | 2025-12 | LC 542（技巧同 pc02） |
| 59 | ACL Service for Another Service | SD | 2025-12 | sd13 |
| 60 | Design In-Memory File System | LLD | 2025-12 | od02 |
| 61 | Longest Univalue Path | Algo | 2025-12 | LC 687 |
| 62 | Copy List with Random Pointer | Algo | 2025-12 | LC 138 |
| 63 | Serialize and Deserialize Dictionary Trie | Algo | 2025-12 | **GAP → od13** |
| 64 | Preorder Traversal Without Invalid Nodes | Algo | 2025-12 | **GAP → pc28** |
| 65 | Original String Exists Given Two Encoded Strings | Algo | 2025-12 | LC 2060 |
| 66 | Rate Limiter | LLD | 2025-12 | od04 |
| 67 | Step-By-Step Directions Between Tree Nodes | Algo | 2025-12 | LC 2096 |
| 68 | Dropped Requests (Rate Limiter) | Algo | 2025-11 | **GAP → q22** |
| 69 | Valid Tic-Tac-Toe State (Extended N×N / K) | Algo | 2025-11 | **GAP → pc29** |
| 70 | S3-Style Storage with Dedup | SD | 2025-11 | sd12 |
| 71 | Durable Key-Value Store Serialization | LLD | 2025-11 | **GAP → od14** |
| 72 | Work Schedule（`?` 填充枚举） | Algo | 2025-07 | **GAP → q23** |
| 73 | Design Leetcode | SD | — | 通用 SD（sd_checklist 覆盖） |
| 74 | Maximum Throughput（流水线升级预算） | Algo | — | **GAP → q24** |
| 75 | Shortest Path in Binary Matrix with Obstacles | Algo | — | LC 1293 |
| 76 | Sort Colors in a RecordCollection In-Place | Algo | — | LC 75 |
| 77 | Distance from Each 1 to the Nearest 2 | Algo | — | **GAP → q25** |
| 78 | Happy Number | Algo | — | pc06 |
| 79 | Maximum Number of Events II | Algo | — | pc05 |
| 80 | Tree Levels After Node Deletions | Algo | — | LC 2458 / q03 |
| 81 | ML Job Scheduler | SD | — | sd02（部分） |
| 82 | LeetCode 1600/1610 with follow-up | Algo | — | od07 |
| 83 | Implement a JSON Parser | LLD | — | **GAP → od15** |
| 84 | Root Equals Average of All Subtrees | Algo | — | LC 2265 |
| 85 | Handle Intervals When Input Is Not Sorted | Algo | — | q12 |
| 86 | Tree Height After Node Removal | Algo | — | LC 2458 |
| 87 | Minimum Meeting Rooms | Algo | — | pc14 |
| — | Sequential String（JoeBao22 OA 2024） | OA | 2024 | **GAP → q20** |

**统计**（脚本核对）：87 题中 kit 已覆盖 34 · LC 原题 19（进通用题单）· 通用 SD 3 · SQL 3 + 前端 1（岗位不符）· **缺口 27 行 + Sequential String → 本轮补建 26 个 id**（pc16–pc29、od11–od15、q20–q25、sd23；Connect Four LLD 与 String-Command 各并入同族 Part）。

## 3. 缺口题预览要点（重建依据）

题面付费，以下是公开预览可见的部分；kit 中凡超出这些的细节一律标 **(reconstructed)**。

- **pc16 Reverse Alphanumeric Segments**：反转每个最长字母 / 数字连续段，其他字符原位；`We're → eW'er`，撇号是边界。
- **pc17 Forest Parent Array Delete Node**：`parent[i]` 编码森林，根 `parent[i]==i`；删除 `delete_index`，返回**重新压缩下标**后的合法 parent 数组。
- **pc18 Number Transformation Path**：`add=+2`、`sub=-2`、`split=floor(/2)`；`transform(a,b)` 返回从 a 到 b 的正整数序列（含首尾），不要求最短。
- **pc19 Rewrite Tree With Subtree Sums**：两棵同形完全二叉树，root2 每个位置写成 root1 对应子树和；`[5,2,3,1,4,6,7] → [28,7,16,1,4,6,7]`。
- **pc20 Four-in-a-row**：`canPlayWin(board,x,y,player)`，board 格为 `"a"/"b"/""`，落子后是否四连（横竖两斜）；同族 LLD「Design Connect Four」。
- **pc21 SnowCal / String-Command Calculator**：单变量 X=0，指令 `ADD`/`MUL`/`FUN…END` 声明函数/`INV` 调用；String-Command 版为 `ADD 6`/`SUB 3`/`MULT 4`/`DIV 2` 累加器。
- **pc22 Document Predicate Search Engine**：stdin 命令、每条一行输出；Part 1 `INSERT_DOC` + 仅 OR 链的 `CHECK_CONTAINS "a b c"`；共 3 个 Part。
- **pc23 Min Coins with Change**：面额 {1,5,10,50,100,200} 无限；可多付再找零；最小化付出 + 找回的硬币总数。
- **pc24 Service Failure Forensics**：三段——二分找最早 error 日志 → BFS/DFS 求所有会级联失败的服务 → DFS 求最长失败传播链。
- **pc25 Grep With Context Lines**：`lines`、`search_target`、`lines_around`，输出命中行及前后 N 行（重叠合并、保序）。
- **pc26 Top K Hash Tags**：`events=[userId, hashtag]`，热度 = 发过该 tag 的**去重用户数**，热度降序、字典序升序取前 k。
- **pc27 Recipe Sequence Matcher**：每个 recipe 是否作为**连续子序列**出现在 ingredients 中；追问 1 只允许 O(1) 额外空间。
- **pc28 Preorder Traversal Without Invalid Nodes**：`edges=[parent,child]`、root、`invalid`；前序遍历，子节点按 edges 顺序，跳过 invalid 节点（(reconstructed)：其子树是否保留需澄清，kit 两种都测）。
- **pc29 Valid Tic-Tac-Toe (Extended)**：N×N、K 连胜；X 先手、交替、有人赢即停；判断局面是否可达。
- **od11 Dynamic Blacklist Filter**：两条并发流（黑名单增删 / 输入值），输入到达时未被拉黑就输出。
- **od12 Top K Book Sales**：`bestSellers(books, counts, k)` 累加销量并即时返回前 k。
- **od13 Dictionary Trie Codec**：不同小写单词建 trie；`serialize` 成字符串，`deserialize` 重建并按字典序返回全部单词；编码自选。
- **od14 Durable KV Serialization**：`put/get/shutdown/restore`，不许 JSON/pickle，键值含任意字符；Part 2 分块到每文件 ≤1024 字节（`save_blob/get_blob/list_files`），UTF-8 边界、元数据、写入顺序与原子性。
- **od15 JSON Parser**：解析一个 JSON 值，输出最小化 JSON，非法输出 `INVALID`；object/array/string/number/bool/null + 转义。
- **q20 Sequential String**：s 只能顺序取字符；对每个 arr[i]，求 s 的最短前缀长度使其包含 arr[i] 的一个排列所需字符，否则 -1（`s="064819848398", ["088","364","071"] → [7,10,-1]`）。
- **q21 Maximum Profit Query Selection**：只选一种查询类型重复跑，利润 `(k // durations[i]) * revenues[i]` 取最大。
- **q22 Dropped Requests**：非降序到达时间，按规则拒绝并返回被拒时间戳（(reconstructed) 经典 HackerRank 版：1 秒内 >3、10 秒内 >20、60 秒内 >60 即拒）。
- **q23 Work Schedule**：7 位 pattern（数字或 `?`），每天 ≤ dayHours，总和恰为 workHours，按字典序列出全部填法。
- **q24 Maximum Throughput**：服务串联，吞吐 = 最小值；每次升级服务 i 花 `scalingCost[i]` 增加 `throughput[i]`（(reconstructed)），预算内最大化最小吞吐——二分答案 + 贪心计费。
- **q25 Distance from Each 1 to Nearest 2**：只含 0/1/2 的数组，对每个 1 输出到最近 2 的距离，无 2 则 -1——左右两遍扫描。
- **sd23 Cross-Platform Logging Library**：多语言 / 多平台 SDK 的日志库设计（级别、结构化、异步缓冲、背压、采样、传输与降级）。
