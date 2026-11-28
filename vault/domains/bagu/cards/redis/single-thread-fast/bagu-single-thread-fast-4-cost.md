---
id: bagu-single-thread-fast-4-cost
node: a.redis.single-thread-fast
type: qa
step: 3
---
## Q
**单线程的代价 · 哪些操作会堵住所有请求**｜必会

面试官：「单线程下，线上哪些操作会让整个 Redis 卡住？删一个两百万成员的大集合，DEL 和 UNLINK 有什么区别？」

## A
**基本回答。** 单线程下任何耗时命令都让后面排队：`KEYS *`（遍历整个键空间）、大集合的 `SMEMBERS`/`HGETALL`/`ZRANGE 0 -1`、同步删大 key、耗时 Lua、同步 `FLUSHALL`、实例太大 fork 慢。对策：`SCAN` 代替 `KEYS`，`UNLINK` 代替 `DEL`，拆大 key。`UNLINK`（4.0+）主线程只把键摘出键空间（O(1)，十几微秒），释放内存交给后台线程；很小的值直接同步释放。`lazyfree-lazy-expire`、`lazyfree-lazy-eviction`、`lazyfree-lazy-user-del` 默认都是 no，过期和淘汰要手动打开才异步释放。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主线程的时间线：一条慢命令，后面全排队</text>
<rect x="8" y="24" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="28" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GET</text>
<rect x="52" y="24" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="127" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">KEYS *（卡几秒）</text>
<rect x="206" y="24" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="236" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GET 排队</text>
<rect x="270" y="24" width="62" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="301" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET 排队</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同样删 200 万成员的 set：</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">DEL</text>
<rect x="60" y="92" width="160" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">释放内存 约 55 毫秒</text>
<text x="228" y="109" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主线程自己干</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">UNLINK</text>
<rect x="60" y="132" width="46" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">摘键</text>
<line x1="106" y1="145" x2="124" y2="145" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="124,145 117.0,148.2 117.0,141.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="126" y="132" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="191" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后台线程释放</text>
<text x="60" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主线程只花十几微秒</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">KEYS→SCAN，DEL→UNLINK，拆大 key</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5 秒的 Lua 也会让其他客户端收到 BUSY</text>
</svg>
上排：一条 `KEYS *` 占住主线程，后面的 GET、SET 全部排队；下排：同样删 200 万成员的 set，DEL 自己卸货约 55 毫秒，UNLINK 只摘键，卸货交给后台线程。
**业务场景。** 运营后台对千万级 key 的实例执行 `KEYS rank:*`，卡住数秒，打赏扣币写入全部超时；改成 `SCAN 0 MATCH rank:* COUNT 100`，每次只扫一小批，请求可以穿插。清一个 200 万成员的 set，`DEL` 阻塞约 55 毫秒（量级，随机器而异），期间所有请求多等 55 毫秒，`UNLINK` 则几乎无感。
**排查。** `SLOWLOG` 只记命令执行时间，不含排队时间；`LATENCY DOCTOR` 看延迟事件；`redis-cli --bigkeys` 找大 key。Lua 超过 `busy-reply-threshold`（旧名 `lua-time-limit`，默认 5000 毫秒）后其他客户端收到 BUSY，靠 `SCRIPT KILL` 或 `SHUTDOWN NOSAVE` 救场。
**容易错。**
- **以为 UNLINK 释放得更快：** 内存释放总量没变，只是不让主线程等。
- **以为只有命令慢会卡：** fork 慢、Lua 超时、同步 `FLUSHALL`、几百 MB 大 key 的迁移/复制/过期都会卡。
