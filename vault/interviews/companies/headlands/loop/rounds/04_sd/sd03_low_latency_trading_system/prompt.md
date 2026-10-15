# sd03 · 低延迟电子交易系统（Low-latency Electronic Trading System）

> 轮次：系统设计（FastPrep 标 System design，无阶段标签；归 onsite 为**推断**）· 置信度：**中**（1 个来源，只有标题 + 一句摘要）
> 来源：FastPrep「Design a Low-Latency Electronic Trading System」，页面标注 "Optiver / Headlands Technologies"，lastSeen 2025-10-29（`catalog/raw/github_repos.md` §3.1.D）。CATALOG Table C `sd03`。
> 注意（与 sd02 同理）：标注两家公司，说明这是一类**交易公司共享的题**，不是 Headlands 独有。
> **与岗位的关系（推断）**：Headlands 的 Java 岗按 JD 偏研究平台 / 存储 / 计算集群 / 监控 [O-C2]，毫秒以下的热路径系统是 C++ 岗 [O-C3]。所以这道题在 Java 岗面试里更可能被问成「**你理解整条链路，并能设计其中 Java 能做好的部分**」（编排、风控监控、对账、研究回放），而不是逐纳秒的网卡优化。**两头都要准备**：能讲热路径的原理，也能说清 Java 适合放在哪。

## 题面

**逐字能确定的一句**（英文原文）：

> 「Ingest market data, validate strategy order intents, route orders to exchanges, and reconcile executions」

四个动词就是四个子系统：**ingest**（行情摄取）→ **validate**（策略订单意图的校验，即交易前风控）→ **route**（路由到交易所）→ **reconcile**（对账成交）。

**本 kit 补全的版本 (reconstructed)**：

> 设计一个低延迟电子交易系统。它从一个或多个交易所接收实时行情；若干策略读取行情并产生「订单意图」；系统对每个意图做风控校验，通过的订单路由到相应交易所；交易所返回的成交/拒绝/撤单回报要被处理，并与独立数据源对账。说明：延迟预算、线程与数据流模型、状态存放与崩溃恢复、故障与安全机制（熔断）、怎么测试与度量。可以假设托管在交易所机房（co-location）。

## 面试官大概会这样推进 (reconstructed)

| 阶段 | 面试官说 / 问 | 你要做的 |
|---|---|---|
| 开场 | 「设计一个低延迟交易系统」 | 先问：延迟目标（µs）？品种数与消息速率？场所数？策略类型？错单 / 丢行情的后果？ |
| 5–10 分钟 | 「这条链路的延迟预算怎么分？」 | 估算：每条消息预算 = 1 / 速率；画流水线；各段 µs |
| 10–25 分钟 | 「画一下架构；线程模型呢？」 | 单写者、按品种分片、run-to-completion、SPSC 环、核心绑定 |
| 25–35 分钟 | 「行情丢包 / 乱序怎么办？」「风控放哪？」 | A/B 仲裁、缺口检测、快照恢复；风控内联 + 独立进程；熔断三层 |
| 35–45 分钟 | 「进程崩了怎么恢复？」「怎么对账？」 | 输入日志 + 重放；与交易所对账；cancel-on-disconnect；主备不双发 |
| 45–60 分钟 | 「用 Java 写，GC 怎么办？」「怎么证明 p99.99？」 | 零分配、预热、堆外、固定线程；线缆上打点、避免协调遗漏 |

## 开场必问的澄清问题（及你可以采用的假设）

| 问题 | 为什么问 | 若没答案，假设 |
|---|---|---|
| tick-to-trade 目标与分位数？ | 决定整个技术栈 | 软件部分 p99 ≤ 10 µs（假设，用于演示拆预算） |
| 品种数、行情峰值速率？ | 每条消息的预算 | 5,000 个品种，聚合峰值 1M msg/s（假设） |
| 场所数？协议？ | 网关与会话复杂度 | 3 个场所；行情组播二进制协议；订单入口为 TCP 二进制/FIX 类 |
| 策略有多少、多复杂？ | 决定策略线程数与隔离 | 20 个策略，计算轻（μs 级） |
| 资产类别？ | 订单类型、风险维度 | 现货股票/期货（限价单、撤单、改单） |
| 错单与丢行情哪个更贵？ | fail-closed 的边界 | 错单贵得多；行情有缺口时对该品种停止交易 |
| 恢复时间要求（RTO）、可接受的停机？ | 主备设计 | 秒级恢复，期间不报价 |
| 监管 / 内部风控要求？ | 风控位置与独立性 | 必须有独立于策略的交易前风控与熔断 |
| 语言 / 运行环境？ | Java 取舍 | 热路径 Java（面试题设定），承认其下限 |

## 约束与不变量（写在白板上）

* **I1 决定性**：同一输入序列（行情 + 回报 + 命令 + 时钟）⟹ 逐位相同的输出（订单 + 状态）。
* **I2 单写者**：每个可变状态恰有一个写线程。
* **I3 fail closed**：任何无法确认状态的情形（行情缺口、会话不明、对账差异、日志写不动）⟹ 停止对该范围发新单。
* **I4 不重复发单**：任一时刻只有一个实例有权发送某账户 / 会话的订单。
* **I5 仓位 = 成交之和**：内部仓位始终能由成交回报序列重新推出，并与交易所 / 清算对账一致。
* **非目标**：交易所撮合引擎本身（见 trellis 的 [design-stock-exchange](../../../../../../../domains/system-design/drills/problems/design-stock-exchange.md)）；策略的 alpha；清算结算。

## 评分入口

[rubric.md](rubric.md) · 参考答案 [model_answer.md](model_answer.md) · 追问 [followups.md](followups.md) · 总体方法 [../00_how_to_run.md](../00_how_to_run.md)。
动手配套：[ld01 SPSC 通道](../../03_lld/ld01_spsc_channel/problem.md) · [ld02 交易 OOD（订单状态机 / 风控 / 重放）](../../03_lld/ld02_trading_ood/problem.md) · [ld03 异步 TCP 通道](../../03_lld/ld03_async_tcp_channel/problem.md) · [hc05 订单簿](../../01_video/hc05_market_order_book/problem.md)。
