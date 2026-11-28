---
id: hi-mock-airbnb-wallet-12-wrap-up
node: fix.airbnb-wallet-mock
type: qa
step: 12
---
## Q
**Airbnb Wallet · 第 12 步 · 收尾：一分钟总结，以及接下来加什么**｜模拟面试

面试官：「还剩一点时间。请你用一分钟把整个设计过一遍，再说说你接下来会加什么，什么时候加。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **一分钟：** 两张表，钱包和交易，余额是副本同事务更新。提现一个事务里先写 pending，再用条件 UPDATE 把钱从可用挪到冻结，0 行返回 409；平台调用在事务之外，幂等键是 transaction_id。结果走同一个 settle：webhook 是常态路径，条件更新忽略终态。pending 的读只读本地，30 秒窗口、每笔一个刷新任务、全局 20 次/秒。每天扫一次 pending 超过 1 小时的，告警最老的年龄。历史走键集分页，夜间核对余额。
- **Kafka：** 作用是平台更新比数据库写入快时做缓冲；代价是额外延迟、重复投递、多一处运维。触发条件：回调持续超 5,000 次/秒（现在峰值约 50），或要在钱包更新器宕机时不丢更新。后者有扫描兜底（最坏 25 小时补回），更便宜的第一步是先把回调落进 inbox 表再处理；业务接受不了那个延迟才上 Kafka。
- **只读备库：** 分走读，代价读到旧值；主库 CPU 持续超 50% 才加。
- **分片：** 按 wallet_id；写和存储水平扩，代价跨片查询和迁移；存储超 10 TB 或写持续超 10,000 行/秒。
- **复式账本：** 多方分账可审计，代价模型更重；出现手续费、多方或审计要求时。
- **扫描改每小时：** 缩短恢复窗口，代价对卡住的转账调用最多 ×24；业务要求收敛快于一天时。
- **只剩 45 分钟：** 前七步 24 分钟压到 16（澄清 2、功能 1、非功能 2、估算 2、实体 2、API 2、高层 5），深入三从 7 压到 2，收尾 7 不动；深入一和二共 20 分钟不能删，最容易被问倒。16 + 20 + 2 + 7 = 45。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 388">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要加的东西：作用 · 代价 · 触发条件</text>
<rect x="8" y="26" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Kafka 缓冲回调</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：写库慢于回调时不丢</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：延迟 · 重复 · 运维</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：回调 &gt; 5,000/秒，或宕机不能等</text>
<rect x="8" y="110" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">只读备库</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：分走读；代价：读到旧值</text>
<text x="18" y="159.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：主库 CPU 持续 &gt; 50%</text>
<rect x="8" y="179" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">按 wallet_id 分片</text>
<text x="18" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：写与存储水平扩；代价：跨片</text>
<text x="18" y="228.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：&gt; 10 TB 或写 &gt; 10,000/秒</text>
<rect x="8" y="248" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="267.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">复式账本</text>
<text x="18" y="282.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：多方分账可审计；代价：重写</text>
<text x="18" y="297.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：出现手续费、多方或审计要求</text>
<rect x="8" y="317" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="336.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">扫描改每小时</text>
<text x="18" y="351.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作用：缩短恢复窗口；代价：调用最多 ×24</text>
<text x="18" y="366.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：业务要求快于一天</text>
</svg>
白板上新增：「要加的东西：作用、代价、触发条件」的清单。

**常见失分。**
- **收尾只列组件：** 说不清冻结、先写后调、一个门、有界刷新、扫描这条线。
- **加了东西不说触发条件：** 分不清是需要还是炫技；作用、代价、触发三件说不全就不加。
- **把 Kafka 当默认：** 没有数字证明写不动，也没说重复投递。
- **「定期扫一下」：** 没有频率、选择规则、上限和告警。

**面试官可能接着问。**
- 平台额度突然降到 30 次/秒？ → 90 次/秒的预算超了，新建峰值 50 次/秒本身就超 30。新建调用进队列按 30 次/秒放行，用户拿 pending；平均 16.5 次/秒低于 30，高峰积压平峰排空；刷新和扫描各降到 5 次/秒，合计 26.5 < 30。这就是队列的触发条件。
- 每人每周 10 笔？ → 估算全部 ×10：峰值约 500 笔/秒、写 2,500 行/秒仍低于 10,000，一个主库够；7 年 18 TB 过 10 TB 线，热库只留最近 1 年（含索引约 5.2 TB），旧分区转冷存储，不分片。
