---
id: hi-sdx-wallet-shard-migration
node: tt.sd.tt-wallet-ledger-service.more
type: qa
step: 3
---
## Q
**账户迁移：冻结、排空、核对**｜补充 · 钱包与复式账本服务 · 加分

面试官：「一个事件溯源的钱包账户要从分片 3 迁到分片 7，期间有转账在进行。怎么保证迁移前后余额一致，用户感知到的不可用时间又尽量短？」

## A
**结论。** 先在线拷贝历史，再冻结、排空在途转账、补拷尾部，两边各自重放核对一致，最后原子切路由。冻结窗口只覆盖后四步，拷贝大头在窗口之外。

**要点。**
- **在线拷贝历史：** 账户仍然可用，把已有事件复制到目标分片；这一步可以很长。
- **冻结：** 拒绝针对该账户的新转账 prepare，返回可重试的「忙」；其他账户不受影响。
- **排空：** 等所有已经 prepare 的转账走到终态（提交或取消）。协调者对每笔转账有超时和终态，所以等待有上限。
- **补拷并核对：** 补拷冻结后产生的尾部事件，在目标分片重放；余额、最后序号、日志哈希三项和源分片一致才通过。
- **切换：** 原子更新路由，解冻；源分片数据再保留一段时间后才删除。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 330">
<rect x="10" y="8" width="210" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="115.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 在线拷贝历史事件</text>
<text x="115.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">账户照常转账</text>
<polyline points="115,48 115.0,59.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="115,66 111.8,59.0 118.2,59.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="66" width="210" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115.0" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 冻结账户</text>
<text x="115.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拒绝新的 prepare</text>
<polyline points="115,106 115.0,117.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="115,124 111.8,117.0 118.2,117.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="124" width="210" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115.0" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 排空在途转账</text>
<text x="115.0" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等已 prepare 的走到终态</text>
<polyline points="115,164 115.0,175.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="115,182 111.8,175.0 118.2,175.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="182" width="210" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 补拷尾部并重放核对</text>
<text x="115.0" y="213.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">余额 · 序号 · 日志哈希</text>
<polyline points="115,222 115.0,233.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="115,240 111.8,233.0 118.2,233.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="240" width="210" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115.0" y="256.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑤ 原子切路由，解冻</text>
<text x="115.0" y="271.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧分片再保留一段时间</text>
<line x1="236" y1="66" x2="236" y2="280" stroke-width="1" stroke="currentColor" opacity="0.4"/>
<line x1="230" y1="66" x2="236" y2="66" stroke-width="1" stroke="currentColor" opacity="0.4"/>
<line x1="230" y1="280" x2="236" y2="280" stroke-width="1" stroke="currentColor" opacity="0.4"/>
<text x="244" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">冻结</text>
<text x="244" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口</text>
<text x="8" y="306" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不可用的只有 ②～⑤，历史越长越要把大头放在 ①。</text>
</svg>

**为什么。** 迁移的风险是同一个账户在两个分片都能写。冻结加排空保证切换时源分片已经没有未完成的写；用同一个纯函数重放核对，保证目标分片的状态确实等于源。

**面试里这样说。** 「迁移分四步：在线拷历史，冻结并排空在途转账，补拷尾部，两边重放比对余额、序号和日志哈希，一致再原子切路由。用户只在冻结到切换这一小段看到『忙，请重试』，不会出现两个分片同时可写。」

**易错。**
- **整个拷贝期都冻结：** 历史很长的账户会不可用很久；大头要在线拷。
- **不排空就切：** 一笔已 prepare 的转账在源分片提交，目标分片永远看不到。
- **只比余额：** 两边余额恰好相等也可能事件不同，要连同序号和日志哈希一起比。
