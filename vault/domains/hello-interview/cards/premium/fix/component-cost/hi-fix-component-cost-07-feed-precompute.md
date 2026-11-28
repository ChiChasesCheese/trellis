---
id: hi-fix-component-cost-07-feed-precompute
node: fix.component-cost
type: qa
step: 7
---
## Q
**News Feed · 加组件：预计算的 feed**｜补强

面试官：「首页要快：一打开就能看到关注的人最近的帖子。你怎么做？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说读时拼：** 「读时去查关注的每个人的帖再合并排序；关注 500 人就是 500 次查询，太慢。」
- **职责：** 「我加每人一个预计算的 feed 列表：发帖时把帖子 id 推到每个粉丝的列表里，首页只读一个列表。」
- **新问题：** 「写放大：普通用户 200 个粉丝，写 200 次；大 V 有 1,000 万粉丝，写 1,000 万次，按每秒 10 万次写要 100 秒，而且大多是写给不看的人。」
- **处理：** 「混合：普通用户发帖时扩散；大 V 不扩散，读时把关注的大 V 的新帖合并进来。」
- **说出阈值：** 「粉丝数超过某个阈值，比如 10 万，就算大 V；阈值是可调的参数。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 229">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">预计算 feed 的写放大</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">普通用户发帖</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">200 个粉丝 → 写 200 个列表</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每秒几次，没有压力</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">大 V 发帖</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1,000 万粉丝 → 写 1,000 万个列表</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每秒 10 万次写也要 100 秒</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">混合方案</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">大 V 不扩散；读时把大 V 的新帖合并进来</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">普通人写时扩散，大 V 读时合并</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我要写在组件旁边的四行</text>
<rect x="8" y="26" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">加：每人一个预计算的 feed 列表</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">为了：打开首页只读一个列表</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新问题：大 V 发一帖，写放大一千万倍</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">处理：大 V 不扩散，读时合并</text>
</svg>
白板上：三种做法的写放大；旁边是组件便签。
**为什么这样说。** （约 1 分钟。）面试官看你有没有发现「读快」是拿写换来的。强的回答立刻算出大 V 的写放大，并给出混合方案。弱的回答是「预计算，读很快」，没有提发帖那一侧。
**面试官可能接着问。**
- 用户取关或删帖？ → 列表里只存帖子 id，读时再过滤掉已删除和已取关的。
- 不活跃用户的列表也要维护吗？ → 只为最近活跃的用户预计算；很久没登录的，回来时现拼一次。
- 列表要多长？ → 只留最近几百条，超出的按时间裁掉；翻到更早的才走读时拼。
**常见失分。**
- **只讲读那一侧：** 预计算省了读，写的账没算。
- **不提大 V：** 这是这个组件最大的新问题。
- **阈值写死：** 要说它是可调的参数。
