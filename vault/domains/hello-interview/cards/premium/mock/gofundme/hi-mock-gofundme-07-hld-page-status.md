---
id: hi-mock-gofundme-07-hld-page-status
node: fix.gofundme-mock
type: qa
step: 7
---
## Q
**GoFundMe · 第 7 步 · 高层设计（二）：活动页与支付结果**｜模拟面试

面试官：「捐款这条流程清楚了。另外两条需求怎么放进同一张图？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **不加新组件：** 「活动页和结果查询都复用应用服务和数据库。新组件我只在数字逼我的时候加。」
- **看支付结果：** 「GET /donations/{donation_id}，按主键查一行，返回 status。前端每 2 秒轮询，Pending 显示『处理中，请勿重复付款』，拿到终态就停。最多轮询 30 秒，之后告诉用户结果出来会在『我的捐款』里看到。」
- **最坏的轮询量：** 「30 秒 ÷ 2 秒 = 15 次一笔，150 笔/秒 × 15 = 2,250 次主键读/秒；绝大多数一次就是终态，实际远小于这个。」
- **看活动页：** 「GET /campaigns/{id}，先用最直接的办法：已募金额是 SUM(amount) WHERE campaign_id 且 status=Success；最近 100 笔是按 created_at 倒序 LIMIT 100；最大 10 笔是按 amount 倒序 LIMIT 10，都带 Success 过滤，各有一个索引。」
- **Pending 不算：** 「Pending 之后可能失败，所以已募金额和两个列表只看 Success。」
- **标记这是基线：** 「我先把它当基线，现在的规模够用。但一个爆红活动每次浏览都要跑这三个查询，这是下一步深入要解决的，我先记下。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 414">
<rect x="12" y="8" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器 · App</text>
<text x="82" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">checkout_attempt_id</text>
<rect x="188" y="8" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="258" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP 前端组件</text>
<text x="258" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">收卡号 · 换令牌</text>
<polyline points="152,22 188,22" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="188,22 181.0,25.2 181.0,18.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="188,40 152,40" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="152,40 159.0,36.8 159.0,43.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">卡号</text>
<text x="170" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌</text>
<polyline points="140,52 140,150" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="140,150 136.8,143.0 143.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="140,52 143.2,59.0 136.8,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="148" y="82" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /donations</text>
<text x="148" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET /donations/{id}</text>
<text x="148" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET /campaigns/{id}</text>
<rect x="12" y="150" width="316" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 + 应用服务</text>
<text x="170" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无状态 · 多实例 · 三类服务合一</text>
<path d="M8,242 a89,6 0 0 1 178,0 v76 a89,6 0 0 1 -178,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M8,242 a89,6 0 0 0 178,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="97" y="260" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库 Postgres</text>
<rect x="16" y="274" width="162" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="97" y="289" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">donations</text>
<rect x="16" y="300" width="162" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="97" y="315" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">campaigns</text>
<polyline points="96,194 96,236" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="96,236 92.8,229.0 99.2,229.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="96,194 99.2,201.0 92.8,201.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="102" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT / UPDATE</text>
<rect x="196" y="236" width="132" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="262" y="254.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付服务商 PSP</text>
<text x="262" y="269.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ref = donation_id</text>
<polyline points="262,194 262,236" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="262,236 258.8,229.0 265.2,229.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="268" y="220" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">charge</text>
<text x="8" y="348" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">活动页三项先用索引查询：</text>
<text x="8" y="366" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SUM(amount) WHERE Success</text>
<text x="8" y="384" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ORDER BY created_at DESC LIMIT 100</text>
<text x="8" y="402" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ORDER BY amount DESC LIMIT 10</text>
</svg>
白板上新增：两条读路径 GET /donations/{id} 和 GET /campaigns/{id}，都走应用服务读数据库；底部写着三个查询。
**为什么这样说。** （约 5 分钟，累计第 29 分钟。）面试官看你能不能用最少的组件把剩下的功能放进来，并且诚实地标出这是基线。强的回答说清楚 Pending 不算入金额，并主动指出活动页的三个查询对爆红活动不够。弱的回答是在这里就堆 Redis、分片、缓存，还没说为什么。
**面试官可能接着问。**
- 为什么用轮询而不是推送？ → 最坏 2,250 次/秒的主键读，对数据库很轻；推送要维护长连接，现在不值得。
- 这三个查询要什么索引？ → (campaign_id, status, created_at) 和 (campaign_id, status, amount)，外加 donation_id 主键；SUM 在没有派生值之前要扫这个活动所有 Success 行，这就是问题所在。
- 轮询 30 秒还是 Pending 怎么办？ → 前端停止轮询，显示『结果确认中』；对账任务会把它收尾，用户稍后刷新就能看到终态。
**常见失分。**
- **把 Pending 算进金额：** 之后失败的捐款会让总额偏大，面试官会直接追问。
- **这里就堆缓存：** 没说清要解决什么，只是在名字上加分。
- **不标记基线的问题：** 面试官发现 SUM 要扫表时，会觉得你没看到。
