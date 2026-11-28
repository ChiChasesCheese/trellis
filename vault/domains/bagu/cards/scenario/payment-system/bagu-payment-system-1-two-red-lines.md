---
id: bagu-payment-system-1-two-red-lines
node: a.scenario.payment-system
type: qa
step: 1
---
## Q
**支付系统设计 · 开场先守住哪两条红线**｜必会

面试官：「设计一个接入第三方渠道的收款系统，要保证用户不被重复扣款，订单也不能在没收到钱时标记已支付。你怎么设计？」

## A
**基本回答。** 开场先定两条红线：同一笔业务只扣一次钱；渠道没确认收到钱，订单就不是已支付。支付出错只有这两个方向：多扣，或没收到钱却发了货。重复躲不掉（客户端重试、服务超时重发、渠道重复回调），通信只能做到至少一次，叠加幂等才等于恰好一次。手段：每笔业务一个唯一业务单号，所有重试复用它做唯一键去重，调渠道时带商户请求号让渠道也去重；订单和支付单状态只前进，转换用条件更新 `WHERE status=旧状态`，影响行数 1 才算成功；以渠道确认为准，请求超时只是「结果未知」（渠道可能已扣款），要查询而不是当失败重发；每天逐笔对账是最后一道防线，因为回调会丢、查询有时间窗口。取舍：宁可到账晚几分钟，也不能记错账。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<rect x="4" y="24" width="130" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="69.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红线 1</text>
<text x="69.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一笔业务只扣一次</text>
<rect x="4" y="120" width="130" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="69.0" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红线 2</text>
<text x="69.0" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没确认就不是已付</text>
<rect x="176" y="14" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">唯一业务单号去重</text>
<rect x="176" y="50" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">状态只前进，条件更新</text>
<rect x="176" y="106" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">以渠道确认为准</text>
<rect x="176" y="142" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="160.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超时 = 结果未知，去查</text>
<line x1="134" y1="46" x2="170.48512981989165" y2="30.363515791475006" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,28.0 171.7,33.1 169.3,27.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="134" y1="46" x2="170.48512981989165" y2="61.63648420852499" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,64.0 169.3,64.4 171.7,58.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="134" y1="142" x2="170.68501078831906" y2="122.78404196802335" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,120.0 172.1,125.4 169.3,120.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="134" y1="142" x2="170.3079002116969" y2="154.10263340389898" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,156.0 169.4,156.9 171.3,151.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="196" width="332" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="216.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">兜底：每天和渠道账单对账</text>
</svg>
左边是两条红线，右边是守住它们的手段，最下面的对账是兜底。
**举个例子。** 用户充值 100 币，业务单号 R-1001：第一次创建支付单 P1（INIT）并带 R-1001 调渠道；连点两次撞唯一键，直接返回 P1。渠道超时则 P1 停在 PROCESSING，用 R-1001 查询，查到成功才推进到 SUCCESS、订单变 PAID。回调和查询都失败时，次日对账发现「渠道有、我方无」再补单入账。
**容易错。**
- **以为有幂等就够：** 幂等只管重复；「没收到钱却标已付」要靠渠道确认和状态机挡，漏网的靠对账。
