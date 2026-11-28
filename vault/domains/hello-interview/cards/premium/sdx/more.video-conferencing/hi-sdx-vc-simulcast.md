---
id: hi-sdx-vc-simulcast
node: more.video-conferencing
type: qa
step: 3
---
## Q
**SFU 怎么让下行不随人数增长**｜补充 · 视频会议（Zoom） · 必会

面试官：「SFU 把每个人的 1.54 Mbps 全分辨率流都转给每个接收者，25 人就是约 37 Mbps 下行，家用网络受不了。你怎么让下行不随人数一直涨？」

## A
**结论。** 发送者同时编码多层（simulcast），SFU 按接收者屏幕上实际显示的大小只转发一层：发言人用高层，其余缩略图用低层。下行由屏幕上看得见的块数决定，不由人数决定。

**要点。**
- **多层编码：** 发送者同时输出高、中、低几个独立码率的流，例如 1.5、0.5、0.15 Mbps。
- **按画面选层：** SFU 知道每个接收者当前布局，大块给高层，缩略图给低层，屏幕外的不转发或只发音频。
- **算一笔账：** 一路发言人 1.5 加 24 路缩略图 24 × 0.15，约 5.1 Mbps；25 人变 250 人，可见块数不变，下行仍是同一量级。
- **全量对比：** 24 路全分辨率约 37 Mbps（24 × 1.54），差了 7 倍多。
- **选层会随事件切换：** 发言人变化、窗口缩放、网络变差，SFU 都要切到合适的层。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="60" y="8" width="220" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发送者同时编码多层</text>
<text x="170.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">高 1.5 · 中 0.5 · 低 0.15 Mbps</text>
<polyline points="170,48 170.0,65.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,72 166.8,65.0 173.2,65.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="60" y="72" width="220" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SFU 只转发需要的层</text>
<text x="170.0" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不解码，按接收者画面选择</text>
<polyline points="120,112 90.6,133.8" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="85,138 88.7,131.3 92.5,136.4" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="220,112 249.4,133.8" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,138 247.5,136.4 251.3,131.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="138" width="150" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="155.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接收者 1（桌面）</text>
<text x="85.0" y="170.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发言人 1.5 Mbps</text>
<text x="85.0" y="185.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">24 缩略图 × 0.15</text>
<rect x="180" y="138" width="150" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="155.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接收者 2（手机）</text>
<text x="255.0" y="170.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只看 1 路大画面</text>
<text x="255.0" y="185.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">其余全用低层</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下行 = 1.5 + 24 × 0.15 = 5.1 Mbps</text>
<text x="10" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">由屏幕上可见的块数决定，与 N 基本无关</text>
</svg>

**为什么。** 界面一次只能显示有限的块数，多出来的人对接收者没有视觉价值，不该占用带宽。

**面试里这样说。** 「发送者做 simulcast，同时编三层。SFU 按接收者的布局选层：发言人高层 1.5 Mbps，其余 24 个缩略图每个 0.15 Mbps，合计约 5.1 Mbps，人数从 25 变到 250，可见块数不变，下行基本不变。」

**易错。**
- **所有人都发高层：** 下行线性增长，弱网用户直接卡死。
- **只有一层编码：** SFU 无从降级，只能整路丢掉。
- **忽略发送者上行：** 多层编码增加发送者上行和编码 CPU，要在上行不足时少发几层。
