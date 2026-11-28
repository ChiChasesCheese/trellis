---
id: hi-mock-airbnb-wallet-11-dive-history-balance
node: fix.airbnb-wallet-mock
type: qa
step: 11
---
## Q
**Airbnb Wallet · 第 11 步 · 深入三：历史读与余额核对**｜模拟面试

面试官：「用户要看交易历史。再问一个：你的余额是一个字段，你怎么保证它和交易对得上？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **分成两个问题：** 历史怎么读；余额怎么保证和交易一致。
- **读的量：** 峰值 694 次/秒，每次一个钱包的索引范围读，几毫秒；每用户 7 年约 52 × 7 = 364 行，一页 20 行。主库加同步备库够，不加缓存：缓存的代价是刚提现完看到旧余额（最容易被投诉），触发条件是读持续超 5,000 次/秒或主库 CPU 持续超 50%。余额和历史读主库，不走缓存和异步副本。
- **键集分页：** 索引 `(wallet_id, created_at DESC, transaction_id DESC)`，查询带上一页最后一行的 `(created_at, transaction_id)`，多取 1 行判断有没有下一页，返回 next_cursor；transaction_id 作第二排序键让它唯一，翻页不重不漏。不用 OFFSET：翻深页要扫过前面的行，插入新交易还会重复或漏行。limit 默认 20、最大 100；导出走异步任务。
- **余额是副本：** 同事务更新所以正常不漂，仍要核对，因为 bug 不会通知你。两条夜间不变式：on_hold 等于该钱包所有 pending 提现之和；ready_to_use + on_hold 等于已完成转入减已完成转出（调整单也是 transactions 的一行）。
- **怎么跑：** 只核当天有交易的钱包：1,000 万笔/周 ÷ 7 ≈ 143 万个钱包，每个约 364 行，≈ 5.2 亿行 ≈ 260 GB；2 小时（7,200 秒）≈ 198 个钱包/秒、36 MB/秒，在备库按 wallet_id 范围分批，不碰主库。全量每月一次，周末 8 小时（28,800 秒），7 年后 1.82 TB ≈ 63 MB/秒。
- **不一致：** 只告警，不自动改；自动改掩盖 bug、破坏审计，修正是新增一条调整交易，历史不改。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 202">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">余额是副本：两条夜间不变式（跑在备库）</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① on_hold = Σ pending 提现金额</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按钱包分组；不等就告警</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② ready + hold = Σ 已完成转入 − Σ 已完成转出</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调整单也是 transactions 的一行</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">规模：143 万钱包 ÷ 7,200 秒 ≈ 198 个/秒</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只核当天有交易的，在备库上跑</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只告警不自动改：改历史就破坏了审计</text>
</svg>
白板上新增：键集分页的索引和查询，和夜间核对的两条不变式。

**常见失分。**
- **OFFSET 分页：** 越翻越慢，插入后重复或漏行。
- **无上限的列表：** 一个活跃用户就能拖慢读。
- **余额读缓存：** 刚提现就看到旧余额，正是最敏感的时刻。
- **没有核对：** 漂移很久才被发现。
- **自动改账：** 掩盖 bug，破坏审计。

**面试官可能接着问。**
- 为什么不一开始就用复式账本？ → 每笔至少两行分录、读余额要汇总或快照，模型更重；触发条件是出现手续费、多方分账或审计合规，现在只有单钱包进出，两张表够。
- 历史表要分区吗？ → 现在不用，第 1 年只有 260 GB；单表超约 1 TB 或建索引、vacuum 明显变慢才分，约第 4 年起按月分区，旧分区转冷存储。
