---
id: hi-sdx-lc-sampling-reading-speed
node: sd.problem-breakdowns.fb-live-comments.more
type: qa
step: 1
---
## Q
**采样率由阅读速度定，不由网关定**｜补充 · Facebook 直播评论 · 追问

面试官：「一场直播评论速率 167 条/秒。你把评论按固定间隔打包成一帧推给每个观众。这时采样率该按什么定？网关的推送量会随评论变多而增加吗？涨到 10 倍规模呢？」

## A
**结论。** 采样率由人的阅读速度决定：每人每秒约 4 条，比例 = 4 ÷ 评论速率，167 条/秒时约 1/42。网关每秒给每条连接只发一帧，推送量等于连接数除以间隔，和评论多少无关；10 倍规模时网关负载不变，采样比例收紧到约 1/417。

**要点。**
- **不采样的账：** 167 条 × 1000 万观众 = 16.7 亿次投递/秒，加机器只是平摊，总量不变。
- **定目标速率：** 人每秒能跟上约 3 到 5 条，取 4 条/秒作为每个观众的目标。
- **算比例：** 4 ÷ 166.7 ≈ 1/42，被采样的评论进实时流，其余照常落库、能在历史里翻到。
- **打包成帧：** 每条连接每秒一帧，5 万连接就是每秒 5 万帧，评论再多也不变。
- **10 倍：** 观众 1 亿、评论约 1667 条/秒，比例 4 ÷ 1667 ≈ 1/417，网关从 200 台加到 2000 台即可，单机负载不变。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<rect x="10" y="8" width="320" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发布的评论：167 条/秒</text>
<text x="170.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全部落库，历史里能翻到</text>
<polyline points="170,48 170.0,63.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,70 166.8,63.0 173.2,63.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="70" width="320" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">采样：目标每人 4 条/秒</text>
<text x="170.0" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">比例 = 4 ÷ 167 ≈ 1/42</text>
<polyline points="170,110 170.0,125.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,132 166.8,125.0 173.2,125.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="132" width="320" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关每秒给每条连接发一帧</text>
<text x="170.0" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5 万连接 → 5 万帧/秒，与评论数无关</text>
<polyline points="170,172 170.0,187.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,194 166.8,187.0 173.2,187.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="194" width="320" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="215.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">观众：每秒看到约 4 条，读得完</text>
<text x="10" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10 倍规模：比例收紧到 1/417，网关单机负载不变</text>
</svg>

**为什么。** 实时流的瓶颈是人，不是服务器：目标速率固定，评论越多，能展示的比例就越小，这是产品形态的变化，应当在界面上说明。

**面试里这样说。** 「采样率我用阅读速度定：每人每秒 4 条，除以 167 条/秒的评论速率，约 1/42。网关按固定间隔每连接发一帧，所以推送量等于连接数除以间隔，和评论数无关。涨到 10 倍，比例收紧到约 1/417，网关多加机器，单机负载不变。」

**易错。**
- **把采样当成网关限流：** 打包之后网关的瓶颈并不在评论数，而在连接数。
- **采样比例写死：** 评论速率变化时没有对应调整，观众要么刷屏要么冷清。
- **没落库：** 没被采样的评论也要存下来，历史视图里仍需能看到。
