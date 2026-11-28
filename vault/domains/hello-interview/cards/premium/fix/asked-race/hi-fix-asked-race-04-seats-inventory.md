---
id: hi-fix-asked-race-04-seats-inventory
node: fix.asked-race
type: qa
step: 4
---
## Q
**先答被问的竞态 · 座位和库存**｜补强

面试官：「两个人同时买座位 A15，怎么保证只有一个人拿到？换成库存只剩 1 件，又怎么做？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **模板：** 「被问的案例是……；我让数据库只放行一个；条件是……；影响 0 行表示……。」
- **座位：** 「被争的是 A15 这一行，所以条件写落在这一行上：status = 'available'。影响 1 行，座位占上；影响 0 行，已经被别人占了。如果只对「剩余座位数」做条件写，两个人仍然可能拿到 A15。」
- **库存：** 「被争的是 qty。UPDATE stock SET qty = qty - n WHERE sku = $s AND qty >= n；1 行成功，0 行售罄。」
- **与钱包是同一个套路：** 「钱包是 ready_to_use >= 金额；只是把名字换掉，句子不变。」
- **重试另说：** 「同一个用户的重发，不应该被当成「被别人占了」；占座时记录 attempt_id，同一个 attempt_id 再来一次视为成功。」
- **占座要有时限：** 「占座后要付款，行锁不能占 10 分钟；用 status = 'held' 加 hold_until；条件是 available，或 held 且已过期。已售出（sold）的座位哪个分支都不进。」
**白板。**
```
UPDATE seats
SET status = 'held', held_by = $u,
    hold_until = now() + interval '10 min'
WHERE seat_id = 'A15'
  AND (status = 'available'
       OR (status = 'held'
           AND hold_until < now()));
-- 1 行: 占上；0 行: 已被占

UPDATE stock
SET qty = qty - $n
WHERE sku = $s AND qty >= $n;
-- 1 行: 成功；0 行: 售罄
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一句话换对象：被问的竞态 → 一条语句 → 0 行</text>
<rect x="8" y="26" width="324" height="74" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">座位 A15：两个人同时买</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">共享状态：A15 这一行</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件 status = 'available'</text>
<text x="18" y="89.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 行：座位已被别人占</text>
<rect x="8" y="108" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">库存 100 件：5,000 人同时抢</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">共享状态：这个 sku 的 qty</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件 qty &gt;= 购买数</text>
<text x="18" y="171.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 行：售罄；赢 100，输 4,900</text>
<rect x="8" y="190" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">钱包 500：两笔 500 提现</text>
<text x="18" y="223.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">共享状态：ready_to_use</text>
<text x="18" y="238.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件 ready_to_use &gt;= 金额</text>
<text x="18" y="253.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 行：余额不足</text>
</svg>
白板上：三个对象三行，每行一个共享状态、一个条件、一个 0 行的含义。
**为什么这样说。** （约 1 分钟。）面试官在看你有没有一套可以搬的句式。强的回答每换一个对象，句式不变，只换共享状态和条件；弱的回答每道题发明一种新办法。
**面试官可能接着问。**
- 5,000 人同时抢 100 件，库存这一行扛得住吗？ → 同一行约 2 ms 一次，约 500 次/秒，5,000 ÷ 500 = 10 秒排完；再多就分桶，或先用 Redis 做准入排队。
- 用户连点两次买同一件呢？ → 订单上有 attempt_id 唯一键，先 INSERT 订单再扣库存，同一个事务；重复的被唯一键挡住。
- 同时买两个连号的座位呢？ → 条件跨两行，一条条件写不够：先按座位号升序给两行加锁，再检查再写。
**常见失分。**
- **只对数量做条件写：** 剩 1 个座位时，两个人仍可能拿到同一个座位。
- **把重试当成冲突：** 用户自己的重发被拒，体验变成「座位被占了」。
- **占座时持行锁等付款：** 一个未付款的用户占住一个连接 10 分钟。
