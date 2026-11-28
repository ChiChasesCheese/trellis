---
id: hi-fix-notification-07-decision-first
node: fix.notification
type: qa
step: 7
---
## Q
**通知系统 · 先说决定，再说原因**｜复盘

面试官：「产品团队的请求超时，他们重试了。怎么保证用户不收到两封支付回执？」（21:19）

你会怎么回答？第一句话说什么？

## A
**当时的回答。**
- **先把问题念一遍：** 「so a product team request times out and they retry how to make sure the user doesn't give to a payment receipt okay so this one makes」（21:52）。
- **说了「让我想一下，别打断」：** 「let me think a bit please don't interrupt me」（22:33）。
- **原因和过程在前，决定在最后：** 讲了重试、讲了要幂等、讲了锁，决定（唯一约束）在提示之后才出现，约 4 分钟。
- **不是这一处：** 同样的复述还出现在 15:52（「let me repeat your question so what happens when one of those providers is slow or down」）、19:14、26:26、31:25。至少 6 处。
**差在哪。**
- **复述不是答案：** 面试官刚问完，复述一遍只是占时间；每次 15 到 60 秒，一场 45 分钟的面试，这样的时间加起来要几分钟。
- **面试官分不清你是不会，还是在铺垫：** 先讲背景再给结论，在没听到结论之前，面试官没有办法判断你是否知道。
- **Senior 要领着对话走：** 先给结论，面试官可以马上点头，或者直接追问下一层；先给过程，他只能等。
**应该这样说。**
- **三格，每次都是这个顺序：** 「结论 → 原因 → 代价或边界。」
- **这一题：** 「用数据库的唯一约束，`notification_id` 是主键，插入如果已存在就什么也不做。原因：同时到的两个重试，数据库原子地让一个成功、一个失败，0 行就是重复，不需要锁，也不需要先查。代价：唯一索引会一直长，去重表只留 7 天。」
- **供应商挂了：** 「每个供应商一个独立队列，失败进重试 topic，带指数退避和抖动，超次数进死信队列，连续失败熔断。原因：Apple 挂了，邮件和短信不能被它拖住。」
- **回执不等活动：** 「两个 topic、两组 worker、两个令牌桶，回执有保底配额。原因：同一个队列里 1,000 万条的活动会让回执排在后面几分钟。」
- **需要想的时候：** 「我先给默认答案，再检查它：……」，不要沉默，也不要复述题目。
- **说完停：** 三格说完就停，让面试官决定追问哪一格。
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 186">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每次回答：三格，先写第一格</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">1 结论（第一句，不复述题目）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">唯一约束，主键是 notification_id</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">2 原因（一个机制或一个数）</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT 0 行 = 重复，数据库原子裁决</text>
<rect x="8" y="130" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">3 代价或不这样做的时候</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">唯一索引会长，去重表只留 7 天</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 164">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个问题，到答案要多久</text>
<text x="8" y="42" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">当时 21:19 提问</text>
<rect x="8" y="48" width="324" height="18" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">到 25:32 才有答案，约 4 分钟（提示后）</text>
<text x="8" y="88" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">改后</text>
<rect x="8" y="94" width="19" height="18" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="34" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第一句约 15 秒</text>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">转写里至少 6 处先复述问题再答</text>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">复述一句 15–60 秒</text>
</svg>
白板上：三格模板，第一格先写；右边是同一道题改前改后的用时。
**为什么这样说。** （约 15 秒。）面试官每一个问题都在判断你是否马上知道。强的回答第一句就是结论；弱的回答第一句是题目。面试官的时间是固定的，先给结论的人，能多讲两个深入点。
**面试官可能接着问。**
- 我答案不确定怎么办？ → 先说你的默认答案，再说你在哪一点上不确定：「我倾向唯一约束；不确定的是去重表要保留多久，我先按 7 天。」
- 问题很大，怎么给一句结论？ → 先给结构：「分三块：入口、队列、存储，先讲队列。」然后第一块给结论。
- 面试官在追问同一个问题第二次？ → 他没有听到想要的东西。直接问：「您想听的是状态存在哪里，还是写入的顺序？」
**常见失分。**
- **先复述问题：** 浪费时间，也显得没有答案。
- **沉默超过 10 秒：** 说出你的默认答案。
- **结论放在最后：** 面试官在原因里迷路。
**同类题。**
- **先答被问的竞态：** 同一个纪律，见「先答被问的那个竞态」。
