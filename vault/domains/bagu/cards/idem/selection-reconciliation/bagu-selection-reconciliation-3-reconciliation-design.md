---
id: bagu-selection-reconciliation-3-reconciliation-design
node: a.idem.selection-reconciliation
type: qa
step: 3
---
## Q
**对账（Reconciliation）· 什么是对账，怎么设计**｜必会

面试官：「你们的支付系统有订单、支付流水，渠道每天还会发账单文件。对账具体怎么做？数据量很大时怎么设计？」

## A
**基本回答。** 对账是拿几份独立产生的记录互相印证：我方订单、我方支付流水、渠道账单，按交易号逐笔比对，找出少了、多了、金额不同的。流程是按业务日取数、统一口径、分层匹配、差异归类、自动处置或转人工。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="8" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我方订单</text>
<line x1="58" y1="36" x2="58" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,52.0 54.8,45.0 61.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="8" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我方支付流水</text>
<line x1="170" y1="36" x2="170" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,52.0 166.8,45.0 173.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="8" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道账单</text>
<line x1="282" y1="36" x2="282" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,52.0 278.8,45.0 285.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="52" width="324" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="66.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">统一口径</text>
<text x="170" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">金额转分 · 同一时区 · 参考号去空格</text>
<line x1="170" y1="88" x2="170" y2="97" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,104.0 166.8,97.0 173.2,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="104" width="324" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第一轮：交易号 + 金额 + 币种精确匹配</text>
<text x="170" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每天 3000 万笔，约命中 99.8%</text>
<line x1="170" y1="140" x2="170" y2="149" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,156.0 166.8,149.0 173.2,149.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="156" width="324" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="170.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">剩约 6 万笔</text>
<text x="170" y="185.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">商户单号 + 时间窗口 + 容差放宽</text>
<line x1="170" y1="192" x2="170" y2="201" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,208.0 166.8,201.0 173.2,201.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="208" width="324" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="222.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">差异归类</text>
<text x="170" y="237.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我方缺 · 渠道缺 · 金额不符 · 重复 · 状态不符</text>
<text x="8" y="266" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">然后自动处置，处理不了的转人工</text>
<text x="8" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按渠道、币种、业务日分区，各区独立匹配、重跑</text>
</svg>
三份记录先统一口径，再分层匹配：第一轮精确匹配吃掉绝大多数，剩下的放宽条件再匹配，仍对不上的归类处置。
**举个例子。** 一天 3000 万笔，三份记录拉齐后：
1. **统一口径：** 一笔 `12.50` 元换成 1250 分，渠道的北京时间和我方的 UTC 时间都转成同一时区，参考号两端的空格去掉。
2. **第一轮：** 用交易号 + 金额 + 币种精确匹配，约 99.8% 命中，也就是约 2994 万笔对平。
3. **剩下约 6 万笔：** 3000 万 × 0.2% = 6 万。用商户单号、时间窗口、容差放宽再匹配，又对上一批。
4. **仍对不上的归类：** 一笔渠道有、我方无，归「我方缺」，先向渠道查询确认，再补记支付并通知订单继续履约；一笔我方有、渠道无，归「渠道缺」，风险最高，转人工；零点前后差几秒的，放进等待队列，次日再对。
**容易错。**
- **不统一口径就开始比：** 金额单位、时区、空格不同，会制造大量假差异。
- **只比总金额：** 一多一少互相抵消，必须逐笔比对。
- **把截止点附近的差异当成真差异：** 先放进等待队列次日再对。
- **发现差异直接忽略：** 差异要归类处置，渠道有、我方无尤其要追查。
