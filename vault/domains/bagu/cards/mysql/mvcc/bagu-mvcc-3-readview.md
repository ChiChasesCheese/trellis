---
id: bagu-mvcc-3-readview
node: a.mysql.mvcc
type: qa
step: 3
---
## Q
**ReadView · 可见性判断规则怎么走**｜必会

面试官：「给你一条版本链和一个读视图，怎么判断某个版本能不能看到？ReadView 里有什么？」

## A
**基本回答。** ReadView（读视图）里有四个值：`m_ids`（创建视图那一刻，所有活跃的、还没提交的事务 ID 列表）、`min_trx_id`（`m_ids` 里最小的）、`max_trx_id`（系统将要分配的下一个事务 ID）、`creator_trx_id`（创建这个视图的事务自己的 ID）。判断某个版本能不能看，拿版本上的 `trx_id` 对照：等于自己 → 可见；小于 `min_trx_id` → 视图创建前就已提交，可见；大于等于 `max_trx_id` → 视图创建后才开始的事务，不可见；介于两者之间，在 `m_ids` 里 → 当时还没提交，不可见，不在 `m_ids` 里 → 已经提交，可见。不可见就沿着 `DB_ROLL_PTR` 找上一个版本，再判断一遍。
自己的修改总是可见：版本的 `trx_id` 等于 `creator_trx_id`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">例：m_ids={100}，视图建于事务 105</text>
<rect x="8" y="30" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id < 100</text>
<text x="58.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已提交 → 可见</text>
<rect x="108" y="30" width="124" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100 ≤ id < 106</text>
<text x="170.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">在 m_ids？看下面</text>
<rect x="232" y="30" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id ≥ 106</text>
<text x="282.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不可见</text>
<line x1="108" y1="70" x2="108" y2="78" stroke-width="1.2" stroke="currentColor"/>
<text x="108" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">min_trx_id=100</text>
<line x1="232" y1="70" x2="232" y2="78" stroke-width="1.2" stroke="currentColor"/>
<text x="232" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">max_trx_id=106</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">中间段：在 m_ids 里 → 不可见；不在 → 可见</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">id = 自己（105）→ 可见，自己的修改自己看得到</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不可见 → 顺 ROLL_PTR 找上一个版本，再判断</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">视图创建时正在跑的事务，之后提交也不可见</text>
</svg>
把事务 ID 排成一条轴，三段对应三类事务：小于 100 的早就提交；大于等于 106 的还没开始；中间这一段要逐个对照 `m_ids`，在名单里的不可见。
**举个例子。** 事务 105 读账户行，视图是 `m_ids={100}`、`min_trx_id=100`、`max_trx_id=106`、`creator_trx_id=105`。版本链：链头 `(余额 50, trx_id=100)` → `(余额 100, trx_id=90)`。
1. 链头 `trx_id=100`：不等于 105，不小于 100，不大于等于 106，在 `m_ids` 里 → 不可见。
2. 沿指针到 `trx_id=90`：90 小于 `min_trx_id` 100 → 已提交，可见，读到 100。
3. **拍照前已提交：**假设链头是 `trx_id=102`（拍照前已提交，100 当时还在跑）：102 介于 100 和 106 之间，不在 `m_ids` 里 → 可见。
4. 假设链头是 `trx_id=106`：大于等于 `max_trx_id` → 拍照之后才开始，不可见。
**容易错。**
- **以为「介于两者之间」就不可见：** 要看它在不在 `m_ids` 里，不在名单里的已经提交，可见。
- **以为事务之后提交了就能看到：** 事务 100 在视图创建时还没提交，哪怕随后提交，它的 ID 还在这个视图的 `m_ids` 里，仍然不可见。
- **以为 max 是最大活跃事务：** `max_trx_id` 是系统将要分配的下一个事务 ID，比所有已分配的都大。
- **以为自己的修改看不到：** 版本的 `trx_id` 等于 `creator_trx_id` 就可见，同一事务先写后读看到的是自己改的值。
