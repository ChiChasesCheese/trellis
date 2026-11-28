---
id: bagu-url-flow-3-tcp-tls
node: a.net.url-flow
type: qa
step: 3
---
## Q
**建连 · TCP 和 TLS 各几个往返，怎么优化**｜必会

面试官：「HTTPS 请求发出第一个字节之前，要花几个往返？怎么优化？」

## A
**基本回答。** TCP 三次握手 1 个 RTT（往返时延）；TLS 1.3 再 1 个，TLS 1.2 要 2 个。所以全新 HTTPS 连接发请求前，TLS 1.3 花 2 个、1.2 花 3 个 RTT；复用已有连接是 0 个，是最大的优化。TLS 1.3 省一个来回，因为 `ClientHello` 直接带 ECDHE 公钥，服务端一次回包就算出密钥并发证书和 Finished。优化：少建连（keep-alive、HTTP/2 复用）、少握手（TLS 会话恢复）、升级 TLS 1.3、OCSP stapling（服务端把吊销状态一并发来，客户端不必另外去查）；HTTP/3 基于 QUIC，把传输和 TLS 握手合并，新连接 1 个 RTT。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="14" y="2" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="194" y="2" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端</text>
<line x1="50" y1="24" x2="50" y2="182" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="230" y1="24" x2="230" y2="182" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="54" y1="50" x2="226" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="226.0,50.0 219.0,53.2 219.0,46.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="140" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SYN</text>
<line x1="226" y1="78" x2="54" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.0,78.0 61.0,74.8 61.0,81.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="140" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SYN+ACK</text>
<line x1="54" y1="112" x2="226" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="226.0,112.0 219.0,115.2 219.0,108.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="140" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ACK，随即 ClientHello</text>
<line x1="226" y1="140" x2="54" y2="140" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="54.0,140.0 61.0,136.8 61.0,143.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="140" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ServerHello+证书+Finished</text>
<line x1="54" y1="170" x2="226" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="226.0,170.0 219.0,173.2 219.0,166.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="140" y="165" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Finished + HTTP 请求</text>
<line x1="296" y1="38" x2="296" y2="80" stroke-width="1.2" stroke="currentColor"/>
<text x="302" y="56" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">TCP</text>
<text x="302" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 RTT</text>
<line x1="296" y1="98" x2="296" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="302" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">TLS</text>
<text x="302" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 RTT</text>
<text x="4" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">TLS 1.3：发请求前共 2 个 RTT</text>
<text x="4" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TLS 1.2：握手多一个来回，共 3 个</text>
<text x="4" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">复用已有连接：0 个</text>
</svg>
每对箭头是 1 个 RTT：TCP 一个，TLS 1.3 一个，客户端在第二个来回里随 Finished 发出第一个 HTTP 请求；1.2 握手多一个来回。
**0-RTT。** TLS 1.3 恢复连接可在第一个包带数据，但可能被攻击者原样重放，只能用于幂等请求（GET 查询），不能下单扣款。
**业务场景。** 东南亚用户到机房 RTT 约 200 ms：TLS 1.2 请求发出前 TCP 200 + TLS 400 = 600 ms，升级 1.3 降到 400 ms，复用已有连接为 0。
**容易错。**
- **把 TLS 1.3 的 1 个 RTT 当总开销：** 前面还有 TCP 的 1 个；合并成 1 个的是 HTTP/3。
- **以为 0-RTT 随便用。**
- **以为 HTTPS 慢是因为加解密：** 慢在多出来的往返，距离越远越明显。
