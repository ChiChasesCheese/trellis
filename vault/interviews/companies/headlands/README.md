# Headlands Technologies · Software Engineer（Java）—— 从这里开始

> 现状（2026-10-14）：HackerRank（job chain，Java）已过 → 下一轮是**一小时技术视频面**（一位工程师，一道基础题被一路追问）。
> 本 kit 的目标有两个，按 Chi 的原话排序：**顺便学东西，越多越好**；其次是把这一轮面好。所以全部材料是**教科书模式**（`study/TEXTBOOK.md`）。

## 地图

| 想做什么 | 去哪 |
|---|---|
| 了解这一轮怎么面、考什么、怎么挂 | [loop/LOOP_GUIDE.md](loop/LOOP_GUIDE.md) |
| 看所有题的优先级（谁被问得最多、最近） | [catalog/PARETO.md](catalog/PARETO.md)（cut line 第 22 行）· [catalog/CATALOG.md](catalog/CATALOG.md) |
| 补基础（复杂度、堆、树、CPU 缓存、操作系统、网络） | [study/00-foundations/README.md](study/00-foundations/README.md) |
| 学 Java 21 新特性（J01–J19） | [study/10-java21/README.md](study/10-java21/README.md) |
| 读某道题的讲义 | `study/30-articles/<id>_*.md` |
| 动手做题 | `loop/rounds/<轮次>/<id>_*/`，命令见下 |
| 语言深度口头题（C++ 面经翻成 Java 问法，45 题） | [loop/rounds/01_video/kq_language_depth/questions.md](loop/rounds/01_video/kq_language_depth/questions.md) |
| 公司是做什么的（从零讲自营交易） | [01-company-brief.md](01-company-brief.md) |
| 简历 vs JD、故事、反问 | [fit.md](fit.md) · [stories.md](stories.md)（有待填模板）· [06-questions-to-ask.md](06-questions-to-ask.md) |
| 证据原文（每条都有 URL + 日期） | `catalog/raw/` |
| 进度 / 已验收 | [CHECKPOINT.md](CHECKPOINT.md) · [LEDGER.md](LEDGER.md) |

## 建议学习路径

基础很薄的话，按这个顺序走；每一站都是「先读讲义 → 再动手 → 最后口头答追问」。

| 站 | 读 | 做 | 为什么排在这 |
|---|---|---|---|
| 0 | `study/10-java21/` 的 J08 → J05 → J07 → J06 → J01 → J02 → J03 → J04 | — | 后面每道题都用 record / sealed / 模式匹配，先把语法读顺 |
| 1 | 讲义 oa01 + 基础 complexity | `oa01_job_chain` | 你做过的题，最好上手；样板讲义 |
| 2 | 讲义 hc03 | `hc03_recursive_sum` | **电面最典型的热身题**：一道简单题被追问到溢出、栈、尾递归、并行 |
| 3 | 基础 heap_priority_queue → 讲义 hc02 | `hc02_merge_k_streams` Part 1–2 | 堆是后面好几题的工具 |
| 4 | 讲义 hc01 | `hc01_stock_trading_dp` | 面经出现最多的电面题；顺便学会动态规划 |
| 5 | 基础 ordered_maps_trees → 讲义 hc05 | `hc05_market_order_book` Part 1–2 | 订单簿 = 有序 map + 队列，交易公司最爱 |
| 6 | 讲义 hc04 | `hc04_queue_mean_snapshot` Part 1–2 | 最新的电面题（2026-03） |
| 7 | 讲义 hc07 + 基础 cpu_cache_locality | `hc07_ticker_hash_map` Part 1–2 | Blind 原题；从零写哈希表 |
| 8 | 讲义 hc06、hc08 | 两题 Part 1–2 | 位运算；树状数组 |
| 9 | J10 → J16 → J11 → J12 + 基础 os_processes_threads_ipc | hc02 / hc04 的并发 Part | 并发是追问的终点，放在最后一起啃 |
| 10 | J17 → J19 + 基础 networking_basics | hc07 / hc05 的性能 Part；`kq_language_depth` | 低延迟 Java、堆外内存、GC/JIT：和 JD 最贴的部分 |

面试前一天：只读 `LOOP_GUIDE.md` 和每题 `REPORT.md` 的「面试官可能的追问」，不碰新题。

## 做题命令（在本目录跑）

```bash
python3 tools/jtest.py start loop/rounds/01_video/hc03_recursive_sum              # starter/ → work/
python3 tools/jtest.py run   loop/rounds/01_video/hc03_recursive_sum --tag part1  # 只跑 Part 1
python3 tools/jtest.py run   loop/rounds/01_video/hc03_recursive_sum --impl reference
python3 tools/jtest.py verify "loop/rounds/*/*"                                   # 全部题的验收门
```

JDK：`brew install openjdk@21`（已装）。想在终端直接用 `java`：`export PATH=/opt/homebrew/opt/openjdk@21/bin:$PATH`。

## 题目一览

| id | 题 | 轮次 | 讲义 |
|---|---|---|---|
| oa01 | Job chain 报表（HackerRank 原题） | OA | ✅ |
| hc01 | 买卖股票 DP 家族 | 电面 | ✅ |
| hc02 | 合并 K 路有序 → 多线程合并数据流 | 电面 | ✅ |
| hc03 | 递归求和 → 溢出 / 栈 / trampoline / 并行 | 电面 | ✅ |
| hc04 | Queue mean + 修正快照 + 单写多读 | 电面 | ✅ |
| hc05 | 订单簿 + 撮合（含 hc14）+ 零分配版 | 电面 | ✅ |
| hc06 | 32 位寄存器位运算解释器 | 电面 | ✅ |
| hc07 | 股票代码 hash map 优化 | 电面 | ✅ |
| hc08 | 订单序列 API（树状数组） | 电面 | ✅ |
| hc09 | Top-K 成交额（含滑动窗口、并行聚合） | 电面 | ✅ |
| hc11 | 订单区间最大重叠 + 撤单（扫描线、线段树） | 电面 | ✅ |
| hc13 | 固定大小内存池（FFM、无锁） | 电面 | ✅ |
| ld01 | 共享内存 SPSC 通道（跨进程） | LLD | ✅ |
| kq | 语言深度 45 题 | 电面口头 | — |

**注意**：除了 oa01，大部分题网上只有题目名和一句话，Part 的具体规则是 kit 补全的，题面里标了 **(reconstructed)**。真面试时以面试官为准——先问清规则再写，本身就是加分项。
