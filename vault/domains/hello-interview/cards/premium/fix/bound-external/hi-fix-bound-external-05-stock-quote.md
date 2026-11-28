---
id: hi-fix-bound-external-05-stock-quote
node: fix.bound-external
type: qa
step: 5
---
## Q
**用户能触发的外部调用 · 股票报价**｜补强

面试官：「股票详情页要最新报价，数据来自行情供应商，按调用计费，额度 300 次/秒。500 万人同时在看，怎么办？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先换键：** 「500 万人看的是大约 3,000 只股票，键是 symbol，不是用户。刷新的数量由股票数决定，不由观看人数决定。」
- **用户的读：** 「读最近一次报价，带 as_of 时间，页面写「延迟报价，截至 10:00:05」；读从不等供应商。」
- **分档窗口：** 「按观看人数分档。热门 300 只，每 5 秒一次：300 ÷ 5 = 60 次/秒。其余 2,700 只，每 30 秒一次：2,700 ÷ 30 = 90 次/秒。合计 150 次/秒，低于 300 次/秒的额度。」
- **读的数字：** 「500 万人每 5 秒读一次 = 1,000,000 次/秒，由进程内缓存加 Redis 挡，不到供应商。」
- **额度不够时：** 「先砍冷门股票的刷新频率，热门保持；比一刀切地拒绝好。」
- **触发条件：** 「供应商如果提供流式行情，一条连接订阅就能替代轮询；这是我换掉轮询的触发。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 201">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">行情页：键是股票代码，不是用户</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">热门 300 只</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每 5 秒刷新：300 ÷ 5 = 60 次/秒</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">其余 2,700 只</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每 30 秒刷新：2,700 ÷ 30 = 90 次/秒</text>
<rect x="8" y="130" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">合计</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">60 + 90 = 150 次/秒 &lt; 额度 300 次/秒</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">页面显示报价的 as_of 时间</text>
</svg>
白板上：键是股票代码，分档窗口，合计与额度。
**为什么这样说。** （约 1 分钟。）面试官看你能不能把「谁触发」和「谁决定调用量」分开。强的回答指出调用量只和被看的对象数有关，并用档位把它压到额度以下；弱的回答是「每个用户查一次，加缓存」。
**面试官可能接着问。**
- 开盘瞬间 3,000 只都变热了呢？ → 热门档变多，调用上限升到 3,000 ÷ 5 = 600 次/秒，超过额度；所以按热度排序，额度内的先刷，其余沿用旧价格，页面标出 as_of。
- 为什么不让每个用户直接订阅供应商？ → 连接数和费用都按用户增长；用我们自己的服务订阅一次，再扇出给用户。
- 价格过期到什么程度要报警？ → 热门股票的 as_of 落后超过 15 秒报警，页面同时灰显。
**同类题。**
- **转账状态、订单物流：** 键是对象，窗口按变化快慢定，上限由额度推出。
- **Robinhood：** 行情读取和下单是两回事，只有下单需要强一致。
