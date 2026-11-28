---
id: hi-fix-apply-once-06-flash-sale
node: fix.apply-once
type: qa
step: 6
---
## Q
**Flash Sale 库存释放 · 只应用一次**｜补强

面试官：「买家占下商品后有 10 分钟付款，超时就把库存还回去。如果过期任务和付款确认同时到，或者过期任务被跑了两次，库存会不会多还或少还？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说数据结构：** 「库存是一个计数器 `stock:{sku}`；占用的预留放在有序集合 `resv:{sku}`，成员是预留 id，分数是到期时间 `expiresAt`。」
- **已应用记录就是成员本身：** 「预留还在集合里，说明还没人处理过它。谁把它 `ZREM` 掉，谁就拿到了处理它的权利。`ZREM` 返回被移除的成员数：1 是我，0 是别人已经处理过。」
- **释放是一个 Lua 脚本：** 「`if redis.call('ZREM', KEYS[1], ARGV[1]) == 1 then redis.call('INCR', KEYS[2]) return 1 end return 0`。移除和归还库存在 Redis 里不可分开，不会出现「移除了但进程崩了，库存没还」。」
- **付款确认也走同一道门：** 「确认时 `ZREM` 这条预留：返回 1，是我的，继续下单；返回 0，说明已经过期被释放，拒绝付款并退款。过期任务和付款确认争的是同一个成员，只有一个赢。」
- **过期任务重复跑：** 「第二次的 `ZREM` 返回 0，不 INCR，库存不会多还。」
- **怎么找过期的：** 「`ZRANGE resv:{sku} -inf <now> BYSCORE LIMIT 0 100`，分批取，每个交给上面的脚本。」
- **Redis 是闸，数据库是账：** 「最后的购买仍然落数据库的条件更新；Redis 崩了，库存按「总量减已确认」重算。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 308">
<rect x="18" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过期任务</text>
<rect x="134" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">付款确认</text>
<rect x="250" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">r1 在 resv 里，分数 = expiresAt，已到期</text>
<text x="58" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Lua：ZREM r1 == 1 才 INCR</text>
<polyline points="54,104 286,104" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,104 279.0,107.2 279.0,100.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="222.4" y="118" width="113.6" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="279.2" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回 1：库存 +1</text>
<text x="174" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREM resv r1</text>
<polyline points="170,166 286,166" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,166 279.0,169.2 279.0,162.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="217.36" y="180" width="118.64" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="276.68" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回 0：已被处理</text>
<text x="174" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拒绝付款并退款</text>
<polyline points="286,228 170,228" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,228 177.0,224.8 177.0,231.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="256" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">过期任务又跑了一次</text>
<text x="58" y="278" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Lua：ZREM → 0，不 INCR</text>
<polyline points="54,290 286,290" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,290 279.0,293.2 279.0,286.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="54" y1="48" x2="54" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="54" y1="80" x2="54" y2="304" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="80" x2="170" y2="81" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="96" x2="170" y2="245" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="260" x2="170" y2="267" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="282" x2="170" y2="304" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="48" x2="286" y2="116" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="140" x2="286" y2="178" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="202" x2="286" y2="304" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="252" x2="105.68" y2="252" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="234.32" y1="252" x2="332" y2="252" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：过期任务和付款确认争同一个成员，只有 ZREM 返回 1 的那个继续。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 188">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">释放：移除和归还库存是一个动作</text>
<rect x="8" y="26" width="324" height="106" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">if redis.call('ZREM', KEYS[1], ARGV[1])</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">    == 1 then</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  redis.call('INCR', KEYS[2])</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  return 1</text>
<text x="18" y="105.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">end</text>
<text x="18" y="120.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">return 0</text>
<text x="8" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">KEYS[1]=resv:{sku}  KEYS[2]=stock:{sku}</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ZREM 返回被移除的成员数：1 = 只有我拿到</text>
</svg>
白板上：释放脚本，移除和归还是一个动作。

**为什么这样说。** 面试官在看你能不能让「只做一次」的判决发生在数据本身上，而不是靠任务只跑一次。弱的回答是「用锁保证过期任务只有一个在跑」：锁一旦失效，库存就多还；强的回答用 `ZREM` 的返回值当判决，并把它和归还库存放进一个脚本。
**面试官可能接着问。**
- 为什么不分成 `ZREM` 和 `INCR` 两条命令？ → 两条之间崩溃，预留没了但库存没还，少卖一件；反过来先 INCR 再 ZREM，崩溃就多还，超卖。一个脚本里两步一起成功。
- 付款确认时预留刚好过期了呢？ → 确认的 `ZREM` 返回 0，拒绝并退款；买家体验差，但库存是对的。
- 过期扫描会不会把刚付款的预留释放？ → 不会，付款确认已经 `ZREM` 掉它，扫描看不到。
- 为什么不给每个预留设一个 TTL 键？ → 到期时要回调才能还库存，Redis 的键过期事件不保证送达；有序集合加扫描更可靠。
**常见失分。**
- **用锁保证任务只跑一个：** 锁超时、任务重启之后，两个实例都在释放。
- **先查预留还在不在，再还库存：** 两个并发的释放都查到「在」。
- **移除和归还分两条命令：** 崩在中间库存对不上。
- **付款确认不检查预留：** 已经过期被还回去的库存又被卖了一次。
