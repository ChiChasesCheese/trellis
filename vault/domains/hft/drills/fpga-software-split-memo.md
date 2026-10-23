---
nodes: [fpga.basics, fpga.trading-uses, fpga.dev-tradeoffs]
tags: [drill]
---
# 练习：写一页备忘录，回答「整套策略能不能搬进 FPGA」

你们的跨交易所套利策略，软件 tick-to-trade（从收到行情到订单发出的时间）约 6 µs。竞争对手上了 FPGA（现场可编程门阵列，field-programmable gate array，把电路设计加载进芯片），约 200 ns。主管问：把整套策略搬进 FPGA 行不行？市场有 1000 只股票，策略只关心其中 20 只。

**要你给出的**
- 一页决策备忘：哪些逻辑放 FPGA、哪些留在软件，各给出理由；说明"软件定参数、硬件按条件发单"怎么运作。
- 手算三个数。(a) 时钟 250 MHz、解码流水线 40 级，延迟多少；20 级每级 4 ns 与 32 级每级 3 ns 比，哪个总延迟更低。(b) 10 Gb/s 链路上 64 字节最小帧的传输时间，为什么说 FPGA 已经接近物理极限。(c) 只关心 20 只股票时，在 FPGA 里过滤能丢掉多少消息。
- 软硬混合带来的新风险，和下单前风控应该放在哪里。
- 回答追问：为什么不干脆做专用集成电路（ASIC）。

**评分要点**
- FPGA 的工作方式：电路本身就是算法，数据每个时钟周期流过一级逻辑，各级同时工作；强项是固定、可并行、流式的处理（解码、过滤、简单触发、风控） ([[hft-fpga-basics-what-is-fpga]])
- 延迟是确定的：没有操作系统、中断、缓存、分支预测失败；(a) 40 × 4 ns = 160 ns 且每个包都一样；20 × 4 = 80 ns 低于 32 × 3 = 96 ns，频率更高不一定延迟更低，因为拆成更多级会增加周期数 ([[hft-fpga-basics-deterministic-latency]], [[hft-fpga-dev-tradeoffs-timing-closure]])
- (b) 512 位 ÷ 10^10 位每秒 = 51.2 ns；一条约 30 字节的行情消息约 24 ns；边收边解码，剩下只有光电转换、线缆（每米约 5 ns）和芯片内部时钟周期。软件约几微秒，FPGA 几十到几百纳秒 ([[hft-fpga-basics-latency-numbers]], [[hft-architecture-tick-to-trade-software-vs-fpga-magnitude]])
- (c) 980 ÷ 1000 = 98% 的消息在 FPGA 里就被丢掉，软件收到更少、更干净的数据，突发时不易积压 ([[hft-fpga-trading-uses-feed-decode-filter]])
- 为什么不全搬：时钟只有几百 MHz，资源有限，复杂分支和浮点不擅长，改一处要重新综合数小时；所以快路径放简单最急的事，复杂易变的留给软件 ([[hft-fpga-basics-limits]])
- 预先计算的触发条件：软件算好条件和订单模板写入 FPGA，行情到来只做固定比较，条件成立就填几个字段发出，几十到几百纳秒 ([[hft-fpga-trading-uses-precomputed-trigger]])
- 混合架构的新风险是两边状态不一致（参数更新有延迟、持仓数字过期、固件与软件版本不同步）；对策是 FPGA 内部有独立的硬限额、参数带版本号并确认、定期对账、不一致就熔断 ([[hft-fpga-trading-uses-hybrid-split]])
- 风控必须是流水线里的一级电路：回软件检查要多几微秒，抵消全部速度优势；绕过则一个错误参数就能连续发出大量订单。ASIC 数月和数百万美元的流片、不能修改、策略优势可能只持续几个月，所以多选 FPGA ([[hft-fpga-trading-uses-risk-in-hardware]], [[hft-fpga-dev-tradeoffs-asic]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
