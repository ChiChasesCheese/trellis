# Headlands Technologies 面试题目总表（Software Engineer · Java · Chicago）

**日期：** 2026-10-14 · **输入：** `catalog/raw/{github_repos,forums,official_and_process}.md`（下文 GH / FO / OP）
**排序：** `RANK.md` → `tools/pareto.py` → `PARETO.md`。**当前轮次 = 电面（一小时技术视频通话，一位工程师）**，`--focus 电面` 给电面权重 1.0。
**Chi 亲历（来源写作「Chi 亲历 2026-10」）：** 投 Software Engineer（Java），做的是 HackerRank「Headlands Tech Coding Test - Java」，**题是 job chain CSV**。这是 Java 版的首份报告，也是该题的又一个独立来源，说明 Java 与 C++ 候选人拿到同一道 OA。下一轮是一小时技术视频通话（本表记作 `电面`）。

## 口径

- `#refs` = 独立来源数。**FastPrep 一个 family 无论几个标题合计 1**；同一条 1p3a 帖被 Telegram 镜像转载只算 1；QuantVault / PracHub 对 1p3a 的改写不算；Blind / WSO / Glassdoor / 1p3a / GitHub 博客互相独立。
- 合并规则：FastPrep 标题与论坛帖在**日期（lastSeen 与发帖日同日）+ 题型**同时吻合，才并入同一 family；只靠日期、没有内容线索的不并，写进说明。
- 置信度：**高** = 至少 2 个独立来源且至少一个有可读题面（逐字或 FastPrep 页），或 ≥3 个独立来源；**中** = 1–2 个来源且至少一个可读，或合并靠推断；**低** = 仅摘要的单源、角色未证实、合并存疑、或 lastSeen 超过 5 年。
- 日期：FastPrep 取页面 `lastSeen`（不是考试日）；论坛取发帖日；`最近` = 该 family 全部来源里最晚的一个。
- 阶段标签：FastPrep 来自页面标题（Phone Screen / Online Assessment / Onsite）；FastPrep 的 Low-level design / System design 没有阶段标签，凡无论坛证据的一律记 `onsite`（推断）。同一 family 多阶段时取权重最高的（电面）。
- 语言：C++ 报告在 D 表给出 `推断：Java 对应` 一行；A 表题本身语言无关，C++ 特定处在 parts 里标注。
- 公开仓库：不含面试官 / 招聘人员姓名、邮件内容。1p3a 帖子正文几乎都在登录墙后，下列 1p3a 内容来自公开摘要 / 预览，已在置信度里反映。

## 格式事实（细节与 URL 在 raw/）

- **漏斗（SWE，综合）**：Greenhouse 投递 → HackerRank（1 题，100–120 分钟；多数帖称只能 C++，Chi 的 Java 版证明有 Java）→ 1 小时 Zoom（一位工程师）→ 部分人有第二次电面 → onsite / final（形态跨度大，见下）。官方：整个流程 2–3 周（OP §D1）。
- **电面形态**：Blind 2024-08「1 小时，先问不用公式求 1..n 之和，面试官持续加优化追问，第二题优化 unordered_map，36 小时内拒信」（FO §1.2 B1）；junior 33 分钟 = 简历 + BQ + 一道简单 OOD（FO §1.1 A4）；一例两次电面（FO §1.1 A7）。**倾向：一道简单题被逐步加深**。
- **onsite 形态（低置信，单源各一例）**：2 电面 + 6 onsite + 1 加面（1p3a 1059121）；3 小时 final = 2 技术 + 1 行为（WSO 2025-03）；约 6 轮 C++ 低层题（博客 2023 秋）。
- **JD 对应（推断）**：Java 岗官方 JD 强调分布式存储、网络、Linux、性能瓶颈、监控，工程师参与面试并写评价（OP §C2）；没有任何面经支持 Java 电面会考这些，C++ 报告的 D 表行是 Java 对应的推断。

## Table A · 编码题（电面 / onsite 用 `hc`，OA 用 `oa`；ID 按 RANK 的打分顺序编号）

| ID | 题（别名） | 阶段 | parts | 最近 | #refs | 置信度 | 来源（raw file §row） |
|---|---|---|---|---|---|---|---|
| oa01 | Job runner / job chain CSV（别名：Headlands Tech Coding Test；Job Runner Chain Reports；Job Chain Metrics Problem） | OA（HackerRank，1 题，100–120 分钟；Java / C++ 同题（见说明）） | p1 解析 CSV 行 job_id, run_time_seconds, next_job_id（0 = 链尾）；p2 判断输入是否为若干条单链表；p3 每条链输出首尾 job、个数、总时长 hh:mm:ss、平均时长；p4 非法输入报错（Malformed Input）；边界：环、多 parent、多 children、独立环；公开用例仅 2 个，需自造用例 | 2026-10 | 9 | 高 | FO §1.2 W3, W4, T1 · FO §1.3 O1, O12, O15, O16 · GH §3.1.B Job Runner Chain Reports · FO §2 Q8 · Chi 亲历 2026-10；#refs 构成：WSO 2020-03 1 + WSO 论坛 2020-02 1 + GitHub gist 题解 2020-03 1 + 1p3a 876489 2022-03 1 + 1p3a 944240 2022-11 1 + 1p3a 旧帖 638585 1 + 1p3a 1186508 2026-08 1 + FastPrep 1 + Chi 亲历 2026-10 1（Java 版，首份 Java 报告）。题面不明确指向 job chain 的帖（921628、1001711、1004587、996155、1036062、Glassdoor 2 小时一题）不计 |
| hc01 | Best Time to Buy and Sell Stock 家族（别名：Best Time to Buy and Sell Stock / Best Time to Buy and Sell Stock II；「stock trading related LeetCode problems」） | 电面（FastPrep 标 Phone Screen & Onsite（II 仅 Onsite）；1p3a 两个技术电面；WSO 阶段未明） | p1 一次交易（LC 121）；p2 多次交易（LC 122）；p3 带约束的状态 DP（WSO 称「Leetcode hard」，1p3a「detailed state tracking」）；follow-up | 2025-12 | 4 | 高 | GH §3.1.A Best Time…, §3.1.C Best Time II · FO §1.1 A3, A16 · FO §1.2 W1；#refs 构成：FastPrep 1（Best Time + II 合计 1）+ 1p3a 1156658 1 + 1p3a 974931 1 + WSO 2025-03 1 |
| oa02 | Disaster Recovery（别名：Disaster Recovery；Commit-history reconstruction；「OA 出了地里没有的新题，需要写个并查集和处理异常 case」） | OA（FastPrep 标 Online Assessment；1p3a SWE OA） | p1 解析损坏日志并丢弃 malformed 条目；p2 并查集把 commit 归并成 repository；p3 范围查询；歧义输出 AMBIGUOUS INPUT!；规模 10^7 条日志 / 10^5 查询（pushpa-kumar 二手摘要，需核 fastprep 原页） | 2026-03 | 3 | 中 | GH §3.1.B Disaster Recovery · GH §1 #3, #10 · FO §1.3 O3, O5；#refs 构成：FastPrep 1（lastSeen 2026-03-21）+ 1p3a 1152383 1（2025-10）+ 1p3a 1095582 1（2024-11，并查集 + 异常 case，按样例形态合并，推断）。1p3a 1169644（2026-03-21 SWE OA，无题面）与 quant-interview-oa-bank 同源，均不计 |
| hc02 | Merge K sorted sequences → streams（别名：Merge K Sorted Sequences；Concurrent Sorted-Stream Merger（LLD 版）；Merge K Sorted Streams with Bounded Concurrency） | 电面（FastPrep Phone Screen + FastPrep LLD；1p3a 两个技术电面（C++）） | p1 合并 k 个有序序列；p2 流式 / 增量读取；p3 follow-up：多线程、non-blocking、有界并发（LLD 版：给定 unsafe 阻塞 client + 有界重叠后台读） | 2024-10 | 3 | 高 | GH §3.1.A Merge K Sorted Sequences, §3.1.D Concurrent Sorted-Stream Merger · FO §1.1 A6, A7 · FO §1.4 X1（不计）；#refs 构成：FastPrep 1（Merge K Sorted Sequences 与 Concurrent Sorted-Stream Merger 合计 1，二者 lastSeen 同为 2024-10-04）+ 1p3a 1089956 1（2024-10-04）+ 1p3a 1071034 1（2024-06） |
| hc03 | Recursive sum 1..n（别名：Checked Recursive Sum；Recursive Sum 1 to N with Overflow and Stack Limits） | 电面（FastPrep 标 Phone Screen；1p3a 与 Blind 的电话 / 视频第一题） | p1 递归求 1..n 之和；p2 不用公式；p3 追问：整数溢出（checked）、递归栈深、尾递归 / 优化变体 | 2024-08 | 4 | 高 | GH §3.1.A Checked Recursive Sum · FO §1.1 A14, A17, A20 · FO §1.2 B1 · FO §2 Q1；#refs 构成：FastPrep 1 + 1p3a 1009358 1（日期与 FastPrep lastSeen 同为 2023-08-10，可能同源，同源则 #refs=3）+ 1p3a 944714 1（tail recursion）+ Blind 2024-08 1。1p3a 715829（2021-02「recursion」泛称）不计 |
| hc04 | Queue mean + corrective snapshot（别名：Queue Mean Queries / Queue Mean from Corrective Snapshots / Streaming Queue with Mean and Snapshots） | 电面（FastPrep 标 Phone Screen；1p3a 技术电面（C++）） | p1 空 FIFO 队列上做 push / pop / get_mean；p2 带 snapshot 的修正事件（普通事件属于一条逻辑历史，snapshot 修正均值，题面被截断） | 2026-03 | 2 | 高 | GH §3.1.A Queue Mean Queries, Queue Mean from Corrective Snapshots · FO §1.1 A1 · FO §1.4 X1（不计）；#refs 构成：FastPrep 1（两个标题合计 1）+ 1p3a 1169914 1（Telegram 镜像同帖不另计；QuantVault 同源不计） |
| hc05 | Market order book（别名：Market Order Book；Glassdoor「making market order book in c++」） | 电面（FastPrep 标 Phone Screen；Glassdoor 把它放在 OA 流程的 Question 1（阶段标签不一致）） | p1 单品种有限内存订单簿，按操作序列处理（add / cancel / match 等，题面被截断，需开 fastprep 页） | 2026-06 | 2 | 中 | GH §3.1.A Market Order Book · GH §1 #2 · FO §1.2 G2；#refs 构成：FastPrep 1（PR #328 在 2026-10 重新同步）+ Glassdoor 2026-02 Amsterdam 1 |
| hc06 | CPU register bitwise operations（别名：CPU Register Bitwise Operations；「debugging and bitwise operations in a code framework」）。Java 对应（推断）：无符号用 long / Integer.toUnsignedLong / >>> | 电面（FastPrep 标 Phone Screen；1p3a 第一轮技术电面（C++，题目「长 + 难」）） | p1 模拟一个无符号 32 位寄存器：初值 + 位运算操作序列；在给定代码框架里 debug | 2025-11 | 2 | 中 | GH §3.1.A CPU Register Bitwise Operations · FO §1.1 A2；#refs 构成：FastPrep 1（lastSeen 2025-11-11）+ 1p3a 1154043 1（2025-11-11） |
| hc07 | Optimized hash map for stock tickers（别名：optimizing a C++ unordered_map for stock tickers；ticker hashing）。Java 对应（推断）：HashMap<String,…> 的冲突处理、自写开放寻址、内存开销 | 电面（Blind 1 小时 Zoom 的第二题；1p3a 电面） | p1 为股票代码设计 / 优化哈希表；p2 追问 hash 冲突与内存开销 | 2024-08 | 2 | 中 | FO §1.2 B1 · FO §1.1 A17 · FO §2 Q2 · OP §D2 Blind 2024-08；#refs 构成：Blind pcb637t7 2024-08 1 + 1p3a 944714 2022-11（「ticker hashing techniques」）1 |
| hc08 | Order sequence API（别名：Order Sequence Prefix Counts and Quantities；Order Management API with Sublinear Queries） | 电面（FastPrep 标 Phone Screen；1p3a 技术电面） | p1 Put(unique_id, quantity) 放入序列；p2 Delete(unique_id, quantity)；p3 前缀 count / quantity 查询（亚线性）；共 4 个 API。1p3a 摘要另有 memory management | 2024-05 | 2 | 高 | GH §3.1.A Order Sequence Prefix Counts and Quantities · FO §1.1 A9 · FO §1.4 X1（不计）；#refs 构成：FastPrep 1（lastSeen 2024-05-10）+ 1p3a 1066045 1（2024-05-10） |
| hc09 | Top trade events by notional（别名：Top K Tickers by Notional；「trading events coding challenge」） | 电面（FastPrep 标 Phone Screen；1p3a 技术电面（C++ / Python 对比）） | p1 平行数组 tickers / prices / volumes，按 price×volume（notional）取最大的若干事件 | 2024-05 | 2 | 中 | GH §3.1.A Top Trade Events by Notional · FO §1.1 A8 · FO §1.4 X1（不计）；#refs 构成：FastPrep 1（lastSeen 2024-05-26）+ 1p3a 1068621 1（2024-05-26，仅摘要「trading events coding challenge」，按日期 + 题型合并） |
| hc10 | Top K frequent elements（别名：Top K Frequent Elements；LC 347）。角色未证实：lastSeen 2026-04-09 与两道 QR 题（梯度下降、Pearson）同日 | 电面（FastPrep 标 Phone Screen） | p1 返回出现次数最多的 k 个值 | 2026-04 | 1 | 低 | GH §3.1.A Top K Frequent Elements；#refs 构成：FastPrep 1 |
| oa03 | As-of join（别名：As-Of Join；QuantVault 的 As-Of Join on a Timestamped Table 无一手来源，不采信） | OA（FastPrep 标 Online Assessment & Onsite） | p1 左右两张时间戳有序表，按 as-of 语义连接（题面被截断） | 2026-08 | 1 | 中 | GH §3.1.B As-Of Join · GH §1 #2 · FO §2 Q10；#refs 构成：FastPrep 1（PR #328 在 2026-10 重新同步） |
| oa04 | Array interval sums（别名：Array Interval Sums）。角色未证实：lastSeen 2026-10-11 与 1p3a 1192691「Full Time QR OA」同日（推断 QR 来源） | OA（FastPrep 标 Online Assessment） | p1 整数数组 nums + 区间查询数组 queries（题面被截断） | 2026-10 | 1 | 低 | GH §3.1.B Array Interval Sums · FO §3 1192691；#refs 构成：FastPrep 1 |
| hc11 | Order interval max overlap + cancellation（别名：Maximum Concurrent Orders in an Interval；Order Interval Overlap and Cancellation Problem） | 电面（1p3a 先过 OA 再技术电面（标题含「挂经」）） | p1 订单区间求最大重叠；p2 按买 / 卖方向处理撤单 | 2025-06 | 1 | 中 | FO §1.1 A5 · FO §1.4 X1（不计）· OP §D3 #17；#refs 构成：1p3a 1134455 1（QuantVault 标题同源不计；FastPrep 无对应条目） |
| hc12 | Triggered order event filter（别名：Triggered Order Event Filter） | onsite（FastPrep 标 Onsite Interview） | p1 按到达顺序处理订单，每行 [price, side]，触发条件过滤（题面被截断） | 2024-10 | 1 | 中 | GH §3.1.C Triggered Order Event Filter；#refs 构成：FastPrep 1 |
| hc13 | Fixed-size memory pool（别名：Fixed-Size Memory Pool）。Java 对应（推断）：预分配对象池 / ByteBuffer 切块 + free list | 电面（FastPrep 标 Phone Screen） | p1 capacity 个等大小块的池，块以编号表示（题面被截断）：分配 / 归还 / 校验。1p3a 1066045 同日 2024-05-10 且摘要含 memory management，可能同一场（推断，未计入 #refs） | 2024-05 | 1 | 中 | GH §3.1.A Fixed-Size Memory Pool · FO §1.1 A9（疑似，不计）；#refs 构成：FastPrep 1 |
| hc14 | Limit order matching（别名：Limit Order Matching） | 电面（FastPrep 标 Phone Screen） | p1 按到达顺序处理有限订单批，每行 [side, price, quantity]（题面被截断） | 2024-04 | 1 | 中 | GH §3.1.A Limit Order Matching；#refs 构成：FastPrep 1（lastSeen 2024-04-05，与 1p3a 1059121 的 9 轮流程同日，见说明） |
| hc15 | Custom stack with bottom increment（别名：Custom Stack with Bottom Increment；LC 1381） | 电面（FastPrep 标 Phone Screen） | p1 容量 maxSize 的栈：push / pop / 对栈底 k 个元素统一加值 | 2024-04 | 1 | 中 | GH §3.1.A Custom Stack with Bottom Increment；#refs 构成：FastPrep 1 |
| hc16 | Decode a run-length stream（别名：Decode a Run-Length Stream） | 电面（FastPrep 标 Phone Screen） | p1 解码游程编码流：每条记录为正整数计数 + 值（题面被截断） | 2023-06 | 1 | 中 | GH §3.1.A Decode a Run-Length Stream；#refs 构成：FastPrep 1 |
| hc17 | Wildcard pattern matching（别名：Text Pattern Matching with Stars；Numeric Wildcard Dictionary Matching；合并不确定，见说明） | 电面（FastPrep 标 Phone Screen（两条）） | p1 小写文本 + 含星号的 pattern 匹配；p2 字典 words × 批量 patterns 的数字通配匹配 | 2019-06 | 1 | 低 | GH §3.1.A Text Pattern Matching with Stars, Numeric Wildcard Dictionary Matching · GH §1 #2；#refs 构成：FastPrep 1（两个标题合计 1；Text Pattern Matching with Stars 在 2026-10 PR #328 重新同步，lastSeen 2017-01） |
| hc18 | Net position from API snapshots（别名：Net Position Calculation from API Snapshots） | onsite（FastPrep 标 Onsite Interview） | p1 由 API 快照计算每个 symbol 的最终带符号持仓数量 | 2024-04 | 1 | 中 | GH §3.1.C Net Position Calculation from API Snapshots；#refs 构成：FastPrep 1 |
| hc19 | House Robber（LC 198） | onsite（FastPrep 标 Onsite Interview） | p1 线性街道上选不相邻位置使总额最大 | 2024-04 | 1 | 中 | GH §3.1.C House Robber；#refs 构成：FastPrep 1 |
| hc20 | Merge Intervals（LC 56） | onsite（FastPrep 标 Onsite Interview） | p1 合并闭区间 | 2024-04 | 1 | 中 | GH §3.1.C Merge Intervals；#refs 构成：FastPrep 1 |
| oa05 | Earliest dependency schedule（别名：Earliest Dependency Schedule） | OA（FastPrep 标 Online Assessment） | p1 N 个任务各有工期与依赖，求最早完成时间（拓扑 / Kahn）。X2 转述 1p3a 1189414「两年前的 OA 是手工解析输入 + 时间戳 + Kahn」，吻合但属转述，不计 | 2023-10 | 1 | 中 | GH §3.1.B Earliest Dependency Schedule · FO §1.4 X2（不计）；#refs 构成：FastPrep 1 |
| oa06 | Exclusive function execution times（别名：Exclusive Function Execution Times；LC 636） | OA（FastPrep 标 Online Assessment） | p1 单线程 CPU 的函数调用日志，新调用暂停旧调用，求各函数独占时间。1p3a 1036062（2024-01-01「就一道题，在图里」）题面是图片，无法对应，不计 | 2024-01 | 1 | 中 | GH §3.1.B Exclusive Function Execution Times · FO §1.3 O6（不计）；#refs 构成：FastPrep 1 |

**A 表说明（合并与不确定处）**

- FastPrep `lastSeen` 同为 2024-04-05 的 7 个条目（Limit Order Matching、Best Time、Best Time II、Custom Stack、House Robber、Merge Intervals、Net Position）与 1p3a 1059121（SWE，2 电面 + 6 onsite + 1 加面，正文被锁）同日，**推断它们是同一条 9 轮流程的产物**；因无内容对应，1059121 不计入其中任何一行的 #refs。
- oa01 的 9 个来源逐条列在 #refs 构成里；因 FastPrep 的 Aug 17 2026 与 1p3a 1186508 同日，若二者同源则为 8，不影响排序。
- Best Time 与 Recursive sum 的 FastPrep 条目与论坛帖同日，可能同源（按规则仍记两个来源）。
- ASOF、ARRAYINT：lastSeen 2026-08 / 2026-10 的 OA 条目，前者无论坛佐证，后者与 QR OA 同日，均偏弱。


## Table B · 低层设计（LLD）

| ID | 题（别名） | 阶段 | parts | 最近 | #refs | 置信度 | 来源（raw file §row） |
|---|---|---|---|---|---|---|---|
| ld01 | Shared-memory single-writer single-reader channel（别名：Shared-Memory Single-Writer Single-Reader Channel）。Java 对应（推断）：MappedByteBuffer 环形缓冲 + 内存序 | 电面（FastPrep LLD（无阶段标签）；1p3a 电面提到 shared memory） | p1 两进程间有界共享内存消息通道：记录所有权、FIFO、显式 full / empty / drained | 2023-08 | 2 | 中 | GH §3.1.D Shared-Memory SPSC Channel · FO §1.1 A13；#refs 构成：FastPrep 1（lastSeen 2023-08-24）+ 1p3a 1011799 1（2023-08-24，摘要「shared memory, system design」，按日期 + 主题合并） |
| ld02 | Trading-related OOD（别名：一道不是很难的 OOD，trading 相关） | 电面（1p3a Junior Engineer 电面，33 分钟含简历 + BQ） | p1 一道简单的交易相关 OOD（无具体题面，被拒） | 2025-07 | 1 | 中 | FO §1.1 A4 · OP §D4 #16；#refs 构成：1p3a 1136321 1 |
| ld03 | Asynchronous TCP message channel（别名：Asynchronous TCP Message Channel）。阶段未标，按后续设计轮归类（推断） | onsite（FastPrep LLD（无阶段标签）） | p1 单 TCP 会话上的有界消息 API：本地环形缓冲、partial I/O 的帧拆分。1p3a 974931（同日 2023-03-09，IPC methods）可能相关，不计 | 2023-03 | 1 | 中 | GH §3.1.D Asynchronous TCP Message Channel · FO §1.1 A16（不计）；#refs 构成：FastPrep 1 |
| ld04 | Incremental lattice coverage tracker（别名：Design an Incremental Lattice Coverage Tracker）。阶段未标，按后续设计轮归类（推断） | onsite（FastPrep LLD（无阶段标签）） | p1 接收几何线段，随输入增长到百万条时维护精确的不同整点数 | 2018-04 | 1 | 低 | GH §3.1.D Design an Incremental Lattice Coverage Tracker；#refs 构成：FastPrep 1 |

FastPrep 的 4 个 LLD 条目：Concurrent Sorted-Stream Merger 并入 Table A 的 Merge K 行（同一场的 follow-up），其余 3 个在本表。


## Table C · 系统设计

| ID | 题（别名） | 阶段 | parts | 最近 | #refs | 置信度 | 来源（raw file §row） |
|---|---|---|---|---|---|---|---|
| sd01 | Unused-code analysis（别名：Design Distributed Unused-Code Analysis；first-round video「remove unused or dead code」） | 电面（Glassdoor 首轮视频；FastPrep System design（无阶段标签）） | p1 口述如何在公司级代码库中识别并删除无用代码；FastPrep 版：固定快照 + 可解释的 unused-code 候选 | 2023-06 | 2 | 中 | GH §3.1.D Design Distributed Unused-Code Analysis · FO §1.2 G3 · FO §2 Q7；#refs 构成：FastPrep 1（lastSeen 2023-06-28）+ Glassdoor RVW98042384 1（日期未显示） |
| sd02 | Future-time job scheduler（别名：Design a Future-Time Job Scheduler；FastPrep 标 Keychain / Headlands）。阶段未标，按后续设计轮归类（推断） | onsite（FastPrep System design（无阶段标签）） | p1 持久化的一次性任务，在请求时间后的有界延迟内触发 | 2026-10 | 1 | 中 | GH §3.1.D Design a Future-Time Job Scheduler；#refs 构成：FastPrep 1 |
| sd03 | Low-latency electronic trading system（别名：Design a Low-Latency Electronic Trading System；FastPrep 标 Optiver / Headlands）。阶段未标，按后续设计轮归类（推断） | onsite（FastPrep System design（无阶段标签）） | p1 行情摄取 → 校验策略订单意图 → 路由到交易所 → 对账成交 | 2025-10 | 1 | 中 | GH §3.1.D Design a Low-Latency Electronic Trading System；#refs 构成：FastPrep 1 |

## Table D · 知识题（语言深度 / OS / 并发 / 网络）

C++ 报告在此改写为 Java 对应并标 `推断：Java 对应`；没有任何来源是 Java 知识题的一手报告。

| ID | 题（别名） | 阶段 | parts | 最近 | #refs | 置信度 | 来源（raw file §row） |
|---|---|---|---|---|---|---|---|
| kq01 | OS 概念 / 并发 / 网络 / 开放式系统题（后续轮）｜推断：Java 对应 = JMM / 线程与锁 / ConcurrentHashMap / NIO 与 TCP / GC / Linux | onsite（Glassdoor 后续轮；博客自述 onsite 约 6 轮 C++ 低层题） | p1 算法、OS 概念、并发、开放式系统题；p2 低层概念（OSTEP、Kurose-Ross 级别） | 2026-02 | 2 | 中 | FO §1.2 G2 · GH §1 #9 · OP §C2（JD：networking and storage systems，不计）；#refs 构成：Glassdoor RVW89062704 2026-02 1 + 54skyxenon 博客 2023 秋 1（岗位推断为 SWE new grad，文中未写） |
| kq02 | 语言版本差异 C++ 11 / 14 / 17 / 20｜推断：Java 对应 = Java 8 → 11 → 17 → 21 特性 | 电面（WSO 较难电话面；1p3a 第一轮电面） | p1 各版本的差异与特性 | 2023-03 | 2 | 中 | FO §1.2 W2 · FO §1.1 A16 · FO §2 Q6；#refs 构成：WSO 2020-11 1 + 1p3a 974931 1 |
| kq03 | IPC 方法（进程间通信）｜推断：Java 对应 = 管道 / socket / MappedByteBuffer / 共享内存与序列化。1p3a 1011799 的 shared memory 记在 SPSC 行，不重复计 | 电面（1p3a 电面 / OA + 电面） | p1 IPC 有哪几种、各自取舍 | 2023-03 | 2 | 中 | FO §1.1 A16, A18 · FO §2 Q6；#refs 构成：1p3a 974931 1 + 1p3a 938472 1（2022-10） |
| kq04 | Why is C++ fast（含 follow-up：为什么比别的编译型语言也快）｜推断：Java 对应 = Java 为什么 / 何时够快（JIT、GC、逃逸分析、内存布局） | 电面（1p3a 技术电面（C++）） | p1 为什么 C++ 比别的语言快；p2 为什么比别的需要编译的语言也快 | 2023-08 | 1 | 中 | FO §1.1 A13 · FO §2 Q6；#refs 构成：1p3a 1011799 1 |
| kq05 | C++ vs Python 差异 + 智能指针｜推断：Java 对应 = Java vs Python、引用语义 / 所有权 / GC 对 RAII | 电面（1p3a 技术电面（C++ / Python，问得较详细）） | p1 C++ / Python 差异，在哪种情形用哪个；p2 smart pointers | 2024-05 | 1 | 中 | FO §1.1 A8 · FO §2 Q6；#refs 构成：1p3a 1068621 1 |
| kq06 | malloc vs new；std::copy vs memcpy 等深层 C++ 细节｜推断：Java 对应 = 对象分配 / System.arraycopy / 内存布局 | 电面（Blind 发帖人断言（阶段未明，按技术口答归电面）） | p1 malloc vs new；p2 std::copy vs memcpy | 2023-03 | 1 | 低 | OP §D2 Blind 2023-03；#refs 构成：Blind 2023-03 1 |

## Table E · 行为 / 流程

| ID | 题（别名） | 阶段 | parts | 最近 | #refs | 置信度 | 来源（raw file §row） |
|---|---|---|---|---|---|---|---|
| bq01 | 现场修 compile error / 在给定代码框架里 debug（电面时间被吃掉） | 电面（1p3a 两次技术电面；另见 CPU register 行） | p1 第一次电面花大量时间修 compile error；第二次顺利仍挂 | 2024-06 | 1 | 中 | FO §1.1 A7；#refs 构成：1p3a 1071034 1（1p3a 1154043 的 debugging 记在 CPU register 行） |
| bq02 | 简历 + 行为题（junior 电面，33 分钟含一道简单 OOD） | 非编码（1p3a Junior Engineer 技术电面） | p1 33 分钟的简历与 BQ | 2025-07 | 1 | 中 | FO §1.1 A4；#refs 构成：1p3a 1136321 1 |
| bq03 | Final 行为面 / company fit（1 对 1 行为面兼 company fit；3 小时 final 含 1 轮行为） | 非编码（WSO SWE Generalist：OA → 行为面 → 3 小时 final（2 技术 + 1 行为）） | p1 行为 / company fit；p2 final 中的行为轮 | 2025-03 | 1 | 中 | FO §1.2 W1；#refs 构成：WSO 2025-03 1 |
| bq04 | 跨时区协作（SDE 电面：一道编码 + cross-time-zone collaboration） | 非编码（1p3a SDE 技术电面） | p1 与其他时区同事协作的经历（无具体题面） | 2023-11 | 1 | 低 | FO §1.1 A12；#refs 构成：1p3a 1030839 1 |

### E2 · 流程事实（不排名，只列出处）

- 官方：整个流程两到三周，团队小所以推进快（OP §D1，视频 19）。
- Blind 2024-08 一例：电面后 36 小时拒信（FO §1.2 B1）；多条 Blind 评论称「一电后排第二电」（FO §1.2 B3）。
- HackerRank 形态：100 分钟 1 题（WSO 2020、1p3a 2023）、2 小时 1 题且题面刻意绕（Glassdoor）；输入输出靠 STDIN / STDOUT 自己解析；公开用例只有 2 个（FO §1.2 W3, G1, G4）。
- 语言：多数帖称只能 C++，1p3a 1186508 称「不是 C++ 也会考这题」，Chi 亲历为 Java 版（FO §0 要点 3）。
- 1p3a 1106014（2025-01）第二轮 SWE 电面、题目不可见（FO §1.1 A11）；1p3a 851894（2022-02）摘要提到 C++ 与 Java（FO §1.1 A19）。


## Table F · 仅 QR / Research Developer 的条目（不排名，除非另在 SWE 报告里出现）


| ID | 题 | 出处 | 为什么不排名 | 来源 |
|---|---|---|---|---|
| f1 | Gradient Descent on a Sinusoidal Objective | FastPrep 标 Phone Screen，lastSeen 2026-04-09 | 数值优化，QR 风格；SWE 报告里无同题 | GH §3.1.A |
| f2 | Pearson Correlation Coefficient | FastPrep 标 Phone Screen，lastSeen 2026-04-09 | 统计，QR 风格；SWE 报告里无同题 | GH §3.1.A |
| f3 | Research Developer OA 四段（10 道统计 MCQ + OLS / Sharpe / 最小化期望绝对偏差 + C++ 滑窗均值含 inf / nan + 2 道 LC） | FastPrep Sliding-Window Means with IEEE Special Values、Minimum Changes for Distinct Adjacent Characters（OA，lastSeen 2026-09-13）+ PracHub 转 1p3a 1189414 | 角色是 Research Developer（1p3a 归 Quant Finance）；SWE 的 OA 是 job chain，不是这套 | GH §3.1.B · FO §1.4 X2 · FO §3 |
| f4 | QR new grad OA「17 题 / 70 分钟」及 QR 新卒 OA 结构 | 1p3a 1124806（2025-04）、QuantVault 流程页（SEO） | QR 新卒；SWE 不适用 | FO §2 Q9 · OP §D2 |
| f5 | QR / 实习 tech phone（假设检验、OLS、STL、C++）与 QR onsite 8 轮 | 1p3a 1151303 / 1151304（2025-10）、1090391 | QR；SWE 不适用 | FO §3 |


## Table G · 不计入排名（原因）


| ID | 项 | 原因 | 来源 |
|---|---|---|---|
| g1 | 「写一个 C++ 程序打印 √42」 | 申请环节题，不是 OA / 电面题；4 个独立仓库见证（2023-05、2024-11、2026-01、2026-04）。Chi 的申请是否含此题未知 | GH §1 #4–#7 |
| g2 | lock-free ring buffer、memory_order_acquire / release、LeetCode-medium | ankitkushawaha1000/HFT 自标 general-prep、very low confidence，生成式，不是候选人报告 | GH §1 #8 |
| g3 | jraymondli HackerRank.md、quantt / techinterview / quantvault 的泛化示例题 | 无出处或疑似 LLM 生成，不采信 | GH §1 #11 · FO §1.4 X3, X4 |
| g4 | QuantVault 无一手来源的标题（As-Of Join on a Timestamped Table 2024-10 等） | 站方改写，与 1p3a 同源或无源，不独立 | FO §1.4 X1 · FO §2 Q10 |
| g5 | LeetCode 公司标签路线 | 20 个 company-wise 仓库里没有 Headlands 文件（只有 HRT，已排除），不要跑 lc_company.py Headlands | GH §2 |

