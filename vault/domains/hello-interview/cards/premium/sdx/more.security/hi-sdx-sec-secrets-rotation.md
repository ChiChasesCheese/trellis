---
id: hi-sdx-sec-secrets-rotation
node: more.security
type: qa
step: 19
---
## Q
**不重启、不丢请求地轮换密钥**｜补充 · 安全 · 追问

面试官：「怎样在不重启服务、不丢一个请求的前提下，轮换数据库密码或 JWT 签名密钥？」

## A
**结论。** 不要一次性切换，要有两个版本同时有效的重叠窗口。被消费的密钥（数据库密码）先并行创建新凭据，客户端热加载，确认旧凭据零使用后再吊销。签名密钥则在公钥集里同时发布新旧公钥，用新密钥签名，新旧都能验证，直到旧令牌全部过期再删旧密钥。

**要点。**
- **数据库密码：** 双用户或双密码方案，新旧并存。
- **客户端热加载：** 监听密钥挂载、认证失败时重新获取，或用短期租约强制重取。
- **吊销旧凭据：** 遥测显示旧凭据零使用后才吊销。
- **签名密钥：** 先在公钥集（JWKS）发布带新密钥编号（kid）的公钥，等验证方都拿到，再改用新密钥签名，验证两把都接受。
- **什么时候删旧：** 旧密钥签的令牌全部过期之后。
- **设计规则：** 只在启动时读取密钥的服务，让轮换变成故障；热加载要从第一天做进去。

**为什么。** 分布式系统里各节点不可能在同一瞬间更新密钥。让新旧并存，就容忍了传播时间差。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">公钥集（JWKS）里的两把密钥</text>
<text x="8" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧 kid1</text>
<rect x="70" y="36" width="100" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="76" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">签名 + 验证</text>
<rect x="170" y="36" width="80" height="22" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<text x="176" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">仅验证</text>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新 kid2</text>
<rect x="120" y="80" width="50" height="22" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<text x="124" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">仅验证</text>
<rect x="170" y="80" width="160" height="22" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="176" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">签名 + 验证</text>
<line x1="120" y1="28" x2="120" y2="112" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="170" y1="28" x2="170" y2="112" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="250" y1="28" x2="250" y2="112" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="120" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">发布 kid2</text>
<text x="250" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">旧令牌已过期</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">切换签名</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先发布新公钥，等验证方都拿到</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再改用新密钥签名，新旧都能验</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">旧令牌过期后才删除旧公钥</text>
</svg>

**面试里这样说。** 「我用重叠窗口轮换：数据库先建新凭据，服务热加载后再吊销旧的；JWT 在 JWKS 里同时发布新旧 kid，用新的签名、两个都验证，旧令牌过期后再下线旧公钥。」

**易错。**
- **原子替换：** 还没拿到新值的节点瞬间认证失败。
- **只在启动时读密钥：** 轮换必须重启，等于一次发布。
- **旧密钥过早删除：** 仍在有效期的令牌全部验证失败。
