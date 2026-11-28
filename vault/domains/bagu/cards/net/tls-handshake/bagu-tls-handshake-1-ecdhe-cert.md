---
id: bagu-tls-handshake-1-ecdhe-cert
node: b.net.tls-handshake
type: qa
step: 1
---
## Q
**TLS / HTTPS · 握手、前向保密与证书**｜必会

面试官：「TLS 握手是怎么进行的？RSA 和 ECDHE 密钥交换有什么区别，什么是前向保密？证书怎么校验？」

## A
**基本回答。** 握手认证服务器身份并协商对称密钥；非对称加密慢，只用来建立密钥，数据用对称加密（AES-GCM 或 ChaCha20-Poly1305）。TLS 1.3 只要 1 个 RTT：`ClientHello` 直接带 ECDHE 公钥（key share），`ServerHello` 回自己的，双方已算出密钥，之后全部加密；服务端再发证书、`CertificateVerify`（私钥签握手内容）和 `Finished`，客户端验证后发 `Finished` 即传数据。TLS 1.2 要 2 个 RTT，且可用 RSA 密钥交换（服务器公钥加密预主密钥），没有前向保密；ECDHE 每次用临时密钥对、用后即弃，服务器私钥日后泄露也解不开已录下的流量。
**2026 亮点。** 前向保密防不了「先录密文、以后用量子计算机解」：主流浏览器和库（OpenSSL 3.5 起默认）已用 X25519+ML-KEM-768 混合密钥交换，代价是 ClientHello 的 key share 从 32 字节涨到约 1.2KB，可能撑成多个包，个别老旧中间设备处理不好；对接外部支付网关或银行专线前先验证兼容性。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 218">
<text x="70" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">客户端</text>
<text x="270" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">服务端</text>
<line x1="70" y1="22" x2="70" y2="190" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="270" y1="22" x2="270" y2="190" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="170" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ClientHello：ECDHE 公钥</text>
<line x1="70" y1="44" x2="270" y2="50" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="270.0,50.0 263.5,52.7 263.7,47.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ServerHello：公钥，此后加密</text>
<line x1="270" y1="88" x2="70" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="70.0,94.0 76.3,91.0 76.5,96.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">证书、签名、Finished</text>
<line x1="270" y1="128" x2="70" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,134.0 76.3,131.0 76.5,136.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Finished，然后传应用数据</text>
<line x1="70" y1="168" x2="270" y2="174" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,174.0 263.5,176.7 263.7,171.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="10" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只要 1 个 RTT（TLS 1.2 要 2 个）</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 158">
<rect x="8" y="12" width="150" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="83.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根 CA（在系统信任库）</text>
<line x1="83" y1="40" x2="83" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,58.0 80.1,51.6 85.9,51.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="58" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中间 CA</text>
<line x1="83" y1="86" x2="83" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,104.0 80.1,97.6 85.9,97.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="104" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="122.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务器证书</text>
<text x="176" y="30" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">校验清单：</text>
<text x="176" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每一级的签名</text>
<text x="176" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">有效期</text>
<text x="176" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">域名与 SAN 是否匹配</text>
<text x="176" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">是否被吊销（OCSP、CRL）</text>
<text x="10" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下级由上级签发，一路追到受信任的根</text>
</svg>
证书校验：服务器证书由中间 CA 签发，中间 CA 由根 CA 签发，根在系统信任库，逐级验签，再看有效期、域名与 SAN 是否匹配、是否被吊销（OCSP、CRL）。
**其他。** 会话恢复（session ticket / PSK）省掉证书和密钥交换；TLS 1.3 的 0-RTT 首包带数据，但可被原样重放（转账会执行两次），只能用于幂等请求。mTLS 让服务端也验客户端证书；HSTS 防降级，App 里证书固定防中间人。
**业务场景。** 支付 App 抓包失败：做了证书固定，只信任预置证书，中间人证书不被接受。
**容易错。**
- **以为 RSA 密钥交换也有前向保密：** 私钥泄露后录下的流量都能解开。
- **以为有 HTTPS 就不用签名：** TLS 保护通道，签名证明消息体来自平台。
- **以为 0-RTT 可用于所有请求。**
