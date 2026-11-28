---
id: bagu-request-signing-keys-1-hmac-rotation
node: b.scenario.request-signing-keys
type: qa
step: 1
---
## Q
**请求签名 · HMAC、防重放与密钥轮换**｜必会

面试官：「渠道给我们回调，我们也给商户回调：怎么证明请求没被伪造、没被篡改、不是旧请求重放？签名密钥要怎么不停机地换？」

## A
**基本回答。** 双方共享密钥，发送方对 `时间戳 + "." + 原始请求体` 算 HMAC-SHA256，时间戳和签名放请求头；接收方重算并恒定时间比较，拒绝时间戳与当前相差超过约 5 分钟的请求。TLS 只保护通道，证明不了请求确实来自对方，也挡不住旧请求原样重发；签名把来源和内容绑在请求上。要对收到的原始字节签名：先解析再序列化会改变空白和字段顺序，签名对不上。时间戳在签名里改不了，窗口外的旧请求拒收；窗口内仍可重放，严格场景再缓存 nonce 或事件号，TTL 不短于窗口，见过就拒。普通 `==` 遇到第一个不同字节就返回，耗时泄露已匹配的前缀长度，会被逐字节猜出签名，所以必须恒定时间比较。对称签名双方都持有密钥，接收方也能伪造，要让对方无法伪造用非对称（私钥签、公钥验）。密钥放 KMS（集中保管、鉴权、审计，信封加密）或 HSM（防篡改硬件，密钥不出硬件）。不停机轮换：头里带 kid，新密钥先下发，重叠期两把都接受，发送方切换后，旧 kid 流量归零才作废；直接换会让对方未切换时全部验签失败。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<rect x="8" y="12" width="120" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="33.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发送方</text>
<text x="68" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">HMAC(密钥, t.体)</text>
<line x1="128" y1="37" x2="214" y2="37" stroke-width="1.2" stroke="currentColor"/>
<polygon points="214.0,37.0 207.0,40.2 207.0,33.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<text x="171" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t、kid、sig</text>
<rect x="214" y="12" width="118" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="273" y="33.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接收方</text>
<text x="273" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用同样方式重算</text>
<text x="8" y="88" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1. 现在与 t 相差超过 5 分钟，就拒收</text>
<text x="8" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2. 按 kid 找到密钥，对 t.原始请求体 重算</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3. 恒定时间比较 sig，不一致就拒收</text>
<line x1="8" y1="138" x2="332" y2="138" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不停机轮换密钥</text>
<rect x="8" y="166" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只用 k1</text>
<rect x="116" y="166" width="120" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="176" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1、k2 都接受</text>
<rect x="248" y="166" width="84" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只用 k2</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发送方切到 k2，旧 kid 流量归零后作废 k1</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">头里带 kid，接收方才知道该用哪把密钥验</text>
</svg>
上半部分是一次请求怎么签、怎么验；下半部分是换密钥时新旧两把都认的重叠期。
**举个例子。** 渠道回调：取 t=1700000000，用 k2 对 `t.原始请求体` 算 HMAC，头里放 `t=…, kid=k2, sig=…`；我们收到时只差 40 秒，按 kid 取 k2 重算，恒定时间比较通过。20 分钟后有人原样重发，时间差超 5 分钟被拒；3 分钟内重发时间窗挡不住，靠缓存的 nonce 或事件号。轮换期里仍带 kid=k1 的回调也能验过，k1 没流量后才作废，中途没有一笔回调被拒。
**容易错。**
- **以为 HTTPS 就够了：** TLS 管通道，签名管来源和内容，各管一层。
