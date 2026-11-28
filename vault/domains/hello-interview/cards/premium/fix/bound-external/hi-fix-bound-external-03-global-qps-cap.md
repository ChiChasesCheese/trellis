---
id: hi-fix-bound-external-03-global-qps-cap
node: fix.bound-external
type: qa
step: 3
---
## Q
**用户能触发的外部调用 · 全局 QPS 上限**｜补强

面试官：「有一万笔 pending 的窗口同时到期，worker 一起去问支付平台，会怎样？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说额度：** 「支付平台给状态查询的额度我假设是 100 次/秒（下单是另一个接口，另算），要和对方确认；我自己的上限取 50 次/秒，留一半余量应付突发。」
- **上限在 worker 这一侧：** 「所有 worker 共用一个令牌桶，每秒 50 个令牌；拿不到令牌的任务等下一秒。实现上可以是 Redis 里一个按秒计数的键，或者固定 5 个 worker，每个每秒最多 10 次。」
- **一万笔同时到期：** 「10,000 ÷ 50 = 200 秒一轮，最老的先刷新；这 200 秒里用户读到的是本地 pending 加 last_checked_at，读不受影响。」
- **对方变慢或报错：** 「429、5xx、超时都指数退避加抖动；连续失败就熔断 30 秒。重试也要先拿令牌，不能绕过上限。」
- **预留给扫描：** 「50 次/秒里，每日扫描最多占 10 次/秒，不会被用户刷新挤掉。」
- **监控：** 「队列里最老任务等了多久，超过 5 分钟告警。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">队列里的 10,000 个刷新任务</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 · 按 last_vendor_check_at 最老优先</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10,000 个任务</text>
<polyline points="170,70 170,104" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,104 166.8,97 173.2,97" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="91" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">令牌桶 50 个/秒</text>
<rect x="8" y="104" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker 们共用一个桶</text>
<text x="170" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拿不到令牌就等下一秒</text>
<polyline points="170,148 170,182" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,182 166.8,175 173.2,175" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="169" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≤ 50 次/秒</text>
<rect x="8" y="182" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="200.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付平台</text>
<text x="170" y="215.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10,000 ÷ 50 = 200 秒一轮</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户的读不在这条链上：照常 1 次主键读</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">外部变慢或报错时</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">429 / 5xx / 超时</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">指数退避，加随机抖动</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重试也要占令牌，不能绕过上限</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">连续失败：熔断</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">暂停刷新 30 秒，队列照常堆积</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">用户读仍是本地 pending</text>
<rect x="8" y="160" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">队列太深：告警</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最老任务等了多久，比深度更要紧</text>
</svg>
白板上：队列到令牌桶到支付平台的一条线，另一侧写用户读不在这条线上。
**为什么这样说。** （约 1 分钟。）面试官要确认你的系统不会成为对方的压力源。强的回答说出额度、自己的上限、一轮要多久；弱的回答是「加个限流」。
**面试官可能接着问。**
- 多个 worker 各自限流会怎样？ → 每个实例各算各的，总额放大为实例数倍；所以要共享一个计数器。
- 为什么上限设 50，不是 100？ → 留余量给突发和我们看不到的其他调用方；顶到额度，一次突发就会被 429。重试和扫描都在这 50 次/秒以内。
- 对方说不接受轮询呢？ → 那就改用 webhook 加每日扫描；轮询只是用户读的补充，不是唯一的路径。
**常见失分。**
- **只在每个实例里限流：** 总额度被放大为实例数倍。
- **重试不占额度：** 一次故障后，重试流量把上限冲破。
- **把限流放在读路径上：** 用户的读就被限住了；限流应该只约束后台刷新。
