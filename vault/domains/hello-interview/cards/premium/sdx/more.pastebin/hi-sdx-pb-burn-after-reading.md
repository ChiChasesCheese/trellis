---
id: hi-sdx-pb-burn-after-reading
node: more.pastebin
type: qa
step: 2
---
## Q
**阅后即焚：原子条件更新，响应不可缓存**｜补充 · 文本分享（Pastebin） · 追问

面试官：「Pastebin 支持『阅后即焚』，链接只能成功读一次。两个人几乎同时打开链接，怎么保证只有一个人看到内容？CDN 要怎么配？」

## A
**结论。** 在权威存储上做一次原子条件更新，只有真正把 consumed 从 false 改成 true 的那个请求能拿到内容；响应标记为不可缓存，绝不能被 CDN 或浏览器存下来。

**要点。**
- **两步会竞态：** 先读再删，两个请求可能都读到内容，再各自删除，破坏「只读一次」。
- **原子条件更新：** `UPDATE paste SET consumed = true WHERE id = ? AND consumed = false`，影响 1 行才返回正文（或用 DELETE … RETURNING）。
- **落在线性一致的权威副本：** 不能在只读副本或区域缓存上判断，否则不同区域各自认为自己是第一次。
- **不能缓存：** 第一次成功响应若被边缘缓存，后面所有请求都从边缘拿到内容，根本到不了源站的条件更新。用 `Cache-Control: no-store`。
- **链接预览会烧掉链接：** 聊天软件会先访问一次链接做预览。常见做法是 GET 只显示确认页，用户点击后用 POST 才读取并销毁。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<rect x="10" y="20" width="70" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="45.0" y="39.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 A</text>
<rect x="10" y="100" width="70" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="45.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 B</text>
<rect x="210" y="50" width="120" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="270.0" y="68.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">权威存储</text>
<text x="270.0" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">consumed = false</text>
<polyline points="80,35 210,60" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210.0,60.0 203.7,55.5 202.5,61.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="120" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件更新</text>
<polyline points="80,115 210,86" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210.0,86.0 202.5,84.4 203.9,90.6" style="fill:var(--accent,#3b6fd4)"/>
<text x="120" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件更新</text>
<text x="10" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">A：影响 1 行 → 返回内容</text>
<text x="10" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B：影响 0 行 → 404</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应 Cache-Control: no-store</text>
</svg>

**面试里这样说。** 「读和销毁必须是一个原子的条件更新，只有影响一行的请求返回内容，并且落在权威副本上。响应加 no-store，否则 CDN 会把第一次的内容发给后面所有人。为防预览机器人烧链接，GET 只显示确认页，POST 才销毁。」

**易错。**
- **先 SELECT 再 DELETE：** 并发下两个请求都能看到内容。
- **在区域副本上判断：** 跨区域各自都是「第一次」。
