---
id: bagu-tcc-2-reserve
node: a.idem.tcc
type: qa
step: 2
---
## Q
**TCC · Try 怎么预留资源**｜必会

面试官：「Try 阶段为什么要冻结额度，不直接扣？账户表怎么设计？」

## A
**基本回答。** 冻结是把可用额度转成冻结额度，业务上仍可回退；直接扣则一旦 Cancel 要做反向补偿。账户表加 `frozen_amount`，Try 把金额从可用转到冻结。
Try 用条件更新：`UPDATE ... SET available = available - 30, frozen = frozen + 30 WHERE id = ? AND available >= 30`；另建冻结记录表，事务号唯一，带状态（active、已确认、已释放），幂等和对账靠它。预留不占数据库行锁，并发比 2PC 好。外部渠道没有 Try，除非支持预授权（授权、请款、撤销），否则改 Saga 加对账。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<rect x="8" y="62" width="76" height="40" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="46" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可用 100</text>
<text x="46" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冻结 0</text>
<rect x="116" y="62" width="76" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="154" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可用 70</text>
<text x="154" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冻结 30</text>
<rect x="256" y="22" width="76" height="40" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="294" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可用 70</text>
<text x="294" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冻结 0</text>
<rect x="256" y="102" width="76" height="40" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="294" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可用 100</text>
<text x="294" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冻结 0</text>
<line x1="84" y1="82" x2="116" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="116.0,82.0 109.0,85.2 109.0,78.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="100" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Try</text>
<line x1="192" y1="74" x2="256" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,48.0 250.7,53.6 248.3,47.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="192" y1="90" x2="256" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,116.0 248.3,116.3 250.7,110.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="294" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Confirm</text>
<text x="294" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Cancel</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Try：额度从可用转到冻结</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Confirm：冻结变成真扣款，写分录</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Cancel：冻结还给可用，无需补偿</text>
</svg>
余额 100、订单 30。Try 把 30 从可用转到冻结，变成可用 70、冻结 30。之后有两条路：Confirm 把冻结的 30 真正扣掉（冻结归零，写分录）；Cancel 把冻结的 30 还回可用，回到 100。
**举个例子。** 钱包余额 100，订单 30，同时要扣库存：
1. **Try 钱包：**`available >= 30` 满足，可用变 70，冻结变 30，写一条冻结记录（active）。
2. **Try 库存：**库存服务失败了。
3. **Cancel 钱包：**冻结记录从 active 变成已释放，可用回到 100，冻结回到 0。用户的余额没变。
4. **如果库存成功：**Confirm 把冻结的 30 变成真正的扣款，冻结归零，写入分录，冻结记录变成已确认。
**容易错。**
- **以为冻结就是扣钱：**冻结只是把可用额度转成冻结额度，钱还在账户里，还能原样还回去。
- **以为外部渠道也能 TCC：**没有 Try 语义就不能，除非渠道支持预授权。
- **没有冻结记录：**没有状态记录，就没法判断是否已经确认或释放，幂等和对账都做不了。
