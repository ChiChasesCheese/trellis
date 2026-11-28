---
id: bagu-webhook-ssrf-1-merchant-url
node: b.scenario.webhook-ssrf
type: qa
step: 1
---
## Q
**Webhook · 商户回调地址的 SSRF 防护**｜加分

面试官：「商户可以填任意回调 URL，平台服务器替他发请求。恶意商户填内网地址会怎样？校验了 IP 为什么还要防 DNS 重绑定？」

## A
**基本回答。** SSRF（服务端请求伪造）：商户可填任意回调 URL，平台服务器在内网里，能访问商户够不到的云元数据服务（`169.254.169.254`，含临时凭证）和内网管理接口，状态码、耗时甚至响应内容都成了探测通道。防护：发送前解析域名，拒绝回环（`127.0.0.0/8`、`::1`）、私网（`10/8`、`172.16/12`、`192.168/16`、`fc00::/7`）、链路本地（`169.254.0.0/16`、`fe80::/10`）、`0.0.0.0/8` 和 `100.64.0.0/10`，并处理 `::ffff:10.0.0.1` 这类映射写法和整数形式 IP，要解析成 IP 后按网段判断，字符串黑名单会被绕过。DNS 重绑定：恶意域名第一次解析给公网 IP 通过校验，TTL 极短，连接时再解析变成 `127.0.0.1`；所以只解析一次，校验这个 IP 并直连，HTTPS 的 SNI 和 Host 仍用原域名。重定向是第二条后路：默认不跟随，必须跟随时每一跳重新解析、重新校验。另限制只允许 https 和固定端口、设连接与总超时、限响应体大小，响应不回显给商户只记状态码。网络层再隔离：worker 放独立网段，安全组默认拒绝内网和元数据地址，只放行经专用出站代理的公网流量；IMDSv2 是再加一层，不能代替它们。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="8" y="8" width="186" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">商户填回调 URL</text>
<line x1="101" y1="42" x2="101" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="101.0,62.0 97.8,55.0 104.2,55.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="62" width="186" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">解析域名，只解析一次</text>
<line x1="101" y1="96" x2="101" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="101.0,116.0 97.8,109.0 104.2,109.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="116" width="186" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="101" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">校验这个 IP 不是内部地址</text>
<line x1="101" y1="150" x2="101" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="101.0,170.0 97.8,163.0 104.2,163.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="170" width="186" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直连这个 IP，不跟随重定向</text>
<line x1="101" y1="204" x2="101" y2="224" stroke-width="1.2" stroke="currentColor"/>
<polygon points="101.0,224.0 97.8,217.0 104.2,217.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="224" width="186" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101" y="245" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">独立网段，经出口代理</text>
<text x="204" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">若连接时再解析：</text>
<text x="204" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">公网 IP 变成</text>
<text x="204" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">127.0.0.1</text>
<text x="204" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拒绝这些网段</text>
<text x="204" y="36" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">127/8、::1</text>
<text x="204" y="52" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10/8、192.168/16</text>
<text x="204" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">172.16/12、fc00::/7</text>
<text x="204" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">169.254/16 元数据</text>
<text x="204" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只放行 https</text>
<text x="204" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">固定端口、有超时</text>
<text x="204" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应不回显</text>
</svg>
左边是投递一次回调的五步，核对和直连用同一个 IP；右边是每一步要守的规矩。
**举个例子。** 恶意商户想拿元数据服务凭证：直接填 `http://169.254.169.254/...` 第一步就被拒；换成 evil.com，第一次解析给公网 IP 通过，若连接时再解析就变成 `127.0.0.1`，所以直连校验过的 IP；evil.com 返回 302 指向 `http://10.0.0.5/admin`，不跟随到此为止；应用层漏了，独立网段加安全组也发不出请求，响应不回显也探测不到。控制台「发送测试事件」若回显响应体，凭证就被带出。
**容易错。**
- **校验一次、连接再解析一次：** 两次解析之间 DNS 可以变，校验的 IP 和连接的 IP 必须是同一个。
