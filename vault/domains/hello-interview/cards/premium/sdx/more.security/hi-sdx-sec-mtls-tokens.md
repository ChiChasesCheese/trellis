---
id: hi-sdx-sec-mtls-tokens
node: more.security
type: qa
step: 17
---
## Q
**服务间认证：mTLS 与令牌各证明什么**｜补充 · 安全 · 追问

面试官：「服务间认证常把 mTLS 和签名令牌一起用。各自证明了对方无法证明的什么？」

## A
**结论。** mTLS 在通道层证明工作负载身份：这条连接确实来自 billing-service，并且加密。令牌携带每个请求的声明：代表哪个用户、有什么权限、给谁用、何时过期。前者回答「哪个服务在调用」，后者回答「以什么权限、为谁、这次请求」。

**要点。**
- **mTLS 证明：** 连接两端用证书互相认证（证书由 SPIFFE 或服务网格 CA 签发），并加密传输。
- **mTLS 做不到：** 同一条连接上的每个请求看起来都一样，不说明代表谁。
- **令牌证明：** 用户标识、范围、受众、过期时间，每个请求都不同。
- **令牌做不到：** 本身不认证通道，被泄露后可被重放。
- **为什么要一起：** 仅有服务身份会造成混淆代理，仅有令牌则没有通道层的身份与保护。

**为什么。** 两者处在不同层次，证明的主体不同：一个是机器，一个是请求背后的人和权限。深度防御要两层都有。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="8" y="14" width="100" height="50" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58" y="35.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">billing</text>
<text x="58" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调用方</text>
<rect x="232" y="14" width="100" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="35.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">orders</text>
<text x="282" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被调方</text>
<text x="170" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">通道 mTLS</text>
<polyline points="108,34 232,34" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="232,34 225.7,37.0 225.7,31.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">请求 令牌</text>
<polyline points="108,64 232,64" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="232,64 225.7,67.0 225.7,61.0" fill="currentColor"/>
<rect x="8" y="108" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">mTLS 回答：哪个服务在调用</text>
<text x="170" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">证书由网格 CA 签发，通道加密</text>
<rect x="8" y="164" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="182.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌回答：代表谁、什么权限、给谁</text>
<text x="170" y="197.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户、scope、aud、过期时间</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缺一层都留有漏洞</text>
</svg>

**面试里这样说。** 「服务间我用 mTLS 证明是哪个工作负载在调用，再用令牌携带终端用户和范围。前者回答哪个服务，后者回答代表谁、有什么权限，二者缺一都留有漏洞。」

**易错。**
- **只靠 mTLS：** 服务可以代任何用户行事，等于混淆代理。
- **只靠令牌：** 没有通道保护，令牌泄露即可重放。
- **证书长期不轮换：** 泄露后长期有效，应使用短寿命证书。
