---
id: bagu-payment-system-4-reconcile
node: a.scenario.payment-system
type: qa
step: 4
---
## Q
**对账与补偿 · 发现并处理渠道与我方的差异**｜必会

面试官：「渠道扣了钱而订单还是未支付，或者我方记了账而渠道没收到，怎么发现并处理？」

## A
**基本回答。** 对账就是拿两份独立来源的记录互相印证：每天把我方支付单和渠道账单按渠道交易号逐笔比对，差异分三类处理。渠道有、我方无：先向渠道查询确认，再补单入账并通知订单继续。我方有、渠道无：风险最高，转人工，多半要撤销订单。金额不符：按口径差异或本金差异分别处理，本金差异转人工。处理动作只追加调整记录，不改原记录。
**一句话记住。** 对账像月底拿自己的记账本和银行对账单逐行打勾，没勾上的就是要查的差异。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="46" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我方支付单</text>
<text x="138" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道账单</text>
<text x="260" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">怎么处理</text>
<rect x="4" y="28" width="84" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T1  100</text>
<rect x="92" y="28" width="84" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T1  100</text>
<rect x="184" y="28" width="152" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一致，通过</text>
<rect x="4" y="66" width="84" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（无）</text>
<rect x="92" y="66" width="84" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T2  50</text>
<rect x="184" y="66" width="152" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">补单入账（先查询确认）</text>
<rect x="4" y="104" width="84" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="46.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T3  80</text>
<rect x="92" y="104" width="84" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="134.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（无）</text>
<rect x="184" y="104" width="152" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高风险：转人工撤单</text>
<rect x="4" y="142" width="84" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T4  100</text>
<rect x="92" y="142" width="84" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T4  90</text>
<rect x="184" y="142" width="152" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">金额不符：分类处理</text>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">截止点前后的交易是时间差，不是真差异</text>
<text x="170" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">放进等待队列，次日再比</text>
</svg>
同一个交易号在两边逐行对照：两边一致就过，缺一边或金额不同才进入处理。
**讲明白。**
- **为什么需要对账：**回调会丢、会乱序，主动查询也有窗口，所以必须有最后一道防线。对账的价值在于两份记录来自不同系统，互相印证。
- **怎么比：**每天把我方支付单与渠道账单按渠道交易号逐笔比对，找出渠道有我方无、我方有渠道无、金额不符三类差异。
- **渠道有、我方无：**典型原因是回调丢了。先向渠道查询确认，再补单入账并通知订单继续。补单也要幂等，以渠道交易号做唯一键，补两次不能入两次账。
- **我方有、渠道无：**风险最高：我方以为收了钱，渠道却没有。转人工，多半要撤销订单。
- **金额不符：**按口径差异（两边算法不同，比如是否含手续费）或本金差异分别处理，本金差异转人工。
- **时间差不是真差异：**截止点前后的交易，一边记在今天、另一边记在明天，不算差异，放进等待队列，次日再比。
- **只追加不改：**处理动作写成追加的调整记录，原记录不动，留下完整痕迹。
- **自动与人工分工：**小额自动处理，超过阈值需要复核；同一根因造成的差异聚成一个案例，批量处理。
**举个例子。** 某天渠道账单有 4 笔，我方也有 4 笔，逐笔按渠道交易号对照。
1. **T1 两边都有、金额一致：**通过。
2. **T2 渠道有、我方无：**先向渠道查询确认确有这笔，再补单入账，订单继续往下走。
3. **T3 我方有、渠道无：**我方以为收了 80，渠道没有，转人工，多半撤销订单。
4. **T4 我方 100、渠道 90：**查原因：如果是手续费口径，按口径差异处理；如果是本金差异，转人工。
5. **23:59:58 的一笔：**我方记在今天，渠道记在明天，放进等待队列，次日再比。
**容易错。**
- **以为有回调就不用对账：**回调会丢、会乱序，对账是最后一道防线。
- **直接改原记录平账：**抹掉了证据，之后没法审计，应该追加调整记录。
- **把截止点附近的差异当错误：**它们是时间差，次日自然对上，当错误处理会制造假案例。
- **补单不做幂等：**重复补单就会重复入账，要以渠道交易号做唯一键。
**业务场景。** 回调服务发布故障两小时，漏了一批成功回调；次日对账出现一批「渠道有、我方无」，按同一根因聚成一个案例，批量查询后补单。
**系统设计。** [[links.tt-payment-reconciliation|支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）]]：追问「差异怎么分类和处置」；这里只讲两方，那里还要加上银行流水核对到账。
**可能问法。**
- 对账怎么做？ → 对账是拿独立来源的记录互相印证：每天把我方支付单与渠道账单按渠道交易号逐笔比对，找出渠道有我方无、我方有渠道无、金额不符三类差异。截止点前后的交易是时间差，不是真差异，放进等待队列次日再比。
- 渠道扣款了订单没更新怎么办？ → 渠道有、我方无：先向渠道查询确认，再补单入账并通知订单继续。补单要幂等，以渠道交易号做唯一键。回调会丢、会乱序，所以对账是最后一道防线。
- 对账差异怎么处理？ → 处理动作只追加调整记录，不改原记录。我方有、渠道无风险最高，转人工，多半要撤销订单；金额不符按口径差异或本金差异分别处理；小额自动处理，超阈值需复核。同一根因的差异聚成一个案例批量处理。
