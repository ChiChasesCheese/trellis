---
id: bagu-rdb-aof-6-recovery
node: a.redis.rdb-aof
type: qa
step: 6
---
## Q
**宕机重启 · 先读 RDB 还是 AOF，有哪些坑**｜追问

面试官：「同时有 RDB 和 AOF，Redis 重启读哪个？线上重启容易踩什么坑？」

## A
**基本回答。** 开了 AOF 就只读 AOF，因为时间点比最近一次 RDB 更靠后；没开 AOF 才读 RDB，两个文件不会合并。7.0 起读清单里的基础文件加增量文件，基础文件是 RDB 还是命令格式按文件头自动识别。AOF 末尾被截断时，`aof-load-truncated yes`（默认）加载到截断处，严重损坏用 `redis-check-aof --fix`。装载期间命令返回 `LOADING`（`INFO persistence` 的 `loading:1`），调用方要重试，不是故障。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="100" y="6" width="140" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 重启</text>
<line x1="170" y1="32" x2="170" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,50 166.8,43.0 173.2,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="50" width="220" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开了 appendonly yes？</text>
<line x1="110" y1="82" x2="83" y2="112" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83,112 85.3,104.7 90.1,108.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="78" y="100" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<line x1="230" y1="82" x2="257" y2="112" stroke-width="1.2" stroke="currentColor"/>
<polygon points="257,112 249.9,108.9 254.7,104.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="262" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">否</text>
<rect x="8" y="112" width="150" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读 AOF</text>
<text x="83" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时间点更靠后</text>
<rect x="182" y="112" width="150" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读 dump.rdb</text>
<line x1="83" y1="156" x2="83" y2="178" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83,178 79.8,171.0 86.2,171.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="178" width="150" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="83" y="197.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">坑：还没有 AOF 文件</text>
<text x="83" y="212.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不会回头读 rdb</text>
<text x="83" y="227.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">启动得到空库</text>
<rect x="182" y="178" width="150" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="257" y="197.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">装载期间</text>
<text x="257" y="212.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">命令返回 LOADING</text>
<text x="257" y="227.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">调用方要重试</text>
</svg>
重启先看 `appendonly` 开没开：开了读 AOF，没开读 `dump.rdb`；左下是切换持久化方式时最常见的坑，右下是装载期间的表现。
**业务场景。** 只开了 RDB 的缓存实例有 2000 万个 key，运维改配置 `appendonly yes` 后直接重启：没有 AOF 文件，Redis 不会回头读 `dump.rdb`，起来是空库，请求全部打到数据库。正确做法是先在线 `CONFIG SET appendonly yes`，等 `INFO persistence` 确认 AOF 重写完成，再改配置文件。
**容易错。**
- **以为开 AOF 改配置重启就行：** 没有 AOF 文件时得到空库。
- **以为主库自动重启最稳：** 主库没持久化，被拉起后数据为空，从库全量同步后把自己的数据也清空；要开持久化，或禁止主库自动重启。
