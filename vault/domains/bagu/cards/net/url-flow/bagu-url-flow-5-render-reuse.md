---
id: bagu-url-flow-5-render-reuse
node: a.net.url-flow
type: qa
step: 5
---
## Q
**响应回来之后 · 浏览器怎么渲染、连接怎么复用**｜追问

面试官：「响应回到浏览器后，到画面出来，还要做什么？连接用完就关吗？」

## A
**基本回答。** 先看缓存：强缓存（`Cache-Control: max-age` / `Expires`）命中不发请求；过期则带 `If-None-Match` / `If-Modified-Since` 协商，没变回 304、无正文。拿到 HTML 解压后解析成 DOM，CSS 解析成 CSSOM，合成渲染树，再布局、绘制、合成。CSS 会阻塞渲染（没有样式算不出位置）；同步 JS 会阻塞 HTML 解析（脚本可能改 DOM）：`defer` 下载不阻塞、HTML 解析完按顺序执行，`async` 下载完立即执行、不保证顺序，有依赖的脚本用 `defer`。子资源在 HTTP/2 下并发复用同一条 keep-alive 连接。首屏慢先看关键资源的体积、是否压缩、是否被 JS 阻塞。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="4" y="6" width="160" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="84" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">强缓存命中</text>
<text x="84" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不发请求，直接用</text>
<rect x="176" y="6" width="160" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过期：带 ETag 去问</text>
<text x="256" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没变：304，无正文</text>
<rect x="4" y="66" width="110" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="59" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">HTML → DOM</text>
<rect x="4" y="102" width="110" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="59" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CSS → CSSOM</text>
<rect x="150" y="82" width="90" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="195" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渲染树</text>
<line x1="115" y1="80" x2="149" y2="94" stroke-width="1.2" stroke="currentColor"/>
<polygon points="149.0,94.0 141.3,94.3 143.7,88.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="115" y1="116" x2="149" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="149.0,104.0 143.5,109.3 141.3,103.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="195" y1="115" x2="195" y2="134" stroke-width="1.2" stroke="currentColor"/>
<line x1="195" y1="134" x2="54" y2="134" stroke-width="1.2" stroke="currentColor"/>
<line x1="54" y1="134" x2="54" y2="147" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,147.0 50.8,140.0 57.2,140.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="148" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">布局 layout</text>
<rect x="120" y="148" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">绘制 paint</text>
<rect x="236" y="148" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">合成 compose</text>
<line x1="105" y1="162" x2="119" y2="162" stroke-width="1.2" stroke="currentColor"/>
<polygon points="119.0,162.0 112.0,165.2 112.0,158.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="221" y1="162" x2="235" y2="162" stroke-width="1.2" stroke="currentColor"/>
<polygon points="235.0,162.0 228.0,165.2 228.0,158.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="4" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CSS 没解析完，渲染树就算不出来</text>
<text x="4" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同步 JS 会阻塞 HTML 解析：defer / async</text>
</svg>
顶部是缓存判断；中间 HTML 和 CSS 两条线汇合成渲染树；底部是把树变成像素的三步。
**业务场景。** 发版后用户仍加载旧 JS：静态资源文件名带内容哈希并设长强缓存，HTML 不缓存或用协商缓存，发版后新 HTML 指向新文件，不依赖缓存过期。
**容易错。**
- **混淆强缓存和协商缓存：** 前者不发请求，后者发请求但可能 304。
- **以为 JS 和 CSS 影响一样：** CSS 阻塞渲染，同步 JS 阻塞解析。
