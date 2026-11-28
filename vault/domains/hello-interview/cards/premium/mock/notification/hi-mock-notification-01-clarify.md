---
id: hi-mock-notification-01-clarify
node: fix.notification-mock
type: qa
step: 1
---
## Q
**通知系统 · 第 1 步 · 开场与澄清**｜模拟面试

面试官：「今天设计一个通知系统，给一家大型消费平台用，推送、邮件、短信都要。你可以先问我任何想问的，边问边在白板上记。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给结论，再问：** 「我把它收成一件事：一个所有产品团队共用的发送服务，渠道是推送（push）、邮件（email）、短信（SMS）。我有一个判断先说出来，再问三类会改变设计的问题，用时不超过 90 秒。」
- **判断：两类流量：** 「这里有两类流量，差别比渠道还大。回执（transactional）：一次支付一条，要几秒内到。活动（campaign）：一次请求扇出到几百万人，几分钟到几小时发完都行。后面的隔离、限流、重试都围绕这两类。」
- **问：规模：** 「多少用户、每天多少条、活动峰值多大？」→ 面试官答：1 亿月活（MAU）、日均 5 亿条、活动峰值约每分钟 500 万条。我记下并写上单位：1 亿 MAU，5 亿条/天，500 万条**每分钟**。
- **问：延迟目标：** 「回执要多快，活动要多久发完？」→ 面试官答：您来定。我假设：回执 p99 在 5 秒内交给供应商；1,000 万人的活动 10 分钟内发完。
- **问：投递保证和退订：** 「可以重复吗？用户退订和偏好要尊重吗？」→ 面试官答：偶尔重复可以容忍，但同一张回执不能收两次；退订必须生效。我记下：至少一次加去重，不承诺恰好一次。
- **问：边界：** 「站内信、模板编辑器、活动人群圈选、A/B 实验，要做吗？」→ 面试官答：都不做；活动给你一个人群编号（audience_id），名单由别的系统产出。我记下：线外四项，不画、不回头。
- **收尾：** 「这六行写在白板角落。接下来我讲功能需求和非功能需求。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 350">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">角落六行：先写数，再写决定</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">两类流量，差别比渠道大</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">回执：一人一条，几秒内到</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">活动：一次扇出几百万人，分钟到小时</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">规模（给定，带单位）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 亿 MAU · 5 亿条/天</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">活动峰值 500 万条/分钟</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">目标（我的假设）</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">回执 p99 ≤ 5 秒交给供应商</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1,000 万人的活动 ≤ 10 分钟发完</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">保证</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">至少一次 + 去重；受理后不丢</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">退订必须生效</text>
<rect x="8" y="294" width="324" height="44" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="312.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">线外：站内信 · 模板编辑器</text>
<text x="18" y="328.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">人群圈选 · A/B 实验</text>
</svg>
白板上新增：角落六行，不画图。
**为什么这样说。** （约 2 分钟，累计第 2 分钟。）面试官看你能不能把开放的题目收成可做的范围，并且问的每个问题都会改变设计：两类流量决定隔离，延迟目标决定要不要队列，投递保证决定重试和去重，退订决定发送前要查什么。强的回答第一句话就给判断，再问问题；弱的回答是把题目复述一遍，等面试官来追问。
**面试官可能接着问。**
- 为什么不先问渠道的细节，比如苹果和谷歌的推送协议？ → 渠道细节只改变适配器，不改变核心设计。两类流量和投递保证会改变队列、限流和去重，所以先问这些。
- 恰好一次（exactly-once）为什么不做？ → 供应商不提供事务，我们调用供应商和记录结果是两件事，中间崩溃就可能多发一次。我给的是至少一次加去重，重复的窗口很小，我会在后面讲清楚。
- 谁给活动的名单？ → 范围外。我只收 audience_id 和模板，负责把它展开成逐人的消息并发出去。
**常见失分。**
- **复述题目当作提问：** 他当时先把题目复述了一遍，面试官追问「streaming 是什么意思」才讲到两类流量。
- **不分两类流量：** 回执和活动混在一条队列里，后面就讲不清为什么回执不会排在活动后面。
- **不问投递保证、退订、延迟目标：** 这三项直接决定设计，面试官会记成没问。
- **把 1 亿写成 100 万：** 白板上写了「1mil users/month」，差 100 倍。
