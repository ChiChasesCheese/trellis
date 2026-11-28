---
id: hi-fix-bound-external-01-freshness-window
node: fix.bound-external
type: qa
step: 1
---
## Q
**用户能触发的外部调用 · 新鲜度窗口**｜补强

面试官：「用户每次打开转账详情页，你都去问支付平台最新状态吗？为什么？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说风险：** 「用户能触发的外部调用，没有上限就等于别人能控制我打向对方的流量。」
- **算一下：** 「10,000 笔 pending，每个页面每 2 秒刷新一次：10,000 ÷ 2 = 5,000 次/秒。对方慢 1 秒，同时在飞 5,000 × 1 = 5,000 个请求，我的线程池先满。」
- **三个设计：** 「读时同步调用，延迟绑在对方身上；读时调用加 TTL，到期那次读仍要等，同时到期的读一起出发；所以我选窗口加后台刷新。」
- **窗口放在行上：** 「交易行加 last_vendor_check_at。读本地行，超过 30 秒就排一个刷新任务，仍然返回 pending；读从不等外部。」
- **上限公式：** 「外部调用 ≤ pending 笔数 ÷ 窗口秒数。10,000 ÷ 30 ≈ 333 次/秒，不管用户怎么刷新。」
- **说出谁来刷新：** 「刷新由后台 worker 做，不是由用户的读做。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读请求里的外部调用，三种设计</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">① 读时同步调用</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">调用数 = 读的数量；延迟绑在对方身上</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对方慢 1 秒，你的读也慢 1 秒</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">② 读时调用，加 TTL 缓存</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">窗口内不调；到期的那次读仍要等对方</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同时到期的读一起出发</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">③ 窗口 + 后台刷新（选这个）</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读只读本地行；过期只入队</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每笔每窗口最多一次，读从不等外部</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 201">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同样 10,000 笔 pending，每秒打向外部</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">没有窗口</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10,000 笔 ÷ 2 秒（轮询）= 5,000 次/秒</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对方慢 1 秒：5,000 次/秒 × 1 秒 = 5,000 个在飞</text>
<rect x="8" y="93" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">30 秒窗口</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10,000 笔 ÷ 30 秒 ≈ 333 次/秒，是上限</text>
<rect x="8" y="145" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">再加全局 QPS 上限</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">取 50 次/秒；10,000 ÷ 50 = 200 秒一轮</text>
</svg>
白板上：三种设计一行一个，下面是三行数字。
**为什么这样说。** （约 1 分钟。）面试官要听到一个上限，而不是「加缓存」。强的回答把上限写成算式，并说明读不等外部；弱的回答是「实时查，超时就降级」。
**面试官可能接着问。**
- 30 秒怎么选？ → 假设：看对方状态变化的快慢和额度；窗口越短越新，调用上限越高；说出来，面试官给别的数就改。
- 为什么不直接加 TTL 缓存？ → TTL 缓存仍然让「到期的那次读」去等对方，并且同时到期的读会一起冲过去；窗口加后台刷新把这两件事都拿出了读路径。
- 页面怎么显示？ → 返回 status 和 last_checked_at，页面写「30 秒前确认，处理中」；用户知道数据有多旧。
**常见失分。**
- **只说「加缓存」：** 没有窗口、没有上限，读仍然会等外部。
- **让用户的读去刷新：** 外部变慢时，用户的读跟着变慢。
- **只给结论，没有数：** 「会很多」不是上限；5,000 次/秒和 333 次/秒差一个数量级。
