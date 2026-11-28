---
id: hi-sdx-sec-webauthn
node: more.security
type: qa
step: 14
---
## Q
**通行密钥登录：服务器存什么、验什么**｜补充 · 安全 · 追问

面试官：「系统层面，服务器为每个通行密钥存什么？每次登录必须验证哪些东西？」

## A
**结论。** 注册时服务器发随机挑战，认证器生成绑定 RP ID 的密钥对，服务器保存凭据 ID、公钥、用户句柄等。登录时发新挑战，认证器对 authenticatorData 与 clientDataJSON 的哈希签名，服务器验签名、挑战、域名、RP ID 哈希和用户在场（UP）或已验证（UV）标志。

**要点。**
- **存什么：** credential_id、public_key、user_handle（不透明的用户 ID，不是邮箱）、签名计数器、传输方式。
- **验签名：** 用保存的公钥验证对应 credential_id 的签名。
- **验挑战：** 必须等于刚发出的，且一次性使用，这是防重放的关键。
- **验域名：** clientDataJSON 的 origin 是预期域名，rpIdHash 等于你的 RP ID 哈希。
- **验标志：** UP 必须置位；无密码登录或升级验证时 UV 也必须置位。
- **设计影响：** RP ID 写进每个凭据，应选可注册域名（如 example.com）以便所有子域共用，以后更换域名会使所有凭据失效；同步型通行密钥的计数器恒为 0，不能靠计数器回退检测克隆；每个用户存多个凭据。

**为什么。** 每一步校验对应一种攻击：挑战防重放，域名与 RP ID 防钓鱼，UV 防他人拿着设备直接登录。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="6" width="150" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务器</text>
<rect x="182" y="6" width="150" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">认证器（设备）</text>
<polyline points="83,42 83,74" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83,74 80.0,67.7 86.0,67.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="92" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 随机挑战</text>
<rect x="182" y="74" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 签名</text>
<text x="257" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">authData + 哈希</text>
<polyline points="257,118 257,144" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257,144 254.0,137.7 260.0,137.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="150" y="140" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 签名</text>
<rect x="8" y="150" width="324" height="100" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 服务器逐项验证</text>
<text x="170" y="189" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">公钥验签（按 credential_id）</text>
<text x="170" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挑战等于刚发的，且一次性</text>
<text x="170" y="219" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">origin 与 rpIdHash 正确</text>
<text x="170" y="234" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UP 置位；需要时 UV 也置位</text>
<text x="8" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">凭据而非用户，是注册与吊销的单位</text>
</svg>

**面试里这样说。** 「我为每个凭据存 credential_id、公钥、用户句柄和计数器。登录时发一次性挑战，验签名、挑战、origin、rpIdHash 和 UP 或 UV 标志。RP ID 选主域名，每个用户允许多个凭据。」

**易错。**
- **挑战可复用：** 同一份签名可被重放。
- **用邮箱当用户句柄：** 泄露个人信息，且邮箱会变。
- **依赖计数器检测克隆：** 同步型通行密钥计数器恒为 0。
