---
id: hi-sdx-vc-cascaded-sfu
node: more.video-conferencing
type: qa
step: 7
---
## Q
**大型网络研讨会：SFU 级联**｜补充 · 视频会议（Zoom） · 追问

面试官：「1000 人的研讨会，5 位主讲，观众分布在 5 个区域。如果所有观众都从主讲所在区域的服务器取流，出口要多少？怎么让跨区域的骨干流量不随观众数增长？」

## A
**结论。** 全从一个区域发，约 7.46 Gbps。改成区域 SFU 级联：每位主讲的流只向其他 4 个区域各发一份，在各区域内部再扇出给观众，跨区域骨干只有 4 × 5 × 1.5 = 30 Mbps，与观众人数无关。

**要点。**
- **不级联：** 995 位观众 × 5 路主讲 × 1.5 Mbps ≈ 7.46 Gbps，全部从源区域出口发出。
- **级联后骨干：** 每个区域每路主讲流只接收一份，4 个区域 × 5 路 × 1.5 Mbps = 30 Mbps。
- **观众流量仍在：** 每区域约 200 位观众的下行还是要发，但发生在本区域内部网络，不过长途骨干。
- **成本规律：** 骨干流量随（主讲数 × 区域数）增长，本地扇出随（本区域观众数）增长，只有前者每字节贵。
- **观众加入就近：** 观众连本区域 SFU，不用关心主讲在哪里。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<rect x="10" y="8" width="320" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主讲区域 SFU（5 路主讲流）</text>
<text x="170.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每路 1.5 Mbps</text>
<polyline points="47,48 47.0,79.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="47,86 43.8,79.0 50.2,79.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="86" width="74" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="47.0" y="102.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 2</text>
<text x="47.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SFU</text>
<polyline points="47,126 47.0,145.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="47,152 43.8,145.0 50.2,145.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="152" width="74" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="47.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地观众</text>
<polyline points="129,48 129.0,79.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="129,86 125.8,79.0 132.2,79.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="92" y="86" width="74" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="129.0" y="102.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 3</text>
<text x="129.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SFU</text>
<polyline points="129,126 129.0,145.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="129,152 125.8,145.0 132.2,145.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="92" y="152" width="74" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="129.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地观众</text>
<polyline points="211,48 211.0,79.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="211,86 207.8,79.0 214.2,79.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="174" y="86" width="74" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="211.0" y="102.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 4</text>
<text x="211.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SFU</text>
<polyline points="211,126 211.0,145.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="211,152 207.8,145.0 214.2,145.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="174" y="152" width="74" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="211.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地观众</text>
<polyline points="293,48 293.0,79.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="293,86 289.8,79.0 296.2,79.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="256" y="86" width="74" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="293.0" y="102.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 5</text>
<text x="293.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SFU</text>
<polyline points="293,126 293.0,145.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="293,152 289.8,145.0 296.2,145.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="256" y="152" width="74" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="293.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地观众</text>
<text x="10" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跨区域：4 区域 × 5 路 × 1.5 = 30 Mbps</text>
<text x="10" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不级联：995 观众 × 5 路 × 1.5 ≈ 7.46 Gbps</text>
<text x="10" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">骨干只随（主讲数 × 区域数）增长，</text>
<text x="10" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">观众扇出留在各区域内部</text>
</svg>

**为什么。** 复制应当尽量靠近观众做，贵的链路只传一份。

**面试里这样说。** 「不级联，995 个观众看 5 路主讲，源区域出口约 7.46 Gbps。我做区域级联：主讲流向其他 4 个区域各发一份，骨干只有 4 乘 5 乘 1.5，约 30 Mbps，观众再多也不涨，扇出留在各区域内部。」

**易错。**
- **所有观众连同一个源区域：** 出口和长途带宽随观众线性涨，跨洋用户延迟还高。
- **级联时转发全分辨率给每个区域：** 按各区域实际需要的层转发，才能继续省骨干。
- **忘了区域间的故障切换：** 区域之间的级联链路断了，该区域观众要能重连到其他路径。
