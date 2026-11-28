---
id: bagu-multi-region-1-home-region
node: b.distributed.multi-region
type: qa
step: 1
---
## Q
**多区域部署 · 归属区域写入与数据驻留**｜追问

面试官：「欧洲用户的支付数据必须留在欧洲，系统怎么做多区域？单主、归属区域写入、多主各有什么取舍？区域切换会丢什么？」

## A
**基本回答。** 账务类选归属区域写入：用户或商户绑定一个归属区域（home region），写都路由到该区域的主库，写者唯一所以没有冲突；其他区域读副本。单主最简单但远端写慢；多主就近写，靠 LWW（最后写入者胜）或 CRDT（可自动合并的数据结构）合并冲突，余额这类不变量合不了。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="6" y="6" width="160" height="166" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="86" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">欧洲区域（归属区）</text>
<rect x="36" y="34" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">欧洲用户</text>
<line x1="86" y1="60" x2="86" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,86.0 82.8,79.0 89.2,79.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="36" y="88" width="100" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="86.0" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库（写）</text>
<line x1="86" y1="116" x2="86" y2="138" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,138.0 82.8,131.0 89.2,131.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="36" y="140" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="86.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本区域副本</text>
<rect x="174" y="6" width="160" height="166" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="254" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">美国区域（归属区）</text>
<rect x="204" y="34" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">美国用户</text>
<line x1="254" y1="60" x2="254" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,86.0 250.8,79.0 257.2,79.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="88" width="100" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="254.0" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库（写）</text>
<line x1="254" y1="116" x2="254" y2="138" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,138.0 250.8,131.0 257.2,131.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="140" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="254.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本区域副本</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写只发往用户的归属区域，写者唯一</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">跨区转账：带幂等键的消息 / Saga</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跨区只同步汇总、脱敏数据（驻留）</text>
<text x="8" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">区域故障切换：副本落后的几秒写入会丢</text>
<text x="8" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（RPO &gt; 0），靠幂等键重试 + 对账补齐</text>
</svg>
两个虚线框是两个区域：用户的写只发往自己归属区域的主库，区域内再有副本读；两个区域之间只同步汇总、脱敏的数据，跨区转账走带幂等键的消息或 Saga。
**容易错。**
- **以为多主就近写最先进：** 余额不能为负这类不变量合并不了，账务要写者唯一。
- **以为数据驻留只是存储位置：** 令牌服务要区域化，灾备站要在允许的地域内，跨区域运维访问受控并留审计，全局服务只用汇总或脱敏数据。
- **以为切换不丢数据：** 异步复制下副本落后的那段写入会丢，同步复制可以不丢，但每次写更慢。
- **以为丢了写入就完了：** 外部副作用仍在，要靠幂等键加对账补齐。
- **以为归属区域写入没有代价：** 跨区域操作没有单库事务，换区域要迁移数据。

**业务场景。** 欧洲区域故障切到备用区域时，最后几秒的支付记录还没复制过去，渠道却已经扣款。商户重试带原幂等键，不会重复扣；缺失的记录由渠道对账找回。
