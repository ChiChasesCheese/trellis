---
id: hi-sdx-url-kgs-outage
node: sd.problem-breakdowns.bitly.more
type: qa
step: 2
---
## Q
**号段服务挂了：写降级，读不受影响**｜补充 · 短链接服务（Bitly） · 追问

面试官：「短链服务的写实例都从一个号段服务（负责分配短码区间）一次领一批，比如 1000 个，在本地发放。这个号段服务整体不可用了，创建和重定向各会怎样？你能扛多久？」

## A
**结论。** 重定向完全不受影响，创建在本地号段用完后才开始失败。能扛多久 = 每批大小 ÷ 每个实例的发号速率，所以批量大小就是容忍时长的旋钮。

**要点。**
- **读路径无依赖：** 重定向只走缓存和主键存储，从不碰号段服务。把低 QPS 的写和高 QPS 的读拆开，故障就被限制在写这一侧。
- **写路径靠本地存货：** 实例手里还有未发完的号，创建照常；发完才拒绝。
- **算容忍时长：** 峰值写约 35 次/秒，3 个写实例，每个约 11.7 次/秒；1000 个号只够约 86 秒。平均写 12 次/秒时每个实例约 4 次/秒，能撑约 250 秒。
- **调大批量或预取：** 想扛 10 分钟，批量要到约 7000；或者用掉 10% 就提前领下一批，把「用完才去领」变成「提前领」。
- **兜底：** 号段服务恢复后，从持久化的最大值继续；浪费的号对几万亿的空间无所谓。

**为什么。** 协调服务只在领号时才用，调用频率是创建速率除以批量大小，远低于每个请求一次。依赖越稀，它的故障对用户越不可见。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写路径（低 QPS）</text>
<rect x="10" y="24" width="86" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="53.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写服务</text>
<rect x="124" y="24" width="92" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地号段</text>
<text x="170.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1000 个</text>
<rect x="244" y="24" width="86" height="44" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="287.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">号段服务</text>
<text x="287.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已宕机</text>
<polyline points="96,46 124,46" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="124.0,46.0 117.0,42.8 117.0,49.2" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="216,46 244,46" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="244.0,46.0 237.0,42.8 237.0,49.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="10" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">号段用完前创建照常；用完后创建被拒</text>
<text x="10" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读路径（高 QPS）</text>
<rect x="10" y="128" width="70" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="45.0" y="154.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<rect x="106" y="128" width="70" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="141.0" y="154.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读服务</text>
<rect x="202" y="128" width="128" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="266.0" y="154.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存 / 库</text>
<polyline points="80,150 106,150" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="106.0,150.0 99.0,146.8 99.0,153.2" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="176,150 202,150" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="202.0,150.0 195.0,146.8 195.0,153.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读路径不经过号段服务，完全不受影响</text>
</svg>

**面试里这样说。** 「号段服务挂了，重定向不受影响，因为读路径只走缓存和主键存储。创建靠本地号段撑：峰值 35 次/秒、3 个实例，1000 个号约 86 秒，所以我把批量调到几千，并在用掉一成时提前预取。」

**易错。**
- **以为协调服务挂了整站不可用：** 读写拆开后，只有创建会降级。
- **批量越大越好：** 实例崩溃会浪费整批未发的号，批量要在「容忍时长」和「浪费量」之间取。
