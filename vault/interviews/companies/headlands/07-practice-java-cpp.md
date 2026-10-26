# 07 · 练习清单：每道题 40 分钟，Java 和 C++ 各写一遍

每道题都是一场真实面试的篇幅：Part 1 写核心代码（约 12–15 分钟），Part 2 写面试官最常加的那一步（约 15 分钟），Part 3 只练口头回答（约 10 分钟）。先读 `problem.md` 动手，写完或卡住了再读 `solution.md`：那里写了从哪一步下手、为什么这样做、两种语言的完整代码和追问的答案。题目按出现频率排好了，时间不够就从上往下做。

## 怎么用

在 `interviews/companies/headlands/` 目录下运行：

```bash
python3 tools/jtest.py   start <题目目录>     # Java：starter/ → work/，在 work/ 里写
python3 tools/jtest.py   run   <题目目录> --tag part1
python3 tools/cpptest.py start <题目目录>     # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   <题目目录> --tag part1
python3 tools/ide.py <题目目录>               # 换题后跑一次，再在 Cursor 里 Reload Window
```

- **按考场条件**：关掉 Cursor Tab，计时，先说思路再写。Part 1 超过 15 分钟就停下读 solution.md，第二天重写。
- **C++ 那一遍**：注意整数溢出（有符号溢出是 UB）、`const&` 传参、边遍历边删要用返回的迭代器。容器对应：`HashMap` → `unordered_map`，`TreeMap` → `map`，`PriorityQueue` → `priority_queue`（默认大顶堆），`ArrayDeque` → `deque`。
- **保存时自动格式化**：Java 按 `tools/java-format.xml`，C++ 按 kit 根目录的 `.clang-format`，你手动换的行会保留。

## 电面高频（先做这些）

| 题 | Java | C++ | 题面 · 解法 | 目录 |
|---|---|---|---|---|
| hc03 · 递归求和 1..n（溢出、栈深、公式） | ☐ | ☐ | [题面](loop/rounds/01_video/hc03_recursive_sum/problem.md) · [解法](loop/rounds/01_video/hc03_recursive_sum/solution.md) | `loop/rounds/01_video/hc03_recursive_sum` |
| hc07 · 股票代码哈希表（打包成整数 + 开放寻址） | ☐ | ☐ | [题面](loop/rounds/01_video/hc07_ticker_hash_map/problem.md) · [解法](loop/rounds/01_video/hc07_ticker_hash_map/solution.md) | `loop/rounds/01_video/hc07_ticker_hash_map` |
| hc01 · 买卖股票（一次、不限次数、最多 k 次） | ☐ | ☐ | [题面](loop/rounds/01_video/hc01_stock_trading_dp/problem.md) · [解法](loop/rounds/01_video/hc01_stock_trading_dp/solution.md) | `loop/rounds/01_video/hc01_stock_trading_dp` |
| hc04 · 队列均值 + 快照修正 | ☐ | ☐ | [题面](loop/rounds/01_video/hc04_queue_mean_snapshot/problem.md) · [解法](loop/rounds/01_video/hc04_queue_mean_snapshot/solution.md) | `loop/rounds/01_video/hc04_queue_mean_snapshot` |
| hc05 · 订单簿 + 限价撮合 | ☐ | ☐ | [题面](loop/rounds/01_video/hc05_market_order_book/problem.md) · [解法](loop/rounds/01_video/hc05_market_order_book/solution.md) | `loop/rounds/01_video/hc05_market_order_book` |
| hc02 · 合并 K 个有序序列 → 惰性迭代器 | ☐ | ☐ | [题面](loop/rounds/01_video/hc02_merge_k_streams/problem.md) · [解法](loop/rounds/01_video/hc02_merge_k_streams/solution.md) | `loop/rounds/01_video/hc02_merge_k_streams` |
| hc10 · 出现次数最多的 k 个数（堆 → 桶排序） | ☐ | ☐ | [题面](loop/rounds/01_video/hc10_top_k_frequent/problem.md) · [解法](loop/rounds/01_video/hc10_top_k_frequent/solution.md) | `loop/rounds/01_video/hc10_top_k_frequent` |
| hc06 · 32 位寄存器位运算 | ☐ | ☐ | [题面](loop/rounds/01_video/hc06_cpu_register_bitwise/problem.md) · [解法](loop/rounds/01_video/hc06_cpu_register_bitwise/solution.md) | `loop/rounds/01_video/hc06_cpu_register_bitwise` |

## 电面其他题

| 题 | Java | C++ | 题面 · 解法 | 目录 |
|---|---|---|---|---|
| hc08 · 订单序列的前缀查询（线性 → 树状数组） | ☐ | ☐ | [题面](loop/rounds/01_video/hc08_order_sequence_api/problem.md) · [解法](loop/rounds/01_video/hc08_order_sequence_api/solution.md) | `loop/rounds/01_video/hc08_order_sequence_api` |
| hc09 · 按成交额取 Top-K（事件 → 代码汇总） | ☐ | ☐ | [题面](loop/rounds/01_video/hc09_top_trades_by_notional/problem.md) · [解法](loop/rounds/01_video/hc09_top_trades_by_notional/solution.md) | `loop/rounds/01_video/hc09_top_trades_by_notional` |
| hc13 · 定长内存池（空闲链表 → 带代数的句柄） | ☐ | ☐ | [题面](loop/rounds/01_video/hc13_fixed_memory_pool/problem.md) · [解法](loop/rounds/01_video/hc13_fixed_memory_pool/solution.md) | `loop/rounds/01_video/hc13_fixed_memory_pool` |
| hc11 · 订单区间最大重叠（扫描线 → 分买卖 + 撤单） | ☐ | ☐ | [题面](loop/rounds/01_video/hc11_order_interval_overlap/problem.md) · [解法](loop/rounds/01_video/hc11_order_interval_overlap/solution.md) | `loop/rounds/01_video/hc11_order_interval_overlap` |
| hc14 · 成交日志 → VWAP（汇总 → 滑动时间窗口） | ☐ | ☐ | [题面](loop/rounds/01_video/hc14_vwap_trade_log/problem.md) · [解法](loop/rounds/01_video/hc14_vwap_trade_log/solution.md) | `loop/rounds/01_video/hc14_vwap_trade_log` |
| hc15 · 成交价的流式中位数（两个堆 → 滑动窗口） | ☐ | ☐ | [题面](loop/rounds/01_video/hc15_streaming_median/problem.md) · [解法](loop/rounds/01_video/hc15_streaming_median/solution.md) | `loop/rounds/01_video/hc15_streaming_median` |
| hc16 · 交易台层级上的树形 DP | ☐ | ☐ | [题面](loop/rounds/01_video/hc16_tree_dp/problem.md) · [解法](loop/rounds/01_video/hc16_tree_dp/solution.md) | `loop/rounds/01_video/hc16_tree_dp` |
| hc22 · 带批量加法的栈（O(k) → 懒标记 O(1)） | ☐ | ☐ | [题面](loop/rounds/01_video/hc22_custom_stack/problem.md) · [解法](loop/rounds/01_video/hc22_custom_stack/solution.md) | `loop/rounds/01_video/hc22_custom_stack` |
| hc23 · 游程编码解码（整串 → 分块流式） | ☐ | ☐ | [题面](loop/rounds/01_video/hc23_rle_decode/problem.md) · [解法](loop/rounds/01_video/hc23_rle_decode/solution.md) | `loop/rounds/01_video/hc23_rle_decode` |
| hc17 · 带 `*` 的模式匹配（DP → 贪心双指针） | ☐ | ☐ | [题面](loop/rounds/01_video/hc17_text_pattern_stars/problem.md) · [解法](loop/rounds/01_video/hc17_text_pattern_stars/solution.md) | `loop/rounds/01_video/hc17_text_pattern_stars` |
| hc21 · 平方根（牛顿法 → 整数平方根） | ☐ | ☐ | [题面](loop/rounds/01_video/hc21_square_root/problem.md) · [解法](loop/rounds/01_video/hc21_square_root/solution.md) | `loop/rounds/01_video/hc21_square_root` |

## Onsite 编码题

| 题 | Java | C++ | 题面 · 解法 | 目录 |
|---|---|---|---|---|
| hc19 · 不相邻取数（House Robber） | ☐ | ☐ | [题面](loop/rounds/02_onsite/hc19_house_robber/problem.md) · [解法](loop/rounds/02_onsite/hc19_house_robber/solution.md) | `loop/rounds/02_onsite/hc19_house_robber` |
| hc20 · 合并区间 → 插入区间 | ☐ | ☐ | [题面](loop/rounds/02_onsite/hc20_merge_intervals/problem.md) · [解法](loop/rounds/02_onsite/hc20_merge_intervals/solution.md) | `loop/rounds/02_onsite/hc20_merge_intervals` |
| hc12 · 触发订单过滤 | ☐ | ☐ | [题面](loop/rounds/02_onsite/hc12_triggered_orders/problem.md) · [解法](loop/rounds/02_onsite/hc12_triggered_orders/solution.md) | `loop/rounds/02_onsite/hc12_triggered_orders` |
| hc18 · 由快照和成交算净持仓 | ☐ | ☐ | [题面](loop/rounds/02_onsite/hc18_net_position/problem.md) · [解法](loop/rounds/02_onsite/hc18_net_position/solution.md) | `loop/rounds/02_onsite/hc18_net_position` |

## OA 题

| 题 | Java | C++ | 题面 · 解法 | 目录 |
|---|---|---|---|---|
| oa01 · Job Chain 报表（你过了的 OA，面试官可能问你怎么写的） | ☐ | ☐ | [题面](loop/rounds/00_oa/oa01_job_chain/problem.md) · [解法](loop/rounds/00_oa/oa01_job_chain/solution.md) | `loop/rounds/00_oa/oa01_job_chain` |
| oa03 · As-of join（每笔成交配上当时最新的报价） | ☐ | ☐ | [题面](loop/rounds/00_oa/oa03_asof_join/problem.md) · [解法](loop/rounds/00_oa/oa03_asof_join/solution.md) | `loop/rounds/00_oa/oa03_asof_join` |

## 设计与并发（onsite 的设计轮）

| 题 | 讲义 | 目录 |
|---|---|---|
| ld01 · 共享内存 SPSC 消息通道 | [[ld01_spsc_channel\|讲义]] | `loop/rounds/03_lld/ld01_spsc_channel` |
| ld02 · 交易相关的 OOD | [[ld02_trading_ood\|讲义]] | `loop/rounds/03_lld/ld02_trading_ood` |
| ld03 · 异步 TCP 消息通道 | [[ld03_async_tcp_channel\|讲义]] | `loop/rounds/03_lld/ld03_async_tcp_channel` |

## 模拟题（Java / Maven）

`mock_maven/` 是两道 Maven 项目形式的模拟题，只练 Java：先读 `mock_maven/README.md`。
