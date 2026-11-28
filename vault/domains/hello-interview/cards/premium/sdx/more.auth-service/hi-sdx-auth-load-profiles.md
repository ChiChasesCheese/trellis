---
id: hi-sdx-auth-load-profiles
node: more.auth-service
type: qa
step: 1
---
## Q
**认证服务三类负载差几个数量级**｜补充 · 认证与身份服务 · 必会

面试官：「1.5 亿日活的认证服务，令牌校验、刷新令牌轮换、密码和账号凭据这三类操作，量级各是多少？存储和一致性怎么因此分开？」

## A
**结论。** 三类负载从高到低跨约 5 个数量级（150 万对十几）：令牌校验约 150 万次/秒，用本地验签；刷新轮换约 3 万次/秒，用分片存储；凭据写入只有十几次/秒，用强一致的单主存储。按负载形状拆存储，别让两种需求互相拖累。

**要点。**
- **校验（示例假设）：** 每人每天 100 次 API 调用，峰值 3 倍，内部再扇出 3 次校验，约 1.56×10^6 次/秒。每次都查中心会话存储，按单主 5 万次/秒要约 31 个分片，所以访问令牌做成短寿命 JWT，用缓存的公钥本地验签，没有网络往返。
- **刷新：** 轮换让每次刷新都是一次写（旧作废、新签发），每人每天约 6 次，峰值约 3 万次/秒。要分片，一致性只需在同一令牌家族内（用于检测重用），按家族 ID 分片，不需要全局事务。
- **凭据：** 注册、改密、锁定每天几十万次，峰值十几次/秒。吞吐不是问题，但读到旧的锁定或改密状态是安全漏洞，所以用强一致的单主，可以跨区域同步复制。
- **原则：** 高频数据不承担强一致的成本，低频的强一致数据也不被高频写拖慢。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 186">
<text x="10" y="20" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">令牌校验 ≈ 156 万/s：本地验签</text>
<rect x="10" y="26" width="186" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">刷新轮换 ≈ 3 万/s：分片存储</text>
<rect x="10" y="68" width="135" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">凭据写入 ≈ 17/s：强一致单主</text>
<rect x="10" y="110" width="37" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">条长按对数刻度，每 30 格差 10 倍</text>
<text x="10" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">最高与最低差约 5 个数量级，存储分开</text>
</svg>

**面试里这样说。** 「认证服务有三条路径：校验约 150 万/秒，靠短寿命 JWT 本地验签；刷新约 3 万/秒，按令牌家族分片；凭据写十几次/秒，放强一致单主。如果都放一个强一致库，吞吐上限会卡死校验和刷新。」

**易错。**
- **每次校验都查会话库：** 150 万次/秒要几十个分片，还多一次往返。
- **把刷新令牌放进强一致单主：** 吞吐上限几万次/秒，撑不住轮换。
