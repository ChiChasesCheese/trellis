# Headlands 面试流程指南（SWE · Java）

> 每条结论后面的 `[x]` 指向 `catalog/raw/` 里的行：`F-A1` = forums.md §1.1 A1，`F-B1` = Blind，`F-G2` = Glassdoor，`F-W1` = WSO，
> `O-D1` = official_and_process.md §D1，`O-C2` = Java JD，`O-G` = 文化表，`G-3.1` = github_repos.md FastPrep 清单。
> `推断` = 本 kit 的判断，没有来源原话。题目排序见 `catalog/PARETO.md`（cut line 第 22 行）。

## 0. 全流程

| 阶段 | 形式 | Chi 的状态 | 证据 |
|---|---|---|---|
| 投递 | Greenhouse | ✅ 2026-09-29 | — |
| HackerRank | 1 题，100–120 分钟，job chain CSV | ✅ 2026-10-10 通过（Java 版） | F-Q8，Chi 亲历 |
| NDA | e-sign | 待签 | Chi 亲历 |
| **技术视频面** | **1 小时，与一位工程师一对一（Zoom）** | **下一步** | F-B1, F-G2, F-G3, O-C2 |
| 第二次电话面 | 有时有 | ? | F-A7, F-A11, F-B3 |
| Onsite / final | 3 小时（2 技术 + 1 行为，WSO 2025）到 6+ 轮（1p3a 2024），博客称 "10+ interviews" | ? | F-W1, F-A10, github_repos.md 54skyxenon 博客 |
| 节奏 | 官方：全程 2–3 周；电面后 36 小时内出结果 | — | O-D1, F-B1 |

## 1. 技术视频面（1 小时）

### 形式

* 一位工程师（也可能是 researcher），Zoom，共享编辑器 [F-G2, F-B1, O-C2]。
* 典型结构是**一道基础题，面试官不断加追问**，而不是多道互不相关的题 [F-B1：「started with summing natural numbers without the formula, then added optimization variants」]；也有两问结构（queue + get_mean → 带快照）[F-A1]。
* 「这家公司保持了 OA 的风格，题目长 + 难」[F-A2]；「面试官反应很快，喜欢讨论 C++ 相关的技术知识」[F-A1]。

### 考什么（按 PARETO 排序的电面题）

| 优先级 | 题（kit id） | 为什么 |
|---|---|---|
| 1 | hc01 买卖股票 DP 家族 | 4 个独立来源，最近 2025-12 [F-A3, F-A16, F-W1] |
| 2 | hc02 合并 K 路有序 → 多线程无阻塞合并数据流 | 3 个来源 [F-A6, F-A7, G-3.1] |
| 3 | hc03 递归求和 + 溢出 / 栈深 / 尾递归 | 4 个来源，典型「越挖越深」热身 [F-A14, F-A17, F-B1, G-3.1] |
| 4 | hc04 Queue mean + snapshot | 最新（2026-03）[F-A1, G-3.1] |
| 5 | hc05 订单簿 / 撮合 | 2026-02、2026-06 [F-G2, G-3.1] |
| 6 | hc06 32 位寄存器位运算 | 2025-11，「debugging and bitwise operations in a code framework」[F-A2, G-3.1] |
| 7 | hc07 股票代码 hash map 优化 | [F-B1, F-A17] |
| 8 | hc08 订单序列 API（Put/Delete + 前缀查询） | [F-A9, G-3.1] |
| 9 | 语言深度 kq02–kq06（C++ 报告 → Java 对应） | 「为什么 C++ 快」「C++ 版本差异」「smart pointers」[F-A13, F-W2, F-A8] |

### 评分（推断，来源是 JD 与官方视频）

* **代码质量**：「clean, well structured, 容易 maintain」[F-A13]；JD「fully automated, scalable, and maintainable solutions with extensive testing」[O-C2]。→ 先说测试用例，再写代码；命名、拆函数、不变量写在类型里（record 紧凑构造器）。
* **性能直觉**：每个追问都是「能不能更快 / 更省」[F-B1]；JD「Address performance limitations … Linux」[O-C2]。→ 每写完一版主动说复杂度、分配、装箱、缓存局部性，然后问「要不要我优化 X」。
* **系统细节的好奇心**：「curious why it was slow」「knowledgeable about a lot of different areas」[O-G]。→ 追问到 JVM（JIT、GC、逃逸分析、内存模型）时别回避，说清楚自己知道到哪一层。
* **低自我、能交流**：「Low ego」[O-C2]；面试官会打断讨论 [F-A1]。

### 常见挂法（来源里的原话）

| 挂法 | 证据 | 对策 |
|---|---|---|
| 花太多时间修编译错误 | 「花了很多时间修 compile error」[F-A7] | 在 Java 21 里练到手熟：`jtest.py` 每题先跑空壳，熟悉 record / switch 模式的语法细节 |
| 语言细节答不深 | 「c++/Python 的区别，会问得比较详细」[F-A8]；「招 c++ linguist」[F-A2] | 做 kq 题库（Java 内存模型、GC、JIT、`volatile`/`VarHandle`、虚拟线程 pinning） |
| 没准备、状态差 | [F-A8] | 面前一天只复习，不刷新题 |
| 基础题答完不会往下挖 | 「optimization variants」[F-B1] | 每道 hc 题的 Part 2–4 就是追问；REPORT「面试官可能的追问」逐条口述一遍 |

### 准备动作（按顺序）

1. 把 cut line 以上的电面题按 PARETO 顺序过一遍：`jtest.py start` → 45 分钟内写完 Part 1–2 → 对照 REPORT 的追问口头答。
2. 每道题的 Java 21 特性表读一遍，至少能说出「为什么用 sealed + 模式 switch 而不是 visitor / instanceof 链」。
3. kq 语言深度题：把 C++ 问法翻成 Java 问法各准备 2 分钟答案（「为什么 Java 能接近 C++ 的速度？什么时候不能？」）。
4. 准备 2 个故事：一次性能排查（从现象到根因）、一次推动自动化/测试（对应 JD）。
5. 反问（`06-questions-to-ask.md`，待写）。

## 2. Onsite（设计层已展开；轮次结构仍低置信，过了电面再细化）

* 「algorithms, OS concepts, concurrency, and open-ended systems questions」[F-G2]；「dp on trees」[F-G2]。
* 3 小时 final：2 技术 + 1 行为 [F-W1]；或 6 轮 + 加面 [F-A10]。
* 系统设计：Unused-code analysis、future-time job scheduler、low-latency trading system [CATALOG C]——三题都只有 1–2 个来源，sd02 / sd03 只有标题 + 一句摘要且标注两家公司（Keychain / Optiver 共享），**题面是 (reconstructed)**。
* 低层设计（LLD）：共享内存 SPSC 通道 [ld01]、交易相关 OOD [ld02，33 分钟电面里的一道简单题]、异步 TCP 消息通道 [ld03] [CATALOG B]。

### 2.1 设计层材料（全部按 senior 门槛准备）

| 先读 | 内容 |
|---|---|
| [loop/rounds/04_sd/00_how_to_run.md](rounds/04_sd/00_how_to_run.md) | 交易公司的设计轮 vs 大厂：µs 延迟预算、决定性、单机性能、内核旁路、行情组播、风控、日志重放、co-location；从零估算 |

| id | 题 | 参考答案 / 追问 / 评分 | 动手配套 |
|---|---|---|---|
| sd01 | 无用代码分析 [F-G3：首轮视频口述题] | [prompt](rounds/04_sd/sd01_unused_code_analysis/prompt.md) · [model_answer](rounds/04_sd/sd01_unused_code_analysis/model_answer.md) · [followups](rounds/04_sd/sd01_unused_code_analysis/followups.md) · [rubric](rounds/04_sd/sd01_unused_code_analysis/rubric.md) | — |
| sd02 | 未来时刻任务调度器 | [prompt](rounds/04_sd/sd02_future_job_scheduler/prompt.md) · [model_answer](rounds/04_sd/sd02_future_job_scheduler/model_answer.md) · [followups](rounds/04_sd/sd02_future_job_scheduler/followups.md) · [rubric](rounds/04_sd/sd02_future_job_scheduler/rubric.md) | ld02 Part 4（journal + 重放）的方法 |
| sd03 | 低延迟电子交易系统 | [prompt](rounds/04_sd/sd03_low_latency_trading_system/prompt.md) · [model_answer](rounds/04_sd/sd03_low_latency_trading_system/model_answer.md) · [followups](rounds/04_sd/sd03_low_latency_trading_system/followups.md) · [rubric](rounds/04_sd/sd03_low_latency_trading_system/rubric.md) | [ld01](rounds/03_lld/ld01_spsc_channel/problem.md) · [ld02](rounds/03_lld/ld02_trading_ood/problem.md) · [ld03](rounds/03_lld/ld03_async_tcp_channel/problem.md) · [hc05](rounds/01_video/hc05_market_order_book/problem.md) |

| id | LLD 题 | 题面 | 讲义 |
|---|---|---|---|
| ld01 | 共享内存 SPSC 通道 | [problem](rounds/03_lld/ld01_spsc_channel/problem.md) | [ld01](../study/30-articles/ld01_spsc_channel.md) |
| ld02 | 交易相关 OOD（订单状态机 / 仓位 PnL / 风控 / 事件溯源） | [problem](rounds/03_lld/ld02_trading_ood/problem.md) | [ld02](../study/30-articles/ld02_trading_ood.md) |
| ld03 | 异步 TCP 消息通道（成帧 / 背压 / 半关闭 / 重连） | [problem](rounds/03_lld/ld03_async_tcp_channel/problem.md) | [ld03](../study/30-articles/ld03_async_tcp_channel.md) |

### 2.2 设计轮的评分（推断，来源是 JD 与官方视频）

* **「knowledgeable about a lot of different areas」[O-G]**：设计题会一层层往下追（JVM → OS → CPU → 网卡）；准备「是什么 → 为什么 → 怎么验证」三层回答。
* **「Comfortable operating at various levels of abstraction, from individual machines to large scale distributed systems」[O-C2]**：既要会算一台机器够不够，也要会讲分片与复制；先算数，再选架构。
* **「fully automated, scalable, and maintainable solutions with extensive testing」[O-C2]**：每个方案都主动说怎么测（确定性重放、虚拟时钟、故障注入）。
* 面试官是将来的同事并写评价 [O-C2]：主动攻击自己的设计、每 10 分钟确认方向。
