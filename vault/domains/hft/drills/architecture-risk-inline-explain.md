---
nodes: [architecture.pre-trade-risk, architecture.order-state, architecture.hot-cold-path]
tags: [drill]
---
# 练习：向新同事解释，为什么下单前风控放在热路径里

新同事看了你们的系统图，问：「下单前风控（pre-trade risk check）为什么要塞进下单的热路径、每笔订单都过一遍？做成独立服务、批量检查不是更干净吗？」你们从收到行情到订单发出（tick-to-trade）的预算是 10 µs，持仓上限是 +1000 股，系统有 5000 个品种、20 个策略。

**要你给出的**
- 一段约 3 分钟的口头讲解：风控为什么必须在订单发出之前、每笔都过，以及为什么检查必须是 O(1)。
- 手算两题。(a) 当前持仓 0，已挂着 800 股买单，策略又想买 300 股，放行吗？(b) 策略连续发了 5 笔各 300 股的买单，回报都还没回来，第 5 笔该不该放行？
- 价格检查：参考价 100.00，允许偏离 500 bps（1 bp = 0.01%），策略本想以 100.00 卖 1000 股却误报成 10.00。判断是否拒绝，说出放行会亏多少，并写出只用乘法的不等式。
- 回答追问：「内联已经最快了，为什么还要独立风控进程和交易所侧的限额？」

**评分要点**
- 检查哪几项：价格合理性（fat finger，胖手指）、单笔数量或金额、持仓上限、下单速率、自成交防范；无法判断时也拒绝，叫出错即停（fail closed） ([[hft-architecture-pre-trade-risk-checks]])
- 为什么必须在发出之前：能把订单送进交易所的经纪商，必须在订单发出前自己直接且独占地控制信用上限、错误订单和合规检查 ([[hft-rules-market-access]])
- O(1) 靠增量维护：下单时加、成交或撤单时减，检查只读几个数组元素，几十纳秒；5000 × 20 × 64 字节约 6.4 MB 放得进 L2 或 L3。每次遍历 1 万张未完成订单要几十微秒，超过整个预算 ([[hft-architecture-pre-trade-risk-o1-incremental]])
- (a) 检查的是最坏情况持仓：0 + 800 + 300 = 1100 大于 1000，拒绝；只看已成交的 0 会误放行 ([[hft-architecture-pre-trade-risk-worst-case-position]])
- (b) 在途订单要按可能已成交计入：前 3 笔累计 900 股可放行，第 4 笔 900 + 300 = 1200 大于 1000 起就该拒绝，第 5 笔当然拒绝；若在途不计入，每次检查时持仓都还是 0，5 笔全放行，全部成交后持仓 1500 股，超限 500 股 ([[hft-architecture-order-state-in-flight-risk]])
- 价格检查：偏离 90.00 大于允许的 5.00，拒绝；放行会白亏 1000 × 90 = 90000 美元。整数定点价格写成 |px − ref| × 10000 ≤ ref × bps，只用乘法，避免除法的舍入和速度问题，乘法溢出也当作拒绝 ([[hft-architecture-pre-trade-risk-fat-finger-example]])
- 三层各防不同的失败：进程内闸门最快但和策略同命运，独立风控网关多几微秒、故障隔离，交易所或清算行侧限额不依赖你的任何代码；取舍是速度对隔离，所以叠加使用 ([[hft-architecture-pre-trade-risk-three-layers]], [[hft-reliability-kill-switch-exchange-side-defenses]])
- 熔断开关在热路径上每笔订单只读一个标志位，几纳秒；触发后撤单、拒绝新单、继续收行情 ([[hft-reliability-kill-switch-what-it-does]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
