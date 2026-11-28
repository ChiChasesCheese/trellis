---
id: bagu-live-comment-5-moderation
node: a.scenario.live-comment
type: qa
step: 5
---
## Q
**内容审核与限流防刷 · 放在链路的哪里**｜追问

面试官：「评论要做内容审核，还要防止刷屏，这些放在发评论的哪一步？」

## A
**基本回答。** 审核分两层：先发后审保证实时，同步层必须毫秒级。同步轻量层：敏感词和黑名单，命中就拦截或仅自己可见；用字典树或 AC 自动机一次扫描匹配多个词，匹配前先归一化（变体、谐音、符号间隔），词库支持热更新。异步深度层：模型和人工审核，不阻塞发送，结果出来后撤回，并推送通知客户端删除已展示的评论（只删数据库不够）。限流防刷：按用户、设备、IP、房间多维度（单一维度易绕过），令牌桶或滑动窗口在 Redis 里用 Lua 实现；相同内容去重，新账号和低信用账号降权；违规者影子封禁（自己看得到、别人看不到），拦截后明确告知反而让他换词。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<rect x="8" y="24" width="64" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发评论</text>
<line x1="72" y1="44" x2="79.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86,44 79.0,47.2 79.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="86" y="24" width="112" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="142" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同步初筛</text>
<text x="142" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">敏感词、黑名单</text>
<line x1="198" y1="44" x2="205.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="212,44 205.0,47.2 205.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="212" y="24" width="120" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">限流去重</text>
<text x="272" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按用户设备 IP</text>
<line x1="142" y1="64" x2="142.0" y2="85.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="142,92 138.8,85.0 145.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="86" y="92" width="112" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发出：MQ 与推送</text>
<line x1="198" y1="110" x2="205.0" y2="110.0" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="212,110 205.0,113.2 205.0,106.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="212" y="92" width="120" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">异步审核</text>
<text x="272" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型、人工</text>
<line x1="272" y1="128" x2="272.0" y2="145.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="272,152 268.8,145.0 275.2,145.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="212" y="152" width="120" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">违规：撤回</text>
<text x="272" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知客户端删除</text>
<text x="150" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">毫秒级</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中同步层：</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">拦截或仅自己可见</text>
</svg>
评论先过毫秒级的同步初筛和限流，通过后马上发出；深度审核在后面异步做，发现违规再撤回。
**举个例子。** 恶意账号用脚本在热门直播间每秒发几十条广告：按用户限流到每秒 2 条，相同内容去重，通过的几条里含广告词的被敏感词拦截（发送者看到「仅自己可见」），漏网的由模型和人工事后复核，确认违规后撤回并通知客户端删除，房间弹幕恢复正常。
**容易错。**
- **只做异步审核：** 违规内容在审出来前已被大量观众看到，同步初筛必须先挡明显的。
- **所有审核都同步做：** 模型和人工太慢，拖住发评论。
