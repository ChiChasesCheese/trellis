---
id: hi-c-sd-data-structures-for-big-data-n13-quantile-how
node: sd.deep-dives.data-structures-for-big-data.notes
type: qa
step: 13
---
## Q
**大数据结构 · 近似分位数怎么实现：桶的三种做法**｜摘要 · 必会

分桶算法怎么更新和查询？固定宽度、指数、动态桶分别适合什么，误差有多大？

## A
- **更新：** 新值来了，算属于哪个桶，把该桶计数加 1。
- **查询分位数：** 从小到大累加各桶的计数，累加到目标百分比所在的桶，就是答案所在区间。
- **累积计数版：** 有的系统每桶存「小于等于上界」的累计数，写入更多（最坏每次写所有桶），但读时不用求和。
- **固定宽度桶：** 等宽区间，简单，适合值域已知且分布比较均匀。
- **指数桶：** 每桶宽度是前一桶的倍数（1–2ms、2–4ms、4–8ms……），适合跨度大、长尾的延迟数据。
- **动态直方图：** 按数据分布自动调整边界，更准，但要定期重算，复杂度通常不值得。
- **误差：** 受桶宽限制，桶宽 10ms，p95 最多偏差约 10ms。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 124" font-family="sans-serif" font-size="11">
<text x="10" y="14" fill="currentColor">固定宽度：每桶 10ms</text>
<rect x="10" y="20" width="50" height="20" fill="none" stroke="currentColor"/>
<rect x="60" y="20" width="50" height="20" fill="none" stroke="currentColor"/>
<rect x="110" y="20" width="50" height="20" fill="none" stroke="currentColor"/>
<rect x="160" y="20" width="50" height="20" fill="none" stroke="currentColor"/>
<rect x="210" y="20" width="50" height="20" fill="none" stroke="currentColor"/>
<rect x="260" y="20" width="50" height="20" fill="none" stroke="currentColor"/>
<text x="10" y="54" text-anchor="middle" fill="currentColor">0</text>
<text x="60" y="54" text-anchor="middle" fill="currentColor">10</text>
<text x="110" y="54" text-anchor="middle" fill="currentColor">20</text>
<text x="160" y="54" text-anchor="middle" fill="currentColor">30</text>
<text x="210" y="54" text-anchor="middle" fill="currentColor">40</text>
<text x="260" y="54" text-anchor="middle" fill="currentColor">50</text>
<text x="310" y="54" text-anchor="end" fill="currentColor">60ms</text>
<text x="10" y="80" fill="currentColor">指数：每桶宽度翻倍</text>
<rect x="10" y="86" width="20" height="20" fill="none" stroke="currentColor"/>
<rect x="30" y="86" width="40" height="20" fill="none" stroke="currentColor"/>
<rect x="70" y="86" width="80" height="20" fill="none" stroke="currentColor"/>
<rect x="150" y="86" width="160" height="20" fill="none" stroke="currentColor"/>
<text x="10" y="120" text-anchor="middle" fill="currentColor">1</text>
<text x="30" y="120" text-anchor="middle" fill="currentColor">2</text>
<text x="70" y="120" text-anchor="middle" fill="currentColor">4</text>
<text x="150" y="120" text-anchor="middle" fill="currentColor">8</text>
<text x="310" y="120" text-anchor="end" fill="currentColor">16ms</text>
</svg>
