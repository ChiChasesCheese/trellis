---
id: bagu-timeout-unknown-5-limit-fallback
node: a.idem.timeout-unknown
type: qa
step: 4
---
## Q
**超时未知 · 重试上限与对账兜底**｜必会

面试官：「重试为什么不能无限重？最后靠什么兜底？」

## A
**基本回答。** 重试要有次数和间隔上限，用指数退避，超过后进入人工或对账流程。最后一道防线是日终对账：和渠道账单逐笔比对，补单、冲正。
**一句话记住。** 重试像敲一扇没人应的门：敲得越来越稀、最多敲几次，敲完就留张字条（对账）。一直不停地猛敲，只会把本来就虚弱的人吵垮。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重试间隔指数增长，有上限</text>
<rect x="26" y="108" width="36" height="8" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1秒</text>
<rect x="76" y="100" width="36" height="16" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="94" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2秒</text>
<rect x="126" y="84" width="36" height="32" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="144" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4秒</text>
<rect x="176" y="60" width="36" height="56" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="194" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8秒</text>
<rect x="226" y="60" width="36" height="56" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="244" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上限</text>
<rect x="276" y="60" width="36" height="56" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="294" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上限</text>
<line x1="18" y1="116" x2="332" y2="116" stroke-width="1.2" stroke="currentColor"/>
<line x1="18" y1="60" x2="332" y2="60" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每次再加一点随机抖动，让客户端错开</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">次数用完 → 人工或日终对账</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">我方有渠道无、渠道有我方无、金额不一致</text>
</svg>
每一根柱子是一次重试前的等待时间：1 秒、2 秒、4 秒、8 秒，成倍增长，到了上限就不再变长。次数用完就不再自动重试，转人工或对账。
**讲明白。**
- **无限重试会雪崩：**依赖故障时，成千上万的客户端都在不停重试，流量被放大，本来只是慢的依赖被彻底打垮，把故障变成雪崩。
- **指数退避：**每次重试的等待时间按倍数增长，如 1 秒、2 秒、4 秒、8 秒，并设上限，再加随机抖动让多个客户端错开。目的是给故障的依赖恢复时间，避免大量客户端同步重试形成流量尖峰。
- **重试几次看路径：**用户同步请求里重试 1 到 2 次，并受总截止时间约束，用户等不起。异步补偿用指数退避，从几秒到几小时，次数有上限。
- **超限转对账或人工：**重试次数用完之后不再自动重试，进入对账或人工流程。
- **悬挂单据扫描：**定期扫描长时间停留在中间状态的单据，主动查询并推进，或者回滚。
- **对账是最后一道防线：**日终和渠道账单逐笔比对，找出三类差异：我方有渠道无、渠道有我方无、金额不一致。按请求号补单或冲正，差异记录进入工单。它覆盖了重试、查询都失败的情况。
- **要看哪些指标：**中间状态单据的数量、补偿次数、对账差异率。
**举个例子。** 渠道故障两个小时，订单 O1 扣款超时：
1. **退避重试：**按 1 秒、2 秒、4 秒、8 秒的间隔查询并重试，间隔不超过上限。
2. **渠道仍不可用：**次数用完，订单转入对账队列，不再自动重试。
3. **渠道恢复后：**次日账单里出现这笔「渠道有我方无」的记录，按请求号补单。
4. **反例：**如果无限重试，故障期间每个客户端都在高频请求，渠道恢复时更容易再次被打垮。
**容易错。**
- **以为多重试几次总能成功：**依赖故障时，重试会放大流量，雪崩只会更严重。
- **固定间隔重试：**所有客户端同时重试，形成尖峰，要指数退避加抖动。
- **以为重试和查询都做了就不用对账：**两者都失败的情况只有对账能兜住。
**业务场景。** 渠道故障两小时，重试到上限后订单转入对账队列；渠道恢复后次日账单里出现这笔，按请求号补单。
**系统设计。** [[links.tt-payment-reconciliation|支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）]]：面试官问「自动流程之外你还有什么兜底」，答三方对账与中间状态扫描。
**相关题。** 练习题 task-scheduler
**可能问法。**
- 重试几次合适？ → 看路径。用户同步请求里重试 1 到 2 次，并受总截止时间约束。异步补偿用指数退避，从几秒到几小时，次数有上限，超过进入对账或人工。无限重试在依赖故障时会放大流量，把故障打成雪崩。
- 对账怎么兜底？ → 日终和渠道账单逐笔比对，找出三类差异：我方有渠道无、渠道有我方无、金额不一致。按请求号补单或冲正，差异记录进入工单。它覆盖了重试、查询都失败的情况，是最后一道防线。
- 指数退避是什么？ → 每次重试的等待时间按倍数增长，如 1 秒、2 秒、4 秒、8 秒，并设上限，再加随机抖动让多个客户端错开。目的是给故障的依赖恢复时间，避免大量客户端同步重试形成流量尖峰。
