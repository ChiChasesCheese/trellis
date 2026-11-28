---
id: hi-sdx-clk-truetime
node: more.clocks
type: qa
step: 4
---
## Q
**TrueTime：区间时间与提交等待**｜补充 · 时钟 · 追问

面试官：「Spanner 的 TrueTime 接口返回的不是一个时间戳，而是什么？事务怎样靠它让时间戳顺序与真实时间顺序一致？代价是什么？」

## A
**结论。** TrueTime 返回一个区间 [earliest, latest]，真实时间一定落在其中，不确定度来自 GPS 和原子钟，通常几毫秒。事务取 latest 作提交时间戳 s，再提交等待（commit wait）到 earliest 超过 s 才对外提交，之后任何事务的时间戳都更大，得到外部一致性。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<rect x="10" y="12" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 取 s</text>
<text x="58.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">= latest</text>
<text x="58.0" y="59.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（区间上界）</text>
<polyline points="106,40 115.0,40.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="122,40 115.0,43.2 115.0,36.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="122" y="12" width="96" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 提交等待</text>
<text x="170.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等到 earliest</text>
<text x="170.0" y="59.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过 s</text>
<polyline points="218,40 227.0,40.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="234,40 227.0,43.2 227.0,36.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="234" y="12" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 对外提交</text>
<text x="282.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">此后开始的事务</text>
<text x="282.0" y="59.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间戳 &gt; s</text>
<text x="8" y="100" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">TrueTime 返回区间 [earliest, latest]，</text>
<text x="8" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">真实时间一定落在区间内。</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">等到 earliest 超过 s，说明真实时间已过 s，</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">之后谁来拿时间戳都比 s 大。</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：不确定度直接变成写延迟。</text>
</svg>

**要点。**
- **区间而不是点：** 接口老实承认「不知道确切时间，只知道范围」。
- **提交等待：** 持有结果不外露，直到 earliest 越过 s，此时真实时间必然已过 s。
- **保证：** 之后开始的任何事务拿到的时间戳都严格大于 s，跨数据中心的事务顺序与真实时间一致，即严格可串行化。
- **代价：** 不确定度直接变成写延迟，所以 Google 要用 GPS 加原子钟把区间压到几毫秒。
- **2026 亮点：** 这套思路不再只属于 Spanner：AWS 的 Time Sync 在部分 EC2 实例上提供微秒级精度的时钟，开源的 ClockBound 给出时钟误差界，Aurora DSQL 在其上建 HLC，事务的开始与提交时间戳由它分配，并确认提交时间戳已成过去才确认提交。代价是依赖云厂商的时钟硬件和实例类型，应用仍不能直接信任普通 NTP 墙钟。

**面试里这样说。** 「Spanner 用时钟的不确定区间换正确性：取区间上界做提交时间戳，等真实时间必然越过它再提交，所以跨地域也能按真实时间排序。没有这种硬件的系统做不到同级保证，只能退到 HLC。」

**易错。**
- **以为 TrueTime 给出精确时间：** 它给的是区间。
- **忽略提交等待的延迟：** 外部一致性是用写延迟换的。
