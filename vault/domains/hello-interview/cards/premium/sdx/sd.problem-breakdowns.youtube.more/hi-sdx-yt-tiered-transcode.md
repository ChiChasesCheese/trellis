---
id: hi-sdx-yt-tiered-transcode
node: sd.problem-breakdowns.youtube.more
type: qa
step: 1
---
## Q
**码率阶梯全转太贵：分层转码**｜补充 · 视频平台（YouTube） · 必会

面试官：「每个上传视频都转出 6 档、两种编码的全套码率阶梯，存储会多多少？如果改成『谁第一次点某一档才现场转』，爆红的冷门视频会出什么问题？你怎么折中？」

## A
**结论。** 全套阶梯约是母版存储的 6.1 倍，而多数视频几乎没人看。纯按需转码又会让爆红视频的第一批观众都等转码。折中是分层：上传时立刻转低中档（360p 到 720p），4K 这类贵的档位等播放量过阈值再异步补齐。

**要点。**
- **6.1 倍怎么来：** 一套阶梯 400+800+1200+2500+4500+15000 = 24400 kbps，两个编码族共 48800，除以母版 8000 kbps 约 6.1。
- **播放量是重尾：** 少数头部视频占绝大多数观看，为长尾视频转 4K 和新编码基本是浪费。
- **纯按需的坑：** 冷门视频突然爆红，大量观众同时请求还不存在的档位，转码队列被打满，每个人都等几十秒到几分钟。
- **分层的做法：** 上传即转低中档，保证随时可播；高档位在近 N 天播放量超过阈值后异步生成，期间降级播放现有档位。
- **阈值是运营参数：** 按实际播放分布调，不写死。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="10" y="8" width="320" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上传完成</text>
<polyline points="170,44 170.0,55.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,62 166.8,55.0 173.2,55.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="62" width="320" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">立即转低中档：360p–720p</text>
<text x="170.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">随时有可播放的版本</text>
<polyline points="170,106 170.0,117.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,124 166.8,117.0 173.2,117.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="124" width="320" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">播放量超过阈值（近 N 天）</text>
<text x="170.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">异步补齐 1080p / 4K / AV1</text>
<polyline points="170,168 170.0,179.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,186 166.8,179.0 173.2,179.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="186" width="320" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="205.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">补齐前：降级播放现有档位</text>
<text x="10" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全套阶梯（2 个编码族）≈ 6.1 倍母版存储</text>
<text x="10" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长尾视频多数没人看，不值得全转</text>
</svg>

**为什么。** 把成本最高的那部分放在有观看需求之后，最坏情况下也有一个立刻可播的档位兜底。

**面试里这样说。** 「全套阶梯两个编码族约 6.1 倍母版存储，所以不能全转。我上传时只转 360 到 720p，保证马上能播；4K 和 AV1 等播放量过阈值再异步补，补齐前降级播放，这样爆红视频也不会让观众排队等转码。」

**易错。**
- **全量预转码：** 存储和算力随上传量线性涨，大部分花在没人看的视频上。
- **完全按需：** 爆红瞬间转码队列被打满，首批观众体验最差。
- **补齐期间阻塞播放：** 应该先用现有档位播，不要让观众等高档位。
