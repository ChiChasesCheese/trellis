---
id: hi-fix-apply-once-08-compare
node: fix.apply-once
type: qa
step: 8
---
## Q
**只应用一次｜补强 · 跨题对照**

同一个模式放进六道题：每道题里，「这个事件我已经应用过」的记录是什么，派生值是什么，重放时发生什么？

## A
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 434">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个模式，六道题里的「已应用」记录</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GoFundMe 总额</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">campaign_total_applied(donation_id)</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">与 += 同一事务；Redis 只 SET</text>
<rect x="8" y="94" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="114" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">钱包转账</text>
<text x="18" y="129" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分录 entry_id 唯一，分录本身就是记录</text>
<text x="18" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">余额由分录派生，可重算</text>
<rect x="8" y="162" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="182" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Robinhood 成交</text>
<text x="18" y="197" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">fills(exec_id) 唯一</text>
<text x="18" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">filled_qty、持仓只在插入成功时加</text>
<rect x="8" y="230" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="250" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">广告聚合</text>
<text x="18" y="265" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">主键 (ad_id, minute)：绝对值 upsert</text>
<text x="18" y="280" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重放写同一个数，不用记录</text>
<rect x="8" y="298" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="318" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Flash Sale 释放</text>
<text x="18" y="333" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREM 返回 1：成员本身是记录</text>
<text x="18" y="348" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Lua 里移除 + INCR 一起</text>
<rect x="8" y="366" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="386" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Ticketmaster 确认</text>
<text x="18" y="401" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">bookings 状态迁移 PENDING→CONFIRMED</text>
<text x="18" y="416" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">赢得迁移的一次才发邮件</text>
</svg>
白板上：六道题里的已应用记录，一行一题。

**同一套三问。** 面对任何由事件更新的派生值，先答：
- **谁触发：** 只有终态才触发，创建、PENDING、中间状态不触发。
- **记录是什么：** 一张唯一约束的已应用表（总额）、事实表本身（分录、成交）、绝对值的主键（聚合表）、集合成员（预留）、状态迁移（预订确认）。
- **和加法怎么绑：** 记录的写入和派生值的更新，在同一个事务或同一个脚本里。

**缓存怎么更新。** 缓存永远是 `SET` 成已提交的值，不用 `INCR`：重复执行也不变，崩了也能补。

**重放得到什么。** 插入 0 行、`ZREM` 返回 0、条件更新 0 行、覆盖成同一个值：四种信号，都意味着「已经做过」，直接返回成功，不报错。

**一句话版本。** 「消费者会重放，所以我先登记「这件事做过了」，登记和加法放进同一个事务；登记不上就是重放，直接跳过；缓存只设成已提交的值。」
