---
id: uth-storage-bloom-3-bits-vs-fp
node: storage.bloom
type: qa
step: 3
---
## Q
**位数与误判率**｜RocksDB · v10.9

过滤器每个 key 多给几位，误判率降多快？要把误判压到 0.1% 要付多少内存？

## A
**背景。** 位数组越大，不同 key 撞到同一位的机会越小，误判越少；代价是内存。

**结构。** 位数组 m 位、n 个 key、k 次探测时，误判率是 `(1 - e^(-k·n/m))^k`；k 取最优（约 0.69 × m/n）后约化为 0.6185^(m/n)：每多给 1 位/key，误判率乘以约 0.62。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 162">
<line x1="56" y1="18" x2="56" y2="118" stroke="currentColor" stroke-width="1.2"/>
<line x1="56" y1="118" x2="332" y2="118" stroke="currentColor" stroke-width="1.2"/>
<line x1="56" y1="30" x2="332" y2="30" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="50" y="34" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10%</text>
<line x1="56" y1="70" x2="332" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="50" y="74" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1%</text>
<line x1="56" y1="110" x2="332" y2="110" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="50" y="114" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0.1%</text>
<line x1="90" y1="30" x2="281" y2="110" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="90" cy="30" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="90" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4.9</text>
<circle cx="180" cy="70" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9.9</text>
<circle cx="281" cy="110" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="281" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15.5</text>
<text x="332" y="154" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位/key</text>
<text x="60" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每多 1 位, 误判率 x 0.62</text>
</svg>
```

**细节。**

| 位/key | 误判率 |
|---|---|
| 4.9 | 10% |
| 9.9 | 1% |
| 15.5 | 0.1% |

- 100 万个 key：9.9 位/key 约 1.2 MB，15.5 位/key 约 1.9 MB。

**为什么。** 收益递减：从 4.9 位到 9.9 位，误判降 10 倍；再降 10 倍要多 5.6 位。所以 10 位/key 是常见的折中。

**对应 LeetCode：** 无直接对应的题
