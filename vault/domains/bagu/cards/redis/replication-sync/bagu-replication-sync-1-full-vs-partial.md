---
id: bagu-replication-sync-1-full-vs-partial
node: b.redis.replication-sync
type: qa
step: 1
---
## Q
**主从复制 · 全量与增量同步**｜追问

面试官：「从库网络抖动 30 秒后重连，是增量同步还是又一次全量？复制积压缓冲区太小会怎样？」

## A
**基本回答。** 从库重连发 `PSYNC replid offset`。主库发现这个偏移量还在复制积压缓冲区（repl backlog，环形，默认 1MB，`repl-backlog-size`）里，就只补发缺的那段；不在了就全量：主库 `bgsave` 生成 RDB 发给从库，期间的新写入另存，之后补发。积压按「断线时长 × 写入速率」估。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 234">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主库写入偏移量：越往右越新</text>
<rect x="8" y="26" width="88" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="52" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已被覆盖</text>
<rect x="96" y="26" width="232" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">积压缓冲区：最近 1MB 写命令</text>
<line x1="52" y1="92" x2="52" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="52,58 55.2,65 48.8,65" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="92" x2="170" y2="58" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,58 173.2,65 166.8,65" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="52" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库 B</text>
<text x="170" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从库 A</text>
<text x="52" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">窗口外：全量</text>
<text x="190" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">窗口内：增量补发缺的一段</text>
<text x="8" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全量同步三步</text>
<rect x="8" y="162" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库 bgsave</text>
<text x="56" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生成 RDB</text>
<line x1="104" y1="182" x2="118" y2="182" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118,182 111,185.2 111,178.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="162" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发给从库</text>
<text x="166" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加载</text>
<line x1="214" y1="182" x2="228" y2="182" stroke-width="1.2" stroke="currentColor"/>
<polygon points="228,182 221,185.2 221,178.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="228" y="162" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">补发期间</text>
<text x="278" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新写入</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">复制缓冲区超限，从库被断开，重连又全量</text>
</svg>
上方的长条是主库保存的最近 1MB 写命令，越新越靠右，再旧的已被覆盖。从库 A 的偏移量落在长条里，主库只补发它缺的那段；从库 B 落在长条外，补不了，只能走图中的全量三步。
**业务场景。** 每秒写 100KB：断线 5 秒产生约 500KB，仍在 1MB 内，只补这段（`sync_partial_ok` 加 1）；断线 30 秒产生约 3MB，偏移量已被覆盖，只能全量（`sync_full` 加 1），fork 和传输 RDB 把主库拖慢，读写延迟飙升。把 `repl-backlog-size` 调到至少 3MB，30 秒抖动就能走增量。
**容易错。**
- **把两个缓冲区搞混：** 积压缓冲区主库一份，环形，让重连走增量；复制缓冲区每个从库一份，存全量期间的新命令，默认 `client-output-buffer-limit replica 256mb 64mb 60`，超限就断开该从库，它重连又触发全量，可能反复。
- **以为全量只是传个文件：** fork、生成并传输 RDB 占主库 CPU、内存和带宽；无盘复制（`repl-diskless-sync yes`）会等 5 秒，攒多个从库一起发。
- **以为复制不丢数据：** 复制是异步的，主库宕机会丢没传出去的写。
