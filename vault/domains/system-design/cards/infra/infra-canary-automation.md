---
id: infra-canary-automation
node: infra.delivery
type: qa
---
## Q
What components turn a canary from "deploy 5% and stare at dashboards" into automated progressive delivery?

## A
- **Baseline pairing**: compare the canary against a **freshly deployed baseline running the old version** at the same size and traffic share — not against the aged full fleet — so warmup, cache state, and node placement don't pollute the comparison.
- **Automated judgement**: predefined metric queries (error rate, latency percentiles, saturation, key business metrics) scored statistically against the baseline at each step (Kayenta/Argo Rollouts style).
- **Stepped weights**: traffic shifts 1→5→25→100%, with a judgement gate before each increase.
- **Automatic rollback**: a failed gate shifts traffic back with no human in the loop — turning rollback MTTR from "someone notices" into seconds.

## Q zh
什么组件把 canary 从"部署 5% 并盯着仪表板"变成自动化渐进式交付？

## A zh
- **基线配对**：针对**新近部署的运行旧版本的基线**以相同大小和流量份额比较 canary——不是针对陈年完整fleet——所以预热、缓存状态、节点放置不污染比较。
- **自动判断**：预定义的指标查询（错误率、延迟百分位、饱和、关键业务指标）在每一步针对基线统计评分（Kayenta/Argo Rollouts 风格）。
- **阶跃权重**：流量移位 1→5→25→100%，在每个增长前有判断门。
- **自动回滚**：失败的门无人工循环地移位流量回——把回滚 MTTR 从"有人注意"变成秒。
