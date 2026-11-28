---
id: hi-sdx-sec-oauth-code-pkce
node: more.security
type: qa
step: 4
---
## Q
**授权码流程为什么先给 code，PKCE 加了什么**｜补充 · 安全 · 必会

面试官：「OAuth2 授权码流程里，客户端为什么在重定向里只拿到一个 code，再去换令牌，而不是直接收到令牌？PKCE 又加了什么保护？」

## A
**结论。** 重定向要经过浏览器（地址栏、历史、Referer、扩展），是不可信通道。一次性的短命 code 在那里没用，令牌只在客户端直连令牌端点的后端通道里发放。PKCE 把 code 绑定到发起流程的那一方，被截获的 code 兑换不了。

**要点。**
- **前端通道：** 重定向走浏览器，URL 里的内容会进历史、日志、Referer。
- **后端通道：** 客户端用 code 直连令牌端点换令牌，令牌不经过浏览器地址栏。
- **PKCE 发起：** 客户端随机生成 code_verifier，把它的 SHA-256 哈希（code_challenge）随授权请求发出。
- **PKCE 兑换：** 换令牌时必须出示原始 verifier，服务端哈希后比对，不一致就拒绝。
- **适用范围：** 没有客户端密钥的公共客户端（单页应用、手机应用）必须用（RFC 9700）；机密客户端也推荐用，OAuth 2.1 草案则要求所有客户端都用。

**为什么。** 攻击者能截获 code（恶意应用抢注重定向地址），但拿不到 verifier，所以兑换失败。PKCE 防的是 code 截获，不是令牌在客户端的保管问题。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="6" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 客户端生成 verifier</text>
<text x="170" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">challenge = SHA256(verifier)</text>
<polyline points="170,50 170,64" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,64 167.0,57.7 173.0,57.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="64" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 浏览器跳到授权服务器</text>
<text x="170" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">请求里带 challenge</text>
<polyline points="170,108 170,122" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,122 167.0,115.7 173.0,115.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="122" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 用户登录同意，回调带 code</text>
<text x="170" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前端通道：code 可能被截获</text>
<polyline points="170,166 170,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,180 167.0,173.7 173.0,173.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="180" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 客户端直连令牌端点</text>
<text x="170" y="213.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后端通道：出示 code + verifier</text>
<polyline points="170,224 170,238" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,238 167.0,231.7 173.0,231.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="238" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="256.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑤ 服务端比对 SHA256(verifier)</text>
<text x="170" y="271.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一致才发令牌</text>
</svg>

**面试里这样说。** 「授权码走前端通道，令牌走后端通道。我加 PKCE：发起时带 code_challenge，兑换时带 code_verifier，被截获的 code 没有 verifier 就换不到令牌。公共客户端必须用，我对所有客户端都开。」

**易错。**
- **用隐式流程：** 令牌直接出现在 URL 片段里，已被废弃。
- **公共客户端放密钥：** 打包进应用的密钥等于公开。
- **verifier 可预测：** 必须是高熵随机数。
