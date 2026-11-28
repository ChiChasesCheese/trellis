---
id: hi-fix-scope-math-06-numbers-to-decisions
node: fix.scope-math
type: qa
step: 6
---
## Q
**GoFundMe · 从数字到决定**｜补强

面试官：「你算了这么多数字，它们改变了你的设计吗？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **一个数字配一个决定：** 「读峰值 15,000 次/秒：缓存挡读，单个热点另外处理。」
- **写：** 「峰值 150 笔/秒：一台主库够，不分片；复杂度花在只扣一次、只加一次上。」
- **存储：** 「1 TB 的记录放一台库，2 TB 的图片放对象存储；存储不是分片的理由。」
- **并发：** 「支付服务商（PSP）同时在飞 1,000 个：限并发，提前谈额度，超出的排队。」
- **面试官说先不管规模：** 「好，我先画单机能跑通的版本；数字我先算一次，只用来指出后面哪几处要加固。」
- **算错了当场改：** 「我刚才说错了，算式是 5,000，以它为准。」自己发现自己改，是加分。
- **什么时候停：** 数字够选方案就停，不算到小数点后。
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数字 → 决定（只留改变设计的数）</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">读 15,000/秒（峰值）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">缓存挡读；单个热点另外处理</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">页面读小结构，不读主库</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">写 150/秒</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一台主库够；不分片</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">复杂度花在正确性上，不花在规模上</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">存储 1 TB / 图片 2 TB</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">数据库一台；图片放对象存储</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存储不是分片的理由</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">PSP 并发 1,000</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">限并发 + 提前谈额度</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">超出的排队，不是直接失败</text>
</svg>
白板上：四行「数字 → 决定」；没有改变设计的数字，不上白板。
**为什么这样说。** （约 1 分钟，放在估算最后。）这是收口：面试官看你的数字有没有用。强的回答每个数字都带一个设计决定，并且知道哪些数字不需要。弱的回答是算了一大串，没有一个数字出现在后面的设计里。
**面试官可能接着问。**
- 哪个数字最重要？ → 对这个系统是写的正确性，而不是量：写每秒只有一百多，所以我把时间花在「只扣一次、只加一次」上。
- 如果数字大十倍呢？ → 读 15 万/秒仍然靠缓存和 CDN；写每秒 1,500 笔单库开始吃紧，我会先看是不是热点行，再谈拆分。
- 估算要多精确？ → 数量级对就够。差两倍不改变设计，差一个数量级才会。
**常见失分。**
- **算了不用：** 数字没有变成决定。
- **数字越报越细：** 小数点不会帮你拿分。
- **被面试官一问就乱：** 数字要有来源，假设要说出来，被问时才能答得稳。
