---
id: bagu-ha-overview-2-replication
node: a.redis.ha-overview
type: qa
step: 2
---
## Q
**主从复制 · 怎么同步，全量和增量怎么区分**｜必会

面试官：「从库怎么和主库同步？什么时候全量、什么时候增量？为什么要尽量避免全量？」

## A
**基本回答。** 从库发 `PSYNC <replid> <offset>`（replid 标识主库的数据历史，offset 是已复制偏移量）。replid 对得上且偏移量还在主库的复制积压缓冲区（环形，`repl-backlog-size`，存最近发出的写命令）里，只发偏移量之后的命令，是增量；否则全量：主库 `BGSAVE` 生成 RDB（默认无盘复制 `repl-diskless-sync yes`，流式直发不落盘），同时缓冲期间新写，从库清空载入后再补发缓冲命令，进入命令传播。要尽量避免全量：主库要 fork、占带宽，从库清空重载；积压缓冲区默认只有 1MB，短暂断线偏移量就被覆盖，每次重连都全量，主库反复 fork，可能陷入无休止的全量同步，要调大到「断线恢复预期时间 × 写入速率」再留余量。命令传播是异步的：从库每秒 `REPLCONF ACK` 上报偏移量，主库不等确认就返回客户端，所以切换可能丢写。PSYNC2（4.0）：新主保留旧主的 replid 作 replid2，换主后其他从库仍可增量，从库也可级联。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<rect x="40" y="6" width="260" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库发 PSYNC replid offset</text>
<line x1="170" y1="34" x2="170" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,48 166.8,41.0 173.2,41.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="48" width="260" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">replid 对得上，且偏移量</text>
<text x="170" y="81" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还在主库的积压缓冲区里？</text>
<line x1="100" y1="92" x2="78" y2="120" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78,120 79.8,112.5 84.8,116.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="72" y="110" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<line x1="240" y1="92" x2="257" y2="120" stroke-width="1.2" stroke="currentColor"/>
<polygon points="257,120 250.6,115.7 256.1,112.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="262" y="110" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">否</text>
<rect x="8" y="120" width="140" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="139.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">增量同步</text>
<text x="78" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只发偏移量之后</text>
<text x="78" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">的命令</text>
<rect x="182" y="120" width="150" height="90" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全量同步</text>
<text x="257" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 主库生成 RDB</text>
<text x="257" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 缓冲期间新写</text>
<text x="257" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 从库清空载入</text>
<text x="257" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 再发缓冲命令</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">积压缓冲区</text>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">默认只有 1MB</text>
<line x1="140" y1="182" x2="140" y2="236" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140,236 136.8,229.0 143.2,229.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="257" y1="210" x2="257" y2="236" stroke-width="1.2" stroke="currentColor"/>
<polygon points="257,236 253.8,229.0 260.2,229.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="236" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="254.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">命令传播：异步，主库不等从库确认</text>
</svg>
从库报上 replid 和偏移量，主库查缓冲区里还有没有这段：有就增量，没有就全量，两条路最后都汇入命令传播。
**业务场景。** 打赏高峰主库每秒写 5MB，从库断线 20 秒，期间产生 100MB 写命令，而积压缓冲区默认 1MB，偏移量早被覆盖，重连触发全量，主库 fork 延迟升高；调到 256MB 后 100MB 全留在缓冲区，只发增量，不用 fork。
**容易错。**
- **以为从库断线一定全量。**
- **以为 1MB 默认值够用。**
- **以为复制是同步的。**
