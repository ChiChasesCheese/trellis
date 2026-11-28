---
id: hi-sdx-sec-confused-deputy
node: more.security
type: qa
step: 9
---
## Q
**混淆代理：只认调用方密钥就放行**｜补充 · 安全 · 必会

面试官：「内部报表服务能读所有租户的数据，对任何请求者都返回结果。一个低权限客户端请求了另一个租户的报表，也拿到了。这是哪类漏洞？API 密钥为什么不能单独作为多租户授权依据？」

## A
**结论。** 这是混淆代理（confused deputy）：有高权限的服务被诱骗用自己的权限替低权限调用方办事。API 密钥只说明「是哪个应用在调用」，不说明「代表谁、能看谁的数据」。授权要依据发起者身份，并在数据层校验。

**要点。**
- **定义：** 特权服务把自己的权限用在了没有该权限的调用方身上。
- **常见场景：** 内部服务信任网络内任何调用者；SSRF 打到云元数据地址（虚拟机是代理）；跨账号访问没有外部 ID。
- **API 密钥的含义：** 标识应用或租户，长期有效，没有用户上下文；适合服务间调用、计量和按客户限流。
- **用户令牌的含义：** 标识用户及范围，短期，携带真正代表用户行事的权限。
- **修法一：** 把终端用户或租户上下文一路传下去（代表用户的令牌交换、签名的用户上下文），在数据层检查。
- **修法二：** 缩小代理自身权限，如每租户一份凭据，使它即使被诱骗也越不了权。

**为什么。** 授权的主体必须是原始请求发起者。只验证「谁在敲门」而不验证「替谁敲门」，就让所有被代理的权限变成了公共权限。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="100" y="8" width="140" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">租户 A 的客户端</text>
<polyline points="170,44 170,72" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,72 167.0,65.7 173.0,65.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="64" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要租户 B 的报表</text>
<rect x="50" y="72" width="240" height="48" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">报表服务（代理）</text>
<text x="170" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">自己能读所有租户</text>
<polyline points="170,120 170,148" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,148 167.0,141.7 173.0,141.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="100" y="148" width="140" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">租户 B 的数据</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">漏洞：只验谁在敲门</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">修法：带上租户上下文，数据层校验</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">并让代理的凭据按租户划分</text>
</svg>

**面试里这样说。** 「我不会只按 API 密钥放行。服务间调用要把租户和用户上下文带下去，数据层校验 order 的租户等于令牌里的租户；同时给报表服务发按租户划分的凭据，让它想越权也做不到。」

**易错。**
- **信任内网调用方：** 一个被攻破的服务就能读所有租户。
- **只在入口校验：** 内部服务之间不再校验，代理照样越权。
- **API 密钥不做哈希存储和轮换：** 泄露后无法安全撤换。
