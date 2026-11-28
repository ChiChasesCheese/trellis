---
id: hi-fix-bound-external-04-order-tracking
node: fix.bound-external
type: qa
step: 4
---
## Q
**用户能触发的外部调用 · 订单物流**｜补强

面试官：「订单详情页要显示物流的最新状态，数据在承运商的 API 里，每家承运商限 20 次/秒。用户一刷新就去查吗？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **同一条规则：** 「读本地的 shipments 行，上面有 status 和 last_carrier_check_at；超过窗口，排一个刷新，读仍然返回本地状态。」
- **窗口按对象的变化快慢定：** 「在途包裹状态几小时才变一次，我取 5 分钟；已签收、已退回是终态，不再刷新。」
- **键是运单：** 「刷新键是 shipment_id，不是用户。一个爆款订单被 10,000 个人看，也只有每 5 分钟一次，约 0.003 次/秒。」
- **额度按承运商分开：** 「每家承运商一个队列和一个令牌桶。读 100 万次/天 ÷ 86,400 ≈ 12 次/秒，峰值按 3 倍约 35 次/秒；最坏情况是每次读都过期、都要调用，假设 6 家承运商、流量平均分，每家约 6 次/秒，低于 20 次/秒的额度。」
- **一家变慢不拖累别家：** 「分队列、分令牌桶，所以 A 家超时，B 家的刷新照常。」
- **能订阅就订阅：** 「承运商如果提供轨迹推送，就用推送为主、扫描兜底；轮询只是补充。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">订单详情页读物流：键是运单</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">键与窗口</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">键 = shipment_id；窗口 5 分钟</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已签收 / 退回是终态，不再刷新</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">上限（每家承运商分开）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读峰值 35 次/秒，分给 6 家 ≈ 6 次/秒</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每家额度 20 次/秒，够用</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">爆款运单被 10,000 人看</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">仍然 1 次 / 5 分钟 ≈ 0.003 次/秒</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">键是运单，不是看的人</text>
</svg>
白板上：键和窗口、按承运商的上限、爆款运单三行。
**为什么这样说。** （约 1 分钟。）面试官在看你是否把同一条规则搬到新题上，并且数字重新算。强的回答每个数字都用单位，并找出键；弱的回答复述转账题的措辞，却没换数字。
**面试官可能接着问。**
- 用户刚下单，还没有任何轨迹呢？ → 状态是「待揽收」，同样走窗口；这一类可以用更长的窗口，例如 30 分钟。
- 承运商接口挂了呢？ → 熔断，用户看到本地状态和「X 分钟前更新」；不报错，也不让页面等。
- 一次要刷新很多单（用户的订单列表）？ → 只刷新当前页可见的订单，每个仍然走自己的窗口。
**同类题。**
- **转账状态、股票报价：** 键分别是 transaction_id、symbol。
- **FB Live Comments：** 读侧的有界结构，同样不让读去调用上游。
