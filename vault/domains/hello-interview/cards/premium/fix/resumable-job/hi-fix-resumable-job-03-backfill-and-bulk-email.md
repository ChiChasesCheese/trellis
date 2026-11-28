---
id: hi-fix-resumable-job-03-backfill-and-bulk-email
node: fix.resumable-job
type: qa
step: 3
---
## Q
**批量任务 · 回填与批量邮件用同一个模式**｜补强

面试官：「同样的问题换个场景：一张 2 亿行的订单表要加一列并回填，或者要给 100 万用户发一封账单邮件，任务跑到一半挂了。你用什么办法让它可续跑？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说是同一个模式：** 「任务表加块表；块的状态和该块的写入同一事务；重启读第一个非 done 的块；重叠由天然幂等的写吸收。三个场景只换三样东西：块怎么切、谁吸收重叠、节奏多快。」
- **回填，块怎么切：** 「按主键范围，id 连续的话 2 亿行 ÷ 5,000 行/块 = 40,000 块。用键范围，不用 OFFSET：OFFSET 要先数过前面的行，而且并发写入时会漂移。」
- **回填，谁吸收重叠：** 「UPDATE 带 `WHERE currency IS NULL`。块重跑时已经填过的行不再匹配，0 行，所以重做是无害的。」
- **回填，节奏：** 「每秒 5 块 × 5,000 行 = 25,000 行/秒；2 亿 ÷ 25,000 = 8,000 秒 ≈ 2.2 小时。放在低谷，看复制延迟，超过 5 秒就暂停。表上同时有线上写入，要先开双写或 CDC 再回填。」
- **迁移到新表：** 「块的写入改成 `INSERT INTO new SELECT … ON CONFLICT (id) DO NOTHING`：线上双写已经写进去的新数据不被旧值覆盖，回填只补空洞。」
- **批量邮件，难点不同：** 「邮件发出去撤不回来，也不在数据库事务里。所以分三步：事务一，认领块并把 1,000 行标 sending；调供应商，在事务外；事务二，把这些行回写 sent、块标 done。崩在哪一步，重启读到的状态都说得清。」
- **批量邮件，谁吸收重叠：** 「调供应商时带每封邮件的幂等键 (campaign_id, user_id)，加上消息行唯一。崩在『调用』和『回写』之间，重启重发同一个键，供应商认得就不再发。」
- **批量邮件，节奏：** 「供应商给我们 200 封/秒：1,000,000 ÷ 200 = 5,000 秒 ≈ 83 分钟。1,000 封一块 = 1,000 块，每块约 5 秒。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 269">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个模式，换三样东西</text>
<rect x="8" y="26" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">回填：2 亿行加一列</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">块 = 主键范围 5,000 行 → 40,000 块</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重叠由 WHERE col IS NULL 吸收</text>
<rect x="8" y="95" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">批量邮件：1,000,000 封</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">块 = 1,000 封 → 1,000 块</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重叠由供应商幂等键 + 唯一行吸收</text>
<rect x="8" y="164" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">活动扇出：1,000 万用户</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">块 = 10,000 人 → 1,000 块</text>
<text x="18" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重叠由 UNIQUE (campaign_id, user_id)</text>
<text x="8" y="241" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不变：任务表 + 块表；块状态与写入同事务；</text>
<text x="8" y="259" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重启从第一个非 done 块继续</text>
</svg>

```
BEGIN;
UPDATE orders
SET currency = 'USD'
WHERE id >= $lo AND id < $hi
  AND currency IS NULL;   -- 重跑：0 行
UPDATE backfill_chunk
SET status = 'done'
WHERE job = 'orders-currency'
  AND chunk_no = $k;
COMMIT;
```
白板上：三个场景三行，每行写块怎么切、谁吸收重叠；下面一句不变的部分。
**为什么这样说。** （约 2 分钟。）面试官要看你是不是只会这一道题。强的回答把模式抽出来，然后只改三样；弱的回答每个场景重新发明一套办法，或者不知道回填也需要续跑。
**面试官可能接着问。**
- 供应商不支持幂等键呢？ → 那就只能二选一：崩溃后宁可重发（至少一次，最多重一批 1,000 封），或者宁可漏发（至多一次，把『sending』的行标 unknown 交给人看）。营销邮件选前者，要在需求里写明。
- 回填的块失败了怎么办？ → 块表加 attempts，失败 3 次标 failed 告警，其余块继续；修好之后把它改回 pending。
- 为什么不整表一条 UPDATE？ → 2 亿行一个事务：持锁很久、日志撑爆、复制延迟飙升，失败就全部回滚重来。分块之后每块 5,000 行，每次只影响一小段。
- 什么时候不需要块表？ → 几万行以内、一个事务能做完、能整体重跑的任务，直接重跑，不要为它建块表。
- 迁移期间怎么保证新旧一致？ → 先开双写或 CDC，记下起点，再回填，追平后切读、切写，最后停旧表；顺序反了会丢回填期间的变更。
**常见失分。**
- **每个场景重新发明：** 看不出这是同一类问题。
- **回填整表一条 UPDATE：** 一个 2 亿行的事务。
- **用 OFFSET 分页做回填：** 越往后越慢，并发写入时还会漏行或重复。
- **邮件的 sent 标记在调用之前：** 崩溃后标了 sent 却没发，永远丢。
- **回填覆盖了线上刚写的新值：** 回填要用 `DO NOTHING` 或版本比较，不能无条件覆盖。
