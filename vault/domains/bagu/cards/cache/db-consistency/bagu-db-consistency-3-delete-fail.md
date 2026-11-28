---
id: bagu-db-consistency-3-delete-fail
node: a.cache.db-consistency
type: qa
step: 3
---
## Q
**缓存一致性 · 删除缓存失败了怎么办**｜必会

面试官：「更新完库，删缓存时 Redis 超时失败，或者进程在两步之间崩溃，缓存就留了旧值。怎么保证最终一致？」

## A
**基本回答。** 删除失败就重试：应用里先同步重试几次，仍然失败就把「删除某个 key」的消息发到 MQ（消息队列），由消费者异步重试，消费者要做幂等（重复处理没有副作用）；TTL 当最后的兜底，TTL 越短，不一致持续得越短，但命中率也越低。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<rect x="8" y="8" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">更新库成功</text>
<rect x="8" y="52" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">删缓存失败或崩溃</text>
<rect x="8" y="96" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用内重试 2、3 次</text>
<rect x="8" y="140" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">投 MQ 异步重试</text>
<line x1="83" y1="36" x2="83" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,52.0 79.8,45.0 86.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="83" y1="80" x2="83" y2="90" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,96.0 79.8,89.0 86.2,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="83" y1="124" x2="83" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,140.0 79.8,133.0 86.2,133.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓存里还是旧值</text>
<text x="170" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">覆盖瞬时抖动</text>
<text x="170" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">退避、限次数</text>
<rect x="8" y="184" width="324" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">兜底：TTL 到期、binlog 订阅补删</text>
<text x="170" y="217.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息也丢了，这几层最终收敛</text>
</svg>
三层依次升级：先在应用里重试，再交给 MQ，最后靠 TTL 和 binlog 兜底。虚线框是不依赖业务代码的最终兜底。
**容易错。**
- **以为失败了没关系：** 删缓存失败，旧值会一直留到 TTL，要有重试。
- **只在内存里重试：** 进程在两步之间崩溃，内存里的重试就没了，要用 MQ 持久化。
- **担心重复消息：** 删除是幂等的，重复无副作用。
- **没有兜底：** 只靠重试不够，重试消息也丢了的极端情况，要靠 TTL 和 binlog 补删收敛：用 Canal 之类订阅 binlog，由独立链路在库更新后再删一次缓存，不依赖业务代码，关键数据再加定时对账扫描。

**业务场景。** 改价后删缓存的请求恰好遇到 Redis 主从切换而失败，重试消息 30 秒后补删成功，用户最多看到半分钟旧价。
