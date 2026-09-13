# INDEX — 53 题 × 考点 × Code Core 节点

> 用法：做错一道题 → 在这张表里找到它那一行 → 去 `00-essentials/` 读对应的章节 →
> 去 SystemDesign 仓库的 **Code Core** 牌组里把对应叶子的卡片加进复习队列。
>
> **考点编号**见 `00-essentials/02-core-topics.md`。

## 刷题顺序

**Top 10（OA 阶段 × 时效 × 引用数）**
`q01 → q09 → q02 → q18 → q17 → q07 → q03 → q15 → q29 → q08`

**然后**：`q04 q13 q05 q06 q10`
**phone screen 组**：`q22 q21 q19 q25 q32`
**算法组**：`qA01`–`qA13`

## 自研题（q01–q41）

| 题 | 一句话 | 主要考点 | 主 Code Core 叶子 | 精华章节 |
|---|---|---|---|---|
| q01 | 按 MCC 判定欺诈商户（CHARGE/DISPUTE） | S05 S10 S11 | `model.reversal` `rules.exact-ratio` `rules.thresholds` | 02 §S05 · 07 §1,2,8 |
| q02 | 商户风险评分（三趟规则） | S04 S05 | `rules.grouping` `rules.thresholds` | 02 §S04 · 07 §3 |
| q03 | Chat 计费（计量 + 套餐 + 分摊） | S06 S07 | `rules.money` `rules.rounding` `rules.tiers` | 04 全文 |
| q04 | 卡号区间补空隙 | S13 S09 | `chrono.intervals` `output.formatting` | 05 §7 · 07 §7 |
| q05 | 卡号校验（Luhn / `*` / `?`） | S14 S15 | `algorithms.strings` `algorithms.backtracking` | 08 §11 |
| q06 | 公司名可用性（归一化 + 注册 + 回收） | S14 S11 | `input.normalization` `model.idempotency` | 02 §S14 |
| q07 | 订阅通知调度（改套餐 + 续期） | S10 S08 S12 | `model.event-stream` `output.ordering` | 05 §3 · 06 §1 |
| q08 | 门店最佳关门时间 + BEGIN/END | A01 S05 S10 | `algorithms.prefix` `model.state-machine` | 08 §1 |
| q09 | Jupyter 负载均衡（粘性 + 容量 + 停机） | S10 S21 A15 | `toolbox.heap` `performance.budget` | 03 §3 |
| q10 | PaymentIntent 命令流 | S10 S11 S18 | `model.state-machine` `model.idempotency` | 02 §S18 · 07 §12 |
| q11 | 订阅数据库（替换 vs 累加） | S01 S05 S12 | `round.reading` `chrono.intervals` | 01 §2 · 05 §7 |
| q12 | 平台余额 + Radar 规则引擎 | S19 S18 | `input.grammar` `input.structured` | 02 §S18 |
| q13 | 账户台账（拒绝透支 + 平台放贷） | S06 S17 | `rules.money` `algorithms.settlement` | 04 §9 |
| q14 | 数据集 Join | S02 S08 | `input.delimited` `output.ordering` | 06 §1,3 |
| q15 | KYC 商户核验（CSV 渐进校验） | S18 S14 | `input.malformed` `input.normalization` | 02 §S18 |
| q16 | 拒付记录解析 + 撤回 | S06 S11 S18 | `input.malformed` `rules.money` | 04 §3 |
| q17 | 数据中心路由（Haversine） | S18 S08 | `input.malformed` `output.ordering` | 06 §1 · 07 §12 |
| q18 | 团伙识别（共享标识符） | A16 S04 | `toolbox.union-find` | 08 §6 |
| q19 | Accept-Language 解析 | S08 S14 | `output.ordering` `input.normalization` | 06 §1,3 |
| q20 | 手续费 + 应收 + 对账 | S06 S04 S07 | `rules.rounding` `rules.fees` `rules.grouping` | 04 §4,5,6 |
| q21 | 货币转换（多跳最优） | A02 S06 | `algorithms.shortest-path` `rules.rounding` | 08 §7 |
| q22 | 运费（路径 + 阶梯价目表） | A03 S07 S13 | `algorithms.shortest-path` `rules.tiers` | 08 §7 · 04 §8 |
| q23 | 限流器（滑窗 + 令牌桶） | S16 S12 | `chrono.windows` `toolbox.deque` | 05 §5,6 |
| q24 | 服务器编号分配 | S11 S21 A15 | `toolbox.heap` `model.idempotency` | 03 §3 |
| q25 | 发票对账 | S05 S11 | `algorithms.settlement` `model.idempotency` | 02 §S11 |
| q26 | AccountScheduler（锁 + LRU） | S05 S08 | `toolbox.cache` `chrono.intervals` | 05 §7 |
| q27 | PaymentLedger（幂等 + 部分退款） | S11 S12 S17 | `model.idempotency` `chrono.intervals` | 02 §S11 |
| q28 | 任务分派（技能 + 专才 + 容量） | S08 S21 | `output.ordering` `toolbox.heap` | 06 §1 |
| q29 | 部署窗口（时区 + 区间补集） | S12 S13 | `chrono.arithmetic` `chrono.intervals` | 05 §4,7 |
| q30 | Stripe Capital 贷款记账 | S06 S18 | `rules.rounding` `input.malformed` | 04 §4 |
| q31 | 心愿单互选排名 | S13 S18 | `output.ordering` `input.malformed` | — |
| q32 | 资金调拨（最少转账） | A10 S17 | `algorithms.settlement` `algorithms.backtracking` | 08 §12 |
| q33 | 分析型数据库（比较器） | S19 S08 | `output.ordering` `python.idioms` | 03 §5 |
| q34 | URL 压缩（numeronym） | S14 S09 | `algorithms.strings` | — |
| q35 | 用户积分 FIFO | S10 S17 | `algorithms.settlement` | 08 §12 |
| q36 | 时间键值映射（TTL） | S12 S13 | `toolbox.cache` `toolbox.sorted` | 03 §4 |
| q37 | 风控规则生效时间 | S12 S13 | `chrono.intervals` `model.event-stream` | 05 §7 |
| q38 | 功能开关（灰度 + 依赖） | S11 S05 | `verification.determinism` `model.state-machine` | 07 §9 |
| q39 | 服务器运行日志（k 次摘除） | A01 S10 | `algorithms.prefix` `algorithms.dp` | 08 §1,9 |
| q40 | 邻近词查询（最小窗口） | S16 S14 | `algorithms.sliding-window` `toolbox.sorted` | 08 §2 |
| q41 | 可观测性指标（时间窗聚合 + 迟滞告警，重建题） | S02 S05 S10 S12 S16 | `chrono.windows` `rules.thresholds` `model.state-machine` | 02 §S12,S16 |

## 算法组（qA01–qA13）

| 题 | LeetCode | 考点 | 主 Code Core 叶子 |
|---|---|---|---|
| qA01 | 2303 累进税 | A06 S06 | `rules.tiers` `rules.rounding` |
| qA02 | 787 ≤K 跳最便宜航线 | A03 | **`algorithms.shortest-path`** |
| qA03 | 1087 花括号展开 | A04 | `algorithms.backtracking` `input.grammar` |
| qA04 | 1169 非法交易 | A05 S16 | `algorithms.sliding-window` `rules.grouping` |
| qA05 | 1604 刷卡告警 | A07 S16 | `chrono.windows` `chrono.parsing` |
| qA06 | 2043 简单银行系统 | A08 S17 | `model.state-machine` `rules.money` |
| qA07 | 56 + 1288 区间 | A09 S13 | `chrono.intervals` |
| qA08 | 465 最优账目结算 | A10 | `algorithms.settlement` `algorithms.backtracking` |
| qA09 | 2050 并行课程 III | A11 | `algorithms.topological` |
| qA10 | 161 一次编辑距离 | A12 | `algorithms.strings` `algorithms.dp` |
| qA11 | 2768 黑格块计数 | A13 | `toolbox.hash` `performance.memory` |
| qA12 | 399 除法求值 | A02 A16 | `toolbox.union-find` `algorithms.graph-traversal` |
| qA13 | 2483 商店最小惩罚 | A01 | `algorithms.prefix` `algorithms.dp` |

## 反过来查：考点 → 题

| 考点 | 题 |
|---|---|
| 严格 vs 非严格阈值 | q01 q02 q05 q08 q13 q15 q23 q26 q28 q32 qA04 qA05 |
| 整数分 + 舍入 | q03 q13 q16 q20 q21 q22 q27 q30 qA01 qA06 |
| 阶梯 / proration | q03 q20 q22 qA01 |
| 事件流 + 撤销 | q01 q07 q09 q10 q11 q35 qA06 |
| 幂等 / 去重 | q01 q06 q09 q10 q16 q24 q25 q27 q38 |
| 时间 / 时区 | q02 q07 q11 q23 q26 q27 q29 q36 q37 qA05 |
| 区间 | q04 q08 q22 q26 q29 q36 q37 qA07 |
| 排序 tie-break | 几乎全部；重点 q07 q14 q17 q19 q20 q28 q31 q33 |
| 字节级输出 | q03 q04 q05 q10 q13 q16 q21 q30 |
| 解析 / 畸形输入 | q02 q12 q14 q15 q16 q17 q19 q30 |
| 堆 / 惰性删除 | q09 q24 q26 q28 |
| 并查集 | q18 qA12 |
| 最短路 | q21 q22 qA02 qA12 |
| 滑动窗口 | q23 q40 qA04 qA05 |
| DP | q39 qA10 qA13 |
| 结算 / FIFO | q13 q25 q32 q35 qA08 |
| 性能（10^5–10^6） | q09 q12 q23 q24 q26 q28 qA09 qA11 |
