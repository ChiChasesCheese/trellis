---
id: hi-fix-scope-math-01-restate-scope
node: fix.scope-math
type: qa
step: 1
---
## Q
**GoFundMe · 范围被划掉之后**｜补强

面试官：「创建活动先不用管，我们假设活动已经在那里了，你接着往下说。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先复述一句：** 「好，创建和编辑活动在范围外。」让面试官听见你收到了。
- **写下一个假设：** 「我假设活动已经存在，接口里只有 campaign_id。」在白板角落写一行，不画字段。
- **说出留下什么：** 「所以接口只有三个：看活动页、捐款、查这一笔的结果。」
- **转身做下一件事：** 「我先写捐款接口，它是系统里最贵的写。」说完就动笔，不再回头。
- **面试官主动问起再回来：** 没人问，这件事就不再出现；问了，再用一两句补上。
- **每个步骤先报时间：** 「API 我用三分钟」。划掉的部分没有得分，时间要给还在得分的部分。
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 257">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">被划掉之后：三句话，然后转身</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 复述</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「创建和编辑活动在范围外。」</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">说出口，让面试官听见你收到了</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 写下假设</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「我假设活动已存在，只有 campaign_id。」</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">白板角落一行字，不画字段</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 转身</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「所以接口三个，先写捐款。」</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">直接开始下一件事，不再回头</text>
<text x="8" y="237" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">面试官主动问起，再回来；否则不再提</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 229">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个动作，三种场景</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Uber：司机注册不用管</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「我假设司机已通过审核、已上线。」</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">接口只剩：叫车、匹配、位置</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Ticketmaster：管理员建活动</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「我假设活动和座位已经建好。」</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">接口只剩：查座位、占座、付款</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">限时捐款：不展示累计金额</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「我不画计数器，最后一分钟再提。」</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">接口只剩：捐款、查结果</text>
</svg>
白板上：三句话的顺序，以及同一个动作在三种场景里的说法。
**为什么这样说。** （约 20 秒。）面试官划掉范围，是在帮你省时间，也在看你会不会听。强的回答用一句复述加一句假设关上这扇门，立刻去做得分的事。弱的回答是点头之后继续画被划掉的部分，或者反复确认「那创建真的不用吗」。
**面试官可能接着问。**
- 如果划掉的东西其实会影响设计呢？ → 我只在边界上提一次：「捐款要先确认活动在进行，我把它当成读一个状态字段。」不展开，也不画。
- 要不要把划掉的东西写在白板上？ → 只写一行假设，放在角落。它的作用是让面试官看到你的边界，不是让你继续画它。
- 面试官说「你可以自己决定要不要做」呢？ → 先问自己：它在不在得分的核心路径上。不在，就说「我先把核心路径做完，有时间再回来」，然后真的只在最后回来。
**常见失分。**
- **接着画被划掉的部分：** 时间花在没有得分的地方，核心接口被挤到后面。
- **没有说出口：** 点头不动笔，面试官分不清你是同意还是没听见。
- **一直回头确认：** 每次回头都在消耗面试官的耐心和你的时间。
