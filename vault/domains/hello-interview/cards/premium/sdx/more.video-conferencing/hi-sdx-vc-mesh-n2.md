---
id: hi-sdx-vc-mesh-n2
node: more.video-conferencing
type: qa
step: 1
---
## Q
**全网状通话为什么撑不过 6 个人**｜补充 · 视频会议（Zoom） · 必会

面试官：「每个人的音视频约 1.54 Mbps。让所有参会者两两直连（全网状，mesh）最简单，没有媒体服务器。6 个人时会发生什么？为什么业界用转发服务器？」

## A
**结论。** 全网状每个人要同时上传和下载 (N-1) 路流，6 人就是 5 × 1.54 ≈ 7.7 Mbps，家用宽带的上行常常撑不住；整网流量按 N(N-1) 增长。所以只有 1 对 1 或两三个人用直连，多人会议都用 SFU 转发。

**要点。**
- **上行是瓶颈：** 家用宽带通常上行远小于下行，7.7 Mbps 的上行已经逼近或超过很多套餐的上限。
- **还要多次编码：** 每个人要把自己的画面分别编码、发送给 N-1 个对端，终端 CPU 和电量一起吃紧。
- **总量平方增长：** 总共有 N(N-1) 路流，人数翻倍，总流量变成约四倍。
- **SFU 的交换：** 每人只上传一路到服务器，N-1 份复制发生在服务器的大出口上，客户端上行固定为一路。
- **1 对 1 保留直连：** 两个人时直连更省钱、延迟更低，打不通时再走中继。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全网状：A 自己发 5 份</text>
<text x="184" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SFU：A 发 1 份</text>
<rect x="10" y="100" width="40" height="32" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="30.0" y="120.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="112" y="26" width="40" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="132.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<polyline points="50,116 107.6,44.5" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112,39 110.1,46.5 105.1,42.4" style="fill:var(--accent,#3b6fd4)"/>
<rect x="112" y="60" width="40" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="132.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<polyline points="50,116 106.2,77.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112,73 108.1,79.6 104.4,74.4" style="fill:var(--accent,#3b6fd4)"/>
<rect x="112" y="94" width="40" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="132.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D</text>
<polyline points="50,116 105.1,108.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112,107 105.5,111.2 104.6,104.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="112" y="128" width="40" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="132.0" y="145.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">E</text>
<polyline points="50,116 105.5,138.4" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112,141 104.3,141.4 106.7,135.4" style="fill:var(--accent,#3b6fd4)"/>
<rect x="112" y="162" width="40" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="132.0" y="179.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<polyline points="50,116 106.9,170.2" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112,175 104.7,172.5 109.1,167.9" style="fill:var(--accent,#3b6fd4)"/>
<rect x="184" y="100" width="40" height="32" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="204.0" y="120.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="236" y="100" width="44" height="32" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258.0" y="120.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SFU</text>
<polyline points="224,116 229.0,116.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="236,116 229.0,119.2 229.0,112.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="298" y="26" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="315.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<polyline points="280,116 296.4,45.8" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,39 299.5,46.5 293.3,45.1" style="fill:var(--accent,#3b6fd4)"/>
<rect x="298" y="60" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="315.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<polyline points="280,116 295.3,79.5" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,73 298.2,80.7 292.3,78.2" style="fill:var(--accent,#3b6fd4)"/>
<rect x="298" y="94" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="315.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D</text>
<polyline points="280,116 291.7,110.1" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,107 293.2,113.0 290.3,107.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="298" y="128" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="315.0" y="145.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">E</text>
<polyline points="280,116 293.9,135.3" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,141 291.3,137.2 296.5,133.4" style="fill:var(--accent,#3b6fd4)"/>
<rect x="298" y="162" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="315.0" y="179.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<polyline points="280,116 296.0,168.3" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,175 292.9,169.2 299.0,167.4" style="fill:var(--accent,#3b6fd4)"/>
<text x="10" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A 上行：5 × 1.54 = 7.7 Mbps  →  1.54 Mbps</text>
<text x="10" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">总流量按 N(N-1) 增长，上行换成服务器出口</text>
</svg>

**为什么。** 复制的工作必须有人做：直连把它压在最弱的一环，也就是用户的上行；SFU 把它搬到最强的一环，也就是数据中心的出口。

**面试里这样说。** 「全网状每人要上传 N-1 路，6 个人就是约 7.7 Mbps 上行，家用带宽撑不住，总流量还按 N 乘 N-1 增长。我用 SFU：每人上传一路，服务器负责复制转发，只有一对一通话保留直连。」

**易错。**
- **只算下行：** 真正先崩的是上行，家用宽带往往是非对称的。
- **说全网状完全不能用：** 两三个人的小会，直连省服务器成本，仍然合理。
- **忘了终端编码成本：** 手机多路编码会发热、耗电，体验比带宽数字更早变差。
