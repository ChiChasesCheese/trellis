---
id: hi-sdx-ig-publish-after-processing
node: sd.problem-breakdowns.instagram.more
type: qa
step: 1
---
## Q
**媒体处理完才能发布并扇出**｜补充 · 图片分享（Instagram） · 追问

面试官：「用户上传完图片或视频，客户端马上调用『发帖』。你是立刻把帖子推给粉丝的动态流，还是等一等？为什么？」

## A
**结论。** 等一等。发帖要以媒体处理状态为闸门：缩放、转码这些衍生版本都就绪（ready）之后，创建帖子才成功并触发扇出；否则粉丝的动态流里会出现打不开的空白图。

**要点。**
- **处理比上传慢：** 缩放图片、把视频转成多档码率，通常比上传本身更耗时。
- **立刻扇出的后果：** 帖子已经进了成千上万个粉丝的动态流，媒体却还没生成，粉丝看到破图或空白。
- **状态当闸门：** 媒体有状态字段（上传中、处理中、ready、失败），创建帖子的调用只有在状态为 ready 时才放行。
- **等待放在哪里：** 放在「上传完成」和「帖子发布」之间，不放在上传确认里，用户的上传不会被拖慢。
- **失败怎么办：** 状态为失败就不发布，告知用户重试；长期卡在处理中的由后台任务清理。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 286">
<rect x="10" y="8" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端上传完成</text>
<text x="85.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">媒体状态：上传中</text>
<polyline points="160,28 173.0,28.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,28 173.0,31.2 173.0,24.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="8" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理队列</text>
<text x="255.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缩放 / 转码</text>
<polyline points="255,48 255.0,65.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,72 251.8,65.0 258.2,65.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="72" width="150" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">衍生版本就绪</text>
<text x="255.0" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">状态：ready</text>
<polyline points="255,112 255.0,131.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,138 251.8,131.0 258.2,131.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="138" width="150" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">创建帖子成功</text>
<text x="255.0" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">触发粉丝扇出</text>
<polyline points="255,178 255.0,195.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,202 251.8,195.0 258.2,195.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="202" width="150" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="223.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">粉丝动态流</text>
<rect x="10" y="72" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发帖请求提前到</text>
<text x="85.0" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">状态未 ready</text>
<polyline points="85,112 85.0,131.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="85,138 81.8,131.0 88.2,131.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="138" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">被拒绝或排队</text>
<text x="85.0" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">稍后重试</text>
<text x="10" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">图和视频的缩略版本没好之前，不让它进粉丝的动态流</text>
</svg>

**为什么。** 扇出是几乎不可撤回的写放大动作，一旦写进粉丝的流就很难收回，所以要在扇出之前确认内容可用。

**面试里这样说。** 「上传完成不等于可发布。我给媒体加状态，处理流水线把缩放和转码做完才置为 ready，创建帖子只在 ready 时成功并触发扇出，这样粉丝的流里不会出现还打不开的媒体，等待发生在上传和发布之间。」

**易错。**
- **上传完立刻发布：** 动态流里出现空白图，修复要回头改很多个粉丝的流。
- **让上传请求等处理完：** 用户在上传界面卡住，超时重试还会产生重复上传。
- **没有失败状态：** 处理出错的帖子既不发布也不报错，用户不知道发生了什么。
