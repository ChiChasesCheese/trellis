---
id: bagu-http-basics-cache-1-get-post-cache
node: b.net.http-basics-cache
type: qa
step: 1
---
## Q
**HTTP 基础 · GET 与 POST、强缓存与协商缓存**｜追问

面试官：「GET 和 POST 有什么区别？强缓存和协商缓存是什么？静态资源更新后用户还看到旧文件，怎么办？」

## A
**基本回答。** GET 与 POST 的区别是语义约定：GET 取资源，安全、幂等、可缓存；POST 提交，不幂等。参数位置、大小限制都是约定和服务器配置，不是协议硬性规定，GET 带请求体语义未定义，很多中间件会丢弃。强缓存：`Cache-Control: max-age`（优先）或 `Expires` 有效期内，浏览器不发请求。协商缓存：带 `If-None-Match`（`ETag` 内容指纹，更精确）或 `If-Modified-Since`（`Last-Modified`，精度到秒）去问服务端，没变回 304、无响应体，省带宽但仍有一次往返。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 312">
<rect x="60" y="6" width="220" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器要一个资源</text>
<line x1="170" y1="32" x2="170.0" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,52 166.8,45.0 173.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="52" width="300" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="70.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地有副本，且没过期？</text>
<text x="170" y="85.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Cache-Control: max-age 或 Expires</text>
<line x1="81" y1="96" x2="81.0" y2="117.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,124 77.8,117.0 84.2,117.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="89" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<line x1="252" y1="96" x2="252.0" y2="117.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252,124 248.8,117.0 255.2,117.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="260" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<rect x="6" y="124" width="150" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="144.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">强缓存命中</text>
<text x="81" y="159.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不发请求，直接用本地</text>
<rect x="170" y="124" width="164" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252" y="144.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协商缓存：发请求</text>
<text x="252" y="159.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带 If-None-Match</text>
<line x1="252" y1="172" x2="252.0" y2="189.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252,196 248.8,189.0 255.2,189.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="170" y="196" width="164" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端对比 ETag</text>
<line x1="230" y1="224" x2="166.4" y2="251.2" stroke-width="1.2" stroke="currentColor"/>
<polygon points="160,254 165.2,248.3 167.7,254.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="280" y1="224" x2="283.8" y2="247.1" stroke-width="1.2" stroke="currentColor"/>
<polygon points="285,254 280.7,247.6 287.0,246.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="70" y="254" width="120" height="46" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130" y="273.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没变：304</text>
<text x="130" y="288.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无响应体，用本地</text>
<rect x="208" y="254" width="126" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271" y="273.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">变了：200</text>
<text x="271" y="288.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新内容 + 新 ETag</text>
</svg>
没过期直接用本地；过期或没有就发请求让服务端核对，没变 304，变了 200 加新内容。
**静态资源更新。** 静态资源设长时间强缓存，文件名带内容哈希，URL 变了旧缓存自然失效；HTML 入口不设强缓存，每次拿到指向新文件名的最新入口。CDN 同理，靠改 URL 或主动刷新。301 会被浏览器长期缓存，之后点击不到服务端。
**业务场景。** 活动页 `app.js` 设 `max-age=31536000` 一年，发布新版本但文件名不变，强缓存期内浏览器连请求都不发，部分用户一直加载旧版；改成 `app.3f9a1c.js` 并让新入口 HTML 引用它后解决。
**容易错。**
- **以为 304 不用发请求：** 请求已发，只是响应没内容。
- **更新静态资源不换文件名：** 强缓存期内用户不会来问。
- **短链接随手用 301：** 后续点击到不了服务端，统计不到。
