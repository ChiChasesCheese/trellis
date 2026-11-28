---
id: hi-fix-gofundme-02-scope
node: fix.gofundme
type: qa
step: 2
---
## Q
**GoFundMe · 第 16:18 分 · 范围**｜复盘

面试官：「创建活动先不用管，我们假设活动已经在那里了。你接着说捐款的接口。」

你会怎么回答？

## A
**当时的回答。**
- **接口顺序：** 你先在白板上列了创建活动、更新活动的接口，之后才回到捐款接口。
- **反复回头：** 之后几次又回到活动相关的字段上。
**差在哪。**
- **时间花在划掉的东西上：** API 这一步只有几分钟，创建和编辑没有任何得分，捐款接口的契约被挤到后面。
- **没有明说「已经划掉」：** 面试官看不出是你没听见还是不认同；一句复述就能把这扇门关上。
**应该这样说。**
- **复述范围：** 「好，创建和编辑活动在范围外。我假设活动已经存在，接口里只出现 campaign_id。」
- **说出留下的：** 「所以接口只有三个：看活动页、捐款、查这一笔的结果。」
- **把时间花在得分处：** 「捐款是系统里最贵的写，我先把它的请求体和返回写清楚。」
- **留一个门：** 「如果您想回头看创建，说一声，我再补。」只说一次，说完就走。
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 274">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">API 板：划掉的写进角落，不再画</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /campaigns/{id}</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">看活动页：总额 · 最近 · 最大</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /donations</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">捐款：金额 · 令牌 · 重试键</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /donations/{id}</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">查这一笔的结果</text>
<line x1="8" y1="190" x2="332" y2="190" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<rect x="8" y="200" width="324" height="62" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="220" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">范围外：创建 / 编辑活动</text>
<text x="18" y="235" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">POST·PUT /campaigns 不画</text>
<text x="18" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">假设：活动已存在，只有 campaign_id</text>
</svg>
白板上：三个接口；划掉的内容只在角落写一行假设，不画字段。
**面试官可能接着问。**
- 活动的目标金额和截止日期放哪？ → 它们属于活动实体，在范围外。我只用 campaign_id 引用；捐款时校验活动还在进行，我把它当成读一个状态字段。
- 范围外的东西会不会影响设计？ → 只影响边界：捐款要先确认活动可收款，我在边界上画一个箭头就够。
**同类题。**
- **Ticketmaster：** 管理员建活动、建场馆不在范围内。
- **Uber：** 司机注册和审核不在范围内。
- **限时捐款网站：** 面试官划掉累计金额展示。
