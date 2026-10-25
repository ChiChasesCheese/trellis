# 07 · Java 和 C++ 各写一遍：练习清单

每道题先用 Java 写一遍，再用 C++ 写一遍，按考场条件：关掉 AI 补全，计时，先说思路再写，写完自己造用例跑。每道题按 Part 推进，前两个 Part 是一场面试最常走到的地方，后面的 Part 当追问练。写完对照 `reference` 和讲义找差距，把卡住的点记在该题下面。

## 怎么用

在 `interviews/companies/headlands/` 目录下运行（每道题的命令在下面表格里）：

```bash
python3 tools/jtest.py start <题目目录>     # 复制 Java 空壳到 work/，在 work/ 里写
python3 tools/jtest.py run   <题目目录> --tag part1
python3 tools/cpptest.py start <题目目录>   # 复制 C++ 空壳到 cpp/work.hpp
python3 tools/cpptest.py run   <题目目录> --tag part1
```

- **限时**：Part 1 约 15 分钟，Part 1 + 2 约 35 分钟；超时就停，读讲义，第二天重写。
- **C++ 那一遍**：先过一遍 [[CPP_CONVENTIONS]] 和 C++ 讲义 C16（CoderPad 现场），注意整数溢出、迭代器失效、`const&` 传参。
- **两遍之间**：不要看 Java 的代码写 C++；先想清楚两种语言里各自地道的数据结构（`TreeMap` 对 `std::map`，`ArrayDeque` 对 `std::deque`）。

## OA 原题

| 题 | Java | C++ | 讲义 | 目录 |
|---|---|---|---|---|
| oa01 · Job Chain 报表（OA，1 题，100–120 分钟） | ☐ | ☐ | [[oa01_job_chain\|讲义]] | `loop/rounds/00_oa/oa01_job_chain` |

## 视频面编码题

| 题 | Java | C++ | 讲义 | 目录 |
|---|---|---|---|---|
| hc01 · Best Time to Buy and Sell Stock 家族（动态规划 / 状态机） | ☐ | ☐ | [[hc01_stock_trading_dp\|讲义]] | `loop/rounds/01_video/hc01_stock_trading_dp` |
| hc02 · 合并 K 个有序序列 → 合并多路数据流（Headlands 一小时技术电面） | ☐ | ☐ | [[hc02_merge_k_streams\|讲义]] | `loop/rounds/01_video/hc02_merge_k_streams` |
| hc03 · 递归求和 1..n（面试官一路追问） | ☐ | ☐ | [[hc03_recursive_sum\|讲义]] | `loop/rounds/01_video/hc03_recursive_sum` |
| hc04 · Queue Mean + 修正快照（Headlands 一小时技术电面） | ☐ | ☐ | [[hc04_queue_mean_snapshot\|讲义]] | `loop/rounds/01_video/hc04_queue_mean_snapshot` |
| hc05 · Market Order Book（订单簿 + 限价撮合） | ☐ | ☐ | [[hc05_market_order_book\|讲义]] | `loop/rounds/01_video/hc05_market_order_book` |
| hc06 · CPU 寄存器位运算（一个无符号 32 位寄存器 + 一串操作） | ☐ | ☐ | [[hc06_cpu_register_bitwise\|讲义]] | `loop/rounds/01_video/hc06_cpu_register_bitwise` |
| hc07 · 股票代码哈希表（design an optimized hash map for stock tickers） | ☐ | ☐ | [[hc07_ticker_hash_map\|讲义]] | `loop/rounds/01_video/hc07_ticker_hash_map` |
| hc08 · Order Sequence API（订单序列的前缀 count / quantity 查询） | ☐ | ☐ | [[hc08_order_sequence_api\|讲义]] | `loop/rounds/01_video/hc08_order_sequence_api` |
| hc09 · Top Trade Events by Notional（按名义金额取 top-k 成交 / ticker） | ☐ | ☐ | [[hc09_top_trades_by_notional\|讲义]] | `loop/rounds/01_video/hc09_top_trades_by_notional` |
| hc11 · 订单区间最大重叠 + 按买 / 卖方撤单 | ☐ | ☐ | [[hc11_order_interval_overlap\|讲义]] | `loop/rounds/01_video/hc11_order_interval_overlap` |
| hc13 · 定长内存池（Fixed-Size Memory Pool） | ☐ | ☐ | [[hc13_fixed_memory_pool\|讲义]] | `loop/rounds/01_video/hc13_fixed_memory_pool` |
| hc16 · Tree DP on a Desk Hierarchy（交易台层级树上的 DP） | ☐ | ☐ | [[hc16_tree_dp\|讲义]] | `loop/rounds/01_video/hc16_tree_dp` |

## 设计与并发（LLD）

| 题 | Java | C++ | 讲义 | 目录 |
|---|---|---|---|---|
| ld01 · 共享内存 SPSC 消息通道（Shared-Memory Single-Writer Single-Reader Channel） | ☐ | ☐ | [[ld01_spsc_channel\|讲义]] | `loop/rounds/03_lld/ld01_spsc_channel` |
| ld02 · 交易相关的 OOD（订单状态机 · 仓位 PnL · 交易前风控 · 事件溯源与重放） | ☐ | ☐ | [[ld02_trading_ood\|讲义]] | `loop/rounds/03_lld/ld02_trading_ood` |
| ld03 · 异步 TCP 消息通道（Asynchronous TCP Message Channel） | ☐ | （暂无 C++ 版） | [[ld03_async_tcp_channel\|讲义]] | `loop/rounds/03_lld/ld03_async_tcp_channel` |

## 模拟题（Java / Maven）

`mock_maven/` 是两道 Maven 项目形式的模拟题，只练 Java：先读 `mock_maven/README.md`。
