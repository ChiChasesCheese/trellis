---
id: hl-sd03-rubric-strong
node: system-design.sd03-low-latency-trading
type: qa
step: 49
---
## Q
低延迟交易系统评分表上，澄清、估算、架构、行情、风控、状态与恢复的「strong」标准是什么？

## A
总原则：**strong = 数字 + 失败模式 + 验证方法**。
- **澄清**：先问延迟目标（分位数）、品种数与消息速率、场所数、错单与丢行情的相对代价、RTO；判断这是热路径题还是平台题；
- **估算**：把速率翻译成每条消息预算（1 µs ≈ 3,000 周期 ≈ 10 次未命中），停顿 × 速率（1 ms = 1,000 条），日志速率与每日体量，簿与风控状态大小，Little 定律；
- **架构**：分片 + 单写者 + run-to-completion，SPSC 环，Feed Handler / 分片 / 网关 / Journaler 分工，说明哪里必须交接、哪里不拆线程；
- **行情**：组播、A/B 仲裁、序号、缺口 ⟹ STALE ⟹ 禁止交易、快照 + 增量恢复，flyweight 解码，数组订单簿，定点价格；
- **风控**：O(1) 内联检查清单，增量聚合，fail closed，三层熔断，独立性论证，监管背景；
- **状态与恢复**：source of truth，决定性 + 输入日志 + 快照重放，日志环不能丢，mmap 与 fsync 的故障层次，恢复流程含对账，ClOrdID 单调。
