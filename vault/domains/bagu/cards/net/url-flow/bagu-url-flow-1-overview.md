---
id: bagu-url-flow-1-overview
node: a.net.url-flow
type: qa
step: 1
---
## Q
**输入网址回车 · 全流程骨架**｜必会

面试官：「在浏览器输入一个网址按回车，到网页显示出来，中间发生了什么？先给我一个 30 秒的整体流程。」

## A
**基本回答。** 八步：解析 URL 并查 HSTS 与强缓存 → DNS 解析 → TCP 三次握手 → TLS 握手 → 发 HTTP 请求 → 服务端处理（CDN、负载均衡、网关、应用、缓存、数据库）→ 浏览器解析渲染 → 连接复用或关闭。DNS 回答「去哪」，TCP 提供可靠通道，TLS 提供加密和身份，HTTP 说明「要什么」。第 1 步先看本地：HSTS 是浏览器自己记住的规则，直接把 `http://` 改成 `https://`，根本不先发明文请求，防第一跳被劫持（不是服务端 301）；强缓存命中则后面七步全省，不发任何请求（要问服务端「变了没」的是协商缓存）。顺序是先 TCP 再 TLS，TLS 跑在 TCP 之上。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 188">
<rect x="3" y="8" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 查缓存</text>
<text x="38" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先看 HSTS</text>
<line x1="74" y1="30" x2="90" y2="30" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,30.0 83.0,33.2 83.0,26.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="91" y="8" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 DNS</text>
<text x="126" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">去哪？</text>
<line x1="162" y1="30" x2="178" y2="30" stroke-width="1.2" stroke="currentColor"/>
<polygon points="178.0,30.0 171.0,33.2 171.0,26.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="179" y="8" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="214" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 TCP</text>
<text x="214" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可靠通道</text>
<line x1="250" y1="30" x2="266" y2="30" stroke-width="1.2" stroke="currentColor"/>
<polygon points="266.0,30.0 259.0,33.2 259.0,26.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="267" y="8" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 TLS</text>
<text x="302" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加密+身份</text>
<rect x="3" y="86" width="70" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="38" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5 HTTP</text>
<text x="38" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要什么</text>
<line x1="74" y1="108" x2="90" y2="108" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,108.0 83.0,111.2 83.0,104.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="91" y="86" width="70" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6 服务端</text>
<text x="126" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">网关→DB</text>
<line x1="162" y1="108" x2="178" y2="108" stroke-width="1.2" stroke="currentColor"/>
<polygon points="178.0,108.0 171.0,111.2 171.0,104.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="179" y="86" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="214" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7 渲染</text>
<text x="214" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DOM+CSS</text>
<line x1="250" y1="108" x2="266" y2="108" stroke-width="1.2" stroke="currentColor"/>
<polygon points="266.0,108.0 259.0,111.2 259.0,104.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="267" y="86" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8 复用</text>
<text x="302" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">keep-alive</text>
<line x1="302" y1="52" x2="302" y2="70" stroke-width="1.2" stroke="currentColor"/>
<line x1="302" y1="70" x2="38" y2="70" stroke-width="1.2" stroke="currentColor"/>
<line x1="38" y1="70" x2="38" y2="85" stroke-width="1.2" stroke="currentColor"/>
<polygon points="38.0,85.0 34.8,78.0 41.2,78.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="4" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">后端岗位把时间花在第 5、6 步（高亮）</text>
<text x="4" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每一步都要能说出：可能出什么问题、怎么观测</text>
</svg>
八格是时间顺序；高亮的 5、6 步是后端岗位花时间的地方。每一步都要能说出可能出什么问题、怎么观测。
**业务场景。** 首次访问 `https://example.com/app.js`，RTT 50 ms：TCP 1 个 RTT 50 ms，TLS 1.3 再 50 ms，还没发出任何业务字节已经 100 ms（不含 DNS）；响应头带 `Cache-Control: max-age=31536000`，第二次访问强缓存命中，0 个请求、0 ms 网络耗时。
**容易错。**
- **以为 HTTPS 先 TLS 再 TCP。**
- **以为强缓存命中还要问服务端。**
- **只会背八步、答不出故障现象：** DNS 失败是「找不到服务器」，TLS 失败是证书错误提示。
