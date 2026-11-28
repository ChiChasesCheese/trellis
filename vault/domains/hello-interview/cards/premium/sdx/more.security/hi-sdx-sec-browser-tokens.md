---
id: hi-sdx-sec-browser-tokens
node: more.security
type: qa
step: 11
---
## Q
**单页应用的令牌放哪里：BFF**｜补充 · 安全 · 追问

面试官：「隐式流程为什么被废弃？用授权码加 PKCE 替代之后，单页应用拿到的令牌今天应该存在哪里？」

## A
**结论。** 隐式流程把访问令牌放在 URL 片段里，会泄露到历史、Referer、日志和扩展，没有绑定也不能发刷新令牌。PKCE 解决的是 code 被截获，不解决令牌被 XSS 偷走。当前默认做法是 BFF（backend for frontend）：令牌留在服务端，浏览器只拿 HttpOnly 的会话 Cookie。

**要点。**
- **隐式流程的缺陷：** 令牌在 URL 片段、没有客户端认证和 PKCE、不能刷新，只能长令牌或隐藏 iframe 续期，后者被第三方 Cookie 限制打断。
- **PKCE 不管保管：** SPA 里仍然持有一个 JS 可读的持有者令牌，XSS 或被污染的 npm 依赖可以外传。
- **BFF：** 服务端组件执行授权码加 PKCE，在服务端保存访问令牌和刷新令牌，浏览器只有 HttpOnly、Secure、SameSite 的会话 Cookie，API 调用由 BFF 代理。
- **必须放浏览器时：** 仅放内存，不放 localStorage；访问令牌寿命短；刷新令牌轮换并检测重用；最好用 DPoP（把令牌绑定到客户端密钥对，没有私钥就无法重放）绑定发送方。

**为什么。** 令牌一旦能被页面脚本读到，任何脚本注入都能取走。让令牌根本不进浏览器，是消除这个风险最彻底的办法。

**面试里这样说。** 「单页应用我用 BFF：服务端完成授权码加 PKCE，令牌留在服务端，浏览器只拿 HttpOnly 的会话 Cookie。必须放在浏览器时只放内存，短寿命，刷新令牌轮换，最好再用 DPoP。」

**易错。**
- **令牌放 localStorage：** XSS 一次就全部拿走。
- **以为 PKCE 能防 XSS：** 它只防授权码被截获。
- **BFF 的会话 Cookie 不设 SameSite：** 换来 CSRF 风险。
