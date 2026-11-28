---
id: hi-sdx-vc-degradation-order
node: more.video-conferencing
type: qa
step: 9
---
## Q
**带宽变差：先降什么，音频最后**｜补充 · 视频会议（Zoom） · 追问

面试官：「会议中某个人的网络变差，拥塞控制算出可用带宽下降。你按什么顺序降级音频和视频？屏幕共享也是同一个顺序吗？」

## A
**结论。** 先降分辨率（或换低层），再降帧率，再关视频，音频最后才动。屏幕共享反过来：先保住清晰度，降帧率。

**要点。**
- **音频便宜又致命：** 语音约 24 到 40 kbps，只有 1.5 Mbps 视频的 2% 左右，丢了音频会议就没法继续。
- **视频分级：** 降分辨率损失最小，降帧率（30 到 15）次之，关视频保住通话。
- **给音频加保护：** 发送调度优先放行音频包，并给音频加前向纠错或冗余包，抵御丢包，而不是降码率。
- **屏幕共享相反：** 内容是文字和图表，分辨率决定能不能看清，所以优先降帧率、保分辨率。
- **SFU 也配合：** 下行不够时，先把缩略图降到最低层或暂停，发言人的画面最后动。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">带宽变差，从上往下依次牺牲</text>
<rect x="10" y="26" width="320" height="42" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 降分辨率 / 换低层</text>
<text x="170.0" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最便宜的画质损失</text>
<polyline points="170,68 170.0,75.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,82 166.8,75.0 173.2,75.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="82" width="320" height="42" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 降帧率 30 → 15</text>
<text x="170.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">画面更卡，仍能看清</text>
<polyline points="170,124 170.0,131.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,138 166.8,131.0 173.2,131.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="138" width="320" height="42" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 关闭视频</text>
<text x="170.0" y="170.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只剩声音，会还能开</text>
<polyline points="170,180 170.0,187.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,194 166.8,187.0 173.2,187.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="194" width="320" height="42" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="211.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 音频降质（最后）</text>
<text x="170.0" y="226.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 32 kbps，开销极小</text>
<text x="10" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">音频约 32 kbps，仅是 1.5 Mbps 视频的 2%</text>
</svg>

**为什么。** 每一步都按体验损失除以省下的带宽排序：音频省不了多少带宽却代价最高，视频的前几步代价小又省得多。

**面试里这样说。** 「带宽下降我按这个顺序：先降视频分辨率或换低层，再降帧率，再关视频，音频最后。音频大约 32 kbps，保住它几乎不花钱，丢了就没法开会。屏幕共享我反过来，保分辨率、降帧率。」

**易错。**
- **音频视频同比例降级：** 视频还没降到底，音频就先变得断续。
- **屏幕共享也先降分辨率：** 文字糊了，共享就失去意义。
- **只降码率不加纠错：** 丢包时音频仍然断断续续，要靠冗余或前向纠错。
