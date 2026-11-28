---
id: bagu-url-flow-4-server-side
node: a.net.url-flow
type: qa
step: 4
---
## Q
**请求到服务端 · 经过哪些层、负载均衡怎么选**｜必会

面试官：「HTTP 请求发出去之后，怎么到达具体的服务，服务端又做了什么？」

## A
**基本回答。** 请求先到 CDN 或边缘节点（命中直接返回，动态接口回源）；再经负载均衡、反向代理（Nginx，可做 TLS 终止）、网关（认证、限流、路由）、应用服务（先查缓存，没有再查库），生成响应。拆这么多层是为了每层只做一件事，出问题看哪层指标变了就知道找谁。负载均衡 L4 只看 IP 加端口、按连接转发（LVS、云 NLB），性能高；L7 解析 HTTP，可按路径、请求头路由，能做 TLS 终止和重试（Nginx、Envoy、云 ALB），更灵活、开销更大；通常 L4 在前扛量，L7 在后精细路由。负载均衡关心「发给哪台」，网关关心「能不能放行、去哪个服务」。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 282">
<rect x="6" y="4" width="128" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="21" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<rect x="6" y="42" width="128" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="70" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CDN / 边缘</text>
<text x="142" y="59" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中就直接返回</text>
<line x1="70" y1="30" x2="70" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,41.0 66.8,34.0 73.2,34.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="80" width="128" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">负载均衡</text>
<text x="142" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L4 看 IP+端口</text>
<text x="142" y="105" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L7 看 HTTP 内容</text>
<line x1="70" y1="68" x2="70" y2="79" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,79.0 66.8,72.0 73.2,72.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="118" width="128" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">反向代理 Nginx</text>
<text x="142" y="135" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TLS 终止、转发</text>
<line x1="70" y1="106" x2="70" y2="117" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,117.0 66.8,110.0 73.2,110.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="156" width="128" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关</text>
<text x="142" y="173" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">认证·限流·路由</text>
<line x1="70" y1="144" x2="70" y2="155" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,155.0 66.8,148.0 73.2,148.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="194" width="128" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="211" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用服务</text>
<text x="142" y="211" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只管业务</text>
<line x1="70" y1="182" x2="70" y2="193" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,193.0 66.8,186.0 73.2,186.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="232" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36" y="249" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存</text>
<rect x="74" y="232" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104" y="249" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<line x1="36" y1="220" x2="36" y2="231" stroke-width="1.2" stroke="currentColor"/>
<polygon points="36.0,231.0 32.8,224.0 39.2,224.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="104" y1="220" x2="104" y2="231" stroke-width="1.2" stroke="currentColor"/>
<polygon points="104.0,231.0 100.8,224.0 107.2,224.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="36" y1="220" x2="104" y2="220" stroke-width="1.2" stroke="currentColor"/>
<text x="142" y="249" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先缓存，没有再查库</text>
<text x="6" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每一层只做一件事，出问题好定位</text>
</svg>
自上而下是请求路径，高亮的 CDN 是第一道也最便宜的一关，右侧是每层职责。
**业务场景。** 点赞接口偶发 502：L7 把请求转给了正在发布重启的实例。502 多半是网关或负载均衡连不上后端或收到无效响应，对照健康检查记录和实例重启时间；靠健康检查摘除实例加有限次数重试，用户感知消失。
**容易错。**
- **以为 L4 和 L7 只是性能区别：** 本质是能不能看懂 HTTP 内容。
- **以为动态接口也走 CDN 缓存。**
- **遇到 502 就怪应用代码。**
