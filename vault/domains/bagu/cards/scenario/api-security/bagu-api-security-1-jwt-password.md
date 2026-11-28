---
id: bagu-api-security-1-jwt-password
node: b.scenario.api-security
type: qa
step: 1
---
## Q
**接口安全 · JWT、密码存储与防刷**｜追问

面试官：「JWT 有什么风险，怎么防篡改？密码怎么传输和存储？登录接口被撞库怎么防？」

## A
**基本回答。** JWT 由 Header、Payload、Signature 三段组成。签名防篡改：服务端用密钥重算比对，固定算法并拒绝 `alg=none`，密钥要保管和轮换；Payload 只是 Base64 编码，谁都能读，不放敏感信息。风险是无状态难吊销（注销、改权限要等过期）、被盗可重放；做法是短期 access token 加 refresh token，要立即失效就查黑名单（这又引入了状态）。令牌放 Authorization 头能避开 CSRF，但存 localStorage 会被 XSS 偷走；放 Cookie 要设 HttpOnly、Secure、SameSite。密码走 HTTPS，服务端只存「随机盐加慢哈希」（bcrypt、argon2）：慢哈希抬高暴力破解成本，盐让相同密码的哈希不同、防彩虹表；MD5、SHA 太快不能用。撞库要按 IP 和按账号两个维度限流（Redis 记失败次数），失败多次出验证码或临时锁定；攻击者用大量代理、每号只试一两次时，单维度拦不住，还要看全局失败率并筛查已泄露的密码。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">JWT = Header . Payload . Signature</text>
<rect x="6" y="22" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Header</text>
<rect x="108" y="22" width="124" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Payload</text>
<rect x="238" y="22" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286.0" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Signature</text>
<text x="54" y="68" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">算法、类型</text>
<text x="170" y="68" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Base64 编码，不加密</text>
<text x="286" y="68" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">防篡改</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">服务端用密钥重算签名再比对</text>
<text x="8" y="110" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">固定算法，拒绝 alg=none</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">密码存储</text>
<rect x="6" y="148" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">密码</text>
<rect x="80" y="148" width="72" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116.0" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+ 随机盐</text>
<rect x="170" y="148" width="104" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="222.0" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bcrypt/argon2</text>
<rect x="290" y="148" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="312.0" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存</text>
<line x1="62" y1="162" x2="78" y2="162" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,162.0 71.0,165.2 71.0,158.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="152" y1="162" x2="168" y2="162" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168.0,162.0 161.0,165.2 161.0,158.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="274" y1="162" x2="288" y2="162" stroke-width="1.2" stroke="currentColor"/>
<polygon points="288.0,162.0 281.0,165.2 281.0,158.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">HTTPS 传输；服务端从不存明文</text>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">撞库：按 IP、按账号两个维度限流</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">失败多次 → 验证码 / 临时锁定</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">JWT 难吊销：短期 token + refresh，黑名单</text>
</svg>
上半部分是 JWT 三段：Payload 只是编码，Signature 用密钥算出、防篡改。下半部分是密码存储：加随机盐，过慢哈希，只存哈希结果。
**业务场景。** 账号被盗被封后，已发出的 access token（30 分钟）仍有效，攻击者还能提现；对被封用户的令牌编号（jti）在网关查黑名单，命中即拒绝，才能立即失效。两个用户都用 `abc123`，盐不同则哈希完全不同，数据库泄露后彩虹表也对不上。
**容易错。**
- **以为 JWT 能随时注销：** 无状态，要等过期。
- **只按 IP 限流：** 攻击者换代理就绕过，要加账号维度。
