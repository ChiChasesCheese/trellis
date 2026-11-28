---
id: hi-sdx-request-hedging
node: sd.core-concepts.networking-essentials.more
type: qa
step: 3
---
## Q
**请求对冲压低尾延迟**｜补充 · 网络基础 · 追问

某读服务有 3 个副本，p99 偏高，慢的原因是偶发的 GC 暂停和慢盘。你不想靠改代码，怎么用「请求对冲」压低尾延迟？代价和前提是什么？

## A
**结论。** 请求超过 p95 还没返回，就向另一个副本再发一份，取先到的、取消另一份。只多约 5% 的请求，就能大幅压低偶发慢事件的影响。

**要点。**
- **机制：** 等到 p95 延迟（例如 40 ms）还没回复，再发给另一个副本；第一个返回的算数，另一份取消。
- **成本：** 只有超过 p95 的请求才多发，最多约 5% 的请求重复，额外负载约 5%。
- **为什么有效：** 慢事件（GC、慢盘）一次只发生在一个副本上，两个副本同时碰上的概率约是平方：1% × 1% = 0.01%。
- **扇出时更明显：** 100 个并行调用，单个 1% 变慢时页面有 63% 碰上慢调用；对冲后每个调用约 0.01%，页面只有约 1%。
- **前提：** 操作幂等或可去重，能取消另一份；不要对冲对冲出来的请求，否则过载时会自我放大。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单位：毫秒</text>
<text x="8" y="46" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">副本 A（慢）</text>
<rect x="24" y="54" width="128.333" height="22" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<text x="160.333" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原本要 300，已取消</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">副本 B</text>
<rect x="117.333" y="116" width="35" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<line x1="117.333" y1="50" x2="117.333" y2="146" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="152.333" y1="50" x2="152.333" y2="146" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="113.333" y="164" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">40 再发</text>
<text x="156.333" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">55 先到者胜</text>
<text x="24" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 发出</text>
</svg>

**面试里这样说。** 「读路径我做请求对冲：超过 p95 还没回就发给另一个副本，先到先用并取消另一份，只多约 5% 负载。前提是读请求幂等；我不对冲写请求，也不对冲被对冲出来的请求。」

**易错。**
- **一开始就同时发两份：** 负载翻倍，成本远高于等到 p95 再发。
- **对冲写请求或按调用计费的调用：** 写会重复执行，计费会翻倍。
- **副本慢是同一个原因：** 过载时所有副本一起慢，对冲只会让情况更糟。
