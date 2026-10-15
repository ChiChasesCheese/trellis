# RANK — 全部 A–E 题一张表（28 法则打分的输入）

> 由 `CATALOG.md` 的 Table A–E 汇总；F（仅 QR）与 G（不计入）不在其中。行序即 `tools/pareto.py` 的排序，因此 PARETO 输出里的 `#` 等于本表行号。跑（在 kit 根 `vault/interviews/companies/headlands`）：
> `python3 tools/pareto.py catalog/RANK.md --table 总表 --focus 电面`
> `#refs` = 独立来源数（FastPrep 一个 family 合计 1；镜像 / 改写不计）。`最近` = 最近一次被报道（FastPrep 取 lastSeen）。轮次 ∈ 电面 / OA / onsite / 非编码。
> 打分：refs × 时效 × 轮次权重（电面 1.0，OA 与 onsite 0.8，非编码 0.6）。注意：Chi 已过 OA，OA 行（含 oa01）的排名只说明该题有多少人见过，不代表要先练。

## 总表

| ID | 题 | 轮次 | 最近 | #refs | 置信度 |
|---|---|---|---|---|---|
| oa01 | Job runner / job chain CSV（HackerRank，Chi 亲历 Java 版） | OA | 2026-10 | 9 | 高 |
| hc01 | Best Time to Buy and Sell Stock 家族（121 / 122 / 状态 DP） | 电面 | 2025-12 | 4 | 高 |
| oa02 | Disaster Recovery（commit 日志 + 并查集） | OA | 2026-03 | 3 | 中 |
| hc02 | Merge K sorted sequences → streams（多线程 / non-blocking） | 电面 | 2024-10 | 3 | 高 |
| hc03 | Recursive sum 1..n（不用公式 / 溢出 / 栈深 / 尾递归） | 电面 | 2024-08 | 4 | 高 |
| hc04 | Queue mean + corrective snapshot | 电面 | 2026-03 | 2 | 高 |
| hc05 | Market order book（单品种内存订单簿） | 电面 | 2026-06 | 2 | 中 |
| hc06 | CPU register bitwise operations（32 位无符号寄存器） | 电面 | 2025-11 | 2 | 中 |
| kq01 | OS / 并发 / 网络 / 开放式系统题｜推断：Java 对应 | onsite | 2026-02 | 2 | 中 |
| hc07 | Optimized hash map for stock tickers（unordered_map 优化） | 电面 | 2024-08 | 2 | 中 |
| hc08 | Order sequence API（Put / Delete + 前缀 count / quantity） | 电面 | 2024-05 | 2 | 高 |
| hc09 | Top trade events by notional（Top K tickers by notional） | 电面 | 2024-05 | 2 | 中 |
| ld01 | Shared-memory SPSC channel（两进程有界消息通道） | 电面 | 2023-08 | 2 | 中 |
| sd01 | Unused-code analysis（识别并删除大型代码库里的无用代码） | 电面 | 2023-06 | 2 | 中 |
| kq02 | 语言版本差异 C++11/14/17/20｜推断：Java 对应 | 电面 | 2023-03 | 2 | 中 |
| kq03 | IPC 方法（进程间通信）｜推断：Java 对应 | 电面 | 2023-03 | 2 | 中 |
| hc10 | Top K frequent elements（LC 347） | 电面 | 2026-04 | 1 | 低 |
| oa03 | As-of join（两张按时间戳排序的表） | OA | 2026-08 | 1 | 中 |
| oa04 | Array interval sums（区间查询） | OA | 2026-10 | 1 | 低 |
| sd02 | Future-time job scheduler（durable one-time jobs） | onsite | 2026-10 | 1 | 中 |
| sd03 | Low-latency electronic trading system | onsite | 2025-10 | 1 | 中 |
| hc11 | Order interval max overlap + cancellation | 电面 | 2025-06 | 1 | 中 |
| ld02 | Trading-related OOD（简单，junior 电面） | 电面 | 2025-07 | 1 | 中 |
| hc12 | Triggered order event filter | onsite | 2024-10 | 1 | 中 |
| hc13 | Fixed-size memory pool | 电面 | 2024-05 | 1 | 中 |
| hc14 | Limit order matching | 电面 | 2024-04 | 1 | 中 |
| hc15 | Custom stack with bottom increment（LC 1381） | 电面 | 2024-04 | 1 | 中 |
| hc16 | Decode a run-length stream | 电面 | 2023-06 | 1 | 中 |
| hc17 | Wildcard pattern matching（星号 / 数字通配字典） | 电面 | 2019-06 | 1 | 低 |
| kq04 | Why is C++ fast｜推断：Java 对应 | 电面 | 2023-08 | 1 | 中 |
| kq05 | C++ vs Python + smart pointers｜推断：Java 对应 | 电面 | 2024-05 | 1 | 中 |
| kq06 | malloc vs new / std::copy vs memcpy｜推断：Java 对应 | 电面 | 2023-03 | 1 | 低 |
| bq01 | 现场修 compile error / 在给定框架里 debug | 电面 | 2024-06 | 1 | 中 |
| bq02 | 简历 + 行为题（junior 电面 33 分钟） | 非编码 | 2025-07 | 1 | 中 |
| bq03 | Final 行为面 / company fit | 非编码 | 2025-03 | 1 | 中 |
| hc18 | Net position from API snapshots | onsite | 2024-04 | 1 | 中 |
| hc19 | House Robber（LC 198） | onsite | 2024-04 | 1 | 中 |
| hc20 | Merge Intervals（LC 56） | onsite | 2024-04 | 1 | 中 |
| oa05 | Earliest dependency schedule（DAG 最早完成时间） | OA | 2023-10 | 1 | 中 |
| oa06 | Exclusive function execution times（LC 636） | OA | 2024-01 | 1 | 中 |
| ld03 | Asynchronous TCP message channel | onsite | 2023-03 | 1 | 中 |
| ld04 | Incremental lattice coverage tracker | onsite | 2018-04 | 1 | 低 |
| bq04 | 跨时区协作 | 非编码 | 2023-11 | 1 | 低 |
