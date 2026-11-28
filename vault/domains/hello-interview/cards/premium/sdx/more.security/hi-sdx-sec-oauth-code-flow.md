---
id: hi-sdx-sec-oauth-code-flow
node: more.security
type: qa
step: 2
---
## Q
**授权码流程：两条通道**｜补充 · 安全：认证、OAuth、密码、授权 · 必会

用户在授权页点了「同意」以后，授权服务器为什么不直接把访问令牌放进跳转 URL 交给 App，而是先给一个一次性的 code，再让 App 拿 code 去换令牌？

## A
**结论。** 跳转经过浏览器，叫前端通道（front channel），URL 会进浏览器历史、日志和 Referer，可能被截获；所以这里只给一次性、几十秒过期的 code。令牌走 App 服务器直连授权服务器的后端通道（back channel），换令牌时 App 还要用密钥（client_secret）证明自己。

**要点。**
- **前端通道不可信：** 浏览器重定向的 URL 用户、插件、日志都看得到。
- **code 单独没用：** 一次性、很快过期，兑换时还要 client_id、client_secret 和注册过的 redirect_uri 全部对上。
- **后端通道可信：** 服务器到服务器的 HTTPS 请求，令牌不经过浏览器。
- **隐式流程已淘汰：** 早年的隐式流程（implicit）把令牌直接放进 URL，现在不推荐。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 352">
<rect x="8" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<polyline points="56,38 56,344" fill="none" stroke-width="1" stroke-dasharray="2 4" stroke="currentColor"/>
<rect x="122" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">App 服务器</text>
<polyline points="170,38 170,344" fill="none" stroke-width="1" stroke-dasharray="2 4" stroke="currentColor"/>
<rect x="236" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">授权服务器</text>
<polyline points="284,38 284,344" fill="none" stroke-width="1" stroke-dasharray="2 4" stroke="currentColor"/>
<polyline points="56,64 284,64" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="284,64 277,60.8 277,67.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 跳到授权页</text>
<text x="278" y="96" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">② 用户登录、点同意</text>
<polyline points="284,128 56,128" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="56,128 63,124.8 63,131.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 跳回 App，URL 带 code</text>
<text x="62" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前端通道：可能被截获</text>
<polyline points="56,172 170,172" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,172 163,168.8 163,175.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="113" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">code 交给后端</text>
<polyline points="170,214 284,214" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="284,214 277,210.8 277,217.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="222" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">④ 交 code + 密钥</text>
<polyline points="284,254 170,254" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,254 177,250.8 177,257.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="227" y="248" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">⑤ 访问令牌</text>
<text x="176" y="272" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后端通道：服务器直连</text>
<rect x="122" y="300" width="210" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="227.0" y="322.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑥ 带令牌调用银行 API</text>
</svg>

**面试里这样说。** 「我用授权码流程：前端通道只回传一次性的 code，App 后端拿 code 加 client_secret 走后端通道换令牌，令牌从不出现在浏览器 URL 里。」

**易错。**
- **令牌放进跳转 URL：** 会留在浏览器历史和各级日志里。
- **不校验 redirect_uri：** 攻击者可以把 code 引到自己的地址。
