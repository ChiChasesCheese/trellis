---
id: bagu-avalanche-1-mass-expire
node: b.cache.avalanche
type: qa
step: 1
---
## Q
**缓存雪崩 · 成因与预防**｜必会

面试官：「凌晨批量预热的活动缓存，整点集体失效，数据库 CPU 打满。这是什么问题，怎么预防，Redis 整体宕机又怎么办？」

## A
**基本回答。** 这是雪崩，有两类成因：大量 key 同一时间过期，或 Redis 整体宕机，请求一起压向数据库。预防：TTL 加随机抖动（`base + random(0, base×20%)`）、多级缓存（本地缓存在 Redis 挂时还能挡一部分）、Redis 高可用（主从加哨兵或 Cluster，跨机架）、限流熔断降级保护数据库、上线前预热。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="105" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没抖动</text>
<text x="255" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加抖动</text>
<text x="10" y="40" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DB 压力</text>
<line x1="10" y1="110" x2="160" y2="110" stroke="currentColor" stroke-width="1.2"/>
<line x1="180" y1="110" x2="330" y2="110" stroke="currentColor" stroke-width="1.2"/>
<rect x="90" y="30" width="30" height="80" stroke-width="1.2" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="184" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<rect x="202" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<rect x="220" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<rect x="238" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<rect x="256" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<rect x="274" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<rect x="292" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<rect x="310" y="94" width="12" height="16" stroke-width="1.2" rx="2" fill="none" stroke="currentColor"/>
<text x="105" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">整点尖峰</text>
<text x="255" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">平缓曲线</text>
<text x="10" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ttl = base + random(0, base × 20%)</text>
<text x="10" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Redis 整体宕机：熔断限流保库，本地缓存先挡</text>
<text x="10" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">恢复后慢速预热，逐步放量</text>
</svg>
左边是批量写入的 key 用同一个 TTL，整点集体过期，数据库压力是一根尖峰；右边加了随机抖动，过期时间被摊开，压力变成平缓的一排。
**容易错。**
- **只加抖动不做限流：** 抖动防的是批量过期，防不了 Redis 整体宕机，还要有限流熔断保数据库。
- **恢复时一次放开全部流量：** 冷缓存会被再次打穿，要慢速预热、逐步放量。
- **把雪崩当成击穿：** 击穿是单个热 key，用互斥锁；雪崩是批量或整体，用抖动、高可用和限流。
- **Redis 宕机时先保数据库：** 靠熔断和限流，数据库能承受多少 QPS 就只放行多少，其余返回降级结果或稍旧的数据。
**举个例子。** 凌晨批量预热 10 万个活动 key，TTL 都是 3600 秒，1 点整同一秒集体过期，数据库 CPU 打满。改成 3600 加随机 0 到 720 秒（base 的 20%），过期分散在 12 分钟里。Redis 宕机时，数据库最多扛 5000 QPS 就只放行 5000，其余返回「稍后再试」或旧数据；恢复后先预热最热的一批再放量。
