---
id: bagu-ha-redundancy-1-rto-rpo
node: b.protect.ha-redundancy
type: qa
step: 1
---
## Q
**高可用架构 · 冗余、故障转移、多活与 RTO/RPO**｜追问

面试官：「封禁名单要全球生效，怎么做高可用？RTO 和 RPO 是什么？异地多活难在哪？」

## A
**基本回答。** 高可用靠冗余加故障转移。RPO 是灾难后最多允许丢多久的数据（时间点），RTO 是从故障到恢复最长允许停多久（时间段），两者是目标不是结果，要靠演练验证；RPO = 0 要求写入在多个故障域确认后才返回，写延迟高。冗余分冷备（只存数据，最慢最便宜）、温备（有备机需启动）、热备（实时同步随时接管）、多活（多处同时服务，最快最贵）。99.99% 可用性一年约停机 52.6 分钟，99.9% 约 8.8 小时。故障转移五步：检测、确认（多次检测加多数派，一次心跳超时可能只是抖动）、切换、通知、恢复；有状态系统要 fencing（fencing token 或租约），新主拿 8，存储只接受 token ≥ 8，旧主的 7 被拒，防脑裂。多活难在数据一致性、跨地域延迟、流量调度（DNS、GSLB）、会话和成本，常按用户或地域单元化，跨单元用 TCC、Saga 或对账补偿；对账补偿能力不足、数据无法按用户切分、成本高于损失的业务不要强上。
**2026 亮点。** 同城把可用区当故障域（cell）：服务只调同 AZ 下游，边缘负载均衡配「排空 AZ」按钮按权重逐步切走（先 1%），故障局限在单个 AZ 时不用先找根因就能缓解；代价是每个 AZ 要有完整服务栈，其余 AZ 要预留吃下被排空流量的余量。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<line x1="10" y1="62" x2="330" y2="62" stroke-width="1.2" stroke="currentColor"/>
<line x1="40" y1="52" x2="40" y2="72" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="52" x2="170" y2="72" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="300" y1="52" x2="300" y2="72" stroke-width="1.2" stroke="currentColor"/>
<text x="40" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最后可恢复点</text>
<text x="170" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">故障</text>
<text x="300" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">服务恢复</text>
<line x1="168" y1="90" x2="49" y2="90" stroke-width="1.2" stroke="currentColor"/>
<polygon points="42.0,90.0 49.0,86.8 49.0,93.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="105" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">RPO：丢多久的数据</text>
<line x1="172" y1="90" x2="291" y2="90" stroke-width="1.2" stroke="currentColor"/>
<polygon points="298.0,90.0 291.0,93.2 291.0,86.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="235" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">RTO：停多久</text>
<text x="8" y="148" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">冗余等级：恢复越快，成本越高</text>
<rect x="6" y="158" width="76" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冷备</text>
<text x="44" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只存数据</text>
<rect x="90" y="158" width="76" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">温备</text>
<text x="128" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">备机待命</text>
<rect x="174" y="158" width="76" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">热备</text>
<text x="212" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实时同步</text>
<rect x="258" y="158" width="76" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="296" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多活</text>
<text x="296" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">都在服务</text>
<line x1="10" y1="220" x2="323" y2="220" stroke-width="1.2" stroke="currentColor"/>
<polygon points="330.0,220.0 323.0,223.2 323.0,216.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="240" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">可用性 99.99% ≈ 一年停机 52.6 分钟</text>
</svg>
时间轴上，最后可恢复点到故障之间丢的数据是 RPO，故障到恢复之间停的时间是 RTO；下面四级冗余越往右恢复越快成本越高。
**业务场景。** 封禁名单部署在 3 个地域，靠地域间复制，复制延迟 2 秒则故障瞬间最多丢最近 2 秒的新增封禁（RPO 取决于复制延迟，封禁属最终一致）；RTO 从发现故障到流量切走，演练测出来约 2 分钟。
**容易错。**
- **把 RTO 和 RPO 搞反。**
- **心跳超时一次就切换。**
- **没做 fencing：** 旧主恢复后继续写造成脑裂。
