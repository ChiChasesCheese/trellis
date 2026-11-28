---
id: bagu-ha-overview-3-sentinel
node: a.redis.ha-overview
type: qa
step: 3
---
## Q
**哨兵 · 怎么发现主库故障，怎么选新主**｜必会

面试官：「哨兵怎么判断主库挂了？为什么要多个哨兵？新主怎么选？」

## A
**基本回答。** 四步。① 主观下线（SDOWN）：每个哨兵每秒 PING，`down-after-milliseconds`（默认 30 秒）内无有效回复，只是它一个人的看法；调小发现更快，但主库因大 key 卡几秒时更易被误切。② 客观下线（ODOWN）：同意下线的哨兵数达到 `quorum`，才触发切换；多个哨兵是防单个哨兵自己网络问题误判。③ 选哨兵 leader：拉票需超过总数一半的多数派同意（不是 quorum），保证同一时刻只有一个哨兵在切换。④ 切换：先排除断线太久和 `replica-priority` 为 0 的从库，再比 `replica-priority` 小者优先、复制偏移量大者优先（复制得多，丢数据最少）、运行 ID 小者优先；选中者执行 `REPLICAOF NO ONE`，其余改复制新主，旧主恢复后降为从库。客户端不写死主库地址，向哨兵查（`SENTINEL get-master-addr-by-name`）或订阅 `+switch-master`。哨兵至少 3 个，分在不同机器和机房。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 298">
<rect x="8" y="8" width="324" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 主观下线（SDOWN）</text>
<text x="170" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">单个哨兵每秒 PING，30 秒内没有效回复</text>
<rect x="8" y="64" width="324" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 客观下线（ODOWN）</text>
<text x="170" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同意下线的哨兵数达到 quorum</text>
<rect x="8" y="120" width="324" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 选哨兵 leader</text>
<text x="170" y="153" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拉票，要超过总数一半的多数派（不是 quorum）</text>
<rect x="8" y="176" width="324" height="74" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 切换</text>
<text x="170" y="209" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排除断线久的、priority 为 0 的</text>
<text x="170" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再比：priority 小 &gt; 偏移量大 &gt; 运行 ID 小</text>
<text x="170" y="239" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选中者 REPLICAOF NO ONE，其余跟随</text>
<line x1="170" y1="52" x2="170" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,64 166.8,57.0 173.2,57.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="108" x2="170" y2="120" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,120 166.8,113.0 173.2,113.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="164" x2="170" y2="176" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,176 166.8,169.0 173.2,169.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">多个哨兵防误判；多数派保证只有一个在切换</text>
<text x="8" y="292" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">偏移量大者优先，是为了少丢数据</text>
</svg>
四步的判定标准不同：单个哨兵怀疑、足够多哨兵确认、选出负责切换的 leader、挑新主并切换。
**业务场景。** 3 个哨兵 `quorum=2`，凌晨 3:00:00 主库 M 宕机，3:00:30 三个哨兵都判主观下线，同意数 3 ≥ 2 成为客观下线；S1 拉票得 2 票（超过 3 的一半）成为 leader；R1 与 R2 priority 相同、R1 偏移量更大，R1 当选，R2 改复制 R1；几秒后客户端从哨兵拿到新主地址。期间写入失败，应用要有重试和降级，如打赏请求先落消息队列，Redis 恢复后再入榜。
**容易错。**
- **把 quorum 当选 leader 的票数。**
- **以为一个哨兵判下线就切换。**
- **客户端写死主库地址。**
