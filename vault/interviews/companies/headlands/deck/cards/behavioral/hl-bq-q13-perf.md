---
id: hl-bq-q13-perf
node: behavioral.question-bank
type: qa
step: 27
---
## Q
讲一个你解决过的性能问题。（诚实版，60–90 秒）
Tell me about a performance problem you solved.

## A
故事：S6（诚实版），辅 S5。

- **先说边界**："The honest version is **capacity reasoning before shipping, not profiling a running system**."
- **S6**：检测器只在 **6 个合成商户**上跑过；生产约 **18,000 商户**、一天最多 **7.6 亿行**；**每行成本 × 峰值行数** → 会超时；第一阶段做成**集合式 SQL**，模型放在**门**后面。
- **S5**：合并 `ON` 上的**一个月窗口**让扫描**有界**（zone-map 剪枝）；代价是**一个月后的去重盲区**。
- **Method**："If it were live I'd **measure per-row latency at small N**, separate **CPU from data movement**, extrapolate."然后问对方的瓶颈。

永远不编"快了 N 倍"。
