---
id: foundations-elastic-vs-manual-scaling
node: foundations.tradeoffs
type: qa
---
## Q
Elastic (auto) scaling vs manually planned capacity — what does each buy, and when is manual the right answer?

## A
- **Elastic**: tracks unpredictable load and saves money at the trough — but reacts with lag (a sharp spike outruns instance boot), and feedback loops surprise you: scaling on the wrong metric, oscillation, or autoscaling silently absorbing a bug until the bill lands.
- **Manual**: fewer moving parts and forced capacity planning — right when load is predictable (daily/weekly cycles) or the unit is **stateful** (DB shards don't autoscale gracefully; rebalancing data is the cost).

Working rule: autoscale stateless compute; scale stateful tiers deliberately, ahead of need.


## Q zh
弹性（自动）扩容 vs 手工计划容量 — 各自的优点是什么，什么时候手工是正确答案？

## A zh
- **弹性扩容**：跟踪不可预测的负载并在低谷省钱 — 但反应有延迟（陡峭的峰值超过实例启动速度），反馈环会让人惊讶：在错误的指标上扩容、震荡、或 autoscaling 悄悄吸收一个 bug 直到账单出来。
- **手工扩容**：较少的活动部件，强制容量规划 — 在负载可预测（每日/周周期）或单位是**有状态**时正确（数据库分片不能优雅地自动扩容；数据重新平衡是代价）。

经验法则：无状态计算自动扩容；有状态层提前刻意地扩容。
