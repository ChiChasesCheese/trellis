---
id: hi-mock-donations-website-charities-03-nonfunctional
node: qb.sd.donations-website-charities.mock
type: qa
step: 3
---
## Q
**限时捐款网站 · 第 3 步 · 非功能需求与估算**｜模拟面试

面试官：「再说说非功能需求。有没有什么数字想先算一下？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **正确性第一：** 「绝不重复扣款，也绝不出现『扣了款但我们没记录』。」
- **失败可恢复：** 「PSP 慢、超时、挂了，都要能恢复；被拒绝要给用户明确提示。」
- **流量尖峰：** 「活动开始、截止前、媒体曝光会有尖峰。」
- **敏感数据：** 「卡号不进我们的系统，合规范围（PCI）最小化。」
- **先算笔数：** 「10 亿美元 ÷ 每笔 10 美元 = 1 亿笔。」
- **再算速率：** 「3 天 = 3 × 24 × 3600 = 259,200 秒；1 亿 ÷ 259,200 ≈ 386 笔/秒。尖峰按 5 倍，386 × 5 ≈ 1,930，我取 2,000 笔/秒。」
- **再算并发：** 「每笔调 PSP 约 0.5 秒，同时在飞的 PSP 请求 = 2,000 × 0.5 = 1,000 个。这个数决定我要给 PSP 调用加并发上限，也要和 PSP 提前约定更高的频率额度。」
- **再算存储和写入：** 「每笔约 1 KB，1 亿笔 ≈ 100 GB，一台数据库放得下。每笔约 4 次写：建行、转处理中、写终态、写发件箱，2,000 × 4 = 8,000 行写/秒，仍在单主库的量级，但余量不大，真上线要压测。」
- **先不管规模：** 「您说先不管规模，所以我先画单机能跑通的版本，这些数字只用来指出后面哪几处要加固。小版本 1 亿美元是 1,000 万笔，约 39 笔/秒，同一套设计更轻松。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 360">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">非功能需求 → 数字 → 逼出什么设计</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">正确性：最多扣一次钱</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">绝不出现「扣了款却没记录」</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 三层防重复 + 对账（深入一、二）</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">失败可恢复：PSP 慢、挂、超时</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">被拒绝 ≠ 故障，用户看到明确结果</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 熔断 + 备用 PSP（深入三）</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">尖峰：386 × 5 ≈ 2,000 笔/秒</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">并发 = 2,000 × 0.5 秒 = 1,000</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 对 PSP 限并发 + 排队（深入三）</text>
<rect x="8" y="236" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="256" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">数据安全：卡号不进我们系统</text>
<text x="18" y="271" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 亿笔 × 1 KB ≈ 100 GB，一台库够</text>
<text x="18" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 令牌化，PCI 范围最小，库不分片</text>
<text x="8" y="314" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10 亿 ÷ 10 美元 = 1 亿笔；÷ 259,200 秒 ≈ 386/秒</text>
<text x="8" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小版本 1 亿美元：1,000 万笔 ≈ 39/秒</text>
<text x="8" y="350" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每笔约 4 次写 × 2,000 = 8,000 行写/秒</text>
</svg>
白板上新增：四张便签，每张三行：需求、数字、它逼出的设计。后面的深入问题就从这几张里选。
**为什么这样说。** （约 3 分钟，累计第 7 分钟。）面试官看数字能不能变成设计决定，以及你在「先别管规模」的限制下是否会分寸得当：数字要算，但不能一上来就谈分片。强的回答每条非功能需求都带一个数字和一个去向：1,000 并发推出限并发和排队，100 GB 推出一台库够，正确性推出三层防重复。弱的回答只说「要高可用、高并发」，或者面试官说先别管规模，却立刻画分库分表。
**面试官可能接着问。**
- 为什么尖峰取 5 倍？ → 没有历史数据，这是我的假设，我说出来：活动开始、截止前和媒体曝光会集中，5 倍是个常见的保守取值，您给别的数我就改。
- 1,000 个并发 PSP 请求够吗？ → 取决于 PSP 给我们的额度。PSP 对每个账号有频率限制，要提前约定更高额度；这个数同时是我的并发上限的来源。
- 8,000 写/秒单库真的行吗？ → 行数小、都是按主键读写，单主库在这个量级可行，但我会留余量并压测；真的不够，再把捐款表按 donationId 哈希分库，因为没有跨记录的事务。
**常见失分。**
- **只说空话：** 「高可用、可扩展」没有数字，面试官无法判断你要的是什么系统。
- **算了不用：** 算出 1,000 并发却没说它改变了哪个决定，估算就成了表演。
- **违背限制：** 面试官说先别管规模，却立刻讲分片和多区域。
- **漏掉正确性：** 这题最贵的事故是重复扣款，不提它，后面的三层防护就没有来由。
