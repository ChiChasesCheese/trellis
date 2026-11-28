---
id: hi-sdx-maps-eta-refresh-endpoint
node: more.google-maps
type: qa
step: 3
---
## Q
**ETA 刷新为何单独一个接口**｜补充 · 地图与导航（Google Maps） · 追问

面试官：「导航平均 20 分钟，客户端每 30 秒刷新一次 ETA。为什么要拆出一个独立的轻量 eta-refresh 接口，而不是让客户端再调一次起步用的路线规划接口？」

## A
**结论。** 一次导航只有 1 次路线规划，却有 20×60÷30 = 40 次 ETA 刷新，刷新请求量约是起步的 40 倍。所以刷新走轻量接口：客户端带上当前位置和剩余路线，服务端只把最新路况套到剩余路段上重算时间，不再整图搜索。

**要点。**
- **算数：** 1200 秒 ÷ 30 秒 = 40，刷新量随「行程时长 ÷ 刷新间隔」增长，路线请求量只随起步次数增长。
- **规划接口按低 QPS 配容量：** 它要做点到点整图搜索，再跑 ETA 模型，按起步的请求量配机器。
- **刷新接口增量更新：** 位置和剩余路线已知，只需把路况变化套到剩余路段上。
- **偏航才回到规划：** 位置偏离路线，或剩余路线上路况剧变，再走完整重新规划。

**为什么。** 如果每次刷新都重新搜图，成本最高的路径就要扛 40 倍的流量，而其中绝大部分结果和上一次几乎一样。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一次 20 分钟的导航</text>
<rect x="20" y="28" width="300" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">起步：1 次完整路线规划</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">之后每 30 秒一次 ETA 刷新，共 40 次</text>
<line x1="20" y1="118" x2="320" y2="118" stroke-width="1" stroke="currentColor"/>
<line x1="20.0" y1="108" x2="20.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="27.5" y1="108" x2="27.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="35.0" y1="108" x2="35.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="42.5" y1="108" x2="42.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="50.0" y1="108" x2="50.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="57.5" y1="108" x2="57.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="65.0" y1="108" x2="65.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="72.5" y1="108" x2="72.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="80.0" y1="108" x2="80.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="87.5" y1="108" x2="87.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="95.0" y1="108" x2="95.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="102.5" y1="108" x2="102.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="110.0" y1="108" x2="110.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="117.5" y1="108" x2="117.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="125.0" y1="108" x2="125.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="132.5" y1="108" x2="132.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="140.0" y1="108" x2="140.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="147.5" y1="108" x2="147.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="155.0" y1="108" x2="155.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="162.5" y1="108" x2="162.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="170.0" y1="108" x2="170.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="177.5" y1="108" x2="177.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="185.0" y1="108" x2="185.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="192.5" y1="108" x2="192.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="200.0" y1="108" x2="200.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="207.5" y1="108" x2="207.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="215.0" y1="108" x2="215.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="222.5" y1="108" x2="222.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="230.0" y1="108" x2="230.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="237.5" y1="108" x2="237.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="245.0" y1="108" x2="245.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="252.5" y1="108" x2="252.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="260.0" y1="108" x2="260.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="267.5" y1="108" x2="267.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="275.0" y1="108" x2="275.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="282.5" y1="108" x2="282.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="290.0" y1="108" x2="290.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="297.5" y1="108" x2="297.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="305.0" y1="108" x2="305.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="312.5" y1="108" x2="312.5" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="320.0" y1="108" x2="320.0" y2="118" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<text x="20" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 分</text>
<text x="320" y="140" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">20 分</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1200 秒 ÷ 30 秒 = 40，刷新是起步的 40 倍</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">刷新不能每次都重搜整张路网图</text>
</svg>

**面试里这样说。** 「一次 20 分钟的导航，30 秒刷新一次，就是 40 次刷新对 1 次规划。我把刷新拆成独立接口：客户端带当前位置和剩余路线，服务端只把最新路况套到剩余路段上算时间；位置偏离或路况剧变才回到完整规划。」

**易错。**
- **把 40 倍当峰值：** 它是均值，不同时段的在途导航数不同，容量要按峰值再估。
- **漏掉路线预览：** 用户只看路线、没出发时也会调规划接口，规划的实际流量比起步次数更高。
